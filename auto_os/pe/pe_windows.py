from time import sleep
from typing import Optional

import pyautogui
import pyperclip


def clipboard_read() -> str:
    # 读取剪贴板内容
    text = pyperclip.paste()
    return text


def clipboard_write(text: str):
    pyperclip.copy(text)
    sleep(0.1)
    paste()


def paste(text: Optional[str] = None):
    if text is not None:
        clipboard_write(text)
    pyautogui.keyDown('control')
    pyautogui.press('v')
    pyautogui.keyUp('control')
