import os
import img2pdf


def convert_images_to_pdf(folder_path='.'):
    """
    将指定文件夹下的所有JPG和PNG图片转换为PDF文件，每个PDF文件以原始图片的名字命名（如果有多张图片，则将它们合并为一个PDF）。

    :param folder_path: 包含图片的文件夹路径，默认为当前文件夹
    """
    # 创建一个空列表来存储图像文件的二进制内容
    images = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 构建文件的完整路径
            image_path = os.path.join(folder_path, filename)
            # 读取图像文件的二进制内容
            with open(image_path, 'rb') as image_file:
                images.append(image_file.read())

                # 如果没有找到任何图像文件，则不执行转换
    if not images:
        print("No images found in the specified folder.")
        return

        # 将所有图像的二进制内容合并为一个PDF文件（这里假设你想要将所有图片合并为一个PDF）
    # 如果你想要每个图片一个PDF，那么你需要在这个循环中处理每个图像
    pdf_bytes = img2pdf.convert(images)

    # 注意：上面的代码将所有图片合并到了一个PDF中。
    # 如果你想要每个图片生成一个PDF，你需要将下面的代码放入上面的for循环中，
    # 并为每个图片单独调用img2pdf.convert([image])，其中image是单个图像的二进制内容。

    # 假设我们想要每个图片一个PDF（取消下面的注释以使用）
    # for img_data in images:
    #     pdf_bytes = img2pdf.convert([img_data])
    #     # 这里需要为每个PDF文件指定一个唯一的名称，或者你可以使用循环索引来创建它们
    #     # 例如：pdf_name = f"{os.path.splitext(filename)[0]}_single.pdf"
    #     # 但由于我们已经在循环外部了，我们需要稍微调整逻辑来保持文件名和内容的对应关系

    # 由于我们假设每个图片一个PDF，我们回到for循环并处理每个图片
    for i, img_data in enumerate(images):
        # 为每个PDF文件生成一个唯一的名称（这里简单地使用索引，但你可以根据需要调整）
        pdf_name = f"{os.path.splitext(os.path.basename(images[i].name))[0] if hasattr(images[i], 'name') else str(i)}.pdf"
        pdf_path = os.path.join(folder_path, pdf_name)

        # 注意：上面的images[i].name可能不起作用，因为images是一个二进制数据的列表。
        # 我们实际上应该使用filename列表或重新构建它。
        # 这里我们假设filename列表与images列表是同步的（即它们有相同的索引和对应的文件名）
        real_filename = os.listdir(folder_path)[i]  # 这通常不是一个好方法，因为它依赖于文件列表的顺序
        # 更好的方法是维护一个文件名列表与images列表同步
        pdf_name_corrected = os.path.splitext(real_filename)[0] + '.pdf'
        pdf_path_corrected = os.path.join(folder_path, pdf_name_corrected)

        # 转换单个图像到PDF并保存
        pdf_bytes_single = img2pdf.convert([img_data])
        with open(pdf_path_corrected, 'wb') as f:
            f.write(pdf_bytes_single)

        print(f"Converted {real_filename} to {pdf_name_corrected}")

    # 注意：上面的代码片段在处理文件名时有一些假设和潜在的问题。


# 在实际应用中，你可能需要更精确地管理文件名和图像数据的对应关系。

# 调用函数，默认处理当前文件夹下的图片
# 注意：由于上面的代码示例在处理文件名时存在一些问题，你可能需要对其进行调整以符合你的具体需求。
# convert_images_to_pdf()  # 取消注释以运行函数

# 一个更健壮的示例，使用文件名列表来保持同步
def convert_images_to_individual_pdfs(folder_path='.'):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for filename in image_files:
        image_path = os.path.join(folder_path, filename)
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()
            pdf_name = os.path.splitext(filename)[0] + '.pdf'
            pdf_path = os.path.join(folder_path, pdf_name)
            pdf_bytes = img2pdf.convert([img_data])
            with open(pdf_path, 'wb') as f:
                f.write(pdf_bytes)
            print(f"Converted {filename} to {pdf_name}")

        # 使用这个更健壮的函数


convert_images_to_individual_pdfs()