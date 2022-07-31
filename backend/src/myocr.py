import pyocr
from PIL import Image, ImageEnhance
import os

tools = pyocr.get_available_tools()
tool = tools[0]
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

def myocr(imgpath: str, lang="jpn", outputfilepath=None):
    img = Image.open(imgpath)

    img_g = img.convert('L') # gray img
    enhancer = ImageEnhance.Contrast(img_g)
    img_con = enhancer.enhance(2.0) # increase contrast

    txt_pyocr = tool.image_to_string(img_con, lang=lang, builder=builder)
    txt_pyocr = txt_pyocr.replace(' ', '')

    if outputfilepath:
        with open(outputfilepath, 'w') as f:
            f.write(txt_pyocr)

if __name__ == "__main__":
    myocr('sample.png', outputfilepath="output2.txt")
