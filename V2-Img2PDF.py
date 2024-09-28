from PIL import Image
import img2pdf
import io
import os


def process_images_for_pdf(image_paths):
    # 创建一个列表来存储处理后的图像二进制数据
    processed_images = []

    for image_path in image_paths:
        # 使用 PIL 打开图像
        with Image.open(image_path) as img:
            # 在这里，Pillow 通常会自动处理 EXIF 旋转
            # 如果你需要忽略 EXIF 旋转（尽管这通常不是必要的），
            # 你可以使用 img._getexif() 来检查 EXIF 数据，但通常不推荐直接修改 PIL 内部状态

            # 将图像保存到 BytesIO 对象中，以便获取其二进制数据
            # 注意：这里我们假设你想要以相同的格式保存图像（例如，如果它是 JPEG，则保存为 JPEG）
            # 如果原始图像不是 JPEG，你可能需要指定一个不同的格式
            image_byte_arr = io.BytesIO()
            img.save(image_byte_arr, format=img.format)  # img.format 通常是 'JPEG', 'PNG' 等
            image_byte_arr = image_byte_arr.getvalue()

            # 将处理后的图像二进制数据添加到列表中
            processed_images.append(image_byte_arr)

            # 现在你可以将 processed_images 传递给 img2pdf.convert()
    pdf_bytes = img2pdf.convert(processed_images, rotation=img2pdf.Rotation.ifvalid)

    # 返回或保存 PDF 字节数据
    return pdf_bytes


def convert_images_to_pdf(folder_path='.'):
    # 遍历指定文件夹下的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 构造图片路径
            image_path = os.path.join(folder_path, filename)
            # 构造只包含当前图片路径的列表
            image_paths = [image_path]
            # 调用函数将图片转换为PDF字节数据
            pdf_bytes = process_images_for_pdf(image_paths)
            # 构造PDF文件名（不带扩展名）
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            # 将PDF字节数据写入文件
            with open(os.path.join(folder_path, pdf_filename), 'wb') as f:
                f.write(pdf_bytes)
            print(f'PDF saved as {pdf_filename}')

        # 调用函数，默认处理当前文件夹下的图片


convert_images_to_pdf()

# # 示例用法
# image_paths = ['查理-20210381-第十届全国青年科普创新大赛.jpg']
# pdf_bytes = process_images_for_pdf(image_paths)
#
# # 如果你想要将 PDF 保存到文件中
# with open('output.pdf', 'wb') as f:
#     f.write(pdf_bytes)