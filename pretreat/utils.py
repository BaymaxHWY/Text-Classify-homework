# 读取文件，以二进制的方式读取可以设置编码方式
def read_file(path):
    with open(path, 'rb') as f:
        content = f.read()
    return content

# 写入文件
def write_file(savepath, content):
    with open(savepath, 'wb') as f:
        f.write(content)