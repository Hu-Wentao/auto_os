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

# 2. 导入特定平台
if sys.platform == "darwin":
    from .macos import *
elif sys.platform == "win32":
    from .windows import *
else:
    raise RuntimeError(f'尚未支持的操作系统[{sys.platform}]')

# 3. 最后导入 general
from .general import *
