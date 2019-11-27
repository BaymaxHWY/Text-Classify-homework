# 为了后续生成词向量空间模型的方便，这些分词后的文本信息还要转换成文本向量信息并对象化，利用了Scikit-Learn库的Bunch数据结构

import os
from sklearn.datasets.base import Bunch
import pickle
import pretreat.utils as utils

#Bunch 类提供了一种key，value的对象形式
#target_name 所有分类集的名称列表
#label 每个文件的分类标签列表
#filenames 文件路径
#contents 分词后文件词向量形式

def file2bunch(input_dir, outpuy_path):
    label_list = os.listdir(input_dir)
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(label_list)
    for label in label_list:
        label_dir = os.path.join(input_dir, label)
        for file in os.listdir(label_dir):
            filepath = os.path.join(label_dir, file)
            bunch.label.append(label)
            bunch.filenames.append(filepath)
            bunch.contents.append(utils.read_file(filepath))
            print("bunch append:", filepath)
    with open(outpuy_path, 'wb') as f:
        pickle.dump(bunch, f)

    print('构建文本对象结束！！！')


def main():
    train_bunch_path = r'D:\Code\Python\datamining\data\train\train_word_bag\train_set.dat'
    train_data_path = r'D:\Code\Python\datamining\data\train\train_seg'
    file2bunch(train_data_path, train_bunch_path)

    test_bunch_path = r'D:\Code\Python\datamining\data\test\test_word_bag\test_set.dat'
    test_data_path = r'D:\Code\Python\datamining\data\test\test_seg'
    file2bunch(test_data_path, test_bunch_path)

if __name__ == '__main__':
    main()