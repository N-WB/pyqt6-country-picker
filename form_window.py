from PyQt6 import QtWidgets
import typing
from typing import Any

class AppWindow(QtWidgets.QMainWindow):
    """An application window containing a label and combobox"""
    
    central_widget: QtWidgets.QWidget
    selected_country_label: QtWidgets.QLabel
    country_picker: QtWidgets.QComboBox

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

        self.country_picker.currentTextChanged.connect(self.selected_country_label.setText)

        self.show()

    def update_country_list(self, new_country_list: list[str]) -> None:
        self.country_picker.addItems(new_country_list)