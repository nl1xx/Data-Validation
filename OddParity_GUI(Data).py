import tkinter as tk
import numpy as np
import random

# 生成100个数据, 每个数据8个二进制位
data = np.random.randint(0, 2, (100, 8))

# 计算监督码 (奇校验)
def parity_check(data):
    return (np.sum(data, axis=1) + 1) % 2

parity = parity_check(data)

# 模拟数据传输中的干扰
corrupted_data = data.copy()
for i in range(100):
    for j in range(8):
        if random.random() < 0.05:  # 5%的概率干扰一个位
            corrupted_data[i, j] = 1 - corrupted_data[i, j]

# 判断哪些数据接收有误, 哪些数据虽然验证无误但实际有误, 统计传输正确率
error_index = []
false_positives_index = []

def calculate_error_rates(original, received):
    errors = 0
    false_positives = 0
    received_parity = []
    for i in range(100):
        received_parity.append((np.sum(received[i]) + parity[i]) % 2)
        if (np.sum(received[i]) + parity[i]) % 2 != 1:
            errors += 1
            error_index.append(i)
        else:
            if int(''.join(map(str, original[i])), 2) != int(''.join(map(str, received[i])), 2):
                false_positives += 1
                false_positives_index.append(i)
    return errors, false_positives, received_parity

parity_errors, parity_false_positives, received_parity = calculate_error_rates(data, corrupted_data)

root = tk.Tk()
root.title("OddParity")

root.geometry("1000x600")

scrollbar_y = tk.Scrollbar(root)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(root, yscrollcommand=scrollbar_y.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y.config(command=canvas.yview)

left_frame = tk.Frame(canvas, bg="lightblue")
middle_frame = tk.Frame(canvas, bg="lightblue")
right_frame = tk.Frame(canvas, bg="lightgreen")
right_frame0 = tk.Frame(canvas, bg="lightgreen")
right_frame1 = tk.Frame(canvas, bg="lightgreen")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


canvas.create_window((0, 0), window=left_frame, anchor='nw', tags="left_frame")
canvas.create_window((200, 0), window=middle_frame, anchor='nw', tags="middle_frame")
canvas.create_window((400, 0), window=right_frame, anchor='nw', tags="right_frame")
canvas.create_window((600, 0), window=right_frame0, anchor='nw', tags="right_frame")
canvas.create_window((800, 0), window=right_frame1, anchor='nw', tags="right_frame")

# 绑定<Configure>事件以更新滚动区域
left_frame.bind("<Configure>", on_frame_configure)
middle_frame.bind("<Configure>", on_frame_configure)
right_frame.bind("<Configure>", on_frame_configure)
right_frame0.bind("<Configure>", on_frame_configure)
right_frame1.bind("<Configure>", on_frame_configure)

tk.Label(left_frame, text="Sent Data", bg="lightblue").pack()
tk.Label(middle_frame, text="Parity", bg="lightblue").pack()
tk.Label(right_frame, text="Received Data to Judge", bg="lightblue").pack()
tk.Label(right_frame0, text="New Parity", bg="lightblue").pack()
tk.Label(right_frame1, text="Right or Wrong", bg="lightblue").pack()

for i in range(100):
    tk.Label(left_frame, text=''.join(map(str, data[i])), bg="lightblue").pack()

for i in range(100):
    tk.Label(middle_frame, text=str(parity[i]), bg="lightblue").pack()

for i in range(100):
    if i in error_index:
        # 校验出错
        color = "red"
        tk.Label(right_frame1, text='校验错误', bg=color).pack()
    elif i in false_positives_index:
        # 校验无误但数据不对
        color = "green"
        tk.Label(right_frame1, text='校验正确数据错误', bg=color).pack()
    else:
        # 没有错误
        color = "white"
        tk.Label(right_frame1, text='正确', bg=color).pack()
    tk.Label(right_frame, text=''.join(map(str, corrupted_data[i])), bg=color).pack()

for i in range(100):
    if received_parity[i] == 1:
        color = "green"
        tk.Label(right_frame0, text=str(received_parity[i]), bg=color).pack()
    else:
        color = "red"
        tk.Label(right_frame0, text=str(received_parity[i]), bg=color).pack()

root.mainloop()
