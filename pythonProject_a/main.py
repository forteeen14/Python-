
import os
import tkinter as tk
from random import random
from tkinter import messagebox
from pillow import Image, ImageTk
class Card:
    def __init__(self, master, image_path, x, y):
        self.master = master
        self.image_path = image_path
        self.is_flipped = False
        self.button = tk.Button(master, command=lambda: self.flip())
        self.button.place(x=x, y=y)
        self.image = None
        self.set_image('back.jpg')  # 假设初始都是背面图片，名为back.jpg

    def set_image(self, path):
        img = Image.open(path)
        img = img.resize((80, 100), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.button.config(image=self.image)

    def flip(self):
        if not self.is_flipped:
            img = Image.open(self.image_path)
            img = img.resize((80, 100), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(img)
            self.button.config(image=self.image)
            self.is_flipped = True
class MemoryCardGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('记忆翻牌游戏')
        self.card_paths = []
        self.cards = []
        self.selected_cards = []
        self.round_count = 0
        self.load_images()
        self.create_cards()

    def load_images(self):
        image_folder = "E:\card"
        image_files = os.listdir(image_folder)
        for i in range(0, len(image_files), 2):
            self.card_paths.append(os.path.join(image_folder, image_files[i]))
            self.card_paths.append(os.path.join(image_folder, image_files[i]))
        random.shuffle(self.card_paths)

    def create_cards(self):
        x_start = 10
        y_start = 10
        x_offset = 90
        y_offset = 110
        index = 0
        for i in range(4):
            for j in range(4):
                card = Card(self.root, self.card_paths[index], x_start + j * x_offset, y_start + i * y_offset)
                self.cards.append(card)
                index += 1

    def flip_card(self, card):
        if len(self.selected_cards) < 2:
            card.flip()
            self.selected_cards.append(card)
            if len(self.selected_cards) == 2:
                self.round_count += 1
                if self.selected_cards[0].image_path == self.selected_cards[1].image_path:
                    # 匹配成功
                    pass
                else:
                    # 不匹配，延迟翻回
                    self.root.after(1000, self.flip_back)

    def flip_back(self):
        for card in self.selected_cards:
            card.set_image('back.jpg')
            card.is_flipped = False
        self.selected_cards = []

    def check_game_over(self):
        all_flipped = True
        for card in self.cards:
            if not card.is_flipped:
                all_flipped = False
                break
        if all_flipped:
            messagebox.showinfo('游戏结束', f'你用了{self.round_count}轮完成游戏。')
            self.root.destroy()
def main():
    game = MemoryCardGame()
    for card in game.cards:
        card.button.config(command=lambda c=card: game.flip_card(c))
    game.root.mainloop()
if __name__ == '__main__':
    main()
