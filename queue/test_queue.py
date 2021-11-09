#coding=utf-8

from queue import Queue #先进先出队列
from queue import PriorityQueue#优先级队列
import time
#队列：先进先出
q = Queue()#创建一个空队列，队列大小没有指定
#判断队列是是否为空
#当一个队列为空的时候如果再用get取则会堵塞，所以取队列的时候一般是用到
#get_nowait()方法，这种方法在向一个空队列取值的时候会抛一个Empty异常
#所以更常用的方法是先判断一个队列是否为空，如果不为空则取值
 
 
print(q.empty())
#队列的操作：存--put()  取--get()
q.put('page1')
q.put('page2')
q.put('page3')
 
print(q.empty())
#判断队列是否已经满了
print(q.full())
 
q1 = Queue(3)#在创建队列时，指定队列大小（表示该队列最多能存多少个元素）
q1.put('1')
q1.put('1')
q1.put('1')
print(q1.full())
