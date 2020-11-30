# 字符转二进制 Python版
if __name__ == '__main__':
    str = "lWoHvYe"
    print('_'.join(format(ord(x), 'b') for x in str))
