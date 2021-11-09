#utf-8

from pathlib import Path

path = Path(__file__).resolve()
print(path.suffix)  #文件后缀
print(path.stem)    #文件名不带后缀
print(path.name)     #带后缀的完整文件名
print(path.parent)  #路径的上级目录