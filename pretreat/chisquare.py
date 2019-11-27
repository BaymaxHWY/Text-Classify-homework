# 卡方检测
# 只对训练集进行卡方检测
# 对于特征：x和类别：y的卡方值的计算
# A:包含x并且属于y的文档个数，B：包含x且不属于y的文档个数，C：不包含x且属于y的文档个数，D：不包含x且不属于y的文档个数
# 公式CHI=(AD-BC)^2/(A+B)(C+D)

# A：y_wdcount中x的值；
# B：除开y以外的label_wdcount中x的值；
# C：y_wdcount中除开x的其余词的值之和 = y_wdcount的文章数 - A；
# D：除开y以外的label_wdcount中除开x的其余词的值之和 = 除开y以外的label_wdcount中的文章数 - B
# 所以只需要知道每个类别中的文章数和计算A、B就可以得到C、D
# 对于每个y计算CHI，并按CHI从大到小排序x保存至文件(每一类一个文件)
# 读取文件选择前1w个词
import os
import pretreat.utils as utils
from operator import itemgetter

def save_chi(path, word_chi):
    with open(path, 'wb') as f:
        for (key, value) in word_chi:
            line = key + ':' + str(value) + '\n'
            f.write(line.encode())

# 获得每个类别下的文章总数
def get_count_document(data_dir):
    label_list = os.listdir(data_dir)
    document_count = dict()
    for label in label_list:
        document_count[label] = len(os.listdir(os.path.join(data_dir, label)))
    return document_count

# 把wdcount文件夹转变为二维dict形式
def get_wdcount(wd_dir):
    wdcount = dict()
    for file in os.listdir(wd_dir):
        wdcount[os.path.splitext(file)[0]] = dict() # key: label_wdcount
        content = utils.read_file(os.path.join(wd_dir, file)).decode('utf-8')
        content = content.split()
        for item in content:
            item = item.split(':')
            wdcount[os.path.splitext(file)[0]][item[0]] = item[1]
    return wdcount

def calculate_chi(document_count, wdcount, save_path, label_list):
    word_count = dict() # 每个词在整个数据集中出现的文档数
    for label in label_list:
        wdindex1 = label + '_wdcount'
        for (k, v) in wdcount[wdindex1].items():
            # k:词，v:在该类别下出现的文章数
            word_count[k] = word_count.get(k, 0) + int(v)

    word_chi = {}
    for label in label_list:
        wdindex1 = label + '_wdcount'
        for (k, v) in wdcount[wdindex1].items():
            # k:词，v:在该类别下出现的文章数
            v = int(v)
            do_count_nothis = 0
            for l in label_list:
                if l is not label:
                    do_count_nothis += document_count[l]
            A = v
            B = word_count[k] - v
            C = document_count[label] - A
            D = do_count_nothis - B
            word_chi[k] = ((A*D-B*C)**2)/((A+B)*(C+D))
            print("k:%s, chi:" % k, word_chi[k])
        # 保持卡方检测结果
        save_chi(os.path.join(save_path, label + '_chi_order.txt'), sorted(word_chi.items(), key=itemgetter(1), reverse=True))
        N = 10000
        print("从%s类中选取前%d", (label, N))
        chi_order = utils.read_file(os.path.join(save_path, label + '_chi_order.txt')).decode('utf-8').split('\n')
        wirte_content = '\n'.join([item.split(':')[0] for item in chi_order[0:N]])
        utils.write_file(os.path.join(save_path, label + '_chi_order_select.txt'), wirte_content.encode())

def main():
    train_data = r'D:\Code\Python\datamining\data\train\train_seg'
    input_data = r'D:\Code\Python\datamining\data\train\wdcount'
    save_order_path = r'D:\Code\Python\datamining\data\train\train_chi_order'

    if not os.path.exists(save_order_path):
        os.makedirs(save_order_path)

    label_list = os.listdir(train_data)

    document_count = get_count_document(train_data) # document_count['体育'] = 1234
    print('>>>'*25)
    print('获得每个类别下的文章总数')
    print(document_count)
    wdcount = get_wdcount(input_data)
    print('>>>' * 25)
    print('读取wdcount')
    calculate_chi(document_count, wdcount, save_order_path, label_list)
    print('CHI_run is finished!')

if __name__ == '__main__':
    main()