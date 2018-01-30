from tkinter.filedialog import *
from re import *
from requests import *
import os

re_imagename = compile(r'n[0-9]+_[0-9]+')
re_derictory = compile(r'n[0-9]+')
re_url = compile(r'http://.*\.jpg')

currentderictory = 'current derictory'

def Get_Image():
    '''文件选取从Image-net下载的，包含url的txt文件。
    图片保存到代码所在文件夹，图片名为图片ID。
    '''
    with open(askopenfilename(),'r') as URLlistfile:
        URLlist = URLlistfile.readlines()
    for URL in URLlist:
        name = re_imagename.findall(URL)[0]
        url = re_url.findall(URL)[0]
        derictory = re_derictory.findall(name)[0]
        if not os.path.exists(currentderictory+derictory):
            os.makedirs(currentderictory+derictory)
        os.chdir(currentderictory+derictory)
        with open(name+'.jpg','wb') as imagefile:
            imagefile.write(get(url).content)
    return None

Get_Image()