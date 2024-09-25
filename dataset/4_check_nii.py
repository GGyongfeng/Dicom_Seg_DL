#查看一下original的所有子级文件夹中是否都是含有segmentation-{其父级文件夹名称}.nii和volume-{其父级文件夹名称}.nii两个文件 
#如果哪个不是，输出其文件夹的名字

import os

def check_nii_files(root_dir):
    """
    检查original文件夹下所有子文件夹是否包含指定的segmentation和volume文件。
    
    :param root_dir: original文件夹的路径
    """
    all_folders_ok = True  # 标记是否所有文件夹都满足要求
    
    # 遍历original文件夹下的所有子文件夹
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        
        # 检查是否是目录
        if os.path.isdir(folder_path):
            # 构造segmentation和volume文件的预期名称
            segmentation_file = f"segmentation-{folder_name}.nii"
            volume_file = f"volume-{folder_name}.nii"
            
            # 检查子文件夹是否包含这两个文件
            has_segmentation = segmentation_file in os.listdir(folder_path)
            has_volume = volume_file in os.listdir(folder_path)
            
            # 如果缺少其中一个文件，输出子文件夹的名称
            if not (has_segmentation and has_volume):
                print(f"文件夹 {folder_name} 缺少必要的文件")
                all_folders_ok = False
    
    # 如果所有文件夹都满足要求，输出总结信息
    if all_folders_ok:
        print("所有子文件夹均包含segmentation.nii和volume.nii文件。")

# 调用函数
root_dir = './dataset/original'  # 替换为original文件夹的实际路径
check_nii_files(root_dir)
