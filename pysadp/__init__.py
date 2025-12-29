__version__ = "1.0.0"
__author__ = "罗辑"
__email__ = "newluo@163.com"
__url__ = "https://github.com/luo703/pysadp"


"""海康威视SADP SDK Python封装

海康威视SADP（Search Active Device Protocol）协议的Python封装，
用于搜索、激活和配置海康威视设备。
"""

from .sadp import SADP
from .model import DeviceInfo
from .ip_generator import IPGenerator

__all__ = [
    "SADP",
    "DeviceInfo",
    "IPGenerator",
]