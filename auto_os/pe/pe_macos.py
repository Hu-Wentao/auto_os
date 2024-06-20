import subprocess
from typing import Optional

import pyautogui
from PIL.Image import Image

from auto_os.primary import BoxLike, Box, BBoxLike, BoxesMethod


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


def write_by_clip(text: str):
    """macos 无法快速连续键盘输入长文本, 通过剪贴板实现输入长文本"""
    clipboard_write(text)
    pyautogui.sleep(0.1)
    paste()


import Quartz.CoreGraphics as CG


def screenshot(region: Box | BoxLike | BBoxLike | None = None) -> Image:
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
    elif isinstance(region, tuple):
        region = CG.CGRectMake(region[0], region[1], region[2], region[3])  # 左,上,宽,高
    elif isinstance(region, dict):
        if BoxesMethod.is_bbox_like(region):
            region: BoxLike = BoxesMethod.to_box(region)
        region: BoxLike
        region = CG.CGRectMake(region['left'], region['top'], region['width'], region['height'])  # 左,上,宽,高

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
