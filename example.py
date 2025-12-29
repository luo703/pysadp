"""示例
使用PYSADP 搜索、激活和配置海康威视设备网络参数。

author: 罗辑
email: newluo@163.com
url: https://github.com/luo703/pysadp
"""

import time
import logging
from typing import List
from pysadp import SADP, DeviceInfo, IPGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# 初次搜索设备标志
first_search = True


def device_discovered_callback(device: DeviceInfo) -> None:
    """设备发现回调函数
    
    Args:
        device: 设备信息
    
    Notes:
        避坑：不要在回调函数中执行激活设备修改IP或其它耗时操作
    """

    # 初次搜索设备时，只处理设备上线的消息
    if first_search:
        if device.result == 1:
            logger.info(f"{device.result_desc}: {device.dev_desc} {device.ipv4_address} {device.mac} {'已激活' if device.is_activated else '未激活'}")
    # 否则处理设备上线和更新的消息
    else:
        if device.result == 1 or device.result == 2:
            logger.info(f"{device.result_desc}: {device.dev_desc} {device.ipv4_address} {device.mac} {'已激活' if device.is_activated else '未激活'}")
    

def wait_for_devices(device_list: List[DeviceInfo], timeout: int = 3) -> None:
    """等待设备响应
    
    Args:
        device_list: 设备列表
        timeout: 等待超时时间，单位秒， 如果等待时间内没有新设备发现,则结束等待,否则重置等待时间继续等待
    """
    last_device_sum = len(device_list)
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(device_list) > last_device_sum:
            # 发现新设备，重置等待时间
            start_time = time.time()
            last_device_sum = len(device_list)
        time.sleep(1)
    logger.info(f"等待设备响应完成,已发现设备数: {len(device_list)}")

def main():
    global first_search

    logger.info("pysadp示例")
    # 初始化SDK
    sadp = SADP(auto_request_interval=3)

    # 注册设备发现回调
    sadp.sadp_data_callback = device_discovered_callback
    # 创建IP地址生成器
    ip_gen = IPGenerator("192.168.1.100", "255.255.255.0")
    #设备密码,用于激活或修改设备
    password = "abc123456"
    
    # 启动SDK
    if not sadp.start():
        return
    try:
        logger.info(f"SDK版本: {sadp.get_sdk_version()}")
        logger.info("正在搜索设备...")
        # 等待设备响应 如设备较多搜索不全,应适当增加超时时间
        wait_for_devices(sadp.device_list, timeout=3)
        first_search = False

        #示例：激活设备
        activated_devices: List[DeviceInfo] = []
        for device in sadp.device_list:
            if not device.is_activated:
                logger.info(f"尝试激活设备 {device.serial_no}...")
                if sadp.activate_device(device, password):
                    logger.info(f"{device.serial_no} 设备激活成功")
                    activated_devices.append(device)
        
        #等待全部已激活设备状态更新
        if len(activated_devices) > 0:
            logger.info(f"等待已激活设备信息更新...")
            for device in activated_devices:
                while not any(d.mac == device.mac and d.is_activated for d in sadp.device_list):
                    time.sleep(1)
        
        # 示例：修改设备IP地址
        for device in sadp.device_list:
            # 只修改已激活且为原始IP的设备
            if device.is_activated and device.ipv4_address == "192.168.1.64":
                logger.info(f"修改设备 {device.serial_no} 的IP地址...")
                result = sadp.modify_device_net_param(
                    device_info=device,
                    password=password,
                    ipv4_address=ip_gen.get_next_ip(),
                    ipv4_subnet_mask=ip_gen.netmask,
                    ipv4_gateway=ip_gen.gateway
                )
                if result['success']:
                    logger.info(f"{device.serial_no} IP修改成功")
                else:
                    #设备IP修改失败，收回IP地址
                    ip_gen.recycle_current_ip()
                    
        #保持程序运行,回车结束
        #input("")

    finally:
        if sadp.sadp_stop():
            logger.info("SADP已停止")

if __name__ == "__main__":
    main()
