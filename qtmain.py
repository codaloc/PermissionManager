# TODO
# read toml file for default checkboxes states and config(like rewrite on resize and file sizes)
# deal with permission issues
# implement the actual permissions

from PyQt5 import QtCore, QtGui, QtWidgets
from qtui import Ui_main_window
from PyQt5.QtCore import Qt, QTimer
import sys
import toml
import os

def get_path_input():
    return ui.path_input.text().strip()


def set_checkboxes_to_default():
    with open("config.toml", "r") as file:
        config = toml.load(file)

        ui.show_dirs_checkbox.setChecked(config["checkboxes_defaults"]["showdirs"])
        ui.show_hidden_checkbox.setChecked(config["checkboxes_defaults"]["showhidden"])
        altsort_state = config["checkboxes_defaults"]["altsort"]
        if altsort_state == 0:
            ui.altsort_checkbox.setCheckState(Qt.Unchecked)
        elif altsort_state == 1:
            ui.altsort_checkbox.setCheckState(Qt.PartiallyChecked)
        elif altsort_state == 2:
            ui.altsort_checkbox.setCheckState(Qt.Checked)


def get_file_list(path):
    files = []
    if os.path.isdir(path):

        for file in os.listdir(path):
            path_file = os.path.join(path,file)
            show_hidden = ui.show_hidden_checkbox.isChecked()
            show_dirs = ui.show_dirs_checkbox.isChecked()
            isfile = os.path.isfile(path_file)
            ishidden = file.startswith(".")

            if ishidden and not show_hidden:
                continue
            if isfile:
                files.append((file,1))
            else:
                if show_dirs:
                    files.append((file, 0))

        check_state = ui.altsort_checkbox.checkState()
        if check_state == Qt.Unchecked:
            files.sort()
        elif check_state == Qt.PartiallyChecked:
            files.sort()
            files.sort(key=lambda x: abs(x[1]-1))
        elif check_state == Qt.Checked:
            files.sort()
            files.sort(key=lambda x: x[1])



        return files
    else:
        print("Error: Not a path")
        return []


def delete_widgets(layout):
    if layout is not None:
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None and type(widget) == QtWidgets.QPushButton:
                widget.setParent(None)
        layout.update()


def draw_path_buttons():
    path = get_path_input()
    files = get_file_list(path)
    delete_widgets(ui.main_grid)
    for file in files:
        create_dynamic_button2(file[0],file[1])

def create_dynamic_button2(button_name,isfile):
    window_size = main_window.size()
    window_width = window_size.width()
    margin = 110
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

    new_grid_button.setMinimumSize(QtCore.QSize(200,100))
    new_grid_button.setMaximumSize(QtCore.QSize(280, 100))
    new_grid_button.setObjectName(f"button_{button_nb}")
    new_grid_button.setText(f"{button_name}")


    new_grid_button.clicked.connect(lambda: folder_clicked(button_name))
    ui.main_grid.addWidget(new_grid_button, row, column, 1, 1)
    new_grid_button.show()
    if not isfile:
        new_grid_button.setStyleSheet("border: 1px solid #444444; border-radius: 6px")

def folder_clicked(name):
    old_path = get_path_input()
    newpath = os.path.join(old_path, name)
    if os.path.isdir(newpath):
        ui.path_input.setText(newpath)
        draw_path_buttons()
    else:
        interacted_with_file(newpath)

def back():
    path = ui.path_input.text()
    path_split = path.split("/")
    if len(path_split) == 2:
        newpath = "/"
    else:
        newpath = "/".join(path_split[:-1])

    ui.path_input.setText(newpath)
    if os.path.exists(newpath):
        draw_path_buttons()
    else:
        path_input_color_alert()

def path_input_color_alert():
    ui.path_input.setStyleSheet("color: red;")
    QTimer.singleShot(300, path_input_revert_to_black)

def path_input_revert_to_black():
    ui.path_input.setStyleSheet("")

def shortcut_triggered():
    if os.path.exists(get_path_input()):
        if os.path.isdir:
            draw_path_buttons()
        else:
            interacted_with_file(get_path_input())
    else:
        path_input_color_alert()

def interacted_with_file(path):
    last_part = path.split("/")[-1]
    ui.text_label.setText(last_part) 

############# create app
app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
ui = Ui_main_window()
ui.setupUi(main_window)
ui.path_input.setText("/")

# could add option to toggle:
ui.centralwidget.resizeEvent = lambda event: draw_path_buttons()

set_checkboxes_to_default()
############# linking functions
ui.back_button.clicked.connect(back)
ui.folder_perms_button.clicked.connect(draw_path_buttons)
ui.show_dirs_checkbox.stateChanged.connect(draw_path_buttons)
ui.show_hidden_checkbox.stateChanged.connect(draw_path_buttons)
ui.altsort_checkbox.stateChanged.connect(draw_path_buttons)
enter_action = QtWidgets.QAction("Enter", ui.path_input)
enter_action.setShortcut(Qt.Key_Return)
enter_action.triggered.connect(shortcut_triggered)
main_window.addAction(enter_action)

############# show and exit
main_window.show()

draw_path_buttons()

sys.exit(app.exec_())
