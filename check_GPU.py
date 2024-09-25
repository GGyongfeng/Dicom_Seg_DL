import torch
import openpyxl

print(torch.cuda.is_available())  # 检查是否有可用的 GPU
print(torch.cuda.current_device())  # 返回当前 GPU 设备的索引
print(torch.cuda.get_device_name(0))  # 返回当前 GPU 的名称
print(torch.version.cuda)  # 返回 PyTorch 支持的 CUDA 版本