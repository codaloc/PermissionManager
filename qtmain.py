# TODO
# deal with permission issues
# deal with large folders

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from qtui import Ui_main_window
from qtpermui import Ui_Dialog
import subprocess
import toml
import sys
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
    global FILE_TARGET_SIZE, FILE_HEIGHT, FILE_FONT_SIZE
    window_size = main_window.size()
    window_width = window_size.width()
    pseudo_margin = 0
    min_button_width = 0
    max_button_width = int(FILE_TARGET_SIZE*1.5)
    number_of_rows = (window_width - pseudo_margin) // FILE_TARGET_SIZE

    button_nb = len(ui.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton))
    row = button_nb // number_of_rows
    column = button_nb % number_of_rows

    new_grid_button = QtWidgets.QPushButton(ui.scrollAreaWidgetContents)
    size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(new_grid_button.sizePolicy().hasHeightForWidth())
    new_grid_button.setSizePolicy(size_policy)

    font = QtGui.QFont()
    font.setPointSize(FILE_FONT_SIZE)
    new_grid_button.setFont(font)

    new_grid_button.setMinimumSize(QtCore.QSize(min_button_width, FILE_HEIGHT))
    new_grid_button.setMaximumSize(QtCore.QSize(max_button_width, FILE_HEIGHT))
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
    window_file_perms(path)

def permission_of_folder():
    path = ui.path_input.text()
    window_file_perms(path)






############# permission window functions

def window_file_perms(path):
    perm_ui.path = path
    show_file_perms(path)
    perm_window.exec() # works in this order (?)
    perm_ui.command_line.hide()
    perm_ui.command_label.hide()
    perm_ui.command_label.setText("Command :")
    perm_ui.run_button.setEnabled(False)


def show_modified_perms():
    human_readable_aired, octal = get_readable_and_octal_from_list(get_checkboxes_values())
    oneliner = f"{human_readable_aired}  ({octal})"
    perm_ui.permission_string.setText(oneliner)

    #changes command in case it is visible
    human_readable_aired, octal = get_readable_and_octal_from_list(get_checkboxes_values())
    command = f"chmod {octal} {perm_ui.path}"
    perm_ui.command_line.setText(command)


def show_file_perms(path):
    if os.path.exists(path):
        command = f"stat {path} -c %a%A" # 755-rwxr-xr-x
        result = subprocess.run(command, capture_output=True, check=True, shell=True)
        output = result.stdout.decode().rstrip()

        human = output[4:]
        octal_perms = output[:3]
        aired_human = ""
        for i, char in enumerate(human):
            if i % 3 == 0 and i != 0:
                aired_human += ("  ")
            aired_human += char
        oneliner = f"{aired_human}  ({octal_perms})"

        perm_ui.permission_string.setText(oneliner)
        perm_ui.file_label.setText(os.path.basename(path))

        set_checkboxes(perms_to_list(octal_perms))


def perms_to_list(octalperms):
    # ocal : [read, write, execute]
    permdict = {
        0: [False, False, False],
        1: [False, False, True],
        2: [False, True, False],
        3: [False, True, True],
        4: [True, False, False],
        5: [True, False, True],
        6: [True, True, False],
        7: [True, True, True]
    }

    allperms = []

    for char in octalperms:
        allperms.append(permdict[int(char)])

    return allperms


def set_checkboxes(perm_list):
    checkboxes_list = [
        perm_ui.ur_checkbox,
        perm_ui.uw_checkbox,
        perm_ui.ue_checkbox,
        perm_ui.gr_checkbox,
        perm_ui.gw_checkbox,
        perm_ui.ge_checkbox,
        perm_ui.or_checkbox,
        perm_ui.ow_checkbox,
        perm_ui.oe_checkbox
    ]

    perm_order_nb=0
    for user in perm_list:
        for permission in user:

            checkboxes_list[perm_order_nb].setChecked(permission)
            #sperm_ui.ur_checkbox.setChecked(True)
            perm_order_nb += 1


def get_checkboxes_values():
    perms_list = []
    perms_list.append([perm_ui.ur_checkbox.isChecked(), perm_ui.uw_checkbox.isChecked(), perm_ui.ue_checkbox.isChecked()])
    perms_list.append([perm_ui.gr_checkbox.isChecked(), perm_ui.gw_checkbox.isChecked(), perm_ui.ge_checkbox.isChecked()])
    perms_list.append([perm_ui.or_checkbox.isChecked(), perm_ui.ow_checkbox.isChecked(), perm_ui.oe_checkbox.isChecked()])
    return perms_list


def get_readable_and_octal_from_list(perms_list):
    bool_dict = {
        (False, False, False): 0,
        (False, False, True): 1,
        (False, True, False): 2,
        (False, True, True): 3,
        (True, False, False): 4,
        (True, False, True): 5,
        (True, True, False): 6,
        (True, True, True): 7
    }
    human_readable_dict = {
        "0": "---",
        "1": "--x",
        "2": "-w-",
        "3": "-wx",
        "4": "r--",
        "5": "r-x",
        "6": "rw-",
        "7": "rwx"
    }

    octalperms = ""
    human_readable = []

    for subperm in perms_list:
        octalperms += str(bool_dict[tuple(subperm)])

    for oct in octalperms:
        human_readable.append(human_readable_dict[oct])
    human_readable = "  ".join(human_readable)

    return human_readable, octalperms


def show_command():
    human_readable_aired, octal = get_readable_and_octal_from_list(get_checkboxes_values())
    command = f"chmod {octal} {perm_ui.path}"
    perm_ui.command_line.show()
    perm_ui.command_label.show()
    perm_ui.command_line.setText(command)


    perm_ui.run_button.setEnabled(True)


def manually_changed_command():
    perm_ui.command_label.setText("Command (edited) :")


def command_failed_color_alert():
    perm_ui.command_line.setStyleSheet("color: red;")
    QTimer.singleShot(400, command_failed_alert_revert)

def command_failed_alert_revert():
    perm_ui.command_line.setStyleSheet("")


def command_success_color_alert():
    perm_ui.file_label.setStyleSheet("color: green;")
    QTimer.singleShot(1000, command_success_alert_revert)

def command_success_alert_revert():
    perm_ui.file_label.setStyleSheet("")



def run_command():
    command = perm_ui.command_line.text()
    print(f"running {command}")
    try:
        result = subprocess.run(command, capture_output=True, check=True, shell=True)
        perm_ui.command_line.hide()
        perm_ui.command_label.hide()
        perm_ui.run_button.setEnabled(False)
        command_success_color_alert()
    except:
        command_failed_color_alert()




############# create app

with open("config.toml", "r") as file:
    config = toml.load(file)
    FILE_TARGET_SIZE = config["files"]["file_target_size"]
    FILE_HEIGHT = config["files"]["file_height"]
    FILE_FONT_SIZE = config["files"]["file_font_size"]


app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
ui = Ui_main_window()
ui.setupUi(main_window)
ui.path_input.setText("/")


perm_window = QtWidgets.QDialog()
perm_ui = Ui_Dialog()
perm_ui.setupUi(perm_window)
perm_ui.command_line.hide()
perm_ui.command_label.hide()



# could add option to toggle:
ui.centralwidget.resizeEvent = lambda event: draw_path_buttons()

set_checkboxes_to_default()
############# linking functions (explorer)
ui.back_button.clicked.connect(back)
ui.folder_perms_button.clicked.connect(draw_path_buttons)
ui.show_dirs_checkbox.stateChanged.connect(draw_path_buttons)
ui.show_hidden_checkbox.stateChanged.connect(draw_path_buttons)
ui.altsort_checkbox.stateChanged.connect(draw_path_buttons)
ui.folder_perms_button.clicked.connect(permission_of_folder)

enter_action = QtWidgets.QAction("Enter", ui.path_input)
enter_action.setShortcut(Qt.Key_Return)
enter_action.triggered.connect(shortcut_triggered)
main_window.addAction(enter_action)

############# linking functions (permissions)
perm_ui.get_button.clicked.connect(lambda: show_file_perms(perm_ui.path))

perm_ui.ur_checkbox.clicked.connect(show_modified_perms)
perm_ui.uw_checkbox.clicked.connect(show_modified_perms)
perm_ui.ue_checkbox.clicked.connect(show_modified_perms)
perm_ui.gr_checkbox.clicked.connect(show_modified_perms)
perm_ui.gw_checkbox.clicked.connect(show_modified_perms)
perm_ui.ge_checkbox.clicked.connect(show_modified_perms)
perm_ui.or_checkbox.clicked.connect(show_modified_perms)
perm_ui.ow_checkbox.clicked.connect(show_modified_perms)
perm_ui.oe_checkbox.clicked.connect(show_modified_perms)

perm_ui.change_button.clicked.connect(show_command)
perm_ui.command_line.textEdited.connect(manually_changed_command)
perm_ui.run_button.clicked.connect(run_command)



############# show and exit
main_window.show()
#perm_window.exec()

draw_path_buttons()

sys.exit(app.exec_())
