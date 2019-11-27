# 对原始数据进行分词处理
import os
import re
import jieba.posseg as pseg

# 写入文件
def write_file(savepath, content):
    with open(savepath, 'wb') as f:
        f.write(content)

# 读取文件，以二进制的方式读取可以设置编码方式
def read_file(path):
    with open(path, 'rb') as f:
        content = f.read()
    return content

# 获取停用词列表
def get_stop_list(stoppath):
    global stop_content
    if os.path.exists(stoppath):
        stop_content = read_file(stoppath).decode('gb18030') # 这里不能使用utf-8编码会导致部分字符无法解析
    else:
        print("this stop filepath is not exists:", stoppath)
        exit(1)
    stop_content = stop_content.replace('\n', ' ')
    stop_words = stop_content.split(' ')
    return stop_words

# 返回文件夹下的所有文件path
def get_dir_file(input_dir):
    if not os.path.exists(input_dir):
        print("this input dir is not exists:", input_dir)
        exit(1)
    #file_list = []
    for label in os.listdir(input_dir):
        label_dir = os.path.join(input_dir, label)
        for file in os.listdir(label_dir):
            if os.path.splitext(file)[-1] == r'.txt':
                # file_list.append(os.path.join(label_dir, file))
                yield os.path.join(label_dir, file) # 使用生成器让运行更流畅
    #yield file_list

# 预处理
def segement(file, stop_list):
    # 1.读文件
    content = read_file(file).decode('utf-8')
    # 2.删除换行、空行、多余空格
    content = ''.join(content.split())
    # 3.过滤掉非名词、非中文、停用词、单个中文词
    # 取出所有中文字符
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    content = re.sub(pattern, '', content)
    words = pseg.cut(content)
    word_list = []
    for word, flag in words:
        if flag == 'n': # 名词
            if len(word) > 1: # 非单字符
                if word not in stop_list:
                    word_list.append(word)
    file_split = file.split(os.sep)
    file_name = os.path.join(file_split[-2], file_split[-1])
    # 4.返回保留文件名(label\文件名.txt)和内容（byte形式，要对str类型进行encode）
    return file_name, ' '.join(word_list).encode()




# path=os.path.join(dirpath,filepath) 拼接路径，无论windows还是linux
# r''可无视转义字符
def main():
    input_dir = r'D:\Code\Python\datamining\THUCNews'
    output_dir = r'D:\Code\Python\datamining\data\fenci_out'
    stop_file_path = r'D:\Code\Python\datamining\stop_words_ch.txt'

    stop_list = get_stop_list(stop_file_path)
    file_list = get_dir_file(input_dir)
    # 预处理
    for file in file_list:
        save_file, content = segement(file, stop_list)
        save_path = os.path.join(output_dir, save_file)
        save_dir = os.path.split(save_path)[0]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        write_file(save_path, content)
        print("process:", file, "success!")
        print('save:', save_path, 'success!')
        print(save_file, 'content:\n', content.decode('utf-8'))
    print('分词结束')

if __name__ == '__main__':
    # 这里定义的变量可以作为全局变量使用
    main()