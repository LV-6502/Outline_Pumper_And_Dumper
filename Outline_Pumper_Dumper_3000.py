import tkinter as tk
from tkinter import filedialog, Entry, messagebox
from PIL import ImageTk, Image, ImageEnhance
import os
import sys
import numpy as np
from tkinter import colorchooser

import tkinter as tk
from tkinter import filedialog, Entry, messagebox
from PIL import ImageTk, Image



def openfile0(xnum,ynum):
    global filename0
    filename0 = filedialog.askdirectory(parent=window,title="Layer 0")
    #print(filename0)
    if filename0:
        b0_l = tk.Label(window, text = "☑")
        b0_l.place(x=xnum,y=ynum)

def Run():
    try:
        directory = "Outlined/"
        parent_dir = filename0
        path = os.path.join(parent_dir, directory)
        os.makedirs(path, exist_ok=True)
        item_number = 0
        for _input_image in os.listdir(filename0):
            if _input_image.endswith('.png'):
                item_number+=1
                input_image = Image.open(filename0+'/'+_input_image)
                input_image.convert('RGBA')
                _original = input_image
                converter = ImageEnhance.Brightness(input_image)
                input_image_blk = converter.enhance(0)
                input_image_blk.convert('RGBA')
                image_data = np.array(input_image_blk)
                r1,g1,b1 = 0,0,0
                r2,g2,b2 = rgb_code
                red, green, blue = image_data[:,:,0], image_data[:,:,1], image_data[:,:,2]
                mask = (red == r1) & (green == g1) & (blue == b1)
                image_data[:,:,:3][mask] = [r2, g2, b2]
                offset_image = Image.fromarray(image_data)
                x,y = offset_image.size
                base_layer = Image.new('RGBA', (x, y), (255, 0, 0, 0))
                coords = (0,0)
                Lcoords = (-1,0)
                Rcoords = (1,0)
                Dcoords = (0,1)
                Ucoords = (0,-1)
                base_layer.paste(offset_image, Lcoords,offset_image.convert('RGBA'))
                base_layer.paste(offset_image, Rcoords,offset_image.convert('RGBA'))
                base_layer.paste(offset_image, Dcoords,offset_image.convert('RGBA'))
                base_layer.paste(offset_image, Ucoords,offset_image.convert('RGBA'))
                base_layer.paste(input_image, coords,input_image.convert('RGBA'))
                _input_image = _input_image[:-4]
                base_layer.save(path+_input_image+"_outlined.png")
        tk.messagebox.showinfo(title="COMPLETE", message=(str(item_number)+" PNG objects completed"))
    except NameError:
        tk.messagebox.showerror(title = "You goofed up", message = "Pick a color & target folder")

def choose_color(xnum,ynum):
    global rgb_code
    rgb_code,_hex = colorchooser.askcolor(title ="Choose color")
    if rgb_code:
        b0_l = tk.Label(window, text = "☑")
        b0_l.place(x=xnum,y=ynum)

window = tk.Tk()
window.geometry("325x160")
window.title("V1.0 - Saving Throw Studios")
heading = tk.Label(text = "Outline Pumper & Dumper 3000", bg="grey", fg="white", width="500",height="3")
heading.pack()

tk.Button(window, text='1. Select Folder', command= lambda: openfile0(130,62),bg="#971414",fg="white", width="15",height="1",anchor='w').place(x=10,y=60)
tk.Button(window, text='2. Pick a Color', command= lambda: choose_color(130,90),bg="#971414",fg="white", width="15",height="1",anchor='w').place(x=10,y=90)
tk.Button(window, text='3. Pump & Dump', command=Run, bg="green", fg="white", width="15",height="1",anchor='w').place(x=10,y=120)

window.mainloop()
