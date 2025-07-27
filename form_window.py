from PyQt6 import QtWidgets
import typing

class AppWindow(QtWidgets.QMainWindow):
    """An application window containing a label and combobox"""
    
    central_widget: QtWidgets.QWidget
    selected_country_label: QtWidgets.QLabel
    country_picker: QtWidgets.QComboBox

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(20, 20, 600, 400)
        self.setWindowTitle("Country Picker")
        
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        new_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(new_layout)


        selected_country_label = QtWidgets.QLabel()
        new_layout.addWidget(selected_country_label)
        
        country_picker = QtWidgets.QComboBox()
        new_layout.addWidget(country_picker)

        self._country_list = None

        self.show()

    def update_country_list(self, new_country_list: list[str]) -> None:
        self._country_list = new_country_list