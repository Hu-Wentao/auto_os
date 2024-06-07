import io
import subprocess

import shutil
from time import sleep
from typing import Optional, Union

import os

import pyautogui
from PIL import Image
from loguru import logger

from auto_os import App, WindowInfo
from tenacity import retry, stop_after_attempt, wait_fixed


def _run_apple_script(cmd) -> str:
    # 执行apple脚本
    result = subprocess.check_output(cmd, shell=True)
    # 对结果进行解码（从bytes转换为str），并去除尾部的换行符
    rst = result.decode('utf-8').strip()
    return rst


def switch_spaces(to_right: bool = True, with_act_app_wait: float = 1) -> Optional[str]:
    """
    向 右/左 切换空间
    mac: 需要系统授权辅助功能
    :param with_act_app_wait: 等待 n 秒后,检查活跃app名称; -1表示不等待,且不检查app名称,直接切换
    :param to_right: 切换到右边屏幕
    :return:
    """
    pyautogui.hotkey('ctrl', 'right' if to_right else 'left')
    if with_act_app_wait >= 0:
        if with_act_app_wait:
            sleep(with_act_app_wait)
        return get_active_window_info()
    pass


def find_active_app_in_spaces(app: Union[App, str], find_from_left=True, find_max_try=16):
    """ 向左/右屏幕尝试 查找活跃的 app
    不允许调用open_app: E4c, 火狐均无法通过这种方式启动(将空白页当成全屏的app), 可能与全屏运行有关
    :param app:
    :param find_from_left: 从最左/右屏幕尝试: 从最左边spaces开始
    :param find_max_try: 向左/右屏幕尝试 查询的最大次数(mac最多创建16个空间)
    :return:
    """
    # 格式化app名称
    app = str(app)

    if (info := get_active_window_info()) and info['app_name'] == app:
        return
    # 1. 尝试open(mac13下,全屏app无法通过打开来定位)
    open_app(app)
    sleep(1)
    if (info := get_active_window_info()) and info == app:
        return
    # 2. 自动切换失败(E4C等应用在mac中无法自动切换), 左右查找活跃app
    for i in range(find_max_try):
        # switch_spaces(to_right=to_right, with_act_app_wait=-1)
        to_right = not find_from_left
        if switch_spaces(to_right=to_right, with_act_app_wait=0.2) == app:
            return
    for i in range(find_max_try):
        to_right = find_from_left
        if switch_spaces(to_right=to_right) == app:
            return
    logger.error(f"没找到活跃的[{app}]")


def deep_copy(src: str, dst: str, show_log=False):
    if show_log:
        print(f"deep_copy [{src} -> {dst}]")
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.islink(src_item):
            link_target = os.readlink(src_item)
            os.symlink(link_target, dst_item)
        elif os.path.isdir(src_item):
            deep_copy(src_item, dst_item)
        else:
            shutil.copy2(src_item, dst_item)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def reset_folder(folder: str):  # rmtree 可能报错 xx路径不存在
    print(f"reset folder [{folder}]")
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def resource_path(file, res_path: str):
    """
    获取相对 .py文件的路径, 用于读取资源文件
    :param file: 固定传入对应.py的 __file__ 动态变量, 代表正在执行的.py文件的位置.(不一定是入口main.py的位置)
    :param res_path: 不带 ./ 或 / 的相对.py文件的路径
    :return:
    """
    current_path = os.path.dirname(os.path.abspath(file))
    # 获取图片的路径
    path = os.path.join(current_path, res_path)
    return path


# ====

def close_app(app_name):
    """
    # 示例：关闭Safari浏览器
    close_app("Safari")

    :param app_name:
    :return:
    """
    print(f"close_app [{app_name}]")
    script = f'''
    tell application "{app_name}"
        if it is running then
            quit
        end if
    end tell
    '''
    try:
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError:
        pass  # 如果应用程序未运行，忽略错误


def open_app(app_name):
    """
    # 示例：打开Safari浏览器
    open_app("Safari")
    :param app_name:
    :return:
    """
    script = f'''
    tell application "{app_name}"
        activate
    end tell
    '''
    try:
        print(f"active app [{app_name}]")
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {app_name}: {e}")


def open_app_chrome(profile: Optional[str] = None, url: Optional[str] = None):
    """profile 用户配置文件, 如 ’Default‘, ‘Profile 1‘ 等"""
    args = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    if profile or url:
        args.append('--args')
        if profile:
            args.append(f'--profile-directory={profile}')
        if url:
            args.append(f'{url}')
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open Chrome: {e}")


def get_window_info(name: str) -> Optional[WindowInfo]:
    # 注意 ‘{{’ 与 ‘}}’ 用于python字符串模板转义
    sc_window_info = f"""\
    tell application "System Events"
      set appName to "{name}" -- 指定应用的名称
      if (name of processes) contains appName then
        tell application process appName
          set windowPos to position of front window
          set windowSize to size of front window
        end tell
      else
        set windowPos to {{0, 0}}
        set windowSize to {{-1, -1}}
      end if
    end tell
    return {{windowPos, windowSize}}
    """
    # 返回 窗口坐标x,y 换行 窗口大小w,h
    process = subprocess.run(['osascript', '-e', sc_window_info], capture_output=True, text=True)
    output = process.stdout.strip()
    # print(output)
    if output == '0, 0, -1, -1' or len(output) == 0:  # on error
        return None  # 没有找到应用(应用没启动)
    sp = output.split(',')
    left, top, width, height = map(int, sp)
    return WindowInfo(
        app_name=name,
        box=(left, top, width, height),
    )


def get_active_window_info() -> Optional[WindowInfo]:
    """ 返回前台窗口信息
    注意: windowName 窗口名, appName 应用名
        对于‘PyCharm’app, 当前项目为auto_wf,程序名为‘test.py’:
            appName=‘pycharm’;windowName=‘auto_wf - test.py’
        对于‘Safari’浏览器, 当前窗口为ChatGPT:
            appName=‘Safari’;windowName=‘当前窗口为ChatGPT’
        对于WildForest移动版:
             appName=‘WildForest’; windowsName未测试
    :return: (应用名,(左,上,右,下))
    """
    sc_active_window_info = '''
    tell application "System Events"
        tell process 1 where frontmost is true
            -- set windowName to name of front window -- 获取窗口名, 如 test.py
            set appName to name -- 获取窗口对应的应用名称,如 pycharm
            set windowPos to position of front window
            set windowSize to size of front window
        end tell
    end tell
    return {appName,  windowPos,  windowSize}
    '''
    process = subprocess.run(['osascript', '-e', sc_active_window_info], capture_output=True, text=True)
    output = process.stdout.strip()
    # print(output)
    if len(output) == 0:  # 可能是点击了关闭窗口按钮, 此时无法获取数据
        return None
    # auto_wf – window_info_test2.py, 0, 25, 1400, 828 #app名称, 左,上,宽,高
    sp = output.split(", ")
    left, top, width, height = map(int, sp[1:])
    return WindowInfo(
        app_name=sp[0],
        box=(left, top, width, height),
    )


def set_full_screen():
    # pyautogui.hotkey('ctrl', 'command', 'f')
    with pyautogui.hold('ctrl'):
        with pyautogui.hold('command'):
            pyautogui.press('f')


def clipboard_read() -> str:
    p = subprocess.Popen(['pbpaste', 'r'],
                         stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode('utf-8')


def clipboard_write(text: str):
    p = subprocess.Popen(['pbcopy', 'w'],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text.encode('utf-8'))


def paste(text: Optional[str] = None):
    if text is not None:
        clipboard_write(text)
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')


Box = tuple[int, int, int, int]  # 左上宽高

import Quartz.CoreGraphics as CG


def screenshot(region: Box | None = None) -> Image.Image:
    """Capture a screenshot of the specified region and return a CGImage object.
    The default region is CG.CGRectInfinite (captures the full screen).

    Args:
        region: A tuple (left, top, width, height) specifying the region to capture.
                If None, captures the full screen.

    Returns:
        A CGImage object representing the captured screenshot.
    """

    if region is None:
        region = CG.CGRectInfinite
    else:
        region = CG.CGRectMake(region[0], region[1], region[2], region[3])  # 左,上,宽,高

    # Create screenshot as CGImage
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault
    )
    data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
    width = CG.CGImageGetWidth(image)
    height = CG.CGImageGetHeight(image)
    bytes_per_row = CG.CGImageGetBytesPerRow(image)
    pil_image = Image.frombuffer("RGBA", (width, height), data, "raw", "BGRA", bytes_per_row, 1)
    return pil_image
