from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
import re

class ManageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clzz Card Types")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        # Layout principal
        main_layout = QHBoxLayout()

        # Parte esquerda do layout
        left_layout = QVBoxLayout()

        # Combobox para listar os card types
        self.card_type_combobox = QComboBox()
        self.card_type_combobox.setPlaceholderText("Select a card type")
        self.card_type_combobox.currentIndexChanged.connect(self.show_card_type_details)
        left_layout.addWidget(self.card_type_combobox)

        # Combobox para selecionar a visualização (Front, Back, CSS)
        self.view_combobox = QComboBox()
        self.view_combobox.addItems(["Front", "Back", "CSS"])
        self.view_combobox.currentIndexChanged.connect(self.update_details_view)
        left_layout.addWidget(self.view_combobox)

        # Caixa de texto para exibir os detalhes
        self.details_textbox = QTextEdit()
        self.details_textbox.setReadOnly(True)
        left_layout.addWidget(self.details_textbox)

        main_layout.addLayout(left_layout)

        # Parte direita do layout
        right_layout = QVBoxLayout()

        # Ajustar os elementos na parte superior
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Input para Deck Colors
        deck_colors_layout = QHBoxLayout()
        self.deck_colors_label = QLabel("Deck Colors:")
        self.deck_colors_input = QLineEdit()
        deck_colors_layout.addWidget(self.deck_colors_label)
        deck_colors_layout.addWidget(self.deck_colors_input)
        right_layout.addLayout(deck_colors_layout)

        # Input para Cloze Colors
        cloze_colors_layout = QHBoxLayout()
        self.cloze_colors_label = QLabel("Cloze Colors:")
        self.cloze_colors_input = QLineEdit()
        cloze_colors_layout.addWidget(self.cloze_colors_label)
        cloze_colors_layout.addWidget(self.cloze_colors_input)
        right_layout.addLayout(cloze_colors_layout)

        # Checkbox para Disable Animations
        disable_animations_layout = QHBoxLayout()
        self.disable_animations_label = QLabel("Disable Animations:")
        self.disable_animations_checkbox = QCheckBox()
        disable_animations_layout.addWidget(self.disable_animations_label)
        disable_animations_layout.addWidget(self.disable_animations_checkbox)
        right_layout.addLayout(disable_animations_layout)

        # Espaçador para empurrar os botões para a parte inferior
        right_layout.addStretch()

        # Botões Salvar e Fechar
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Ok")
        self.save_button.clicked.connect(self.save_changes)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.close_button)
        right_layout.addLayout(buttons_layout)

        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.save_button.clicked.connect(self.save_card_type_changes)

        # Encontrar os card types com a classe 'clzz'
        self.find_clzz_card_types()

    def find_clzz_card_types(self):
        """Finds all card types that contain the element <span class="clzz"></span>."""
        model_manager = mw.col.models
        self.clzz_card_types = {}

        for model in model_manager.models.values():
            for tmpl in model['tmpls']:
                if '<span class="clzz"></span>' in tmpl['qfmt'] or '<span class="clzz"></span>' in tmpl['afmt']:
                    self.clzz_card_types[model['name']] = model

        # Atualizar o combobox com os nomes dos card types encontrados
        if self.clzz_card_types:
            self.card_type_combobox.addItems(self.clzz_card_types.keys())
        else:
            self.details_textbox.setPlainText("No card type found.")
            self.card_type_combobox.setDisabled(True)

    def show_card_type_details(self):
        """Shows the details of the selected card type and updates the inputs."""
        selected_card_type = self.card_type_combobox.currentText()
        if selected_card_type and selected_card_type in self.clzz_card_types:
            model = self.clzz_card_types[selected_card_type]

            # Atualizar os campos de entrada
            self.update_color_inputs(model)
            self.update_details_view()
        else:
            self.details_textbox.setPlainText("Select a valid card type.")

    def update_details_view(self):
        """Updates the content view based on the option selected in the view_combobox."""
        selected_card_type = self.card_type_combobox.currentText()
        if not selected_card_type or selected_card_type not in self.clzz_card_types:
            self.details_textbox.setPlainText("Select a valid card type.")
            return

        model = self.clzz_card_types[selected_card_type]
        selected_view = self.view_combobox.currentText()

        if selected_view == "Front":
            content = model['tmpls'][0]['qfmt']
        elif selected_view == "Back":
            content = model['tmpls'][0]['afmt']
        elif selected_view == "CSS":
            content = model['css']
        else:
            content = "Invalid view."

        self.details_textbox.setPlainText(content)

    def update_color_inputs(self, model):
        """Updates the Deck Colors and Cloze Colors fields."""
        qfmt = model['tmpls'][0]['qfmt']
        colors = self.extract_variable(qfmt, 'colors')
        colorsClz = self.extract_variable(qfmt, 'colorsClz')

        self.deck_colors_input.setText(', '.join(colors) if colors else "")
        self.cloze_colors_input.setText(', '.join(colorsClz) if colorsClz else "")

    def extract_variable(self, content, variable_name):
        """Extract values ​​from an array in a template script."""
        pattern = rf"var {variable_name} = \[(.*?)\];"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            # Remover espaços extras e dividir valores
            values = match.group(1).split(',')
            return [value.strip().strip("'\"") for value in values]
        return []

    def save_card_type_changes(self):
        """Saves the color values ​​in the Front and Back fields of the selected card type."""
        selected_card_type = self.card_type_combobox.currentText()
        if not selected_card_type:
            showInfo("No card type selected.")
            return

        # Obtenha os valores dos inputs
        colorsHTML = self.deck_colors_input.text().strip()
        colorsClzHTML = self.cloze_colors_input.text().strip()

        # Formate os elementos HTML
        colorsEl = f'<script> var colors = [{colorsHTML}]; </script>'
        colorsClzEl = f'<script> var colorsClz = [{colorsClzHTML}]; </script>'

        # Obtenha o modelo do card type selecionado
        model_manager = mw.col.models
        model = model_manager.byName(selected_card_type)
        if not model:
            showInfo("Error locating the template for the selected card type.")
            return

        # Atualize o Front e o Back
        for tmpl in model['tmpls']:
            tmpl['qfmt'] = colorsEl + colorsClzEl + tmpl['qfmt']
            tmpl['afmt'] = colorsEl + colorsClzEl + tmpl['afmt']

        # Salve as mudanças no banco de dados do Anki
        model_manager.save(model)
        mw.reset()

    def save_changes(self):
        self.save_card_type_changes()
