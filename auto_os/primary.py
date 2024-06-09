from typing import TypedDict

Box = tuple[int, int, int, int]  # 左,上,宽,高
BBox = tuple[int, int, int, int]  # 左,上,右,下


class WindowInfo(TypedDict):
    app_name: str
    box: tuple[int, int, int, int]  # 截图box,左上宽高;


class App(TypedDict):
    name: str
    win_exe_name: str  # 用于定位, foo.exe
    win_exe_path: str  # 用于win平台定位, C:\...\foo.exe
