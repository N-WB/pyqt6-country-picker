from PyQt6 import QtWidgets
import typing
import compose
from typing import Any

def format_country_name(country_name: str) -> str:
    return "Selected: " + country_name

class AppWindow(QtWidgets.QMainWindow):
    """An application window containing a label and combobox for picking countries"""
    
    central_widget: QtWidgets.QWidget
    selected_country_label: QtWidgets.QLabel
    country_picker: QtWidgets.QComboBox
    countries_data: list[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setGeometry(20, 20, 600, 400)
        self.setWindowTitle("Country Picker")
        
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        new_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(new_layout)


        self.selected_country_label = QtWidgets.QLabel()
        new_layout.addWidget(self.selected_country_label)
        
        self.country_picker = QtWidgets.QComboBox()
        new_layout.addWidget(self.country_picker)

        slot = compose.compose(self.selected_country_label.setText, format_country_name)
        self.country_picker.currentTextChanged.connect(slot)
        
        self.show()