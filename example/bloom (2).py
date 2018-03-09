#coding:utf-8
#auther :duhaipeng
#web:www.duhaipeng.com

from bitarray import bitarray
import mmh3

class BloomFilter():
    
    #初始化布隆过滤器
    def __init__(self, size, hash_count):      
        self.bit_array = bitarray(size)
        #所有位初始化为0
        self.bit_array.setall(0)
        self.size = size
        self.hash_count = hash_count

    #用于添加元素
    def add(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1
        return self
    
    #python3有的__contains__方法，用于使用in方法
    def __contains__(self, item):
        out = True
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                out = False

        return out


def main():
    #布隆过滤器实例化，12个比特位，3个hash计算
    bloom = BloomFilter(12,3)

    #初始化数组num_1
    num_1 = ['1', '2', '3', '4', '5', '6', '7','8','9','10']

    #将num_1添加到布隆过滤器
    for i in num_1:
        bloom.add(i)

    #初始化数组num_2（用于测试）
    num_2 = ['11', '12', '13', '14', '15']

    #检测布隆过滤器的误报
    for i in num_2:
        if i in bloom:
            print('{} 此处是误报\n'.format(i))
        else:
            print('{} 不在过滤器\n'.format(i))
    print ("*"*15)

if __name__ == '__main__':
    print ("*"*15)
    main()
    
