# 统计每个词在其类别下的包含的文档数
# 保存格式：类别__wdcount.txt 内容：词：出现的文档数
import os
import pretreat.utils as utils

def save_wdcount(path, word_document):
    with open(path, 'wb') as f:
        for key, value in word_document.items():
            line = key + ':' + str(value) + '\n'
            f.write(line.encode())

def wdcount(input_dir, save_dir):
    # 计算文档数
    for label in os.listdir(input_dir):
        label_dir = os.path.join(input_dir, label)
        print(label)
        word_document = {}
        for file in os.listdir(label_dir):
            content = utils.read_file(os.path.join(label_dir, file)).decode('utf-8')
            content_set = set(content.split()) # 只需要知道词是否在这篇文档中出现过
            save_file = os.path.join(save_dir, label + '_wdcount.txt')
            for word in content_set:
                word_document[word] = word_document.get(word, 0) + 1
                print(word, "+1")
        save_wdcount(save_file, word_document)
        print ('>>>' * 25)
        print ('Writing in the file named %s \n' % save_file)


def main():
    print('start')
    input_path = r'D:\Code\Python\datamining\data\train\train_seg'
    save_path = r'D:\Code\Python\datamining\data\train\wdcount'
    wdcount(input_path, save_path)

if __name__ == '__main__':
    main()