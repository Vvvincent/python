from progressbar import *
from PIL import Image
import urllib.request
import xlsxwriter
import xlrd
import io

def download_img(img_url):
    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            img = io.BytesIO(response.read())
            return img
    except:
        return None

if __name__ == '__main__':
    # 下载要的图片
    filePath = str(input("Please input URL: "))
    try:
        workbook = xlrd.open_workbook(filePath)
        sheet1 = workbook.sheet_by_index(0)
        workbook1 = xlsxwriter.Workbook('images.xlsx')
        worksheet = workbook1.add_worksheet()
        worksheet.set_default_row(67)
        progress = ProgressBar()
        for i in progress(range(1,sheet1.nrows)):
            row = i - 1
            url = str(sheet1.cell(i, 0).value.encode('utf-8')).split("'")[1]
            img_bytes = download_img(url)
            if img_bytes is None:
                worksheet.write(row, 0, url)
                continue
            img = Image.open(img_bytes)
            img = img.resize((220,300))
            resized_img_bytes = io.BytesIO()
            # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
            img.save(resized_img_bytes, format="JPEG")
            # 从字节流管道中获取二进制
            worksheet.write(row, 0, url)
            worksheet.insert_image(row,10, url, {'image_data': resized_img_bytes,'x_scale': 0.3, 'y_scale': 0.3})
        workbook1.close()
        print("Success")
    except:
        print("Failure")


