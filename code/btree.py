import numpy as np


class Node():
    def __init__(self, s):
        self.s = s
        self.v = -1.0
        self.delta = -1.0
        self.up = None
        self.down = None
        return super().__init__()


class Btree_model():
    def __init__(self, asset=3310.24 , priod=8, sig=0.215228, r=[0.09, 0.13, 0.1532, 0.1468, 0.1586, 0.1792, 0.2008, 0.2214], f_rate = [0.17, 0.1767, 0.1814, 0.19, 0.2005, 0.2111, 0.2214, 0], delta_t=0.25):
        self.asset=asset
        self.priod_num=priod
        self.sig=sig
        self.r=r
        self.f_rate=f_rate
        self.delta_t=delta_t

        self.u = np.exp(self.sig * np.sqrt(self.delta_t))
        self.d = np.exp(-self.sig * np.sqrt(self.delta_t))
        self.p = [(np.exp(i * self.delta_t) - self.d)/(self.u - self.d) for i in r]
        self.q = [1 - self.p[i] for i in range(self.priod_num)]
        print(self.u)
        print(self.d)
        print(self.p)
        print(self.q)

        self.root = Node(self.asset)
        self.node_num = 1

        for i in range(1, 2**(priod+1)):
            pre = self.root
            stack = []
            if i == 1:
                continue
            
            n = i
            while n >=2 :
                stack.append(n%2)
                n = int(n/2)

            while len(stack) > 1:
                way = stack.pop()
                if way:
                    pre = pre.up
                else:
                    pre = pre.down

            if stack.pop():
                pre.up = Node(pre.s * self.u)
            else:
                pre.down = Node(pre.s * self.d)

            self.node_num += 1
            

        # stack에 넣고 하나씩 빼서 이동

        return super().__init__()

    
    def print_tree(self):
        f = open("btree_delta.csv", 'w')
        for i in range(self.priod_num+1):
            print_list = self.print_line(i)
            term = 2**(9-i)-1
            print_set = ""
            for j, values in enumerate(print_list):
                if j == 0:
                    print_set = print_set + ',' * int(term/2)
                else:
                    print_set = print_set + ',' * term
                print_set = print_set + str(values[2]) + ','
            print_set += '\n'
            f.write(print_set)
        f.close()


    def print_line(self, deep):
        if deep == 0:
            return [[self.root.s, self.root.v, self.root.delta]]

        line_num = []

        for i in range(2**deep):
            num = str(bin(i))[2:]
            
            pre = self.root

            if len(num) < len(str(bin(2**deep-1))[2:]):
                for i in range(len(str(bin(2**deep-1))[2:]) - len(num)):
                    pre = pre.down
            for j in num:
                if int(j) == 0:
                    pre = pre.down
                else:
                    pre = pre.up
            line_num.append([pre.s, pre.v, pre.delta])
        return line_num


    def cal_last_value(self):
        final_level = self.priod_num
        for i in range(2**final_level):
            way = str(bin(i)[2:])
            if len(way) < final_level:
                way = '0'*(final_level - len(way)) + way

            pre = self.root
            value = 0
            for level, choice in enumerate(way):
                if choice == '0':
                    pre = pre.down
                else:
                    pre = pre.up
                
                if pre.s > self.asset * 1.02:
                    value += 1.5 * np.exp(self.f_rate[level]*(0.25*(final_level-level-1)))
                elif pre.s > self.asset:
                    value += 1 * np.exp(self.f_rate[level]*(0.25*(final_level-level-1)))
            pre.v = 100 + value
            pre.delta = 0.0


    def cal_value(self, node, level):
        if not node.up and not node.down:
            return

        self.cal_value(node.down, level+1)
        self.cal_value(node.up, level+1)

        node.v = (self.p[level] * node.up.v + self.q[level] * node.down.v) / (np.exp(self.r[level] * self.delta_t))
        node.delta = (node.up.v - node.down.v) / (node.up.s - node.down.s)
                    
                
my_t = Btree_model()
my_t.cal_last_value()
my_t.cal_value(my_t.root, 0)
my_t.print_tree()