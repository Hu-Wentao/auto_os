"""
Peripheral Equipment 外部设备
- 鼠标键盘操作
- 屏幕截图
"""

import os
import sys

# print("sys.path",sys.path)
if (_package_path := os.path.dirname(__file__)) not in sys.path:
    sys.path.insert(0, _package_path)

# 2. 导入特定平台
if sys.platform == "darwin":
    from .pe_macos import *
elif sys.platform == "win32":
    from .pe_windows import *
else:
    raise RuntimeError(f'尚未支持的操作系统[{sys.platform}]')
# ====
