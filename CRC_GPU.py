import numpy as np
import torch
import random
import tkinter as tk


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

num = 100
data = np.random.randint(0, 2, (num, 8))
poly = np.array([1, 0, 1, 1], dtype=np.uint8)

# np -> tensor
data_tensor = torch.tensor(data, dtype=torch.uint8).to(device)
poly_tensor = torch.tensor(poly, dtype=torch.uint8).to(device)


def crc_generator(data, poly):
    num_zeros = len(poly) - 1
    padded_data = torch.nn.functional.pad(data, (0, num_zeros), 'constant')
    # 计算CRC
    for i in range(len(padded_data)):
        current_data = padded_data[i]
        while True:
            ones = (current_data == 1)
            if not ones.any():
                break
            index_of_first_one = ones.nonzero(as_tuple=True)[0]
            if index_of_first_one[0] >= len(current_data) - num_zeros:
                break
            # 使用poly_tensor进行异或操作
            current_data[index_of_first_one[0]:index_of_first_one[0] + len(poly)] ^= poly_tensor
        # 更新padded_data
        padded_data[i] = current_data
    crc_check = padded_data[:, -num_zeros:]
    crc_data = torch.cat((data, crc_check), dim=1)
    return crc_data


def disturb(data):
    # 模拟数据传输中的干扰
    corrupted_data = data.clone()
    for i in range(num):
        for j in range(8):
            if random.random() < 0.05:  # 5%的概率干扰一个位
                corrupted_data[i, j] = 1 - corrupted_data[i, j]
    return corrupted_data


def crc_check(received_data, poly):
    error_index = []
    errors = 0
    remainder_list = []
    for i in range(received_data.shape[0]):
        current_data = received_data[i].clone()
        while True:
            if 1 not in current_data:
                break
            index_of_first_one = (current_data == 1).nonzero(as_tuple=True)[0]
            # 如果第一个1的位置在数据尾部的CRC校验码之外，则停止
            if index_of_first_one[0] >= len(current_data) - len(poly) + 1:
                break
            current_data[index_of_first_one[0]:index_of_first_one[0] + len(poly)] ^= poly_tensor
        remainder = current_data[-len(poly) + 1:]
        remainder_list.append(remainder)
        if not torch.all(remainder == 0):
            errors += 1
            error_index.append(i)
    return errors, error_index, remainder_list

crc_data = crc_generator(data_tensor, poly_tensor)

disturbed_data = disturb(crc_data)

error_item, _, remainder = crc_check(disturbed_data, poly_tensor)

root = tk.Tk()
root.title("CRC")

root.geometry("800x600")

scrollbar_y = tk.Scrollbar(root)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(root, yscrollcommand=scrollbar_y.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y.config(command=canvas.yview)

left_frame0 = tk.Frame(canvas, bg="lightblue")
left_frame = tk.Frame(canvas, bg="lightblue")
right_frame = tk.Frame(canvas, bg="lightgreen")
right_frame0 = tk.Frame(canvas, bg="lightgreen")


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.create_window((0, 0), window=left_frame0, anchor='nw', tags="left_frame")
canvas.create_window((200, 0), window=left_frame, anchor='nw', tags="left_frame")
canvas.create_window((400, 0), window=right_frame, anchor='nw', tags="right_frame")
canvas.create_window((600, 0), window=right_frame0, anchor='nw', tags="right_frame")

left_frame0.bind("<Configure>", on_frame_configure)
left_frame.bind("<Configure>", on_frame_configure)
right_frame.bind("<Configure>", on_frame_configure)
right_frame0.bind("<Configure>", on_frame_configure)

poly_str = ''.join(map(str, poly))
tk.Label(left_frame0, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
tk.Label(left_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
tk.Label(right_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
tk.Label(right_frame0, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
tk.Label(left_frame0, text="Original Data", bg="lightblue").pack()
tk.Label(left_frame, text="Add Parity/Sent Data", bg="lightblue").pack()
tk.Label(right_frame, text="Received Data", bg="lightblue").pack()
tk.Label(right_frame0, text='Remainder', bg="lightblue").pack()

# tensor -> list
for i in range(num):
    tk.Label(left_frame0, text=''.join(map(str, data[i].tolist())), bg="lightblue").pack()

for i in range(num):
    tk.Label(left_frame, text=''.join(map(str, crc_data[i].tolist())), bg="lightblue").pack()

for i in range(num):
    if i in _:
        color = "red"
        tk.Label(right_frame, text=''.join(map(str, disturbed_data[i].tolist())), bg=color).pack()
    else:
        tk.Label(right_frame, text=''.join(map(str, disturbed_data[i].tolist()))).pack()

for i in range(len(remainder)):
    if torch.all(remainder[i] == 0):
        color = "white"
    else:
        color = "red"
    tk.Label(right_frame0, text=''.join(map(str, remainder[i].tolist())), bg=color).pack()

root.mainloop()
