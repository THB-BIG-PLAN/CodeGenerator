# -*- coding: gbk -*-

from PIL import Image
import easygui as eg
import os

pth = eg.fileopenbox(title='���Ҫת����ͼƬ')  # ��ͼƬ
dir = os.path.dirname(pth)  # ����ͼƬ���ڵ�·��
name = os.path.basename(pth)  # ����ͼƬ���Ƽ���չ��
name = os.path.splitext(name)[0]  # ����ͼƬ����
out_name = os.path.join(dir, name + '.txt')  # ��������ּ�·��
img = Image.open(pth)
out_img = img.convert('L')  # ͼƬת��Ϊ�Ҷ�ģʽ
w, h = out_img.size  # ����ͼƬ��С
n = 600 / max(w, h)  #ͼ����С��������ȻͼƬת�����ܴ�
if n < 1:
    out_img = out_img.resize((int(w * n), int(h * n * 0.5)))  # ���ַ��Ŀ��һ�����2���ĸ߶�
else:
    out_img = out_img.resize((int(w), int(h)))
w, h = out_img.size
#asciis='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^\ '
asciis = "@%#*+=-:. "  # �Ҷȱ�
texts = ''
for row in range(h):
    for col in range(w):
        gray = out_img.getpixel((col, row))
        texts += asciis[int(gray / 255 * (len(asciis) - 1))]  # ���ݻҶ�ֵѡ��ͬ���Ӷȵ� ASCII �ַ�
    texts += '\n'
with open(out_name, "w") as file:
    file.write(texts)
    file.close()
