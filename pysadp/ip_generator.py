"""
IP地址生成器模块

提供IP地址生成功能，根据给定的IP和掩码长度，每次调用返回下一个可用的IP地址
"""

import logging
import ipaddress
from typing import Optional, Union

class IPGenerator:
    """IP地址生成器类"""

    
    gateway: str
    """网关IP地址"""

    def __init__(self, start_ip: str, netmask: Union[str, int],gateway: Optional[str] = None):
        """初始化IP地址生成器
        
        Args:
            start_ip: 起始IP地址，例如 "192.168.1.100"
            netmask: 子网掩码，例如 "255.255.255.0" 或 24
            gateway: 网关IP地址，如不提定则默认为网络地址中的第一个IP
        """
        self.start_ip = start_ip
       
        
        # 创建起始IP对象
        start_ip_obj = ipaddress.IPv4Address(start_ip)
        
        # 创建网络对象（基于起始IP和掩码长度）
        self.network = ipaddress.IPv4Network(f"{start_ip}/{netmask}", strict=False)
        
        # 获取可用的主机地址范围
        self.available_hosts = list(self.network.hosts())

        if gateway is None:
            self.gateway = str(self.network.network_address + 1)
        else:
            # 验证网关IP是否在网络范围内
            gateway_obj = ipaddress.IPv4Address(gateway)
            if gateway_obj not in self.network:
                raise ValueError(f"网关IP {gateway} 不在网络 {self.network} 范围内")
            self.gateway = gateway


        # 找到起始IP在可用主机列表中的位置
        try:
            self.current_index = self.available_hosts.index(start_ip_obj)
        except ValueError:
            # 如果起始IP不在可用主机列表中，从第一个可用主机开始
            self.current_index = 0
            logging.warning(f"警告: 起始IP {start_ip} 不在可用主机范围内，将从第一个可用IP开始")
        
        # 最大可用IP数量
        self.max_available = len(self.available_hosts)
        
        if self.max_available == 0:
            raise ValueError("该网络没有可用的主机地址")
    
    def get_next_ip(self) -> str:
        """获取下一个可用的IP地址
        
        Returns:
            str: 下一个可用的IP地址
            
        Raises:
            IndexError: 当超出最大可用IP数量时抛出异常
        """
        if self.current_index >= self.max_available:
            raise IndexError(f"超出最大可用IP数量 ({self.max_available})")
        
        next_ip = str(self.available_hosts[self.current_index])
        self.current_index += 1
        
        return next_ip
    
    @property
    def netmask(self) -> str:
        """获取子网掩码
        
        Returns:
            str: 子网掩码
        """
        return str(self.network.netmask)
    
    def get_current_ip(self) -> Optional[str]:
        """获取当前IP地址（不移动指针）
        
        Returns:
            Optional[str]: 当前IP地址，如果还没有开始获取则返回None
        """
        if self.current_index == 0:
            return None
        return str(self.available_hosts[self.current_index - 1])
    
    def reset(self) -> None:
        """重置生成器，从头开始"""
        self.current_index = 0
    
    def get_remaining_count(self) -> int:
        """获取剩余可用的IP地址数量
        
        Returns:
            int: 剩余可用IP数量
        """
        return self.max_available - self.current_index
    
    def recycle_current_ip(self) -> bool:
        """回收当前IP，使得下次get_next_ip可以重新获得相同的IP
        
        Returns:
            bool: 回收是否成功（如果当前没有IP被使用则返回False）
        """
        if self.current_index <= 0:
            return False
        
        # 将当前索引减1，这样下次get_next_ip会重新获得相同的IP
        self.current_index -= 1
        return True
    
    def get_network_info(self) -> dict:
        """获取网络信息
        
        Returns:
            dict: 包含网络信息的字典
        """
        return {
            "network_address": str(self.network.network_address),
            "broadcast_address": str(self.network.broadcast_address),
            "netmask": str(self.network.netmask),
            "total_hosts": self.max_available,
            "used_hosts": self.current_index,
            "available_hosts": self.get_remaining_count(),
            "gateway": self.gateway
        }
    
    def __str__(self) -> str:
        return (f"IPGenerator(start_ip='{self.start_ip}', netmask={self.netmask}, "
                f"current_index={self.current_index}, max_available={self.max_available}")




# 示例使用
if __name__ == "__main__":
    print("示例1: 使用IP和掩码长度")
    ip_gen = IPGenerator("192.168.1.110", 24)
    
    print(f"网络信息: {ip_gen.get_network_info()}")
    
    for i in range(5):
        try:
            next_ip = ip_gen.get_next_ip()
            print(f"第{i+1}个IP: {next_ip} mask: {ip_gen.netmask} gateway: {ip_gen.gateway}")
        except IndexError as e:
            print(f"错误: {e}")
            break
    
    print(f"剩余IP数量: {ip_gen.get_remaining_count()}")