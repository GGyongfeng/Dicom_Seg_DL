#遍历original的所有子级文件夹(已知每个文件夹下都有两个nrrd的文件)
#将其中的Segmentation-label.nrrd文件重命名为segmentation-{其父级文件夹名称}.nrrd
#将另一个nrrd文件命名为volume-{其父级文件夹名称}.nrrd

import os

def rename_nrrd_files_in_folders(directory):
    """
    遍历指定目录的所有子文件夹，将 .nrrd 文件根据父级文件夹名称进行重命名：
    1. Segmentation-label.nrrd -> segmentation-{父级文件夹名称}.nrrd
    2. 另一个 .nrrd 文件 -> volume-{父级文件夹名称}.nrrd
    :param directory: 要遍历的根目录
    """
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            
            # 获取文件夹中的 .nrrd 文件列表
            nrrd_files = [f for f in os.listdir(folder_path) if f.endswith('.nrrd')]
            
            # 确保文件夹中有两个 .nrrd 文件
            if len(nrrd_files) == 2:
                # 生成新文件名
                parent_folder_name = os.path.basename(folder_path)
                
                # 分别对Segmentation-label.nrrd 和 另一个 .nrrd 文件重命名
                for nrrd_file in nrrd_files:
                    old_file_path = os.path.join(folder_path, nrrd_file)
                    if nrrd_file == 'Segmentation-label.nrrd':
                        new_file_name = f'segmentation-{parent_folder_name}.nrrd'
                    else:
                        new_file_name = f'volume-{parent_folder_name}.nrrd'
                    
                    new_file_path = os.path.join(folder_path, new_file_name)
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} -> {new_file_path}")
            else:
                print(f"Warning: {folder_path} does not contain exactly two .nrrd files.")

if __name__ == "__main__":
    # 指定要遍历的根目录 'original'
    root_directory = './dataset/original'  # 根据实际情况调整路径
    
    # 调用函数进行重命名
    rename_nrrd_files_in_folders(root_directory)
