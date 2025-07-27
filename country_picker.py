"""An app that presents a window containing a blank label and ComboBox."""

from PyQt6 import QtWidgets
import form_window
import typing

if __name__ == "__main__":

    application: QtWidgets.QApplication = QtWidgets.QApplication([])

    window: form_window.AppWindow = form_window.AppWindow()
    window.show()
    
    application.exec()