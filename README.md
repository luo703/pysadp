# PYSADP - 海康威视SADP SDK Python封装

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/luo703/pysadp.svg)](https://github.com/luo703/pysadp/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/luo703/pysadp.svg)](https://github.com/luo703/pysadp/network)

海康威视SADP SDK协议的Python封装库，提供设备搜索、激活和网络配置功能。

### 暂时实现了3个最常用功能封装

- 搜索设备
- 激活设备
- 修改网络参数

### 安装

```bash
# 克隆仓库
git clone https://github.com/luo703/pysadp.git
```

### 项目结构

```
pysadp/
├── pysadp/                # 主包
│   ├── __init__.py        # 包初始化
│   ├── sadp.py            # SADP协议封装
│   ├── base.py            # 基础结构和常量
│   ├── model.py           # 数据模型
│   ├── ip_generator.py    # IP地址生成器
│   └── sdk_errors.py      # 错误码映射
├── sdk/                   # 海康威视SDK文件
├── example.py             # 使用示例
└── README.md              # 项目文档
```

### 运行示例

```bash
python example.py
```

## 📦 SDK 文件说明

本项目自带海康威视提供的SADP SDK文件。以下文件不可缺少：

- `HCSadpSDK_Log_Switch.xml`
- `libcrypto-1_1-x64.dll`
- `libssl-1_1-x64.dll`
- `Sadp.dll`
- `Sadp.lib`
- `npf64.sys`

官方SDK及相关文档：<https://open.hikvision.com/download/5cda567cf47ae80dd41a54b3?id=643174655be04ffabef494f3f1f07746>

---
**作者**: 罗辑  
**邮箱**: <newluo@163.com>  
**GitHub**: [https://github.com/luo703/pysadp](https://github.com/luo703/pysadp)
