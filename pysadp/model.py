class DeviceInfo:
    """设备信息类，映射SADP_DEVICE_INFO_V40结构体

    """
    
    # 基本设备信息字段
    series: str
    """设备系列（保留）"""
    
    serial_no: str
    """设备序列号"""
    
    mac: str
    """设备物理地址"""
    
    ipv4_address: str
    """设备IPv4地址"""
    
    ipv4_subnet_mask: str
    """设备IPv4子网掩码"""
    
    device_type: int
    """设备类型，具体数值代表的设备型号"""
    
    port: int
    """设备网络SDK服务端口号(默认8000)"""
    
    number_of_encoders: int
    """设备编码器个数，即设备编码通道个数。对于解码器，其值设为0"""
    
    number_of_hard_disk: int
    """设备硬盘数目"""
    
    device_software_version: str
    """设备软件版本号"""
    
    dsp_version: str
    """设备DSP版本号"""
    
    boot_time: str
    """开机时间"""
    
    result: int
    """消息类型：
    SADP_ADD        1   新设备上线，之前在SADP库列表中未出现的设备
    SADP_UPDATE     2   在线的设备的网络参数或者某些状态改变
    SADP_DEC        3   设备下线，设备自动发送下线消息或120秒内检测不到设备
    SADP_RESTART    4   之前SADP库列表中出现过之后下线的设备再次上线
    SADP_UPDATEFAIL 5   设备更新失败"""
    
    dev_desc: str
    """设备型号描述"""
    
    oem_info: str
    """OEM产商信息"""
    
    ipv4_gateway: str
    """IPv4网关"""
    
    ipv6_address: str
    """IPv6地址"""
    
    ipv6_gateway: str
    """IPv6网关"""
    
    ipv6_mask_len: int
    """IPv6子网前缀长度"""
    
    support: int
    """按位表示,对应为为1表示支持
    0x01:是否支持Ipv6
    0x02:是否支持修改Ipv6参数
    0x04:是否支持Dhcp
    0x08:是否支持udp多播
    0x10:是否含加密节点
    0x20:是否支持恢复密码
    0x40:是否支持重置密码
    0x80:是否支持同步IPC密码"""
    
    dhcp_enabled: int
    """Dhcp状态, 0 不启用 1 启用"""
    
    device_ability: int
    """设备能力
    0：设备不支持"设备类型描述" 'OEM厂商' 'IPv4网关' 'IPv6地址' 'IPv6网关' 'IPv6子网前缀''DHCP'
    1：支持上述功能"""
    
    http_port: int
    """Http 端口"""
    
    digital_channel_num: int
    """数字通道数"""
    
    cms_ipv4: str
    """CMS注册服务器IPv4地址"""
    
    cms_port: int
    """CMS注册服务器监听端口"""
    
    oem_code: int
    """0-基线设备 1-OEM设备"""
    
    activated: int
    """设备是否激活;0-激活，1-未激活（老的设备都是已激活状态）"""
    
    base_desc: str
    """基线短型号，不随定制而修改的型号，用于萤石平台进行型号对比"""
    
    support1: int
    """按位表示, 1表示支持，0表示不支持
    0x01:是否支持重置密码方式2
    0x02;是否支持设备锁定功能
    0x04:是否支持导入GUID重置密码
    0x08:是否支持安全问题重置密码
    0x10:是否支持OEM更换Logo
    0x20:是否支持绑定操作
    0x40:是否支持恢复未激活
    0x80:是否支持wifi信号增强模式"""
    
    hc_platform: int
    """是否支持HCPlatform 0-保留, 1-支持, 2-不支持"""
    
    enable_hc_platform: int
    """是否启用HCPlatform  0-保留, 1-启用， 2-不启用"""
    
    ezviz_code: int
    """0-基线设备, 1-萤石设备"""
    
    detail_oem_code: int
    """详细OEMCode信息:oemcode由客户序号（可变位,从1开始，1~429496)+菜单风格（2位）+区域号（2位）三部分构成
    规则说明：oemcode最大值为4294967295，最多是十位数
    0: 老设备
    1: 新基线设备
    10101: 有具体OEM code的为OEM设备"""
    
    modify_verification_code: int
    """是否修改验证码 0-保留， 1-修改验证码， 2-不修改验证码"""
    
    max_bind_num: int
    """支持绑定的最大个数（目前只有NVR支持该字段）"""
    
    oem_command_port: int
    """OEM命令端口"""
    
    support_wifi_region: int
    """设备支持的wifi区域列表，按位表示，1表示支持，0表示不支持
    0x01:是否支持default（默认功率和北美一致）
    0x02:是否支持china
    0x04:是否支持nothAmerica
    0x08:是否支持japan
    0x10:是否支持europe
    0x20:是否支持world"""
    
    enable_wifi_enhancement: int
    """是否启用wifi增强模式,0-不启用，1-启用"""
    
    wifi_region: int
    """设备当前区域，0-default，1-china，2-nothAmerica，3-japan，4-europe,5-world"""
    
    support2: int
    """按位表示, 1表示支持，0表示不支持
    0x01:是否支持通道默认密码配置（该密码用于nvr添加IPC， 默认使用的是nvr admin密码，会单独保存在本地）
    0x02:是否支持邮箱重置密码
    0x04:是否支持未激活配置SSID和Password"""
    
    # V40扩展字段
    licensed: int
    """设备是否授权：0-保留,1-设备未授权，2-设备已授权"""
    
    system_mode: int
    """系统模式 0-保留,1-单控，2-双控，3-单机集群，4-双控集群"""
    
    controller_type: int
    """控制器类型 0-保留，1-A控，2-B控"""
    
    ehmoe_version: str
    """Ehmoe版本号"""
    
    specific_device_type: int
    """设备类型，1-中性设备  2-海康设备"""
    
    sdk_over_tls_port: int
    """私有协议中 SDK Over TLS 命令端口"""
    
    security_mode: int
    """设备安全模式：0-standard,1-high-A,2-high-B,3-custom"""
    
    sdk_server_status: int
    """设备SDK服务状态, 0-开启，1-关闭"""
    
    sdk_over_tls_server_status: int
    """设备SDKOverTLS服务状态, 0-关闭，1-开启"""
    
    user_name: str
    """管理员用户的用户名（设备安全模式在非标准模式下是允许用户设置管理员用户的用户名，标准模式默认为admin）"""
    
    wifi_mac: str
    """设备所连wifi的Mac地址"""
    
    data_from_multicast: int
    """0-链路 1-多播"""
    
    support_ezviz_unbind: int
    """是否支持萤石解绑 0-不支持 1-支持"""
    
    support_code_encrypt: int
    """是否支持重置口令AES128_ECB解密  0-不支持 1-支持"""
    
    support_password_reset_type: int
    """是否支持获取密码重置方式参数  0-不支持 1-支持"""
    
    ezviz_bind_status: int
    """设备萤石云绑定状态,0-未知,1-已绑定,2-未绑定"""
    
    physical_access_verification: str
    """设备支持的物理接触式添加方式,1#AP配网传递,2#用户令牌（用户token）绑定,3#物理按键接触,4#扫码绑定（设备token）"""

    @property
    def is_activated(self) -> bool:
        """返回设备是否已激活
        Returns:
            bool: True表示已激活，False表示未激活
        """
        return self.activated == 0

    @property
    def result_desc(self) -> str:
        """消息类型描述
        Returns:
            str: 消息类型描述
        """
        descriptions = {
            1: "新设备上线",
            2: "设备更新",
            3: "设备下线",
            4: "设备重启",
            5: "设备更新失败"
        }
        return descriptions.get(self.result)
    
    def __init__(self, sadp_device_info_v40):
        """初始化设备信息对象
        
        Args:
            sadp_device_info_v40: SADP_DEVICE_INFO_V40结构体实例
        """
        # 保存原始结构体引用
        self._raw = sadp_device_info_v40
        
        # 映射基础设备信息
        base_info = sadp_device_info_v40.struSadpDeviceInfo
        
        # 字符串字段需要解码
        self.series = base_info.szSeries.decode('utf-8').strip('\x00')
        self.serial_no = base_info.szSerialNO.decode('utf-8').strip('\x00')
        self.mac = base_info.szMAC.decode('utf-8').strip('\x00')
        self.ipv4_address = base_info.szIPv4Address.decode('utf-8').strip('\x00')
        self.ipv4_subnet_mask = base_info.szIPv4SubnetMask.decode('utf-8').strip('\x00')
        self.device_type = base_info.dwDeviceType
        self.port = base_info.dwPort
        self.number_of_encoders = base_info.dwNumberOfEncoders
        self.number_of_hard_disk = base_info.dwNumberOfHardDisk
        self.device_software_version = base_info.szDeviceSoftwareVersion.decode('utf-8').strip('\x00')
        self.dsp_version = base_info.szDSPVersion.decode('utf-8').strip('\x00')
        self.boot_time = base_info.szBootTime.decode('utf-8').strip('\x00')
        self.result = base_info.iResult
        self.dev_desc = base_info.szDevDesc.decode('utf-8').strip('\x00')
        self.oem_info = base_info.szOEMinfo.decode('utf-8').strip('\x00')
        self.ipv4_gateway = base_info.szIPv4Gateway.decode('utf-8').strip('\x00')
        self.ipv6_address = base_info.szIPv6Address.decode('utf-8').strip('\x00')
        self.ipv6_gateway = base_info.szIPv6Gateway.decode('utf-8').strip('\x00')
        self.ipv6_mask_len = base_info.byIPv6MaskLen
        self.support = base_info.bySupport
        self.dhcp_enabled = base_info.byDhcpEnabled
        self.device_ability = base_info.byDeviceAbility
        self.http_port = base_info.wHttpPort
        self.digital_channel_num = base_info.wDigitalChannelNum
        self.cms_ipv4 = base_info.szCmsIPv4.decode('utf-8').strip('\x00')
        self.cms_port = base_info.wCmsPort
        self.oem_code = base_info.byOEMCode
        self.activated = base_info.byActivated
        self.base_desc = base_info.szBaseDesc.decode('utf-8').strip('\x00')
        self.support1 = base_info.bySupport1
        self.hc_platform = base_info.byHCPlatform
        self.enable_hc_platform = base_info.byEnableHCPlatform
        self.ezviz_code = base_info.byEZVIZCode
        self.detail_oem_code = base_info.dwDetailOEMCode
        self.modify_verification_code = base_info.byModifyVerificationCode
        self.max_bind_num = base_info.byMaxBindNum
        self.oem_command_port = base_info.wOEMCommandPort
        self.support_wifi_region = base_info.bySupportWifiRegion
        self.enable_wifi_enhancement = base_info.byEnableWifiEnhancement
        self.wifi_region = base_info.byWifiRegion
        self.support2 = base_info.bySupport2
        
        # 映射V40扩展字段
        self.licensed = sadp_device_info_v40.byLicensed
        self.system_mode = sadp_device_info_v40.bySystemMode
        self.controller_type = sadp_device_info_v40.byControllerType
        self.ehmoe_version = sadp_device_info_v40.szEhmoeVersion.decode('utf-8').strip('\x00')
        self.specific_device_type = sadp_device_info_v40.bySpecificDeviceType
        self.sdk_over_tls_port = sadp_device_info_v40.dwSDKOverTLSPort
        self.security_mode = sadp_device_info_v40.bySecurityMode
        self.sdk_server_status = sadp_device_info_v40.bySDKServerStatus
        self.sdk_over_tls_server_status = sadp_device_info_v40.bySDKOverTLSServerStatus
        self.user_name = sadp_device_info_v40.szUserName.decode('utf-8').strip('\x00')
        self.wifi_mac = sadp_device_info_v40.szWifiMAC.decode('utf-8').strip('\x00')
        self.data_from_multicast = sadp_device_info_v40.byDataFromMulticast
        self.support_ezviz_unbind = sadp_device_info_v40.bySupportEzvizUnbind
        self.support_code_encrypt = sadp_device_info_v40.bySupportCodeEncrypt
        self.support_password_reset_type = sadp_device_info_v40.bySupportPasswordResetType
        self.ezviz_bind_status = sadp_device_info_v40.byEZVIZBindStatus
        self.physical_access_verification = sadp_device_info_v40.szPhysicalAccessVerification.decode('utf-8').strip('\x00')
        

    def __eq__(self, value):
        if not isinstance(value, DeviceInfo):
            return False
        return self.mac == value.mac
    
    def __str__(self):
        return f"ip:'{self.ipv4_address}', mac:'{self.mac}', serial_no:'{self.serial_no}',  {'未激活' if self.activated else '已激活' }"
    