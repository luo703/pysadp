from ctypes import Structure,c_char,c_ubyte,c_uint16,c_ulong,c_int

MAX_USERNAME_LEN = 32
MAX_PASS_LEN = 16
MAX_IPV6_ADDR_LEN = 128
MAX_IPV4_ADDR_LEN = 16
MAX_PORT_LEN = 5

class SADP_DEVICE_INFO(Structure):
    _fields_ = [
        ("szSeries", c_char * 12),                 # 设备系列（保留）
        ("szSerialNO", c_char * 48),               # 设备序列号
        ("szMAC", c_char * 20),                    # 设备物理地址
        ("szIPv4Address", c_char * 16),            # 设备IPv4地址
        ("szIPv4SubnetMask", c_char * 16),         # 设备IPv4子网掩码
        ("dwDeviceType", c_ulong),                 # 设备类型，具体数值代表的设备型号
        ("dwPort", c_ulong),                       # 设备网络SDK服务端口号(默认8000)
        ("dwNumberOfEncoders", c_ulong),           # 设备编码器个数，即设备编码通道个数。对于解码器，其值设为0
        ("dwNumberOfHardDisk", c_ulong),           # 设备硬盘数目
        ("szDeviceSoftwareVersion", c_char * 48),  # 设备软件版本号
        ("szDSPVersion", c_char * 48),             # 设备DSP版本号
        ("szBootTime", c_char * 48),               # 开机时间
        ("iResult", c_int),                        # 信息类型：1-设备上线 2-设备更新 3-设备下线 4-设备重启 5-设备更新失败
        ("szDevDesc", c_char * 24),                # 设备类型描述 与dwDeviceType对应
        ("szOEMinfo", c_char * 24),                # OEM产商信息
        ("szIPv4Gateway", c_char * 16),            # IPv4网关
        ("szIPv6Address", c_char * 46),            # IPv6地址
        ("szIPv6Gateway", c_char * 46),            # IPv6网关
        ("byIPv6MaskLen", c_ubyte),                 # IPv6子网前缀长度
        ("bySupport", c_ubyte),                     # 按位表示,对应为为1表示支持
        ("byDhcpEnabled", c_ubyte),                 # Dhcp状态, 0 不启用 1 启用
        ("byDeviceAbility", c_ubyte),               # 设备能力
        ("wHttpPort", c_uint16),                     # Http 端口
        ("wDigitalChannelNum", c_uint16),            # 数字通道数
        ("szCmsIPv4", c_char * 16),                # CMS注册服务器IPv4地址
        ("wCmsPort", c_uint16),                      # CMS注册服务器监听端口
        ("byOEMCode", c_ubyte),                     # 0-基线设备 1-OEM设备
        ("byActivated", c_ubyte),                   # 设备是否激活;0-激活，1-未激活（老的设备都是已激活状态）
        ("szBaseDesc", c_char * 24),                # 基线短型号，不随定制而修改的型号，用于萤石平台进行型号对比
        ("bySupport1", c_ubyte),                    # 按位表示, 1表示支持，0表示不支持
        ("byHCPlatform", c_ubyte),                  # 是否支持HCPlatform 0-保留, 1-支持, 2-不支持   
        ("byEnableHCPlatform", c_ubyte),            # 是否启用HCPlatform  0-保留, 1-启用， 2-不启用
        ("byEZVIZCode", c_ubyte),                   # 0-基线设备, 1-萤石设备
        ("dwDetailOEMCode", c_ulong),              # 详细OEMCode信息
        ("byModifyVerificationCode", c_ubyte),      # 是否修改验证码 0-保留， 1-修改验证码， 2-不修改验证码
        ("byMaxBindNum", c_ubyte),                  # 支持绑定的最大个数（目前只有NVR支持该字段）
        ("wOEMCommandPort", c_uint16),               # OEM命令端口
        ("bySupportWifiRegion", c_ubyte),           # 设备支持的wifi区域列表，按位表示，1表示支持，0表示不支持
        ("byEnableWifiEnhancement", c_ubyte),       # 是否启用wifi增强模式,0-不启用，1-启用
        ("byWifiRegion", c_ubyte),                  # 设备当前区域，0-default，1-china，2-nothAmerica，3-japan，4-europe,5-world
        ("bySupport2", c_ubyte),                    # 按位表示, 1表示支持，0表示不支持
    ]


class SADP_DEVICE_INFO_V40(Structure):
    _fields_ = [
        ("struSadpDeviceInfo", SADP_DEVICE_INFO),  # 基础设备信息
        ("byLicensed", c_ubyte),                    # 设备是否授权：0-保留,1-设备未授权，2-设备已授权
        ("bySystemMode", c_ubyte),                  # 系统模式 0-保留,1-单控，2-双控，3-单机集群，4-双控集群
        ("byControllerType", c_ubyte),              # 控制器类型 0-保留，1-A控，2-B控
        ("szEhmoeVersion", c_char * 16),           # Ehmoe版本号
        ("bySpecificDeviceType", c_ubyte),          # 设备类型，1-中性设备  2-海康设备
        ("dwSDKOverTLSPort", c_ulong),             # 私有协议中 SDK Over TLS 命令端口
        ("bySecurityMode", c_ubyte),                # 设备安全模式：0-standard,1-high-A,2-high-B,3-custom
        ("bySDKServerStatus", c_ubyte),             # 设备SDK服务状态, 0-开启，1-关闭
        ("bySDKOverTLSServerStatus", c_ubyte),      # 设备SDKOverTLS服务状态, 0-关闭，1-开启
        ("szUserName", c_char * (MAX_USERNAME_LEN + 1)),  # 管理员用户的用户名
        ("szWifiMAC", c_char * 20),                # 设备所连wifi的Mac地址
        ("byDataFromMulticast", c_ubyte),           # 0-链路 1-多播
        ("bySupportEzvizUnbind", c_ubyte),          # 是否支持萤石解绑 0-不支持 1-支持
        ("bySupportCodeEncrypt", c_ubyte),          # 是否支持重置口令AES128_ECB解密  0-不支持 1-支持
        ("bySupportPasswordResetType", c_ubyte),    # 是否支持获取密码重置方式参数  0-不支持 1-支持
        ("byEZVIZBindStatus", c_ubyte),             # 设备萤石云绑定状态,0-未知,1-已绑定,2-未绑定
        ("szPhysicalAccessVerification", c_char * 16),  # 设备支持的物理接触式添加方式
        ("byRes", c_ubyte * 411),                   # 保留，置为0
    ]


# 待修改的设备网络参数
class SADP_DEV_NET_PARAM(Structure):
    _fields_ = [
        ("szIPv4Address", c_char * MAX_IPV4_ADDR_LEN),      # IPv4地址
        ("szIPv4SubNetMask", c_char * MAX_IPV4_ADDR_LEN),   # IPv4子网掩码
        ("szIPv4Gateway", c_char * MAX_IPV4_ADDR_LEN),      # IPv4网关
        ("szIPv6Address", c_char * MAX_IPV6_ADDR_LEN),      # IPv6地址
        ("szIPv6Gateway", c_char * MAX_IPV6_ADDR_LEN),      # IPv6网关
        ("wPort", c_uint16),                                  # 设备网络SDK服务端口号(默认8000)
        ("byIPv6MaskLen", c_ubyte),                          # IPv6掩码长度
        ("byDhcpEnable", c_ubyte),                           # DHCP使能
        ("wHttpPort", c_uint16),                              # HTTP端口
        ("dwSDKOverTLSPort", c_ulong),                     # 私有协议中 SDK Over TLS 命令端口
        ("byRes", c_ubyte * 122),                            # 保留
    ]


# 设备返回网络参数信息
class SADP_DEV_RET_NET_PARAM(Structure):
    _fields_ = [
        ("byRetryModifyTime", c_ubyte),  # 剩余可尝试修改网络参数次数
        ("bySurplusLockTime", c_ubyte),  # 剩余时间，单位：分钟，用户锁定时此参数有效
        ("byRes", c_ubyte * 126),        # 保留
    ]

