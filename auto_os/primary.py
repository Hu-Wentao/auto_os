from random import randint
from typing import TypedDict

from typing_extensions import deprecated

Box = tuple[int, int, int, int]  # 左,上,宽,高
BBox = tuple[int, int, int, int]  # 左,上,右,下


class BoxLike(TypedDict):
    left: int
    top: int
    width: int
    height: int


class BBoxLike(TypedDict):
    left: int
    top: int
    right: int
    bottom: int


class BoxesMethod:

    @staticmethod
    def random_point(bbox: BoxLike | BBoxLike) -> tuple[int, int]:
        bbox: BBoxLike = BoxesMethod.to_bbox(box=bbox)
        x = randint(bbox["left"], bbox["right"])
        y = randint(bbox["top"], bbox["bottom"])
        return x, y

    @staticmethod
    def get_box(box: BoxLike | BBoxLike) -> Box:
        box: BoxLike = BoxesMethod.to_box(bbox=box)
        return box["left"], box["top"], box["width"], box["height"]

    @staticmethod
    def get_bbox(bbox: BBoxLike | BoxLike) -> BBox:
        return bbox["left"], bbox["top"], bbox["right"], bbox["bottom"]

    @staticmethod
    def of_box(bbox: Box) -> BoxLike:
        return BoxLike(**{
            'left': bbox[0],
            'top': bbox[1],
            'width': bbox[2],
            'height': bbox[3],
        })

    @staticmethod
    def of_bbox(bbox: BBox) -> BBoxLike:
        return BBoxLike(**{
            'left': bbox[0],
            'top': bbox[1],
            'right': bbox[2],
            'bottom': bbox[3],
        })

    @staticmethod
    def offset_box(box: BoxLike, delta_x: int = 0, delta_y: int = 0) -> BoxLike:
        return BoxLike(**{
            **box,
            'left': box["left"] + delta_x,
            'top': box["top"] + delta_y,
        })

    @staticmethod
    def offset_bbox(bbox: BBoxLike, delta_x: int = 0, delta_y: int = 0) -> BBoxLike:
        return BBoxLike(**{
            'left': bbox["left"] + delta_x,
            'top': bbox["top"] + delta_y,
            'right': bbox["right"] + delta_x,
            'bottom': bbox["bottom"] + delta_y,
        })

    @staticmethod
    def to_bbox(box: BoxLike) -> 'BBoxLike':
        if BoxesMethod.is_bbox_like(box):
            box: BBoxLike
            return box
        else:
            return BBoxLike(**{
                **box,
                'right': box["left"] + box["width"],
                'bottom': box["top"] + box["height"],
            })

    @staticmethod
    def to_box(bbox: BBoxLike) -> 'BoxLike':
        if BoxesMethod.is_box_like(bbox):
            bbox: BoxLike
            return bbox
        else:
            return BoxLike(**{
                'left': bbox["left"],
                'top': bbox["top"],
                'width': bbox["right"] - bbox["left"],
                'height': bbox["bottom"] - bbox["top"],
            })

    @staticmethod
    def is_box_like(box: BoxLike | BBoxLike) -> bool:
        return set(BoxLike.__annotations__.keys()) == set(box.keys())

    @staticmethod
    def is_bbox_like(bbox: BoxLike | BBoxLike) -> bool:
        return set(BBoxLike.__annotations__.keys()) == set(bbox.keys())


@deprecated('使用[WindowBox]')
class WindowInfo(TypedDict):
    app_name: str
    box: tuple[int, int, int, int]  # 截图box,左上宽高;


class WindowBox(BoxLike):
    # left: int
    # top: int
    # width: int
    # height: int
    app_name: str  # 应用名称
    process: str  # 进程名称, 例如vscode主页进程名为 Electoral; pycharm特定代码窗口 进程名为代码窗口名 test.py等


class App(TypedDict):
    name: str
    win_exe_name: str  # 用于定位, foo.exe
    win_exe_path: str  # 用于win平台定位, C:\...\foo.exe
