#遍历指定文件夹original下的所有子级文件夹
#将nrrd文件转化为nii文件
#如果已经有转化过的，就跳过
import os
import nibabel as nib
import nrrd

def convert_nrrd_to_nii(original_folder):
    for root, dirs, files in os.walk(original_folder):
        for file in files:
            if file.endswith('.nrrd'):
                nrrd_path = os.path.join(root, file)
                nii_path = os.path.splitext(nrrd_path)[0] + '.nii'
                
                # 如果已经有转换后的文件，则跳过
                if os.path.exists(nii_path):
                    print(f"已存在：{nii_path}，跳过转换。")
                    continue
                
                # 转换文件
                data, header = nrrd.read(nrrd_path)
                nii_img = nib.Nifti1Image(data, affine=None)  # 根据需要设置affine
                nib.save(nii_img, nii_path)
                print(f"转换完成：{nrrd_path} -> {nii_path}")

# 指定 original 文件夹路径
original_folder = './dataset/original'
convert_nrrd_to_nii(original_folder)
