#已知 现在original下的每个子文件夹都包含两个nii文件
# -分别为volume-{文件夹名}.nii和segmentation-{文件夹名}.nii

#对original下的所有子文件夹进行数据划分 
# 按照训练集：测试集：验证集 = 6 :2 :2 的比例将文件夹进行随机划分
# 将划分为 训练集 的文件夹下的volume-{文件夹名}.nii 复制到 ./train/image、segmentation-{文件夹名}.nii 移动到 ./train/label
# 将划分为 验证集 的文件夹下的volume-{文件夹名}.nii 复制到 ./validate/image、segmentation-{文件夹名}.nii 移动到 ./validate/label
# 将划分为 测试集 的文件夹下的volume-{文件夹名}.nii 复制到 ./test/image、segmentation-{文件夹名}.nii 移动到 ./test/label

import os
import shutil
import random

def create_directory_structure():
    """
    创建目标目录结构
    """
    os.makedirs('./train/image', exist_ok=True)
    os.makedirs('./train/label', exist_ok=True)
    os.makedirs('./validate/image', exist_ok=True)
    os.makedirs('./validate/label', exist_ok=True)
    os.makedirs('./test/image', exist_ok=True)
    os.makedirs('./test/label', exist_ok=True)

def move_files(folder_name, dataset, src_folder):
    """
    根据数据集类型移动文件
    :param folder_name: 文件夹名称
    :param dataset: 数据集类型 (train, validate, test)
    :param src_folder: 原始文件夹路径
    """
    volume_file = f'volume-{folder_name}.nii'
    segmentation_file = f'segmentation-{folder_name}.nii'
    
    # 构建子文件夹的完整路径
    sub_folder_path = os.path.join(src_folder, folder_name)

    if dataset == 'train':
        dst_image = './train/image'
        dst_label = './train/label'
    elif dataset == 'validate':
        dst_image = './validate/image'
        dst_label = './validate/label'
    elif dataset == 'test':
        dst_image = './test/image'
        dst_label = './test/label'

    try:
        # 移动文件
        shutil.move(os.path.join(sub_folder_path, volume_file), os.path.join(dst_image, volume_file))
        shutil.move(os.path.join(sub_folder_path, segmentation_file), os.path.join(dst_label, segmentation_file))
        print(f"Moved {volume_file} and {segmentation_file} to {dataset} set.")
    except FileNotFoundError:
        print(f"Warning: {volume_file} or {segmentation_file} not found in {sub_folder_path}.")
    except Exception as e:
        print(f"Error moving files from {sub_folder_path}: {e}")

def split_datasets(original_folder, train_ratio, validate_ratio):
    """
    从指定目录中读取文件夹，按比例划分为训练集、验证集和测试集
    :param original_folder: 原始文件夹路径
    :param train_ratio: 训练集比例
    :param validate_ratio: 验证集比例
    """
    all_folders = [d for d in os.listdir(original_folder) if os.path.isdir(os.path.join(original_folder, d))]
    
    # 随机打乱文件夹顺序
    random.shuffle(all_folders)

    # 计算划分的索引
    total_count = len(all_folders)
    validate_count = int(total_count * validate_ratio)
    train_count = int(total_count * train_ratio)

    # 划分数据集
    train_folders = all_folders[:train_count]
    validate_folders = all_folders[train_count:train_count + validate_count]
    test_folders = all_folders[train_count + validate_count:]

    # 移动文件
    for folder in train_folders:
        move_files(folder, 'train', original_folder)
    for folder in validate_folders:
        move_files(folder, 'validate', original_folder)
    for folder in test_folders:
        move_files(folder, 'test', original_folder)

if __name__ == "__main__":
    # 在代码中直接指定参数
    original_folder = './dataset/original'  # 指定原始文件夹路径
    train_ratio = 0.6  # 训练集比例
    validate_ratio = 0.2  # 验证集比例

    # 计算测试集比例
    test_ratio = 1.0 - (train_ratio + validate_ratio)

    if test_ratio < 0:
        raise ValueError("The sum of train_ratio and validate_ratio must be less than or equal to 1.")

    create_directory_structure()
    split_datasets(original_folder, train_ratio, validate_ratio)
