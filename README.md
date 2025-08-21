# Amazing Hand Python SDK

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

一个用于控制 Amazing Hand 机械手的高级 Python SDK。

本 SDK 旨在提供一个简洁、高级的 Python 接口，将复杂的底层通信和设置封装起来，让开发者可以专注于动作的实现和创新。

---

## **目录**

- [功能特性](#功能特性)
- [项目结构](#项目结构)
- [安装指南](#安装指南)
- [快速上手](#快速上手)
- [API 文档](#api文档)
  - [初始化](#初始化)
  - [核心方法](#核心方法)
  - [预设手势](#预设手势)
- [运行示例](#运行示例)
- [许可证](#许可证)

---

### **功能特性**

- **轻松连接**: 仅需一行代码即可初始化和连接机械手。
- **独立控制**: 支持对每个手指（拇指、食指、中指、无名指）的独立、精确控制。
- **预设手势**: 内置多种常用手势（如张开、握拳、胜利、OK等），方便直接调用。
- **支持左右手**: 可通过参数轻松切换左手或右手模式。
- **自定义校准**: 支持传入自定义校准数据，以适应不同硬件的差异。

---

### **项目结构**

```tree
.
├── amazingctrl/              # SDK 核心代码目录
│   ├── __init__.py
│   └── amazingctrl.py        # AmazingHand 主控制类
├── examples/                 # 示例代码目录
│   ├── gesture_sequence.py
│   ├── single_finger_control.py
│   └── custom_gesture.py
├── LICENSE                   # MIT 许可证
├── README.md                 # 项目说明文档
├── requirements.txt          # 依赖库列表
└── setup.py                  # 包安装配置文件
```

---

### **安装指南**

1. **克隆本仓库**

    ```bash
    git clone https://github.com/your_username/AmazingHandSDK.git
    cd AmazingHandSDK
    ```

2. **安装依赖**
    你可以选择以下两种方式之一进行安装：

    - **作为包安装 (推荐)**:
        此方法会将 `amazingctrl` 安装到你的 Python 环境中，方便在任何地方导入。

        ```bash
        pip install .
        ```

    - **仅安装依赖库**:
        如果你只想在当前项目目录下运行示例，可以只安装所需的依赖库。

        ```bash
        pip install -r requirements.txt
        ```

---

### **快速上手**

以下是一个简单的示例，展示了如何连接机械手并让它做一���胜利手势。

```python
import time
import amazingctrl

# --- 重要提示 ---
# 请将 "/dev/tty.usbmodemXXXX" 替换为你的机械手实际占用的串口号。
# Windows 系统上通常是 "COM3", "COM4" 等。
PORT = "/dev/tty.usbmodemXXXX"

try:
    # 1. 初始化控制器
    hand = amazingctrl.AmazingHand(port=PORT)

    # 2. 启动连接并给电机供电
    hand.start()
    time.sleep(1) # 等待机械手准备就绪

    # 3. 发送指令：做一个胜利手势
    print("正在做出胜利手势...")
    hand.victory()
    time.sleep(2) # 保持手势 2 秒

    # 4. 恢复为张开状态
    print("正在张开手掌...")
    hand.open()
    time.sleep(1)

except Exception as e:
    print(f"发生错误: {e}")
    print("请检查串口号是否正确，以及机械手是否已连接。")

finally:
    # 5. 操作结束，务必停止并释放电机
    if 'hand' in locals():
        print("正在停止机械手...")
        hand.stop()
```

---

### **API文档**

#### **初始化**

`amazingctrl.AmazingHand(port, side=1, calibration_data=None)`

- **`port`** (str): 必需参数。机械手连接的串口号。
- **`side`** (int, 可选): `1` 代表右手 (默认值), `2` 代表左手。
- **`calibration_data`** (list, 可选): 一个包含8个浮点数的列表，用���伺服电机的精细校准。

#### **核心方法**

- `hand.start()`: 连接到机械手并启用所有电机的扭矩，使其准备好接收指令。
- `hand.stop()`: 禁用所有电机的扭矩，释放机械手。在程序结束时调用此方法非常重要。
- `hand.index(angle_1, angle_2, speed)`: 控制食指。
- `hand.middle(angle_1, angle_2, speed)`: 控制中指。
- `hand.ring(angle_1, angle_2, speed)`: 控制无名指。
- `hand.thumb(angle_1, angle_2, speed)`: 控制拇指。
  - `angle_1` (float): 控制关节1（左右摆动）。
  - `angle_2` (float): 控制关节2（前后弯曲）。
  - `speed` (int): 设定电机的运动速度。

#### **预设手势**

- `hand.open()`: 手掌完全张开。
- `hand.close()`: 握拳。
- `hand.point()`: 食指指向。
- `hand.victory()`: 胜利手势 (V)。
- `hand.ok()`: OK 手势。
- `hand.pinch()`: 捏合手势。

---

### **运行示例**

在运行任何示例之前，请确保你已经：

1. 完成了[安装指南](#安装指南)中的步骤。
2. **修改了示例文件中的 `PORT` 变量**，使其与你的设备串口号匹配。

- **示例1: 手势序列**
    运行一个预设的常见手势序列。

    ```bash
    python examples/gesture_sequence.py
    ```

- **示例2: 单指控制**
    演示如何独立控制食指的弯曲和摆动。

    ```bash
    python examples/single_finger_control.py
    ```

- **示例3: 创建自定义手势**
    展示如何通过组合多个手指的动作来创建一个新的手势（“竖起大拇指”）。

    ```bash
    python examples/custom_gesture.py
    ```

---

### **许可证**

本项目采用 [MIT License](./LICENSE) 开源。
