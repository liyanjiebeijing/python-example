import os
import shutil

def test_os_walk():    
    os.makedirs('root')
    os.makedirs('root/first')
    os.makedirs('root/second')
    with open('root/first/hello.txt' , 'w') as f:
        f.write("hello test\n")

    with open('root/first/world.txt' , 'w') as f:
        f.write("world test\n")

    with open('root/second/hello.txt' , 'w') as f:
        f.write("hello test\n")

    with open('root/second/world.txt' , 'w') as f:
        f.write("world test\n")

    with open('root/tree.txt' , 'w') as f:
        f.write("tree test\n")

    for dirpath, dirnames, filenames  in os.walk('root'):
        print(f'dirpath: {dirpath}, dirnames: {dirnames}, filenames: {filenames}')

    shutil.rmtree('root')


if __name__ == '__main__':
    test_os_walk()
