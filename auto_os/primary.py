from typing import TypedDict


class WindowInfo(TypedDict):
    app_name: str
    box: tuple[int, int, int, int]  # 截图box,左上宽高;

    @property
    def bbox(self):  # 截图位置,左上右下;
        l, t, w, h = self.box
        return l, t, l + w, t + h


class App(TypedDict):
    name: str
    win_exe_name: str  # 用于定位, foo.exe
    win_exe_path: str  # 用于win平台定位, C:\...\foo.exe
