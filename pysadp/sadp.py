import os
import ctypes
import logging
from .model import DeviceInfo
from typing import List, Optional,Callable
from .sdk_errors import sdk_err_msg
from .base import  SADP_DEV_NET_PARAM, SADP_DEV_RET_NET_PARAM, SADP_DEVICE_INFO_V40

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class SADP:
    """海康威视SADP协议封装类"""

    device_list: List[DeviceInfo] = []
    """ 已发现设备列表 """
    
    sadp_data_callback:Optional[Callable[[DeviceInfo],None]] = None
    """ SADP数据回调函数 """
    
    def __init__(self,auto_request_interval: int = 10, sdk_path: str = None) -> None:
        """初始化SDK
        
        Args:
            auto_request_interval: 自动搜索的时间间隔，为0则不自动搜索，默认为10秒
            sdk_path: 自定义SDK文件路径
        
        """

        dlls = ["libcrypto-1_1-x64.dll", "libssl-1_1-x64.dll", "Sadp.dll"]
        if sdk_path is None:
            self.sdk_path = os.path.join(os.path.dirname(__file__), "sdk")
        else:
            self.sdk_path = sdk_path

        for dll in dlls:
            dll_path = os.path.join(self.sdk_path, dll)
            if not os.path.exists(dll_path):
                raise FileNotFoundError(f"未找到sadp库文件: {dll_path}")
            lib = ctypes.CDLL(dll_path)
            if dll == "Sadp.dll":
                self.lib = lib

        self._set_auto_request_interval(auto_request_interval)
        

    def call_func(self, func_name: str, *args) -> int:
        """调用SDK函数
        
        Args:
            func_name: 函数名称
            *args: 函数参数
            
        Returns:
            函数返回值
        """

        return int(getattr(self.lib, func_name)(*args))

    def get_sdk_version(self) -> str:
        """获取SDK版本
        
        Returns:
            str: 版本号，例如V3.1.1.3
        """
        res = self.call_func("SADP_GetSadpVersion")
        
        # 31~24位值为a，23~16位值为b，15~8位值为c，7~0位值为d，则版本号为Va.b.c.d
        a = (res >> 24) & 0xFF
        b = (res >> 16) & 0xFF
        c = (res >> 8) & 0xFF
        d = res & 0xFF
        
        return f"V{a}.{b}.{c}.{d}"
    
    
    def start(self) -> bool:
        """开始sadp设备搜索
        
        Args:
            
        Returns:
            bool: 是否启动成功
        """
        
        PDEVICE_FIND_CALLBACK_V40 = ctypes.CFUNCTYPE(None, ctypes.POINTER(SADP_DEVICE_INFO_V40), ctypes.c_void_p)
        
        # 内部回调包装函数
        def internal_callback(lpDeviceInfoV40, pUserData):           
            if lpDeviceInfoV40:
                device_info = DeviceInfo(lpDeviceInfoV40.contents)
                if device_info not in self.device_list:
                    self.device_list.append(device_info)
                else:
                    self.device_list.remove(device_info)
                    if device_info.result != 3:
                        self.device_list.append(device_info)
                if self.sadp_data_callback :
                    self.sadp_data_callback(device_info)
                
        
        # 转换回调函数为C类型
        c_callback = PDEVICE_FIND_CALLBACK_V40(internal_callback)
        
        # 保存回调函数引用，防止被垃圾回收
        self._callback_ref = c_callback
        
        # 调用SADP_Start_V40
        res = self.call_func("SADP_Start_V40", c_callback)
        if not res:
            self.print_error("启动SADP协议失败")
            return False
        return True
    
    def sadp_stop(self) -> bool:
        """停止SADP协议
        Returns:
            bool: 是否停止成功
        """
        res = self.call_func("SADP_Stop")
        if not res:
            self.print_error("停止SADP协议失败")
        return bool(res)
    
    def activate_device(self, device_info: DeviceInfo, password: str) -> bool:
        """激活设备
        
        Args:
            device_info: 设备信息对象
            password: 设备密码
            
        Returns:
            bool: 是否激活成功
            
        """       
        res = self.call_func("SADP_ActivateDevice", device_info.serial_no.encode("utf-8"), password.encode("utf-8")) 
        if not res:
            self.print_error("激活设备失败")
        return bool(res)
    
    
    def modify_device_net_param(self, device_info: DeviceInfo, password: str, ipv4_address: Optional[str] = None, 
                              ipv4_subnet_mask: Optional[str] = None, ipv4_gateway: Optional[str] = None,
                              port: Optional[int] = None, http_port: Optional[int] = None, ipv6_address: Optional[str] = None,
                              ipv6_gateway: Optional[str] = None, ipv6_mask_len: Optional[int] = None,
                              dhcp_enable: Optional[bool] = None) -> dict:
        """修改设备网络参数
        
        Args:
            device_info: 设备信息对象
            password: 设备密码
            ipv4_address: 设备IPv4地址，若为None则使用当前地址
            ipv4_subnet_mask: 设备IPv4子网掩码，若为None则使用当前掩码
            ipv4_gateway: 设备IPv4网关，若为None则使用当前网关
            port: 设备网络SDK服务端口号(默认8000)，若为None则使用当前端口
            http_port: HTTP端口(默认80)，若为None则使用当前端口
            ipv6_address: 设备IPv6地址，若为None则使用当前地址
            ipv6_gateway: 设备IPv6网关，若为None则使用当前网关
            ipv6_mask_len: 设备IPv6子网掩码长度，若为None则使用当前长度
            dhcp_enable: 是否启用DHCP(默认False)，若为None则使用当前状态
            
        Returns:
            dict: 包含修改结果的字典
                - success: bool，是否修改成功
                - error_code: int，错误码
                - error_message: str，错误信息
                - retry_modify_time: int，剩余可尝试修改次数
                - surplus_lock_time: int，剩余锁定时间(分钟)
        """

        # 初始化网络参数结构体
        sadp_dev_net_param = SADP_DEV_NET_PARAM()
        sadp_dev_net_param.szIPv4Address = ipv4_address.encode("utf-8") if ipv4_address else device_info.ipv4_address.encode("utf-8")
        sadp_dev_net_param.szIPv4SubNetMask = ipv4_subnet_mask.encode("utf-8") if ipv4_subnet_mask else device_info.ipv4_subnet_mask.encode("utf-8")
        sadp_dev_net_param.szIPv4Gateway = ipv4_gateway.encode("utf-8") if ipv4_gateway else device_info.ipv4_gateway.encode("utf-8")
        sadp_dev_net_param.szIPv6Address = ipv6_address.encode("utf-8") if ipv6_address else device_info.ipv6_address.encode("utf-8")
        sadp_dev_net_param.szIPv6Gateway = ipv6_gateway.encode("utf-8") if ipv6_gateway else device_info.ipv6_gateway.encode("utf-8")
        sadp_dev_net_param.byIPv6MaskLen = ipv6_mask_len if ipv6_mask_len else device_info.ipv6_mask_len 
        sadp_dev_net_param.wPort = port if port else device_info.port
        sadp_dev_net_param.wHttpPort = http_port if http_port else device_info.http_port
        sadp_dev_net_param.dwSDKOverTLSPort = 0
        if dhcp_enable is not None:
            sadp_dev_net_param.byDhcpEnable = 1 if dhcp_enable else 0
        else:
            sadp_dev_net_param.byDhcpEnable = device_info.dhcp_enabled   
        
        # 初始化返回参数结构体
        ret_net_param = SADP_DEV_RET_NET_PARAM()
        
        res = self.call_func("SADP_ModifyDeviceNetParam_V40", 
                          device_info.mac.encode("utf-8"), 
                          password.encode("utf-8"),
                          ctypes.byref(sadp_dev_net_param),
                          ctypes.byref(ret_net_param),
                          ctypes.sizeof(ret_net_param))

        result = {
            'success': bool(res),
            'retry_modify_time': ret_net_param.byRetryModifyTime,
            'surplus_lock_time': ret_net_param.bySurplusLockTime
        }
        if not res:
            # 获取错误码和错误信息
            error_code = self.call_func("SADP_GetLastError")
            error_message = sdk_err_msg(error_code)
            
            result['error_code'] = error_code
            result['error_message'] = error_message
            
            # 根据错误码提供更详细的信息
            if error_code == 2018:  # SADP_LOCKED
                result['error_message'] = f"设备已锁定，锁定时间:{ret_net_param.bySurplusLockTime}分钟"
            elif error_code == 2024:  # SADP_PASSWORD_ERROR
                result['error_message'] = f"密码错误，剩余尝试修改次数:{ret_net_param.byRetryModifyTime}次"
            elif error_code == 2019:  # SADP_NOT_ACTIVATED
                result['error_message'] = "设备未激活"

            logger.error(f"修改设备网络参数失败: {result.get('error_message')}")
        return result


    def _set_auto_request_interval(self, interval: int) -> bool:
        """设置自动搜索的时间间隔
        
        Args:
            interval: 时间间隔，单位为秒，0则不自动请求
            
        Returns:
            bool: 是否设置成功
        """
        res = self.call_func("SADP_SetAutoRequestInterval", interval)
        return bool(res)
        
    def print_error(self, prefix: str = "") -> None:
        """打印SDK错误信息
        
        Args:
            prefix: 错误描述前缀
        """
        error_code = self.call_func("SADP_GetLastError")
        error_message = sdk_err_msg(error_code)
        logger.error(f"{prefix} 错误码: {error_code} 错误信息: {error_message}")


