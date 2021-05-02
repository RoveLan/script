# -- coding: utf-8 --
import glob
import random
import xml.etree.ElementTree as ET
import operator
import numpy as np


def cas_iou(box, cluster):
    x = np.minimum(cluster[:, 0], box[0])
    y = np.minimum(cluster[:, 1], box[1])

    intersection = x * y
    area1 = box[0] * box[1]

    area2 = cluster[:, 0] * cluster[:, 1]
    iou = intersection / (area1 + area2 - intersection)

    return iou


def avg_iou(box, cluster):
    return np.mean([np.max(cas_iou(box[i], cluster)) for i in range(box.shape[0])])


def kmeans(box, k):
    # 取出一共有多少框
    row = box.shape[0]

    # 每个框各个点的位置
    distance = np.empty((row, k))

    # 最后的聚类位置
    last_clu = np.zeros((row,))

    np.random.seed()

    # 随机选5个当聚类中心
    cluster = box[np.random.choice(row, k, replace=False)]
    # cluster = random.sample(row, k)
    while True:
        # 计算每一行距离五个点的iou情况。
        for i in range(row):
            distance[i] = 1 - cas_iou(box[i], cluster)

        # 取出最小点
        near = np.argmin(distance, axis=1)

        if (last_clu == near).all():
            break

        # 求每一个类的中位点
        for j in range(k):
            cluster[j] = np.median(
                box[near == j], axis=0)

        last_clu = near

    return cluster


def load_data(path):
    data = []
    # 对于每一个xml都寻找box
    for xml_file in glob.glob('{}/*xml'.format(path)):
        tree = ET.parse(xml_file)
        height = int(tree.findtext('./size/height'))
        width = int(tree.findtext('./size/width'))
        if height <= 0 or width <= 0:
            continue

        # 对于每一个目标都获得它的宽高
        for obj in tree.iter('object'):
            xmin = int(float(obj.findtext('bndbox/xmin'))) / width
            ymin = int(float(obj.findtext('bndbox/ymin'))) / height
            xmax = int(float(obj.findtext('bndbox/xmax'))) / width
            ymax = int(float(obj.findtext('bndbox/ymax'))) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)
            # 得到宽高
            data.append([xmax - xmin, ymax - ymin])
    return np.array(data)


# if __name__ == '__main__':
#     # 运行该程序会计算'./VOCdevkit/VOC2007/Annotations'的xml
#     # 会生成yolo_anchors.txt
#     SIZE = 640
#     anchors_num = 9
#     # 载入数据集，可以使用VOC的xml
#     path ='E:\\data\\toc\\toc_xml'   #"/home/ubuntu/Z/XYZ/DET/z-yolov3-cfg-linux/data/Annotations"
#
#     # 载入所有的xml
#     # 存储格式为转化为比例后的width,height
#     data = load_data(path)
#
#     # 使用k聚类算法
#     out = kmeans(data, anchors_num)
#     out = out[np.argsort(out[:, 0])]
#     print('acc:{:.2f}%'.format(avg_iou(data, out) * 100))
#     print(out * SIZE)
#     data = out * SIZE
#     f = open("yolo_anchors.txt", 'w')
#     row = np.shape(data)[0]
#     for i in range(row):
#         if i == 0:
#             x_y = "%d,%d" % (data[i][0], data[i][1])
#         else:
#             x_y = ", %d,%d" % (data[i][0], data[i][1])
#         f.write(x_y)
#     f.close()
def ratio():
    anchor = open('E://PycharmProjects//yolov5-pytorch//yolo_anchors.txt')  # 原始anchors
    expand_anchor = open('E://PycharmProjects//yolov5-pytorch//ratio_anchors.txt', 'w')  # 变换后的anchor保存地址
    ratio = 0.5  # 最小的锚框缩小倍数
    base_ratio = 3  # 最大的锚框扩大倍数
    box = anchor.read().split(',')
    box = np.array(box)
    for i in range(0, len(box)):
        box[i] = float(box[i].strip())
    box = box.reshape((len(box) // 2, 2))
    new_box = np.zeros((len(box), 2))
    length = len(box)
    new_box[0, 0] = int(float(box[0, 0]) * ratio)
    new_box[0, 1] = int(float(box[0, 1]) * ratio)
    new_box[-1, 0] = int(float(box[-1, 0]) * base_ratio)
    new_box[-1, 1] = int(float(box[-1, 1]) * base_ratio)
    print(box)
    for i in range(1, length - 1):
        new_box[i, 0] = (float(box[i, 0]) - float(box[0, 0])) / (float(box[-1, 0]) - float(box[0, 0])) * (
                    new_box[-1, 0] - new_box[0, 0]) + new_box[0, 0]
        new_box[i, 1] = new_box[i, 0] * float(box[i, 1]) / float(box[i, 0])
        new_box[i, 0] = int(new_box[i, 0])
        new_box[i, 1] = int(new_box[i, 1])

    for i in range(length):
        if i == 0:
            x_y = "%d,%d" % (new_box[i][0], new_box[i][1])
        else:
            x_y = ",  %d,%d" % (new_box[i][0], new_box[i][1])
        expand_anchor.write(x_y)
    expand_anchor.close()
    anchor.close()
    print(new_box)

def anchors(path, size, num, times):

    # 载入所有的xml
    # 存储格式为转化为比例后的width,height
    data = load_data(path)
    out, acc =0, 0
    # 使用k聚类算法
    for i in range(times):
        print(i)
        if i > 0:
            t = kmeans(data, num)
            t = t[np.argsort(t[:, 0])]
            acc1 = 'acc:{:.2f}%'.format(avg_iou(data, t) * 100)
            print('l:', t_acc, avg_iou(data, t))
            print(t_acc > avg_iou(data, t))
            if t_acc > avg_iou(data, t):
                continue
            else:
                print('else')
                out = t
                acc = acc1
        else:
            out = kmeans(data, num)
            out = out[np.argsort(out[:, 0])]
            acc = 'acc:{:.2f}%'.format(avg_iou(data, out) * 100)
        print('ll:', acc)
        t_acc = avg_iou(data, out)

    print('last:', acc)
    print(out * size)
    data = out * size

    f = open("yolo_anchors.txt", 'w')
    row = np.shape(data)[0]
    for i in range(row):
        if i == 0:
            x_y = "%d,%d" % (data[i][0], data[i][1])
        else:
            x_y = ", %d,%d" % (data[i][0], data[i][1])
        f.write(x_y)
    f.close()#acc:85.73 32,56, 46,80, 58,120, 67,149, 83,159, 85,237, 110,206, 140,230, 220,372
#anchors('E:\\data\\toc\\toc_xml', 640, 9, 10)
ratio();

