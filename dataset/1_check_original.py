#查看一下original的所有子级文件夹中是否都含有一个名为Segmentation-label.nrrd的文件
#如果哪个没有，输出其文件夹的名字，以及其内部的两个nrrd文件的名字
#查看一下original的所有子级文件夹中是否都是含有两个后缀名为.nrrd的文件
#如果哪个不是，输出其文件夹的名字

import os

def check_folders_for_nrrd_files(directory, required_file, nrrd_count=2):
    """
    遍历目录的所有子文件夹，检查是否包含指定的文件和是否有两个后缀为 .nrrd 的文件
    :param directory: 要遍历的根目录
    :param required_file: 要检查的文件名
    :param nrrd_count: 需要的 .nrrd 文件数量
    """
    missing_file_folders = []
    incorrect_nrrd_folders = []

    # 遍历子文件夹
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            file_path = os.path.join(folder_path, required_file)
            
            # 假设 folder_path 是你的文件夹路径
            if not os.path.exists(file_path):
                # 获取文件夹中的所有 .nrrd 文件
                nrrd_files = [f for f in os.listdir(folder_path) if f.endswith('.nrrd')]
                
                # 检查是否有 Segmentation.seg.nrrd 文件，并重命名
                segmentation_file = os.path.join(folder_path, 'Segmentation.seg.nrrd')
                if os.path.exists(segmentation_file):
                    new_name = os.path.join(folder_path, 'Segmentation-label.nrrd')
                    os.rename(segmentation_file, new_name)
                else:
                    # 只有在 Segmentation.seg.nrrd 文件不存在时，才将信息添加到列表
                    missing_file_folders.append({
                        'folder': folder_path,
                        'nrrd_files': nrrd_files
                    })

            # 统计文件夹中 .nrrd 文件的数量
            nrrd_files = [f for f in os.listdir(folder_path) if f.endswith('.nrrd')]
            if len(nrrd_files) != nrrd_count:
                incorrect_nrrd_folders.append(folder_path)
    
    # 输出缺少指定文件的文件夹
    if missing_file_folders:
        print(f"以下文件夹缺少文件 {required_file}:")
        for folder in missing_file_folders:
            print(folder)
    else:
        print(f"所有子文件夹都包含文件 {required_file}")

    # 输出 .nrrd 文件数量不符合要求的文件夹
    if incorrect_nrrd_folders:
        print(f"\n以下文件夹中不包含 {nrrd_count} 个 .nrrd 文件:")
        for folder in incorrect_nrrd_folders:
            print(folder)
    else:
        print(f"所有子文件夹都包含 {nrrd_count} 个 .nrrd 文件")

if __name__ == "__main__":
    # 指定要遍历的根目录 'original' 和要检查的文件 'Segmentation-label.nrrd'
    root_directory = './dataset/original'  # 可以根据实际情况修改路径
    file_to_check = 'Segmentation-label.nrrd'
    
    # 检查文件夹是否包含指定文件和两个 .nrrd 文件
    check_folders_for_nrrd_files(root_directory, file_to_check)
