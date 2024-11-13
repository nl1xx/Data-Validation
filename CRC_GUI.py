import tkinter as tk
import random
import numpy as np

num = 3
data = np.random.randint(0, 2, (num, 8))


def crc_generator(data, poly):
    num_zeros = len(poly) - 1
    padded_data = np.pad(data, ((0, 0), (0, num_zeros)), mode='constant')
    # 计算CRC
    for i in range(len(padded_data)):
        current_data = padded_data[i]
        while True:
            index_of_first_one = np.argmax(current_data)
            if index_of_first_one >= len(current_data) - num_zeros:
                break
            current_data[index_of_first_one:index_of_first_one + len(poly)] ^= poly
        # 更新padded_data
        padded_data[i] = current_data
    crc_check = padded_data[:, -num_zeros:]
    crc_data = np.concatenate((data, crc_check), axis=1)
    return crc_data


def disturb(data):
    # 模拟数据传输中的干扰
    corrupted_data = data.copy()
    for i in range(num):
        for j in range(8):
            if random.random() < 0.05:  # 5%的概率干扰一个位
                corrupted_data[i, j] = 1 - corrupted_data[i, j]
    return corrupted_data


def crc_check(received_data, poly):
    error_index = []
    errors = 0
    for i in range(received_data.shape[0]):
        current_data = received_data[i].copy()
        while True:
            if 1 not in current_data:
                break
            index_of_first_one = np.argmax(current_data == 1)
            # 如果第一个1的位置在数据尾部的CRC校验码之外，则停止
            if index_of_first_one >= len(current_data) - len(poly) + 1:
                break
            current_data[index_of_first_one:index_of_first_one + len(poly)] ^= poly
        remainder = current_data[-len(poly) + 1:]
        if not np.all(remainder == 0):
            errors += 1
            error_index.append(i)
    return errors, error_index


# 生成多项式
poly = np.array([1, 0, 1, 1], dtype=np.uint8)

crc_data = crc_generator(data, poly)

disturbed_data = disturb(crc_data)

error_item, _ = crc_check(disturbed_data, poly)

root = tk.Tk()
root.title("CRC")

root.geometry("800x600")

scrollbar_y = tk.Scrollbar(root)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(root, yscrollcommand=scrollbar_y.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y.config(command=canvas.yview)

left_frame = tk.Frame(canvas, bg="lightblue")
right_frame = tk.Frame(canvas)


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.create_window((0, 0), window=left_frame, anchor='nw', tags="left_frame")
canvas.create_window((400, 0), window=right_frame, anchor='nw', tags="right_frame")

# 绑定<Configure>事件以更新滚动区域
left_frame.bind("<Configure>", on_frame_configure)
right_frame.bind("<Configure>", on_frame_configure)


poly_str = ''.join(map(str, poly))
tk.Label(left_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
tk.Label(right_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()

for i in range(num):
    tk.Label(left_frame, text=''.join(map(str, crc_data[i])), bg="lightblue").pack()

for i in range(num):
    if i in _:
        color = "red"
    else:
        color = "white"
    tk.Label(right_frame, text=''.join(map(str, disturbed_data[i])), bg=color).pack()

root.mainloop()
