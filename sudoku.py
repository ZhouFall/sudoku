#coding=utf-8
import datetime
from collections import Counter    #查找重复数据
import numpy as np

class solution(object):
    def __init__(self,board):
        self.b = board    #数独数据
        self.t = 0    #尝试次数

    def check_repeat(self,data):    #检查输入的9个数是否有重复
        c = dict(Counter(data))
        # print(c)
        for key, v in c.items():
            if key == 0:
                pass
            else:
                if v != 1:
                    # print('有重复数据')
                    return False
        return True

    def check_row(self):    #检查所有行是否有重复数据
        for row in range(0,9):
            result = self.check_repeat(self.b[row])
            if result == False:
                return result
        return True

    def check_column(self):    #检查所有列是否有重复数据
        list = np.array(self.b)
        for column in range(0, 9):
            result = self.check_repeat(list.T[column])
            if result == False:
                return result
        return True

    def check_square(self):    #检查所有九宫格是否有重复数据
        square = []
        for i in range(0,9):
            row, col = int(i / 3) * 3, int(i % 3) * 3
            square.append(self.b[row][col:col+3]+self.b[row+1][col:col+3]+self.b[row+2][col:col+3])
            # print(square[i])
            result = self.check_repeat(square[i])
            if result == False:
                return result
        return True

    def check_board(self):    #检查输入的数独是否有输入错误
        result = self.check_row() and self.check_column() and self.check_square()
        return result

    def cal_count(self,x,y):
        count = 9
        value = [1,2,3,4,5,6,7,8,9]
        row = self.b[x]   #一行数据
        column = list(np.array(self.b).T[y])   #一列数据
        x, y = int(x / 3) * 3, int(y / 3) * 3
        square = self.b[x][y:y + 3] + self.b[x + 1][y:y + 3] + self.b[x + 2][y:y + 3]
        data = list(set(row+column+square))
        data.remove(0)
        count = count-len(data)
        for i in range(len(data)):
            value.remove(data[i])
        return count,value

    def cal_count_all(self):
        count = []
        value = []
        # index = 0
        for i in range(0, 9):
            for j in range(0, 9):    #遍历整个数独，每个位置检查横向纵向九宫格
                # index = index+1
                if self.b[i][j] != 0:
                    value.append(self.b[i][j])
                    count.append(10)    #题目中填好的数字
                else:
                    tmp_count,temp_value = self.cal_count(i,j)
                    # 增加一个打断，如果检测到一个格子里只有1种或者2种解法，后面的就不用计算了
                    # if (tmp_count == 1):
                    #     print(tmp_count, index, temp_value)
                    #     return tmp_count, index, temp_value
                    count.append(tmp_count)
                    value.append(temp_value)
        #遍历完之后，每个格子都有3种或者以上的填法
        # print(count)
        min = np.min(count)
        index = int(np.argmin(count))
        # print(min,index)
        return min,index,value[index]

    def try_it(self,min,index,value):#主循环
        self.t += 1
        if min == 10:
            print('数独破解完成，一种可能的结果如下:')
            for i in self.b:
                print(i)
            # print(self.b)
            return True  # 返回True
        else:
            x, y = int(index / 9), int(index % 9)
            for i in value:    #从筛选过后的值填入
                self.b[x][y]=i    #将符合条件的填入0格
                next_min,next_index,next_value= self.cal_count_all() #找出下一个可填数字最少的格子
                end=self.try_it(next_min,next_index,next_value)
                if not end:   #在递归过程中存在不符合条件的，即 使try_it函数返回False的项
                    self.b[x][y] = 0    #回朔到上一层继续
                #不添加以下两句的话，数组得出一个方案之后不会结束，会继续测试value里面的其他值，可以用于求解多解法的数独，加上之后，只会打印一种方案
                else:
                    return True
            return False    #屏幕上填满数字，最后一次try还是失败了，返回false
    def start(self):
        begin = datetime.datetime.now()
        min,index,value = self.cal_count_all()    #找出当前可填数字最少的格子
        self.try_it(min, index,value)
        end = datetime.datetime.now()
        print('\ncost time:', end - begin)
        print('times:',self.t)

if __name__ =="__main__":
    #原始数独，使用列表来表示
    board = [
        [0,0,0,8,0,0,0,0,0],
        [0,3,0,0,9,2,0,0,1],
        [0,9,0,0,0,0,0,0,0],
        [7,0,0,0,0,0,8,0,0],
        [0,0,5,7,0,0,9,0,0],
        [2,0,0,0,0,0,0,0,0],
        [0,0,3,5,2,0,1,0,0],
        [0,5,0,0,0,0,4,0,2],
        [0,0,6,0,0,4,0,0,0],
        ]
    sudoku = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]

    s = solution(sudoku)
    if s.check_board() == False:
        print('输入的数独有重复数据，请检查输入数据')
    else:
        print('开始破解数独数据')
        s.start()
