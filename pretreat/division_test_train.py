# 将数据按比例额划分为训练集、测试集
import os
import random

# 写入文件
def write_file(savepath, content):
    with open(savepath, 'wb') as f:
        f.write(content)

# 读取文件，以二进制的方式读取可以设置编码方式
def read_file(path):
    with open(path, 'rb') as f:
        content = f.read()
    return content

def main():
    origin_data = r'D:\Code\Python\datamining\data\fenci_out'
    train_data = r'D:\Code\Python\datamining\data\train\train_seg'
    test_data = r'D:\Code\Python\datamining\data\test\test_seg'

    train_rate = 0.5
    test_rate = 1 - train_rate

    label_list = os.listdir(origin_data)
    for label in label_list:
        label_dir = os.path.join(origin_data, label)
        txt_list = os.listdir(label_dir)
        # 把这一类中的文件路径分别分成两份，打乱排序
        random.shuffle(txt_list)
        train_list = txt_list[0:int(train_rate*len(txt_list))]
        test_list = txt_list[int(test_rate*len(txt_list)):]
        print('train_list:', train_list)
        print('test_list:', test_list)
        train_label_dir = os.path.join(train_data, label)
        test_label_dir = os.path.join(test_data, label)
        if not os.path.exists(train_label_dir):
            os.makedirs(train_label_dir)
        if not os.path.exists(test_label_dir):
            os.makedirs(test_label_dir)
        #训练集
        for filename in train_list:
            data = read_file(os.path.join(label_dir, filename))
            filepath = os.path.join(train_label_dir, filename)
            write_file(filepath, data)
            print("train存储：", filepath)
        #测试集
        for filename in test_list:
            data = read_file(os.path.join(label_dir, filename))
            filepath = os.path.join(test_label_dir, filename)
            write_file(filepath, data)
            print("test存储：", filepath)
    print("划分完成")

if __name__ == '__main__':
    # 这里定义的变量可以作为全局变量使用
    main()