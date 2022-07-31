'''
配置Study To Do
'''
import os,shutil

def setup():
    # 创建文件夹
    os.mkdir(os.getenv('APPDATA')+'\\Study To Do')
    os.mkdir(os.getenv('APPDATA')+'\\Study To Do\\Plan')
    # # 复制文件
    shutil.copytree('data',os.getenv('APPDATA')+'\\Study To Do\\data')
    shutil.copytree('ico',os.getenv('APPDATA')+'\\Study To Do\\ico')
    # 获取参数

setup()