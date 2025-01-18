from PyQt5 import QtCore, QtGui, QtWidgets
from qtui import Ui_main_window
import sys
import os


def back():  #only helper right now
    text = ui.path_input.text()
    print(text)
    ui.text_label.setText(text)
    print(ui.show_dirs_checkbox.isChecked())
    print(ui.show_hidden_checkbox.isChecked())
    print(get_file_list(get_path_input()))


def get_path_input():
    print(f"got:{ui.path_input.text().strip()}")
    return ui.path_input.text().strip()


def get_file_list(path):
    files = []
    print(f"path:{path}")
    if os.path.isdir(path):
        for file in os.listdir(path):
            path_file = os.path.join(path,file)
            if not ui.show_hidden_checkbox.isChecked():
                if file.startswith('.'):
                    continue
                else:
                    if ui.show_dirs_checkbox.isChecked():
                        files.append(file)
                    else:
                        if os.path.isfile(path_file):
                            files.append(file)
            else:
                if ui.show_dirs_checkbox.isChecked():
                    files.append(file)
                else:
                    if os.path.isfile(path_file):
                        files.append(file)

        files.sort()
        return files
    else:
        return []


def delete_widgets(layout):
    if layout is not None:
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        layout.update()


def draw_path_buttons():
    path = get_path_input()
    files = get_file_list(path)
    delete_widgets(ui.main_grid)
    for file in files:
        create_dynamic_button2(file)

def create_dynamic_button2(button_name):
    window_size = main_window.size()
    window_width = window_size.width()
    margin = 100
    button_width = 200
    number_of_rows = (window_width - margin) // button_width

    button_nb = len(ui.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton))
    row = button_nb // number_of_rows
    column = button_nb % number_of_rows

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

    new_grid_button.setText(f"{button_name}")
    new_grid_button.clicked.connect(lambda: folder_clicked())
    new_grid_button.show()

def folder_clicked():
    pass

# def change_path_input(endpath):
#     old_path = get_path_input()
#     ui.path_input.setText(os.path.join(old_path,endpath))

############# create app
app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
ui = Ui_main_window()
ui.setupUi(main_window)
ui.path_input.setText("/")

# could add option to toggle:
ui.centralwidget.resizeEvent = lambda event: draw_path_buttons()

############# linking functions
ui.back_button.clicked.connect(back)
ui.folder_perms_button.clicked.connect(draw_path_buttons)
ui.show_dirs_checkbox.stateChanged.connect(draw_path_buttons)
ui.show_hidden_checkbox.stateChanged.connect(draw_path_buttons)

############# show and exit
main_window.show()

draw_path_buttons()

sys.exit(app.exec_())
