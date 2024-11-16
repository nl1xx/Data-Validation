import numpy as np
import torch
import random
import tkinter as tk
from tkinter import simpledialog

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
    for i in range(len(padded_data)):
        current_data = padded_data[i]
        while True:
            ones = (current_data == 1)
            if not ones.any():
                break
            index_of_first_one = ones.nonzero(as_tuple=True)[0]
            if index_of_first_one[0] >= len(current_data) - num_zeros:
                break
            current_data[index_of_first_one[0]:index_of_first_one[0] + len(poly)] ^= poly
        padded_data[i] = current_data
    crc_check = padded_data[:, -num_zeros:]
    crc_data = torch.cat((data, crc_check), dim=1)
    return crc_data

def disturb(data):
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
            if index_of_first_one[0] >= len(current_data) - len(poly) + 1:
                break
            current_data[index_of_first_one[0]:index_of_first_one[0] + len(poly)] ^= poly
        remainder = current_data[-len(poly) + 1:]
        remainder_list.append(remainder)
        if not torch.all(remainder == 0):
            errors += 1
            error_index.append(i)
    return errors, error_index, remainder_list


def update_polynomial():
    new_poly_str = simpledialog.askstring("Input", "Enter the new polynomial (e.g., 1011):", parent=root)
    if new_poly_str:
        new_poly = np.array([int(bit) for bit in new_poly_str], dtype=np.uint8)
        global poly_tensor
        poly_tensor = torch.tensor(new_poly, dtype=torch.uint8).to(device)
        crc_data = crc_generator(data_tensor, poly_tensor)
        disturbed_data = disturb(crc_data)
        error_item, _, remainder = crc_check(disturbed_data, poly_tensor)
        update_gui(crc_data, disturbed_data, remainder, error_item)


def update_gui(crc_data, disturbed_data, remainder, error_item):
    for widget in left_frame0.winfo_children():
        widget.destroy()
    for widget in left_frame1.winfo_children():
        widget.destroy()
    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()
    for widget in right_frame0.winfo_children():
        widget.destroy()

    poly_str = ''.join(map(str, poly_tensor.cpu().numpy()))
    tk.Label(left_frame0, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
    tk.Label(left_frame1, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
    tk.Label(left_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
    tk.Label(right_frame, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
    tk.Label(right_frame0, text=f'Generator Polynomial: {poly_str}', bg="lightblue").pack()
    tk.Label(left_frame0, text="Original Data", bg="lightblue").pack()
    tk.Label(left_frame1, text="CRC", bg="lightblue").pack()
    tk.Label(left_frame, text="Add Parity/Sent Data", bg="lightblue").pack()
    tk.Label(right_frame, text="Received Data", bg="lightblue").pack()
    tk.Label(right_frame0, text='Remainder', bg="lightblue").pack()

    crc_length = len(poly_tensor) - 1  # CRC校验位的长度
    for i in range(num):
        data_str = ''.join(map(str, data[i].tolist()))
        crc_str = ''.join(map(str, crc_data[i, -crc_length:].tolist()))  # 根据多项式长度获取CRC校验位
        tk.Label(left_frame0, text=data_str, bg="lightblue").pack()
        tk.Label(left_frame1, text=crc_str, bg="lightblue").pack()

    for i in range(num):
        crc_data_str = ''.join(map(str, crc_data[i].tolist()))
        tk.Label(left_frame, text=crc_data_str, bg="lightblue").pack()

    for i in range(num):
        disturbed_data_str = ''.join(map(str, disturbed_data[i].tolist()))
        tk.Label(right_frame, text=disturbed_data_str, bg="lightgreen").pack()

    for i in range(len(remainder)):
        if torch.all(remainder[i] == 0):
            color = "white"
        else:
            color = "red"
        remainder_str = ''.join(map(str, remainder[i].tolist()))
        tk.Label(right_frame0, text=remainder_str, bg=color).pack()


root = tk.Tk()
root.title("CRC")
root.geometry("1200x600")

scrollbar_y = tk.Scrollbar(root)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(root, yscrollcommand=scrollbar_y.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y.config(command=canvas.yview)

left_frame0 = tk.Frame(canvas, bg="lightblue")
left_frame1 = tk.Frame(canvas, bg="lightblue")
left_frame = tk.Frame(canvas, bg="lightblue")
right_frame = tk.Frame(canvas, bg="lightgreen")
right_frame0 = tk.Frame(canvas, bg="lightgreen")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.create_window((0, 0), window=left_frame0, anchor='nw', tags="left_frame")
canvas.create_window((200, 0), window=left_frame1, anchor='nw', tags="left_frame")
canvas.create_window((400, 0), window=left_frame, anchor='nw', tags="left_frame")
canvas.create_window((600, 0), window=right_frame, anchor='nw', tags="right_frame")
canvas.create_window((800, 0), window=right_frame0, anchor='nw', tags="right_frame")

left_frame0.bind("<Configure>", on_frame_configure)
left_frame1.bind("<Configure>", on_frame_configure)
left_frame.bind("<Configure>", on_frame_configure)
right_frame.bind("<Configure>", on_frame_configure)
right_frame0.bind("<Configure>", on_frame_configure)

top_frame = tk.Frame(root, bg="lightgrey")
top_frame.pack(side=tk.TOP, fill=tk.X)

tk.Button(top_frame, text="Update Polynomial", command=update_polynomial).pack(side=tk.LEFT, padx=5, pady=5)

crc_data = crc_generator(data_tensor, poly_tensor)
disturbed_data = disturb(crc_data)
error_item, _, remainder = crc_check(disturbed_data, poly_tensor)
update_gui(crc_data, disturbed_data, remainder, error_item)

root.mainloop()
