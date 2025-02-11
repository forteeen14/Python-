import os
import tkinter as tk
from random import shuffle
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from tkinter import ttk  # 导入ttk用于美化控件

from Card import Card

#图片尺寸
def resize_image(input_path, output_path, width, height):
    try:
        image = Image.open(input_path)
        resized_image = image.resize((width, height))

        resized_image.save(output_path)
        print(f"图片 {input_path} 已成功调整为 {width}x{height} 像素，并保存到 {output_path}")
    except Exception as e:
        print(f"处理图片 {input_path} 时出错: {e}")


class MemoryCardGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('390x520')
        self.root.configure(bg='#E0FFFF')  # 设置背景颜色为淡青色
        self.root.title('记忆翻牌游戏')

        # 添加游戏信息面板
        self.info_frame = tk.Frame(self.root, bg='#E0FFFF')
        self.info_frame.place(x=10, y=430, width=370, height=80)

        # 添加计时器
        self.time_label = tk.Label(self.info_frame, text="时间: 0秒",bg='#87CEEB', fg='white', font=('Arial', 12))
        self.time_label.pack(side=tk.LEFT, padx=10)

        # 得分显示
        self.score_label = tk.Label(self.info_frame, text="得分: 0",bg='#32CD32', fg='white', font=('Arial', 12))
        self.score_label.pack(side=tk.LEFT, padx=10)

        # 重新开始按钮
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=5)
        self.restart_btn = ttk.Button(self.info_frame, text="重新开始",command=self.restart_game, style='TButton')
        self.restart_btn.pack(side=tk.RIGHT, padx=10)

        # 初始化游戏变量
        self.start_time = time.time()
        self.score = 0
        self.timer_running = True
        self.update_timer()  #开始计时
        self.card_paths = []
        self.cards = []
        self.selected_cards = []
        self.round_count = 0
        self.load_images()
        self.create_cards()

    def load_images(self):
        image_folder = r"card"
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]
        for i in range(0, len(image_files)):
            self.card_paths.append(os.path.join(image_folder, image_files[i]))
            self.card_paths.append(os.path.join(image_folder, image_files[i]))  # 重复添加两次相同的文件路径（保证一一配对）
        shuffle(self.card_paths)  # 打乱卡片路径列表

        '''if len(image_files) < 8:
            messagebox.showerror("错误", "图片数量不足，至少需要 8 张图片。")
            self.root.destroy()
            return

        # 确保图片数量是偶数
        if len(image_files) % 2 != 0:
            image_files = image_files[:-1]  # 去掉最后一张图片，确保数量是偶数

        for image_file in image_files:
            card_path = os.path.join(image_folder, image_file)
            resized_path = os.path.join(image_folder, f"resized_{image_file}")
            resize_image(card_path, resized_path, 100, 150)  # 调整图片尺寸
            self.card_paths.append(resized_path)
            self.card_paths.append(resized_path)  # 每张图片添加两次，确保配对

        shuffle(self.card_paths)  # 打乱顺序'''

    def create_cards(self):
        x_start = 10
        y_start = 10
        x_offset = 90
        y_offset = 110
        index = 0
        for i in range(4):
            for j in range(4):
                index1 = index % len(self.card_paths)
                card = Card(self.root, self.card_paths[index1], x_start + j * x_offset, y_start + i * y_offset)
                #self.card_paths[index]
                self.cards.append(card)
                index += 1

    def flip_card(self, card):
        if len(self.selected_cards) < 2:
            card.flip()
            card.is_flipped=True
            self.selected_cards.append(card)
            if len(self.selected_cards) == 2:
                self.round_count += 1
                if self.selected_cards[0].image_path == self.selected_cards[1].image_path:
                    # 匹配成功
                    #for selected_card in self.selected_cards:
                     #   selected_card.is
                    self.update_score(10)  # 匹配成功加10分
                    self.selected_cards = []
                    self.check_game_over()
                else:
                    # 不匹配，延迟翻回
                    self.root.after(1000, self.flip_back)
                    card.is_flipped = False

    def flip_back(self):
        back_path = r'back.jpg'
        resized_back_path = r'photo\resized_back.jpg'
        resize_image(back_path, resized_back_path, 90, 110)  # 调整背面图片尺寸
        for card in self.selected_cards:
            card.set_image(resized_back_path)
            card.is_flipped = False
        self.selected_cards = []

    def check_game_over(self):
        all_flipped = True
        for card in self.cards:
            if not card.is_flipped:
                all_flipped = False
                break
        if all_flipped:
            self.timer_running = False
            elapsed = int(time.time() - self.start_time)
            messagebox.showinfo('游戏结束',f'你用了{self.round_count}轮完成游戏。\n用时: {elapsed}秒\n得分: {self.score}')
            self.root.destroy()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"时间: {elapsed}秒")
            self.root.after(1000, self.update_timer)  # 每秒更新一次

    def update_score(self, points):
        self.score += points
        self.score_label.config(text=f"得分: {self.score}")

    def restart_game(self):
        self.timer_running = False
        self.root.destroy()
        main()  # 重新开始游戏


def main():
    game = MemoryCardGame()
    for card in game.cards:
        card.button.config(command=lambda c=card: game.flip_card(c))
    game.root.mainloop()

if __name__ == '__main__':
    main()