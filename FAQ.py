import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTextEdit, QPushButton, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class InvasiveSpeciesChat(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("AGRINOVA - Chat bot")
        self.main_window = main_window  # Store the reference to the main window
        self.setWindowTitle("मेरो खेतबारी सहयोगी (My Farm Helper)")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("favicon.png"))
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create top bar with back button
        top_bar = QHBoxLayout()
        back_button = QPushButton("← फर्कनुहोस् (Back)")
        back_button.setFont(QFont('Arial', 10, QFont.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #2C5F2D;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #1F4F20;
            }
        """)
        back_button.clicked.connect(self.go_back)
        top_bar.addWidget(back_button)
        top_bar.addStretch()
        layout.addLayout(top_bar)
        
        # Create header
        header = QLabel("तपाईंको खेतबारीको लागि जानकारी प्राप्त गर्नुहोस् (Get Information for Your Farm)")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont('Arial', 14, QFont.Bold))
        header.setStyleSheet("color: #2C5F2D; padding: 10px;")
        layout.addWidget(header)
        
        # Create chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont('Arial', 12))
        self.chat_display.setStyleSheet("background-color: #F0F7F4; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.chat_display)
        
        # Create input area
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(50)
        self.input_field.setFont(QFont('Arial', 12))
        self.input_field.setPlaceholderText("कृपया बोटको नाम लेख्नुहोस् (Please type plant name here)")
        self.input_field.setStyleSheet("border: 2px solid #2C5F2D; border-radius: 10px; padding: 5px;")
        
        send_button = QPushButton("पठाउनुहोस् (Send)")
        send_button.setFont(QFont('Arial', 12, QFont.Bold))
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #2C5F2D;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1F4F20;
            }
        """)
        send_button.clicked.connect(self.process_input)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)
        
        # Initialize the species database
        self.species_info = {
            "parthenium hysterophorus": {
                "common_names": ["congress grass", "gajar ghas"],
                "danger_level": "उच्च खतरा (High Risk)",
                "symptoms": "- बालीको उत्पादनमा कमी (Reduces crop yield)\n- मानिसमा एलर्जी (Causes allergies in humans)\n- पशुधनको लागि विषाक्त (Toxic to livestock)",
                "control": "- हातले उखेल्ने (Manual removal)\n- जैविक नियन्त्रण (Zygogramma bicolorata beetle)\n- झारपात नाशक औषधि (Herbicides)",
                "prevention": "- नियमित निरीक्षण (Regular monitoring)\n- स्वच्छ बीउको प्रयोग (Use clean seeds)\n- खेतबारी सफा राख्ने (Keep farm clean)"
            },
            "eichhornia crassipes": {
                "common_names": ["water hyacinth"],
                "danger_level": "मध्यम खतरा (Medium Risk)",
                "symptoms": "- सिंचाई प्रणालीमा अवरोध (Clogs irrigation systems)\n- कीरा र रोगको वृद्धि (Harbors pests and diseases)",
                "control": "- यान्त्रिक हटाउने (Mechanical removal)\n- जैविक नियन्त्रण (Neochetina eichhorniae weevils)",
                "prevention": "- पानीको स्रोत सफा राख्ने (Regular cleaning of water bodies)\n- नियमित निगरानी (Regular monitoring)"
            },
            "mikania micrantha": {
                "common_names": ["mile-a-minute weed"],
                "danger_level": "उच्च खतरा (High Risk)",
                "symptoms": "- बालीलाई लुकाउँछ (Smothers crops)\n- सूर्यको प्रकाश रोक्छ (Blocks sunlight)\n- उत्पादन घटाउँछ (Reduces yields)",
                "control": "- हातले काट्ने (Manual cutting)\n- जैविक नियन्त्रण (Puccinia spegazzinii rust fungus)",
                "prevention": "- नियमित घाँस काट्ने (Regular weeding)\n- अनुगमन गर्ने (Monitoring)"
            },
            "lantana camara": {
                "common_names": ["lantana weed"],
                "danger_level": "उच्च खतरा (High Risk)",
                "symptoms": "- खेतिहरूमा आक्रमण गर्छ (Invades farmlands)\n- माटोको उर्वरता घटाउँछ (Reduces soil fertility)\n- पशुहरूको लागि विषाक्त (Toxic to livestock)",
                "control": "- जरा उखेल्ने (Uprooting)\n- नियन्त्रित आगो लगाउने (Controlled burning)\n- हर्बिसाइड (Herbicides)",
                "prevention": "- छिटो पत्ता लगाउने (Early detection)\n- हटाउने (Removal)"
            },
            "ageratina adenophora": {
                "common_names": ["crofton weed", "banmara"],
                "danger_level": "मध्यम खतरा (Medium Risk)",
                "symptoms": "- छिटो फैलिन्छ (Spreads rapidly)\n- चराउने जमीन घटाउँछ (Reduces grazing land)\n- मकै र गहुँको बालीलाई असर गर्छ (Affects maize and wheat crops)",
                "control": "- हातले हटाउने (Manual removal)\n- जैविक नियन्त्रण (Procecidochares utilis gall fly)",
                "prevention": "- नियमित अनुगमन (Regular monitoring)\n- हटाउने (Removal)"
            },
            "chromolaena odorata": {
                "common_names": ["siam weed"],
                "danger_level": "उच्च खतरा (High Risk)",
                "symptoms": "- स्थानीय वनस्पतिहरूलाई प्रतिस्पर्धा गर्छ (Outcompetes native vegetation)\n- जमीनको उत्पादकता घटाउँछ (Reduces land productivity)",
                "control": "- काट्ने (Slashing)\n- आगो प्रबन्धन (Fire management)\n- रासायनिक नियन्त्रण (Chemical control)",
                "prevention": "- जमीन नियमित सफा गर्ने (Regular clearing of land)"
            },
            "leucaena leucocephala": {
                "common_names": ["subabul", "ipil-ipil"],
                "danger_level": "मध्यम खतरा (Medium Risk)",
                "symptoms": "- खेतिहरूमा आक्रमणकारी फैलावट (Aggressive spread into farmlands)\n- माटोको संरचना असर गर्छ (Affects soil composition)\n- बालीको ठाउँ घटाउँछ (Reduces crop space)",
                "control": "- बीज बनाउनु अघि काट्ने (Cutting before seeding)\n- रासायनिक नियन्त्रण (Chemical control)",
                "prevention": "- नियमित अनुगमन (Regular monitoring)\n- हटाउने (Removal)"
            },
            "xanthium strumarium": {
                "common_names": ["cocklebur", "dhotre ghans"],
                "danger_level": "मध्यम खतरा (Medium Risk)",
                "symptoms": "- मकै, गहुँ, र चामल खेतसँग प्रतिस्पर्धा गर्छ (Competes with maize, wheat, and rice fields)\n- पशुहरूको लागि विषाक्त बीज उत्पादन गर्छ (Produces toxic seeds harmful to livestock)",
                "control": "- हातले जरा उखेल्ने (Manual uprooting)\n- हर्बिसाइड (Herbicides)",
                "prevention": "- नियमित घाँस काट्ने (Regular weeding)\n- अनुगमन गर्ने (Monitoring)"
            },
            "persicaria perfoliata": {
                "common_names": ["asiatic tear thumb", "lahare jhadi"],
                "danger_level": "मध्यम खतरा (Medium Risk)",
                "symptoms": "- छिटो बढ्ने बेलाले सरसों र तरकारी जस्ता युवा बालीलाई लुकाउँछ (Fast-growing vine that smothers young crops like mustard and vegetables)",
                "control": "- यान्त्रिक हटाउने (Mechanical removal)\n- मल्च गर्ने (Mulching)",
                "prevention": "- नियमित घाँस काट्ने (Regular weeding)\n- अनुगमन गर्ने (Monitoring)"
            },
            "ipomoea carnea": {
                "common_names": ["pink morning glory", "beshram"],
                "danger_level": "उच्च खतरा (High Risk)",
                "symptoms": "- सिंचाई नहरहरू बन्द गर्छ (Chokes irrigation canals)\n- धान र गहुँसँग प्रतिस्पर्धा गर्छ (Competes with paddy and wheat crops)\n- गाईवस्तुको लागि विषाक्त (Toxic to cattle)",
                "control": "- जरा उखेल्ने (Uprooting)\n- चराउने नियन्त्रण (Grazing control)\n- रासायनिक उपचार (Chemical treatment)",
                "prevention": "- सिंचाई नहर नियमित सफा गर्ने (Regular clearing of irrigation canals)"
            }
        }
        
        # Show welcome message
        self.show_welcome_message()
    
    def go_back(self):
        try:
            # Hide the current window
            self.hide()
            
            # Show the main window
            self.main_window.show()
        except Exception as e:
            print(f"Error returning to main menu: {e}")
        
    def show_welcome_message(self):
        welcome_text = """
        🌿 स्वागत छ! (Welcome!)
        
        म तपाईंको खेतबारी सहयोगी हुँ। कृपया कुनै पनि हानिकारक बोटको नाम टाइप गर्नुहोस्, 
        र म तपाईंलाई त्यसको बारेमा जानकारी दिनेछु।
        
        You can type either the common name or scientific name of any harmful plant.
        """
        self.chat_display.append(welcome_text)
    
    def process_input(self):
        user_input = self.input_field.toPlainText().lower().strip()
        self.input_field.clear()
        
        # Display user input
        self.chat_display.append("\n👨‍🌾 तपाईं: " + user_input)
        
        # Search for the plant in our database
        found = False
        for species, info in self.species_info.items():
            if user_input in [species.lower()] + [name.lower() for name in info["common_names"]]:
                response = f"""
                \n🌱 बोटको जानकारी:
                
                खतराको स्तर (Danger Level):
                {info['danger_level']}
                
                लक्षणहरू (Symptoms):
                {info['symptoms']}
                
                नियन्त्रणका उपायहरू (Control Measures):
                {info['control']}
                
                रोकथामका उपायहरू (Prevention):
                {info['prevention']}
                """
                self.chat_display.append(response)
                found = True
                break
        
        if not found:
            self.chat_display.append("\n❌ माफ गर्नुहोस्, यो बोटको बारेमा मलाई जानकारी छैन। कृपया अर्को नाम प्रयास गर्नुहोस्।\n(Sorry, I don't have information about this plant. Please try another name.)")
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create the main window (dummy placeholder)
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Main Window")
    
    main_window = MainWindow()
    
    # Create and show the chat window, passing the main window instance
    chat_window = InvasiveSpeciesChat(main_window)
    chat_window.show()
    
    sys.exit(app.exec_())