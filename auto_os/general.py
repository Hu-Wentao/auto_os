import pyautogui

from auto_os import clipboard_write


def paste():
    with pyautogui.hold('command'):
        pyautogui.press('v')


def write_by_clip(text: str):
    clipboard_write(text)
    pyautogui.sleep(0.1)
    paste()
