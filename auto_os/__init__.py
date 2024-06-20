"""
适配操作系统的函数
例如查询窗口信息, 截屏, 剪贴板, 文件系统等等
"""
import os
import sys

# print("sys.path",sys.path)
if (_package_path := os.path.dirname(__file__)) not in sys.path:
    sys.path.insert(0, _package_path)

# 1. 导入公共依赖
from .primary import *

# 文件系统模块
import fs

# 外设: 鼠标,键盘,屏幕
import pe

# 窗口管理
import wm
