# -- coding: utf-8 --

'''
1、读取指定目录下的所有文件
2、读取文件，正则匹配出需要的内容，获取文件名
3、打开此文件(可以选择打开可以选择复制到别的地方去)
'''
import os
import random
import cv2
# import re
#
#
# # 遍历指定目录，显示目录下的所有文件名
# def eachFile(filepath):
#     pathDir = os.listdir(filepath)
#     for allDir in pathDir:
#         child = os.path.join('%s\%s' % (filepath, allDir))
#         if os.path.isfile(child):
#             readFile(child)
#             #print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
#             continue
#         eachFile(child)
#
#
# # 遍历出结果 返回文件的名字
# def readFile(filenames):
#     fopen = open(filenames, 'r')  # r 代表read
#     fileread = fopen.read()
#     fopen.close()
#     t = re.search(r'clearSpitValve', fileread)
#     if t:
#         #print "匹配到的文件是:"+filenames
#         print(filenames)
#         arr.append(filenames)
#
#
# if __name__ == "__main__":
#
#     filenames = 'E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\coco\\\labels\\val2014'  # refer root dir
#     arr = []
#     print(filenames)
#     eachFile(filenames)
#     for i in arr:
#         print(i)
def findfile(file_path):
    listRs = os.listdir(file_path)
    for file_item in listRs:
        full_path = os.path.join(file_path, file_item)
        if os.path.isdir(full_path):
            findfile(full_path)
        else:
            print(file_item)
    else:
        return '没有数据'
def write(file_path, out_path):
    liRs = os.listdir(file_path)
    random.shuffle(liRs)
    for i in liRs:
        lines = open(file_path+i, encoding="utf-8").read().split("\n")
        with open(out_path, mode='a+', encoding="utf-8") as w:
            for j in lines:
                w.write(file_path.split('\\')[-3] + '/' + file_path.split('\\')[-2] + '/' + i + "\n")
                w.write(j + "\n")
    print(len(liRs))
    # print(file_path.split('\\')[-3:-1])
# write('E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\coco\\labels\\val2014\\', 'E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\coco\\labels.txt')
# write('E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\coco\\labels\\train2014\\', 'E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\coco\\labels.txt')

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False
# 定义要创建的目录
#mkpath = "d:\\qttc\\web\\"
# 调用函数
#mkdir(mkpath)
def rename(path):
    files = os.listdir(path)
    for i, file in enumerate(files):#os.path.splitext(file)[0]
        NewName = os.path.join(path, "2021_4_23_" + str(i+1) + '.jpg')
        OldName = os.path.join(path, file)
        os.rename(OldName, NewName)
#rename("d:\\360极速浏览器下载\\toc")



def wf(path):
    files = os.listdir(path)
    for file in files:
        with open('train.txt', mode='a+') as w:
            w.write('data/custom/images/'+file + "\n")
#wf('E:\\PycharmProjects\\pytorch-yolov3\\venv\\data\\custom\\images')

img = cv2.imread('mask/train/images/-1x-1_jpg.rf.69d9b61e3cdb8a9047dad25099fcc8ef.jpg')
#cv2.imshow('qwe',img)
print(img)
# os.path 模块主要用于获取文件的属性。
#
# 以下是 os.path 模块的几种常用方法：
# 方法    说明
# os.path.abspath(path)     返回绝对路径
# os.path.basename(path)     返回文件名
# os.path.commonprefix(list)     返回list(多个路径)中，所有path共有的最长的路径
# os.path.dirname(path)     返回文件路径
# os.path.exists(path)     如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。
# os.path.lexists     路径存在则返回True,路径损坏也返回True
# os.path.expanduser(path)     把path中包含的"~"和"~user"转换成用户目录
# os.path.expandvars(path)     根据环境变量的值替换path中包含的"$name"和"${name}"
# os.path.getatime(path)     返回最近访问时间（浮点型秒数）
# os.path.getmtime(path)     返回最近文件修改时间
# os.path.getctime(path)     返回文件 path 创建时间
# os.path.getsize(path)     返回文件大小，如果文件不存在就返回错误
# os.path.isabs(path)     判断是否为绝对路径
# os.path.isfile(path)     判断路径是否为文件
# os.path.isdir(path)     判断路径是否为目录
# os.path.islink(path)     判断路径是否为链接
# os.path.ismount(path)     判断路径是否为挂载点
# os.path.join(path1[, path2[, ...]])     把目录和文件名合成一个路径
# os.path.normcase(path)     转换path的大小写和斜杠
# os.path.normpath(path)     规范path字符串形式
# os.path.realpath(path)     返回path的真实路径
# os.path.relpath(path[, start])     从start开始计算相对路径
# os.path.samefile(path1, path2)     判断目录或文件是否相同
# os.path.sameopenfile(fp1, fp2)     判断fp1和fp2是否指向同一文件
# os.path.samestat(stat1, stat2)     判断stat tuple stat1和stat2是否指向同一个文件
# os.path.split(path)     把路径分割成 dirname 和 basename，返回一个元组
# os.path.splitdrive(path)     一般用在 windows 下，返回驱动器名和路径组成的元组
# os.path.splitext(path)     分割路径，返回路径名和文件扩展名的元组
# os.path.splitunc(path)     把路径分割为加载点与文件
# os.path.walk(path, visit, arg)     遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数
# os.path.supports_unicode_filenames     设置是否支持unicode路径名