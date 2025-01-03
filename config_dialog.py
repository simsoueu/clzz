from aqt import mw
from aqt.qt import *
import json
import os
from aqt.utils import showInfo

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clzz Card Type Configuration")

        # Default settings
        self.default_settings = {
            "card_type_name": "Clzz Card",
            "show_decks": True,
            "show_hints": True,
            "show_blur": True,
            "deck_colors": ["#FF6B6B", "#FFA463", "#FFFF6B", "#63FF91", "#63C4FF"],
            "cloze_colors": ["#0BBA2E", "#0BBA5D"],
            "custom_front": """<script></script>""",
            "custom_back": """<script></script>""",
            "custom_css_checkbox": True,
            "custom_css": """@font-face {
  font-family: cheltenham-it;
  src: url(_cheltenham-italic-700.woff2);
}

@font-face {
  font-family: 'imWriter';
  src: url(_iAWriter.ttf);
}

@font-face {
  font-family: 'franklin';
  src: url(_franklin-normal-500.woff2);
}

.card {
    font-family: 'imWriter', 'Yu Gothic Medium', 'Samsung Sans', 'Roboto', sans-serif;
    font-size: 24px;
    text-align: center;
    line-height: 2.4rem;
    margin: auto 200px;
}

.cloze {
    font-weigth: bold;
}


.deck-name {
    font-family: 'cheltenham-it', 'imperial';
    font-size: 2rem;
    font-weight: bold;
    margin-top: 20px;
    padding-bottom: 40px;
}

code {
    font-family: SF Mono, 'Consolas', 'Fira Sans', courier, monospaced;
}

#extra {
    margin-top: 15px
}

@media screen and (max-width: 400px) {
    .deck-name {
        font-size: 1.6rem;
        margin-top: 10px;
        padding-bottom: 10px;
    }

    .card {
        font-family: 'franklin', 'Yu Gothic Medium', 'Samsung Sans', 'Roboto', sans-serif;
        font-size: 20px;
        text-align: center;
        line-height: 2rem;
        margin: auto 10px;
    }
}
""",
            "auto_color_bold": True,
        }

        # UI elements
        self.card_type_name_label = QLabel("Card Type Name:")
        self.card_type_name_input = QLineEdit()
        self.show_decks_checkbox = QCheckBox("Show current deck as header")
        self.show_hints_checkbox = QCheckBox("Enable toggable hints")
        self.show_blur_checkbox = QCheckBox("Show Cloze as Blur")
        self.deck_colors_checkbox = QCheckBox("Deck Colors")
        self.deck_colors_input = QLineEdit()
        self.cloze_colors_checkbox = QCheckBox("Cloze Colors")
        self.cloze_colors_input = QLineEdit()

        self.custom_front_checkbox = QCheckBox("Custom Front")
        self.custom_front_input = QTextEdit()
        self.custom_front_input.setFontFamily("Courier New")
        
        self.custom_back_checkbox = QCheckBox("Custom Back")
        self.custom_back_input = QTextEdit()
        self.custom_back_input.setFontFamily("Courier New")
        
        self.custom_css_checkbox = QCheckBox("Custom CSS")
        self.custom_css_input = QTextEdit()
        self.custom_css_input.setFontFamily("Courier New")
        
        self.auto_color_bold_checkbox = QCheckBox("Auto Color Bold")

        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QGridLayout()
        color_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Add widgets to layouts
        top_layout.addWidget(self.card_type_name_label, 0, 0)
        top_layout.addWidget(self.card_type_name_input, 0, 1)
        top_layout.addWidget(self.show_decks_checkbox, 1, 0)
        top_layout.addWidget(self.show_hints_checkbox, 2, 0)
        top_layout.addWidget(self.show_blur_checkbox, 3, 0)
        top_layout.addWidget(self.auto_color_bold_checkbox, 2, 1)

        color_layout.addWidget(self.deck_colors_checkbox)
        color_layout.addWidget(self.deck_colors_input)
        color_layout.addWidget(self.cloze_colors_checkbox)
        color_layout.addWidget(self.cloze_colors_input)
        top_layout.addLayout(color_layout, 4, 0, 1, 2)

        top_layout.addWidget(self.custom_front_checkbox, 5, 0)
        top_layout.addWidget(self.custom_front_input, 6, 0, 1, 2)
        top_layout.addWidget(self.custom_back_checkbox, 7, 0)
        top_layout.addWidget(self.custom_back_input, 8, 0, 1, 2)
        top_layout.addWidget(self.custom_css_checkbox, 9, 0)
        top_layout.addWidget(self.custom_css_input, 10, 0, 1, 2)

        main_layout.addLayout(top_layout)

        # Buttons
        restore_button = QPushButton("Restore Defaults")
        restore_button.clicked.connect(self.restore_defaults)
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(restore_button)
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Connect signals to slots
        self.deck_colors_checkbox.stateChanged.connect(self.toggle_deck_colors_input)
        self.cloze_colors_checkbox.stateChanged.connect(self.toggle_cloze_colors_input)
        self.custom_front_checkbox.stateChanged.connect(self.toggle_custom_front_input)
        self.custom_back_checkbox.stateChanged.connect(self.toggle_custom_back_input)
        self.custom_css_checkbox.stateChanged.connect(self.toggle_custom_css_input)

        # Load and display settings


        self.restore_defaults();

    def load_default_settings(self):
        with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
            self.default_settings = json.load(f)

    def load_user_settings(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "user_settings.json"), "r") as f:
                self.user_settings = json.load(f)
        except FileNotFoundError:
            self.user_settings = {}

        self.card_type_name_input.setText(self.user_settings.get("card_type_name", self.default_settings["card_type_name"]))
        self.show_decks_checkbox.setChecked(self.user_settings.get("show_decks", self.default_settings["show_decks"]))
        self.show_hints_checkbox.setChecked(self.user_settings.get("show_hints", self.default_settings["show_hints"]))
        self.show_blur_checkbox.setChecked(self.user_settings.get("show_blur", self.default_settings["show_blur"]))
        self.deck_colors_checkbox.setChecked(self.user_settings.get("use_deck_colors", True))
        self.deck_colors_input.setText(",".join(self.user_settings.get("deck_colors", self.default_settings["deck_colors"])))
        self.toggle_deck_colors_input(self.deck_colors_checkbox.checkState())
        self.cloze_colors_checkbox.setChecked(self.user_settings.get("use_cloze_colors", True))
        self.cloze_colors_input.setText(",".join(self.user_settings.get("cloze_colors", self.default_settings["cloze_colors"])))
        self.toggle_cloze_colors_input(self.cloze_colors_checkbox.checkState())
        self.custom_front_checkbox.setChecked(self.user_settings.get("use_custom_front", True))
        self.custom_front_input.setPlainText(self.user_settings.get("custom_front", self.default_settings["custom_front"]))
        self.toggle_custom_front_input(self.custom_front_checkbox.checkState())
        self.custom_back_checkbox.setChecked(self.user_settings.get("use_custom_back", True))
        self.custom_back_input.setPlainText(self.user_settings.get("custom_back", self.default_settings["custom_back"]))
        self.toggle_custom_back_input(self.custom_back_checkbox.checkState())
        self.custom_css_checkbox.setChecked(self.user_settings.get("use_custom_css", True))
        self.custom_css_input.setPlainText(self.user_settings.get("custom_css", self.default_settings["custom_css"]))
        self.auto_color_bold_checkbox.setChecked(self.user_settings.get("auto_color_bold", self.default_settings["auto_color_bold"]))

    def save_settings(self):
        user_settings = {
            "card_type_name": self.card_type_name_input.text(),
            "show_decks": self.show_decks_checkbox.isChecked(),
            "show_hints": self.show_hints_checkbox.isChecked(),
            "show_blur": self.show_blur_checkbox.isChecked(),
            "use_deck_colors": self.deck_colors_checkbox.isChecked(),
            "deck_colors": self.deck_colors_input.text().split(","),
            "use_cloze_colors": self.cloze_colors_checkbox.isChecked(),
            "cloze_colors": self.cloze_colors_input.text().split(","),
            "use_custom_front": self.custom_front_checkbox.isChecked(),
            "custom_front": self.custom_front_input.toPlainText(),
            "use_custom_back": self.custom_back_checkbox.isChecked(),
            "custom_back": self.custom_back_input.toPlainText(),
            "use_custom_css": self.custom_css_checkbox.isChecked(),
            "custom_css": self.custom_css_input.toPlainText(),
            "auto_color_bold": self.auto_color_bold_checkbox.isChecked(),
        }

        try:
            with open(os.path.join(os.path.dirname(__file__), "user_settings.json"), "w") as f:
                json.dump(user_settings, f, indent=4)
            self.create_card_type()
            # showInfo("Card Type created successfully!")
        except Exception as e:
            showInfo(f"Error creating card type: {e}")

    def load_settings(self):
        """Carregar as configurações do arquivo ou usar valores padrão"""
        settings_file = self.get_settings_file()
        try:
            with open(settings_file, "r") as f:  # Correct indentation here
                self.user_settings = json.load(f)
        except FileNotFoundError:
            self.user_settings = {}
        
        if os.path.exists(settings_file):
            with open(settings_file, "r") as file:
                settings = json.load(file)
                self.show_hints_checkbox.setChecked(settings.get("show_hints", False))
                self.show_blur_checkbox.setChecked(settings.get("show_blur", False))
                self.current_colors = settings.get("colors", self.default_settings["deck_colors"]) 


                self.custom_css_input.setPlainText(self.default_settings["custom_css"])
                # Carregar cores salvas (similar to previous implementation)

    def restore_defaults(self):
        self.card_type_name_input.setText(self.default_settings["card_type_name"])
        self.show_decks_checkbox.setChecked(self.default_settings["show_decks"])
        self.show_hints_checkbox.setChecked(self.default_settings["show_hints"])
        self.show_blur_checkbox.setChecked(self.default_settings["show_blur"])
        self.deck_colors_checkbox.setChecked(True)
        self.deck_colors_input.setText(",".join(self.default_settings["deck_colors"]))
        self.toggle_deck_colors_input(True)
        self.cloze_colors_checkbox.setChecked(True)
        self.cloze_colors_input.setText(",".join(self.default_settings["cloze_colors"]))
        self.toggle_cloze_colors_input(True)
        self.custom_front_checkbox.setChecked(True)
        self.custom_front_input.setPlainText(self.default_settings["custom_front"])
        self.toggle_custom_front_input(True)
        self.custom_back_checkbox.setChecked(True)
        self.custom_back_input.setPlainText(self.default_settings["custom_back"])
        self.toggle_custom_back_input(True)
        self.custom_css_checkbox.setChecked(True)
        self.custom_css_input.setPlainText(self.default_settings["custom_css"])
        self.toggle_custom_css_input(True)
        self.auto_color_bold_checkbox.setChecked(self.default_settings["auto_color_bold"])

    def create_card_type(self):
        card_type_name = self.card_type_name_input.text().strip()
        colorsHTML = self.deck_colors_input.text().strip()
        colorsClzHTML = self.cloze_colors_input.text().strip()

        if not card_type_name:
            showInfo("Please enter a Card Type Name.")
            return

        # Check for existing card type name
        mm = mw.col.models
        existing = mm.by_name(card_type_name)

        if existing:
            showInfo("O tipo de nota '" + card_type_name + "' já existe!")
            return

        # Create a new card type
        model = mw.col.models.new(card_type_name)
        # model["tmpls"].append({})
        # model["tmpls"][0]["qfmt"] = "{{FrontSide}}"
        # model["tmpls"][0]["afmt"] = "{{FrontSide}}\n\n<hr id=answer>\n{{BackSide}}"

        mm.add_field(model, mm.new_field("Text"))
        mm.add_field(model, mm.new_field("Extra"))

        # Adiciona o template Cloze com a estrutura HTML personalizada
        template = {
            "name": card_type_name,
            "qfmt": """
<script>
    var boldElements = document.querySelectorAll("b, strong");
    var elements = document.querySelectorAll('.cloze');
    var keyDownHandled = false;
    var other = ["#FF6B6B", "#FFA463", "#FFFF6B"];
    function animateColor(element, array) {
        let colorIndex = 0;
        element.style.transition = "color 2s ease-in-out";
        setInterval(() => {
            element.style.color = array[colorIndex]; // Aplica a cor
            colorIndex = (colorIndex + 1) % array.length; // Alterna as cores
        }, 3000); // Muda a cor a cada 1 segundo (1000 ms)
    }</script>""",  
            "afmt": """<script>
    var boldElements = document.querySelectorAll("b, strong");
    var elements = document.querySelectorAll('.cloze');
    var keyDownHandled = false;
    
    var other = ["#FF6B6B", "#FFA463", "#FFFF6B"];
    var colorsClz = ["#0bba2e", "#0bba5d", "#0bba5d", "#0bba5d"]; 
    function animateColor(element, array) {
        let colorIndex = 0;
        element.style.transition = "color 2s ease-in-out";
        setInterval(() => {
            element.style.color = array[colorIndex]; // Aplica a cor
            colorIndex = (colorIndex + 1) % array.length; // Alterna as cores
        }, 3000); // Muda a cor a cada 1 segundo (1000 ms)
    }</script>
            """
            # "afmt": "{{cloze:Text}}<br>{{Extra}}",
        }
        
    
        # Adiciona o modelo ao banco de dados

        # coment bellow
        # Set CSS
        if self.auto_color_bold_checkbox.isChecked():
            try:  
                htmlEl = f'<script> var colors = [{colorsHTML}]; </script>'
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format for colorsClzHTML: {colorsHTML}")
                # Handle the error, e.g., display an error message to the user
                htmlEl = """<script>var colors = ["#FF6B6B", "#FFA463", "#FFFF6B", "#63FF91", "#63C4FF", "#B163FF", "#FF63D2", "#F7C294", "#A3D8A3", "#92B5E9"];</script>"""            

            
            template["qfmt"] += htmlEl
            template['afmt'] += htmlEl

        if self.cloze_colors_checkbox.isChecked():
            try:
                htmlEl = f'<script> var colorsClz = [{colorsClzHTML}]; </script>'
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format for colorsClzHTML: {colorsClzHTML}")
                # Handle the error, e.g., display an error message to the user
                htmlEl = """<script>var colorsClz = ["#0bba2e", "#0bba5d", "#0bba5d", "#0bba5d"];</script>"""            

            template["qfmt"] += htmlEl
            template['afmt'] += htmlEl



        if self.custom_css_checkbox.isChecked():
            model["css"] = self.custom_css_input.toPlainText()
        else:
            model["css"] = """
            .card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
.cloze {
    font-weight: bold;
    color: blue;
}
.nightMode .cloze {
    color: lightblue;
}"""

        if self.show_decks_checkbox.isChecked():
            template["qfmt"] += """<span class="clzz"></span><div class="deck-name">{{Subdeck}}</div>{{cloze:Text}}"""
            template['afmt'] += """<span class="clzz"></span><div class="deck-name">{{Subdeck}}</div>
{{cloze:Text}}<br>
<div id='extra'>{{Extra}}</div>"""
        else:
            template['qfmt'] += """<span class="clzz"></span>{{cloze:Text}}"""
            template['afmt'] += """<span class="clzz"></span>{{cloze:Text}}<br>
<div id='extra'>{{Extra}}</div>"""

        # # Set deck colors (if enabled)
        if self.deck_colors_checkbox.isChecked():
            template["qfmt"] += """<script>var deckNameElement = document.querySelector('.deck-name');
var updatedText = deckNameElement.innerText.replace(/^\d+/g, '').trim();
deckNameElement.innerText = updatedText;
deckNameElement.style.color = "#FF6B6B";
animateColor(deckNameElement, other);
</script>"""
            template["afmt"] += """<script>var deckNameElement = document.querySelector('.deck-name');
var updatedText = deckNameElement.innerText.replace(/^\d+/g, '').trim();
deckNameElement.innerText = updatedText;
deckNameElement.style.color = "#FF6B6B";
animateColor(deckNameElement, other);
</script>"""


        if self.auto_color_bold_checkbox.isChecked():
            template["qfmt"] += """<script>
                boldElements.forEach(element => { color = colors.shift(); element.style.setProperty("color", color, "important"); })
            </script>
            """

            template["afmt"] += """<script>
                boldElements.forEach(element => { color = colors.shift(); element.style.setProperty("color", color, "important"); })
            </script>
            """

        if self.show_blur_checkbox.isChecked():
            htmlEl = """<script>
                elements.forEach(element => {
    element.style.fontWeight = 'bold'
    element.style.color = "#0bba2e"
    // Obter o valor do atributo `data-cloze`
    text = element.getAttribute('data-cloze');
       
    // Substituir o texto interno pelo valor de `data-cloze`
    if (element.innerText.includes('[...]')) {
        element.innerText = text.replace(/<\/?[^>]+(>|$)/g, '');
        element.style.filter = 'blur(7px)';
    }
       
    // Adicionar o efeito de blur via CSS
    animateColor(element, colorsClz);
})
            </script>
            """
            template["qfmt"] += htmlEl

            template["afmt"] += htmlEl
        

        if self.show_hints_checkbox.isChecked():
            htmlEl = """
<script>
document.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() === 'h' && !event.repeat && !keyDownHandled) {
        keyDownHandled = true;
        elements.forEach(element => {
        if (element.innerText.substring(0,1) == '[') {
            if (element.style.filter === 'blur(7px)') {
                element.style.filter = 'none';
            } else {
                element.style.filter = 'blur(7px)';
            }
        }
        });
    }
});

document.addEventListener('keyup', (event) => {
    if (event.key.toLowerCase() === 'h') {
        keyDownHandled = false; // Permitir próximo disparo
    }
});
</script>
            """
            template["qfmt"] += htmlEl

            template["afmt"] += htmlEl

        if self.cloze_colors_checkbox.isChecked():
            htmlEl = """
            <script>
        elements.forEach(element => {
            element.style.fontWeight = 'bold'
            element.style.color = "#0bba2e"
            // Obter o valor do atributo `data-cloze`
            text = element.getAttribute('data-cloze');
           
            // Substituir o texto interno pelo valor de `data-cloze`
            console.log('previous Text:', element.innerText)
            if (element.innerText.includes('[...]')) {
                element.innerText = text.replace(/<\/?[^>]+(>|$)/g, '');
                element.style.filter = 'blur(7px)';
            }        
            animateColor(element, colorsClz);
        })</script>
            """

            template["qfmt"] += htmlEl

            template["afmt"] += htmlEl

        if not self.auto_color_bold_checkbox.isChecked():
            htmlEl = """
            <script>
            elements.forEach(element => {
                element.style.fontWeight = 'bold'
                element.style.color = "blue"
                // Obter o valor do atributo `data-cloze`
                text = element.getAttribute('data-cloze');
               
                // Substituir o texto interno pelo valor de `data-cloze`
                console.log('previous Text:', element.innerText)
                if (element.innerText.includes('[...]')) {
                    element.innerText = text.replace(/<\/?[^>]+(>|$)/g, '');
                    element.style.filter = 'blur(7px)';
                }        
            })</script>
            """

            template["qfmt"] += htmlEl

            template["afmt"] += htmlEl
        # css


        
        


        # if self.custom_back_checkbox.isChecked():
        #     model["tmpls"][0]["afmt"] = self.custom_back_input.toPlainText()

        # Auto-color bold elements
        # if self.auto_color_bold_checkbox.isChecked():
            # model["css"] += "\n.card .cloze:not(.cloze-deletion) b { color: red; }"

        model["tmpls"] = [template]  # Define os templates
        model["type"] = 1  # Define como Cloze

        # mw.models.save(model)
        # mw.reset()
        mm.add(model)
        mw.reset()
        showInfo("O tipo de nota '" + card_type_name + "' foi criado com sucesso!")
        

    def toggle_deck_colors_input(self, state):
        self.deck_colors_input.setEnabled(state)  # Use state directly

    def toggle_cloze_colors_input(self, state):
        self.cloze_colors_input.setEnabled(state)  # Use state directly

    def toggle_custom_front_input(self, state):
        self.custom_front_input.setEnabled(state)  # Use state directly

    def toggle_custom_back_input(self, state):
        self.custom_back_input.setEnabled(state)  # Use state directly

    def toggle_custom_css_input(self, state):
        self.custom_css_input.setEnabled(state)  # Use state directly

    def apply_settings(self):
        self.save_settings()  # Call the save_settings method to save changes
        self.close()  # Close the dialog after applying settings

    def get_settings_file(self):
        """Returns the path to the user settings file."""
        return os.path.join(os.path.dirname(__file__), "user_settings.json")
