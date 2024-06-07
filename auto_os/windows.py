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


def find_active_app_in_spaces(app: App):
    """在win中找到app"""
    import psutil
    import subprocess
    from win32gui import SetForegroundWindow, FindWindow
    def switch_to_app(app_name, executable_path):
        # 检查是否已有实例运行
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if app_name.lower() in proc.info['name'].lower():
                # 获取窗口句柄并切换到前台
                hwnd = FindWindow(None, proc.info['name'])
                if hwnd:
                    SetForegroundWindow(hwnd)
                return

        # 如果没有找到运行的实例，则启动新的实例
        subprocess.Popen(executable_path)
    # 用记事本作为示例
    # switch_to_app('notepad.exe', 'notepad.exe')
    switch_to_app(app['win_exe_name'], app['win_exe_path'])