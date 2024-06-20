"""
File System 操作集合
- 自动适配当前操作系统
- 提供所有文件操作相关函数
"""

import os
import sys

# print("sys.path",sys.path)
if (_package_path := os.path.dirname(__file__)) not in sys.path:
    sys.path.insert(0, _package_path)

# 2. 导入特定平台
if sys.platform == "darwin":
    from .fs_macos import *
elif sys.platform == "win32":
    from .fs_windows import *
else:
    raise RuntimeError(f'尚未支持的操作系统[{sys.platform}]')

# ====
