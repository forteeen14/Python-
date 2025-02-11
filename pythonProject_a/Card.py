import os
import tkinter as tk
from random import shuffle
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from tkinter import ttk  # 导入ttk用于美化控件


class Card:
    def __init__(self, master, image_path, x, y):
        self.master = master
        self.image_path = image_path
        self.is_flipped = False
        self.button = tk.Button(master, command=lambda: self.flip(),borderwidth=3, relief="ridge")  # 添加3D边框样式
        self.button.place(x=x, y=y)
        self.image = None
        self.set_image(r'back.jpg')

    def set_image(self, path):
        try:
            img = Image.open(path)
            img = img.resize((90, 110))  # 统一调整图片尺寸
            img = ImageTk.PhotoImage(img)
            self.image = img
            self.button.config(image=self.image)
        except Exception as e:
            print(f"加载图片 {path} 时出错: {e}")

    def flip(self):
        if not self.is_flipped:
            try:
                img = Image.open(self.image_path)
                img = img.resize((90, 110))  # 统一调整图片尺寸
                img = ImageTk.PhotoImage(img)
                self.image = img
                self.button.config(image=self.image)
                self.is_flipped = True
            except Exception as e:
                print(f"加载图片 {self.image_path} 时出错: {e}")