# # #!/usr/bin/env python3


#Import the required Libraries
from tkinter import *
from PIL import Image, ImageTk
import time
import os
import threading
import random

win_width = 960
win_height = 720
play_interval = 2
Path = 'image' 
move_max = 200  

def getfiles():
    files = os.listdir(Path)
    for x in files:
        if not (x.endswith('.jpg') or x.endswith('.JPG') or x.endswith('.png')):
            files.remove(x)
    return files


canvas_width = win_width
canvas_height = win_height
def create_canvas():
    win = Tk()
    win.geometry("%dx%d" % (win_width, win_height))
    canvas= Canvas(win, width = canvas_width, height = canvas_height)
    canvas.pack()
    return win, canvas

g_files = getfiles()
g_files.sort()
g_win, g_canvas = create_canvas()
g_index = 0
def image_change():
    try:
        global g_index
        img_path = '%s/%s' % (Path, g_files[g_index])
        img_in = Image.open(img_path)
        w, h = img_in.size
        img_ratio = w * 1.0 / h
        canvas_ratio = canvas_width * 1.0 / canvas_height
        if canvas_ratio > img_ratio:
            new_h = canvas_height
            new_w = int(1.0 * canvas_height * w / h)
            left = int((canvas_width - new_w) / 2)
            top = 0            
        else:
            new_w = canvas_width
            new_h = int(1.0 * canvas_width * h / w)
            left = 0
            top = int((canvas_height - new_h) / 2)
            
                            
        img_out = img_in.resize((new_w, new_h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_out)
       
        #shaking for 2 seconds
        canvas_img = g_canvas.create_image(left, top, anchor=NW, image = img)

        start = time.time()
        while time.time() - start < 2.0:
            move_top = random.randint(-move_max, move_max)
            move_left = random.randint(-move_max, move_max)                        
            g_canvas.move(canvas_img, move_left, move_top)
            time.sleep(0.1)
            g_canvas.move(canvas_img, -move_left, -move_top)
            time.sleep(0.1)
        
        time.sleep(play_interval)
        g_canvas.delete(canvas_img)

        g_index += 1
        if g_index < len(g_files):             
            t = threading.Thread(target=image_change)  
            t.start()
        else:
            g_canvas.create_text(win_width / 2 - 80, win_height / 2 - 10, 
                text="Finish testing", font=("Purisa", 48))


    except Exception as e:
        print("Exception: %s " % e)
        sys.exit(1)


t = threading.Thread(target=image_change)  
t.start()  


g_win.mainloop()
