import tkinter as tk
import random
import numpy as np


# 计算校验位数量
def r(data_length):
    parity_r = 0
    while True:
        if 2 ** parity_r >= parity_r + data_length + 1:
            break
        parity_r += 1
    return parity_r


# 计算Hamming校验码
def calculate_hamming_code(data, data_length, parity_r):
    check_positions = []
    check_positions_binary = []
    total_length = data_length + parity_r
    hamming_data = [0] * total_length
    current_position = 0

    for i in range(parity_r):
        check_positions.append(2 ** i)

    for i in check_positions:
        check_positions_binary.append(format(i, '08b'))

    data_index = 0
    for i in range(1, total_length + 1):
        if i not in check_positions:
            hamming_data[i - 1] = data[data_index]
            data_index += 1

    for k in check_positions_binary:
        first_index_one_binary = 0
        for first_one in range(len(k)):
            if k[first_one] == '1':
                first_index_one_binary = first_one
                break
        same_one_position = []
        for item in [format(i + 1, '08b') for i in range(total_length)]:
            if item != k:
                for data_index in range(len(item)):
                    if item[data_index] == '1' and data_index == first_index_one_binary:
                        same_one_position.append(int(item, 2))
        all_data = hamming_data[same_one_position[0] - 1]
        for i in range(len(same_one_position) - 1):
            all_data ^= hamming_data[same_one_position[i + 1] - 1]
        hamming_data[check_positions[current_position] - 1] = all_data
        current_position += 1
    return hamming_data, check_positions


# 生成数据并计算Hamming校验
def generate_data():
    global data, hamming_data_2d, corrupted_data, hamming_position, parity_r, data_length, num, total_length

    # 获取用户输入的数据长度
    data_length = int(entry_data_length.get())
    parity_r = r(data_length)
    total_length = data_length + parity_r

    # 生成原始数据和Hamming校验码
    data = np.random.randint(0, 2, (num, data_length))
    hamming_datas = [calculate_hamming_code(d, data_length, parity_r) for d in data]
    hamming_data_2d = np.array([h for h, _ in hamming_datas])
    hamming_position = hamming_datas[0][1]

    # 生成干扰数据
    corrupted_data = hamming_data_2d.copy()
    for i in range(num):
        num_flips = random.choice([0, 1, 2])
        if num_flips > 0:
            corrupted_data[i, :data_length] = flip_bit(corrupted_data[i, :data_length], num_flips, hamming_position)

    update_gui()


# 更新GUI
def update_gui():
    # 清空所有 Frame
    for widget in left_frame1.winfo_children():
        widget.destroy()
    for widget in left_frame2.winfo_children():
        widget.destroy()
    for widget in left_frame3.winfo_children():
        widget.destroy()
    for widget in right_frame1.winfo_children():
        widget.destroy()
    for widget in right_frame2.winfo_children():
        widget.destroy()
    for widget in right_frame3.winfo_children():
        widget.destroy()

    hamming_str = ''.join(map(str, hamming_position))
    tk.Label(left_frame1, text=f'Hamming position: {hamming_str}', bg="lightblue").pack()
    tk.Label(left_frame2, text=f'Hamming position: {hamming_str}', bg="lightblue").pack()
    tk.Label(left_frame3, text=f'Hamming Code', bg="lightblue").pack()
    tk.Label(right_frame1, text=f'Received Data', bg="lightblue").pack()
    tk.Label(right_frame2, text=f'Fixed Data', bg="lightblue").pack()
    tk.Label(right_frame3, text=f'Detail', bg="lightblue").pack()

    # 显示原始数据和Hamming校验码
    for i in range(num):
        tk.Label(left_frame1, text=''.join(map(str, data[i])), bg="lightblue").pack()
        tk.Label(left_frame2, text=''.join(map(str, hamming_data_2d[i])), bg="lightgreen").pack()
        hamming_code_str = ''.join(str(hamming_data_2d[i][pos - 1]) for pos in hamming_position)
        tk.Label(left_frame3, text=hamming_code_str, bg="lightyellow").pack()

    # 显示收到的数据和修正后的数据
    error, error_index = correct_data(corrupted_data, hamming_position)
    fixed_data, one_mistake, no_mistake, multi_mistake = fix(corrupted_data, hamming_position)

    for i in range(num):
        color = "red" if i in error_index else "white"
        tk.Label(right_frame1, text=''.join(map(str, corrupted_data[i])), bg=color).pack()

        if i in one_mistake:
            color = "green"
            # 获取错一位的位置
            error_position = detect_error(corrupted_data[i], hamming_position)
            error_position_str = f"一位错: {error_position}"
        elif i in no_mistake:
            color = "white"
            error_position_str = "正确"
        else:
            color = "yellow"
            error_position_str = "多位错"

        tk.Label(right_frame2, text=''.join(map(str, fixed_data[i])), bg=color).pack()
        tk.Label(right_frame3, text=error_position_str, bg="lightcyan").pack()


# 翻转位
def flip_bit(data, num_flips, hamming_position):
    for _ in range(num_flips):
        pos = random.randint(0, data_length - 1)
        while (pos + 1) in hamming_position:
            pos = random.randint(0, data_length - 1)
        data[pos] = 1 - data[pos]
    return data


# 校验数据
def correct_data(corrupted_data, hamming_position):
    errors = 0
    error_index = []
    for i in range(num):
        error_position = detect_error(corrupted_data[i], hamming_position)
        if error_position != 0:
            errors += 1
            error_index.append(i)
    return errors, error_index


# 检测错误位置
def detect_error(data, hamming_position):
    final_result = []
    for pos in hamming_position:
        parity = 0
        for i in range(len(data)):
            if (i + 1) & pos:
                parity ^= data[i]
        final_result.append(parity)
    return int(''.join(map(str, final_result[::-1])), 2)


# 修正错误
def fix(corrupted_data, hamming_position):
    fixed_data = corrupted_data.copy()
    one_mistake_index, no_mistake_index, multi_mistake_index = [], [], []

    for i in range(num):
        error_position = detect_error(corrupted_data[i], hamming_position)
        if 1 <= error_position <= total_length:
            fixed_data[i][error_position - 1] ^= 1
            if np.array_equal(fixed_data[i], hamming_data_2d[i]):
                one_mistake_index.append(i)
            else:
                multi_mistake_index.append(i)
        else:
            no_mistake_index.append(i)

    return fixed_data, one_mistake_index, no_mistake_index, multi_mistake_index


# 创建 GUI 界面
root = tk.Tk()
root.title("Hamming Parity")
root.geometry("800x600")

num = 100
entry_data_length = tk.Entry(root)
entry_data_length.pack()
tk.Button(root, text="Generate Data", command=generate_data).pack()

left_frame1 = tk.Frame(root, bg="lightblue")
left_frame2 = tk.Frame(root, bg="lightgreen")
left_frame3 = tk.Frame(root, bg="lightyellow")
right_frame1 = tk.Frame(root, bg="lightblue")
right_frame2 = tk.Frame(root, bg="lightgreen")
right_frame3 = tk.Frame(root, bg="lightcyan")

left_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
left_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
left_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.mainloop()
