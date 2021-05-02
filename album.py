# -- coding: utf-8 --
import random

import cv2
from matplotlib import pyplot as plt

import albumentations as A

BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)  # White


def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    # x_min, y_min, w, h = bbox
    # x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    x_min, y_min, x_max, y_max = bbox
    x_min, y_min, x_max, y_max = int(x_min),int(y_min),int(x_max),int(y_max)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35,
        color=TEXT_COLOR,
        lineType=cv2.LINE_AA,
    )
    return img


def visualize(image, bboxes, category_ids, category_id_to_name):
    img = image.copy()
    for bbox, category_id in zip(bboxes, category_ids):
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name)
    # plt.figure(figsize=(12, 12))
    # plt.axis('off')
    # plt.imshow(img)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyWindow('test')


image = cv2.imread('E:\\data\\toc\\toc\\2021_4_23_5.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
"""
<xmin>146</xmin><ymin>116</ymin><xmax>221</xmax><ymax>210</ymax>
<xmin>371</xmin><ymin>105</ymin><xmax>449</xmax><ymax>193</ymax>
<xmin>89</xmin><ymin>205</ymin><xmax>176</xmax><ymax>315</ymax>
<xmin>449</xmin><ymin>208</ymin><xmax>537</xmax><ymax>299</ymax>

"""
bboxes = [[146, 116, 221, 210],
          [371, 105, 449, 193],
          [89, 205, 176, 315],
          [449, 208, 537, 299]]
category_ids = [0, 1, 1, 0]
category_id_to_name = {0: 'mask', 1: 'nomask'}
visualize(image, bboxes, category_ids, category_id_to_name)
transform = A.Compose(
    [A.HorizontalFlip(p=0.5),
     A.ShiftScaleRotate(p=0.3)],
    bbox_params=A.BboxParams(format='pascal_voc', label_fields=['category_ids']),
)

transformed = transform(image=image, bboxes=bboxes, category_ids=category_ids)
visualize(
    transformed['image'],
    transformed['bboxes'],
    transformed['category_ids'],
    category_id_to_name,
)
print(bboxes,transformed['bboxes'])