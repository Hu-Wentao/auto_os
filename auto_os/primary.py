from random import randint
from typing import TypedDict, Protocol

Box = tuple[int, int, int, int]  # 左,上,宽,高
BBox = tuple[int, int, int, int]  # 左,上,右,下


class BoxLike(Protocol):
    def __init__(self, left: int, right: int, width: int, height: int):
        self.left = left
        self.top = right
        self.width = width
        self.height = height

    def random_point(self):
        x = randint(self.left, self.left + self.width)
        y = randint(self.top, self.top + self.height)
        return x, y

    def get_box(self) -> Box:
        return self.left, self.top, self.width, self.height

    def to_bbox(self) -> 'BBoxLike':
        return BBoxLike(self.left, self.top, self.left + self.width, self.top + self.height, )


class BBoxLike(Protocol):
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def random_point(self):
        x = randint(self.left, self.right)
        y = randint(self.top, self.bottom)
        return x, y

    def get_bbox(self) -> BBox:
        return self.left, self.top, self.right, self.bottom

    def to_box(self) -> BoxLike:
        return BoxLike(self.left, self.top, self.right - self.left, self.bottom - self.top)


class WindowInfo(TypedDict):
    app_name: str
    box: tuple[int, int, int, int]  # 截图box,左上宽高;


class App(TypedDict):
    name: str
    win_exe_name: str  # 用于定位, foo.exe
    win_exe_path: str  # 用于win平台定位, C:\...\foo.exe
