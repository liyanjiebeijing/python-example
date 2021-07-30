import os
import hashlib
import shutil
import sys

def rename(file_dir):
    '''
    rename all the files in file_dir by their md5 values
    '''
    for name in os.listdir(file_dir):
        suffix = name.split('.')[-1]
        src_path = os.path.join(file_dir, name)
        with open(src_path, 'rb') as f:
            new_name = hashlib.md5(f.read()).hexdigest()
        dst_path = os.path.join(file_dir, new_name + '.' + suffix)
        shutil.move(src_path, dst_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('%s: usage <file_dir>' % (sys.argv[0]))
        sys.exit(0)

    rename(sys.argv[1])