# Dicom_Seg_DL

## 项目概述

本项目旨在实现医学图像分割，特别是肝脏病灶的分割。项目包含数据预处理和训练部分，使用 U2NET 模型进行训练。数据预处理步骤将原始医学影像和对应标签处理为适合模型训练的格式，并提供训练的配置和执行方式。

## 文件结构

```
project_root/
├── dataset/
│   ├── test/
│   │   ├── image/
│   │   └── label/
│   ├── train/
│   │   ├── image/
│   │   └── label/
│   └── validate/
│       ├── image/
│       └── label/
├── data/
│   ├── train/
│   └── validate/
├── tools/
│   ├── data_loader.py
│   ├── u2net.py
│   ├── utils.py
├── config.py
├── u2net_train.py
└── README.md
```

### 文件和文件夹说明

- **dataset/**: 存放原始医学影像和标签的目录。需要按照训练集、验证集和测试集进行划分。
  - **train/**: 包含训练集的图像和标签，命名规则需一致。
  - **validate/**: 包含验证集的图像和标签，命名规则需一致。
  - **test/**: 包含测试集的图像和标签。

- **data/**: 存放预处理后的数据。
  - **train/**: 存放处理后的训练数据。
  - **validate/**: 存放处理后的验证数据。

- **tools/**: 存放项目中使用的工具函数和模型定义。
  - **data_loader.py**: 数据加载器，用于处理图像和标签。
  - **u2net.py**: U2NET 模型的定义。
  - **utils.py**: 工具函数，包括模型评估等。

- **config.py**: 存放项目的配置参数，包括数据路径、模型选择和训练参数。

- **u2net_train.py**: 训练脚本，用于训练 U2NET 模型。

## 使用方法

### 1. 数据准备

在 `dataset` 文件夹中创建如下结构：

```
dataset/
├── original/ #原始数据
│   ├── 517990
│   ├── 525613
│   ├── ......
├── train/
│   ├── image/    # 训练图像
│   └── label/    # 训练标签
├── validate/
│   ├── image/    # 验证图像
│   └── label/    # 验证标签
└── test/
    ├── image/    # 测试图像
    └── label/    # 测试标签
```

只需要将原始数据放置在original文件

### 2. 数据预处理

运行 `6_get_final_data.py` 脚本进行数据预处理。该脚本会读取 `dataset` 文件夹中的图像和标签，进行格式转换，并保存到 `data` 文件夹中。

```bash
python 6_get_final_data.py
```

### 3. 调整配置

在 `config.py` 文件中，调整相关参数，例如训练集和验证集路径、图像尺寸、模型名称及使用的 GPU 型号。

### 4. 训练模型

使用 `u2net_train.py` 进行模型训练。可以通过命令行运行脚本，并设置参数。

```bash
python u2net_train.py
```

该脚本会读取 `config.py` 中的设置，进行模型训练，并保存训练过程中的模型。

### 5. 评估模型

训练完成后，可以使用 `model_evaluate.py` 进行模型评估，查看在验证集上的表现。

## 注意事项

- 请确保所有图像和标签的尺寸一致，并且图像通道数为 1。
- 如果使用 GPU 进行训练，请确保 CUDA 环境已正确配置。

## 贡献指南

欢迎任何形式的贡献！如果您有建议、bug 报告或功能请求，请通过提交 issue 或者 pull request 的方式与我们联系。

### 如何贡献

1. Fork 本仓库。
2. 在您的分支上进行修改。
3. 提交 Pull Request。

感谢您对本项目的关注与支持！希望这个项目能够对医学图像处理领域有所帮助。