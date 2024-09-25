import os
import numpy as np
import SimpleITK as sitk

def get_array(image_dir: str, label_dir: str, save_dir):
    """
    把同一个文件夹中所有患者的CT数据，合并到一起，并将数据类型转换为float32
    :param image_dir:
    :param label_dir:
    :param save_dir: 保存路径
    :return:
    """
    os.makedirs(save_dir, exist_ok=True)

    image_all = []
    label_all = []
    files_to_delete = []

    print("读取并比对所有nii文件中......\n")
    for image_file in os.listdir(image_dir):
        # 读取图像
        image_path = os.path.join(image_dir, image_file)
        assert os.path.exists(image_path), f"{image_path} 不存在"
        itk_img = sitk.ReadImage(image_path)
        image = sitk.GetArrayFromImage(itk_img).astype(np.float32)  # 转换为 float32
        image_all.append(image)

        # 读取标签
        label_path = os.path.join(label_dir, f"segmentation-{image_file.split('-')[-1].split('.')[0]}.nii")
        assert os.path.exists(label_path), f"{label_path} 不存在"
        itk_label = sitk.ReadImage(label_path)
        label = sitk.GetArrayFromImage(itk_label).astype(np.float32)  # 转换为 float32
        label[label > 0] = 1  # 本身有两个类别1和2，但只分割病灶位置
        label_all.append(label)

    # 检查label文件夹的所有nii文件的形状是否为 (512, 512)
    label_inconsistent_files = []
    for label_file in os.listdir(label_dir):
        label_path = os.path.join(label_dir, label_file)
        itk_label = sitk.ReadImage(label_path)
        label_shape = sitk.GetArrayFromImage(itk_label).shape[1:]  # 获取 H 和 W
        if label_shape != (512, 512):  # 检查是否为 (512, 512)
            label_inconsistent_files.append(label_path)

    # 检查image文件夹的所有nii文件的形状是否为 (512, 512)
    image_inconsistent_files = []
    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)
        itk_img = sitk.ReadImage(image_path)
        image_shape = sitk.GetArrayFromImage(itk_img).shape[1:]  # 获取 H 和 W
        if image_shape != (512, 512):  # 检查是否为 (512, 512)
            image_inconsistent_files.append(image_path)

    # 输出不一致文件的数量
    print(f"不一致的label.nii文件数量: {len(label_inconsistent_files)}个")
    print(f"不一致的image.nii文件数量: {len(image_inconsistent_files)}个")

    # 询问是否删除不一致的文件
    files_to_delete_pairs = []
    for label_file in label_inconsistent_files:
        file_id = label_file.split('-')[-1].split('.')[0]
        image_file = os.path.join(image_dir, f"volume-{file_id}.nii")
        files_to_delete_pairs.append((image_file, label_file))

    for image_file in image_inconsistent_files:
        file_id = image_file.split('-')[-1].split('.')[0]
        label_file = os.path.join(label_dir, f"segmentation-{file_id}.nii")
        files_to_delete_pairs.append((image_file, label_file))

    if files_to_delete_pairs:
        print("\n检测到不一致的文件，以下文件将成对删除：")
        for image_file, label_file in files_to_delete_pairs:
            # 获取 image_file 的形状
            itk_image = sitk.ReadImage(image_file)
            image_shape = sitk.GetArrayFromImage(itk_image).shape
            
            # 获取 label_file 的形状
            itk_label = sitk.ReadImage(label_file)
            label_shape = sitk.GetArrayFromImage(itk_label).shape
            
            print(f"删除 volume 文件: {image_file} - 形状: {image_shape}")
            print(f"删除 segmentation 文件: {label_file} - 形状: {label_shape}")

        confirm_delete = input("是否确认删除以上文件？(y/n): ")
        if confirm_delete.lower() == 'y':
            for image_file, label_file in files_to_delete_pairs:
                os.remove(image_file)
                os.remove(label_file)
            print("不一致的文件已删除。")
        else:
            print("未删除任何文件。")

    # 检查是否所有形状一致,确认执行拼接
    if len(label_inconsistent_files) == 0 and len(image_inconsistent_files) == 0:
        label_file_count = len(label_all)
        image_file_count = len(image_all)

        # 输出文件数量
        print(f"\n要拼接的label文件夹中的文件个数: {label_file_count}")
        print(f"要拼接的image文件夹中的文件个数: {image_file_count}")

        # 确认是否进行拼接
        confirm_concat = input("是否确认拼接这些文件？(y/n): ")
        if confirm_concat.lower() == 'y':
            label_cat = np.concatenate(label_all, axis=0)  # 拼接标签
            image_cat = np.concatenate(image_all, axis=0)  # 拼接特征

            print("image_cat:", image_cat.shape)
            print("label_cat:", label_cat.shape)

            # 保存为numpy格式
            np.save(os.path.join(save_dir, 'image.npy'), image_cat)
            np.save(os.path.join(save_dir, 'label.npy'), label_cat)
            print(f'保存至:', save_dir)
        else:
            print("未进行拼接。")
    else:
        print("\n由于标签数组或图像数组形状不一致，未进行拼接和保存。")

if __name__ == '__main__':
    # 需要转换的目录：train validate
    dir_type = "train"

    get_array(image_dir=f"./dataset/{dir_type}/image",
              label_dir=f"./dataset/{dir_type}/label",
              save_dir=f'../data/{dir_type}')

