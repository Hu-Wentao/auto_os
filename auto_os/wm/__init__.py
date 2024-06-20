"""
Window Manager 窗口管理
- 窗口位置查询
"""

import os
import sys

# print("sys.path",sys.path)
if (_package_path := os.path.dirname(__file__)) not in sys.path:
    sys.path.insert(0, _package_path)

# 2. 导入特定平台
if sys.platform == "darwin":
    from .wm_macos import *
elif sys.platform == "win32":
    from .wm_windows import *
else:
    raise RuntimeError(f'尚未支持的操作系统[{sys.platform}]')
# ====
