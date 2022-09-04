# Copyright: Dmitry Savosh (d.savosh@gmail.com)

import pyautogui
import time
import webbrowser

MOVE_DURATION = 0.3
LOCATE_DURATION = 3
MAX_ASSETS_TO_DOWNLOAD = 2000

clicked_pos = []
old_launcher_pos = None


def check_overwrite_files_question():
    pos = pyautogui.locateOnScreen('screens/add_to_project/overwrite_files_question_label.png', grayscale=False,
                                   confidence=.99)
    if pos:
        pos = pyautogui.locateOnScreen('screens/add_to_project/yes_button.png', grayscale=False, confidence=.99)
        if pos:
            pyautogui.click(pos)


def locate(image: str, sec=LOCATE_DURATION):
    if sec < 1:
        sec = 1
    for i in range(sec):
        check_overwrite_files_question()
        pos = pyautogui.locateOnScreen("screens/" + image, grayscale=False, confidence=.99)
        if pos:
            return pyautogui.center(pos)
        if i < sec - 1:
            time.sleep(1)
    return None


def locate_all(image: str, sec=LOCATE_DURATION):
    if sec < 1:
        sec = 1
    for i in range(sec):
        check_overwrite_files_question()
        pos_list = list(pyautogui.locateAllOnScreen("screens/" + image, grayscale=False, confidence=.99))
        if len(pos_list) > 0:
            pos_list = [pyautogui.center(pos) for pos in pos_list]
            return pos_list
        if i < sec - 1:
            time.sleep(1)
    return []


def move_to_pos(pos, duration=MOVE_DURATION, x_off=0, y_off=0):
    pyautogui.moveTo(pos.x + x_off, pos.y + y_off, duration=duration)


def move_to_if_exist(image: str, sec=LOCATE_DURATION, duration=MOVE_DURATION, x_off=0, y_off=0):
    pos = locate(image, sec)
    if pos:
        move_to_pos(pos, duration, x_off, y_off)
    return pos


def move_to(image: str, sec=LOCATE_DURATION, duration=MOVE_DURATION, x_off=0, y_off=0):
    res = move_to_if_exist(image, sec, duration, x_off, y_off)
    if res:
        return res
    else:
        print("Cant locate " + image)
        exit()


def click_if_exist(image: str, sec=LOCATE_DURATION, duration=MOVE_DURATION, x_off=0, y_off=0, move_out=False):
    pos = locate(image, sec)
    if pos:
        if move_out:
            # move out to prevent unclickable buttons bug
            move_to_pos(pos, duration, x_off, y_off)
            move_to_pos(pos, 0.2, x_off, y_off - 30)
            click_pos(pos, 0.2, x_off, y_off)
        else:
            click_pos(pos, duration, x_off, y_off)
    return pos


def click(image: str, sec=LOCATE_DURATION, duration=MOVE_DURATION, x_off=0, y_off=0, move_out=False):
    res = click_if_exist(image, sec, duration, x_off, y_off, move_out)
    if res:
        return res
    else:
        print("Cant locate " + image)
        exit()


def click_pos(pos, duration=MOVE_DURATION, x_off=0, y_off=0):
    pyautogui.click(pos.x + x_off, pos.y + y_off, duration=duration)


def locate_any(images, sec=LOCATE_DURATION):
    if sec < 1:
        sec = 1
    for i in range(sec):
        for image in images:
            pos = locate(image, 0)
            if pos:
                return pos
        if i < sec - 1:
            time.sleep(1)
    return None


def click_any_if_exist(images, sec=LOCATE_DURATION, duration=MOVE_DURATION):
    pos = locate_any(images, sec)
    if pos:
        pyautogui.click(pos, duration=duration)
    return pos


def click_any(images, sec=LOCATE_DURATION, duration=MOVE_DURATION):
    res = click_any_if_exist(images, sec, duration)
    if res:
        return res
    else:
        print("Cant locate any of images:")
        for image in images:
            print(image)
        exit()


def get_temp_project_name():
    milliseconds = int(round(time.time() * 1000))
    return "temp" + str(milliseconds)


def open_and_download_asset(asset_id: str):
    webbrowser.open(f"com.epicgames.launcher://ue/marketplace/item/{asset_id}", new=2)
    for i in range(3):
        if click_any(['asset_page/create_project_button1.png', 'asset_page/create_project_button2.png'], 0):
            create_project()
            break
        if click_any(['asset_page/add_to_project_button1.png', 'asset_page/add_to_project_button2.png'], 0):
            add_to_project()
            break


def install_plugin():
    if not locate("install_plugin/install_plugin_label.png"):
        print('Cant locate "Install Plugin" title.')
        return
    if locate("install_plugin/you_cannot_install_label.png"):
        click("install_plugin/cancel_button.png", LOCATE_DURATION, MOVE_DURATION, 0, 0, True)
        return
    click("install_plugin/install_button.png", LOCATE_DURATION, MOVE_DURATION, 0, 0, True)
    click_if_exist("install_plugin/dismiss_button.png", 0)


def create_project():
    if not locate('create_project/choose_project_name_label.png'):
        print('Cant locate "Choose Project Name" title.')
        return
    pos = locate('create_project/name_label.png')
    if pos:
        click_pos(pos, MOVE_DURATION, 100)
        with pyautogui.hold('ctrl'):
            pyautogui.press(['a'])
        pyautogui.press("backspace")
        pyautogui.write(get_temp_project_name())
        click("create_project/create_button.png")


def add_to_project():
    move_out_pos = locate("add_to_project/select_project_to_add_label.png", 2)
    if not move_out_pos:
        print('Cant locate "Select the Project to Add the Asset" title.')
        return
    if not click_if_exist('add_to_project/temp_project_name.png', 0):
        click('add_to_project/show_all_projects_checkbox.png')
        click('add_to_project/temp_project_name.png')
        move_to_pos(move_out_pos, duration=0.1)  # move out
        pos = locate('add_to_project/engine_not_compatible_label.png', 0)
        if pos:
            click('add_to_project/select_version_label.png', x_off=100)
            click_any(
                ['add_to_project/5.0.png',
                 'add_to_project/4.27.png',
                 'add_to_project/4.26.png',
                 'add_to_project/4.25.png',
                 'add_to_project/4.24.png',
                 'add_to_project/4.23.png',
                 'add_to_project/4.22.png',
                 'add_to_project/4.21.png',
                 'add_to_project/4.20.png',
                 'add_to_project/4.19.png',
                 'add_to_project/4.18.png',
                 'add_to_project/4.17.png',
                 'add_to_project/4.16.png',
                 'add_to_project/4.15.png',
                 'add_to_project/4.14.png',
                 'add_to_project/4.13.png',
                 'add_to_project/4.12.png',
                 'add_to_project/4.11.png',
                 'add_to_project/4.10.png'], 0)
    move_to_pos(move_out_pos, duration=0.1)  # move out
    click('add_to_project/confirm_button.png')


def check_launcher_on_screen():
    global old_launcher_pos
    launcher_pos = locate('library_button.png', 0)
    if not launcher_pos:
        print("Epic Launcher is not on screen!")
        exit()
    if old_launcher_pos and launcher_pos != old_launcher_pos:
        print("Epic Launcher was moved!")
        exit()
    old_launcher_pos = launcher_pos


def get_not_clicked_yet(pos_list):
    if len(clicked_pos) == 0:
        return pos_list[0]

    for pos in pos_list:
        found = False
        for clicked in clicked_pos:
            if clicked.x == pos.x and clicked.y == pos.y:
                found = True
                break
        if not found:
            return pos
    return None


def click_to_asset_button(pos):
    clicked_pos.append(pos)
    move_to_pos(pos, MOVE_DURATION, -120, 10)  # move out to prevent unclickable button bug
    click_pos(pos, MOVE_DURATION, 0, -20)


def detect_window_height():
    lib_button = locate("library_button.png", 0)
    set_button = locate("settings_button.png", 0)
    window_height = int(set_button.y - lib_button.y)
    return window_height


def download_from_library():
    global clicked_pos
    for i in range(MAX_ASSETS_TO_DOWNLOAD):
        # time.sleep(2)
        check_launcher_on_screen()

        pos_list = locate_all('assets_list/add_to_project_button1.png', 0)
        if len(pos_list) > 0:
            pos = get_not_clicked_yet(pos_list)
            if pos:
                click_to_asset_button(pos)
                add_to_project()
                continue

        pos_list = locate_all('assets_list/create_project_button1.png', 0)
        if len(pos_list) > 0:
            pos = get_not_clicked_yet(pos_list)
            if pos:
                click_to_asset_button(pos)
                create_project()
                continue

        pos_list = locate_all('assets_list/install_to_engine_button.png', 0)
        if len(pos_list) > 0:
            pos = get_not_clicked_yet(pos_list)
            if pos:
                click_to_asset_button(pos)
                install_plugin()
                continue

        height = detect_window_height()
        scroll_size = int(height * -3.5)
        pyautogui.scroll(scroll_size)

        clicked_pos = []
        if not locate_any(['assets_list/add_to_project_button1.png', 'assets_list/create_project_button1.png',
                           'assets_list/add_to_project_button2.png', 'assets_list/create_project_button2.png',
                           'assets_list/install_to_engine_button.png'], 0):
            print("Complete!")
            return


def focus_window():
    click('library_button.png', y_off=-40, duration=0.2)
    move_to('library_button.png', y_off=100, duration=0.2)

focus_window()
download_from_library()
# download_asset("7634212ae5334367a18858a44ce598d4")
