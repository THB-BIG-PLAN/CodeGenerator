import pandas as pd
import re
import warnings


class Node:
    def __init__(self, period, TimeOutFlag=False):
        self.period = period  # 节点存储的数据
        self.next = None  # 指向下一个节点，初始为 None


class LinkedList:
    def __init__(self):
        self.head = None  # 链表的头节点，初始为 None

        def append(self, data):
            new_node = Node(data)  # 创建一个新节点
            if not self.head:  # 如果链表为空
                self.head = new_node  # 将新节点设为头节点
                return
            last = self.head  # 从头节点开始遍历
            while last.next:  # 找到链表的最后一个节点
                last = last.next
            last.next = new_node  # 将新节点添加到末尾

        def delete(self, node):
            if node == self.head:
                self.head = node.next
                node.next = None
                return
            prev = self.head
            while prev.next!= node:
                prev = prev.next
            prev.next = node.next
            node = None

        def check(self):
            current = self.head
            while current != None:
                current.period -= 1
                if current.period == 0:
                    current.TimeOutFlag = True
                    self.delete(current)
                current = current.next


