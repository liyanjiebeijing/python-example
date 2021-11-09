from queue import PriorityQueue

q = PriorityQueue()

q.put(4)
q.put(2)
q.put(5)
q.put(1)
q.put(3)

print(list(q))
print(q.qsize())

while not q.empty():    
    next_item = q.get()
    # print(f'queue length = {q.qsize()}')
    print(next_item)


