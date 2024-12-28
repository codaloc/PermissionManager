from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_main_window
import sys

def back():
    text = ui.path_input.text()
    print(text)
    ui.text_label.setText(text)

def delete_widgets(layout):
    if layout is not None:
        for i in reversed(range(layout.count())): 
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        layout.update()
        
def draw_all_buttons(number_of_buttons):
    window_size = main_window.size()
    width = window_size.width()
    row_number = (width-100) // 200

    delete_widgets(ui.main_grid)
    for i in range(number_of_buttons):
        create_dynamic_button(row_number)


def create_dynamic_button(row_number):
    button_nb = len(ui.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton))
    row = button_nb // row_number
    column = button_nb % row_number

    new_grid_button = QtWidgets.QPushButton(ui.scrollAreaWidgetContents)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(new_grid_button.sizePolicy().hasHeightForWidth())
    new_grid_button.setSizePolicy(sizePolicy)
    new_grid_button.setMinimumSize(QtCore.QSize(200, 100))
    new_grid_button.setMaximumSize(QtCore.QSize(200, 100))
    new_grid_button.setObjectName(f"button_{button_nb}")
    ui.main_grid.addWidget(new_grid_button, row, column, 1, 1)
    
    new_grid_button.setText(f"Grid Button {button_nb}")
    new_grid_button.clicked.connect(lambda: print(f"Clicked {new_grid_button.text()}"))
    new_grid_button.show()
############# create app
app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
ui = Ui_main_window()
ui.setupUi(main_window)
ui.centralwidget.resizeEvent = lambda event: draw_all_buttons(15)

############# linking functions
ui.back_button.clicked.connect(back)
ui.folder_perms_button.clicked.connect(lambda: draw_all_buttons(15))





############# show and exit
main_window.show()
sys.exit(app.exec_())