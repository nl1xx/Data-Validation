# 海明校验(任意数据长度)
import random
import numpy as np


# 生成100个数据, 每个数据8个二进制位
data_length = 8
num = 10
data = np.random.randint(0, 2, (num, data_length))
print("Original Data:")
print(data)
print("-------------------")


def r():
    parity_r = 0
    while True:
        if 2 ** parity_r >= parity_r + data_length + 1:
            break
        parity_r += 1
    return parity_r


parity_r = r()


# 计算海明校验码
def calculate_hamming_code(data):
    check_positions = []
    check_positions_binary = []
    total_length = data_length + parity_r
    hamming_data = [0] * total_length
    current_position = 0

    for i in range(parity_r):
        check_positions.append(2 ** i)

    for i in check_positions:
        check_positions_binary.append(format(i, '04b'))

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
        for item in [format(i + 1, '04b') for i in range(total_length)]:
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


hamming_position = []
hamming_datas = [calculate_hamming_code(data) for data in data]
for _, hamming_index in hamming_datas:
    hamming_position = hamming_index
    print("Hamming Position: ", hamming_position)
    break
print("-------------------")

include_hamming_parity_data = []
for hamming_data, _ in hamming_datas:
    hamming_data_num = ''.join(str(bit) for bit in hamming_data)
    include_hamming_parity_data.append(hamming_data_num)

hamming_data_2d = np.array([list(map(int, data)) for data in include_hamming_parity_data])
print("Sent Data:")
print(hamming_data_2d)
print("-------------------")


# 干扰数据
def flip_bit(data, num_flips, hamming_position):
    for _ in range(num_flips):
        # 随机选择一个位置进行翻转, 并且不在校验位位置
        pos = random.randint(0, data_length - 1)
        while (pos + 1) in hamming_position:
            pos = random.randint(0, data_length - 1)
        data[pos] = 1 - data[pos]
    return data


corrupted_data = hamming_data_2d.copy()
for i in range(num):
    num_flips = random.choice([0, 1, 2])  # 随机选择0次, 1次或2次出错
    if num_flips > 0:
        corrupted_data[i, :data_length] = flip_bit(corrupted_data[i, :data_length], num_flips, hamming_position)

print("Received Data:")
print(corrupted_data)
print("-------------------")


# 显示错误
def correct_data(corrupted_data, hamming_position):
    errors = 0
    error_index = []
    hamming_position_binary = []
    for i in hamming_position:
        hamming_position_binary.append(format(i, '04b'))

    for i in range(num):
        index_binary = []
        final_result = []
        for j in range(data_length + parity_r):
            index_binary.append(format(j + 1, '04b'))
        for hamming_index in range(len(hamming_position_binary)):
            array = []
            for index in index_binary:
                if int(index, 2) & int(hamming_position_binary[hamming_index], 2) == int(hamming_position_binary[hamming_index], 2):
                    array.append(index)
            result = corrupted_data[i, int(array[0], 2) - 1]
            for num_index in range(len(array) - 1):
                result ^= corrupted_data[i, int(array[num_index + 1], 2) - 1]
            final_result.append(result)
        for number in final_result:
            if number == 1:
                errors += 1
                error_index.append(i)
                break

    return errors, error_index


error, _ = correct_data(corrupted_data, hamming_position)
print("Error Display")
for i in range(num):
    if i in _:
        print("\033[31m{}\033[0m".format(corrupted_data[i]))
    else:
        print(corrupted_data[i])
print("-------------------")

print("Error Item: ", error)
print("-------------------")
print(f"Accuracy: {((num - error) / num)*100 :.2f}%")
print("-------------------")


# 修改
def fix(corrupted_data, hamming_position):
    hamming_position_binary = []
    for i in hamming_position:
        hamming_position_binary.append(format(i, '04b'))

    new_data = corrupted_data.copy()
    one_mistake_index = []
    no_mistake_index = []
    multi_mistake_index = []

    for i in range(num):
        index_binary = []
        final_result = []
        final_result_reverse = []
        for j in range(data_length + parity_r):
            index_binary.append(format(j + 1, '04b'))

        for hamming_index in range(len(hamming_position_binary)):
            array = []
            for index in index_binary:
                if int(index, 2) & int(hamming_position_binary[hamming_index], 2) == int(
                        hamming_position_binary[hamming_index], 2):
                    array.append(index)

            result = corrupted_data[i][int(array[0], 2) - 1]
            for num_index in range(len(array) - 1):
                result ^= corrupted_data[i, int(array[num_index + 1], 2) - 1]
            final_result.append(result)

            final_result_reverse = final_result[::-1]

        error_position = int(''.join(map(str, final_result_reverse)), 2)
        if error_position != 0:
            new_data[i][error_position - 1] = 1 - new_data[i][error_position - 1]
            if np.array_equal(new_data[i], hamming_data_2d[i]):
                one_mistake_index.append(i)
            else:
                # new_data[i][error_position - 1] = (new_data[i][error_position - 1] + 1) % 2
                multi_mistake_index.append(i)
        else:
            no_mistake_index.append(i)

    return new_data, one_mistake_index, no_mistake_index, multi_mistake_index


print("Fixed Data:")
fixed_data, one_mistake, no_mistake, multi_mistake = fix(corrupted_data, hamming_position)
for i in range(num):
    if i in one_mistake:
        print("1 mistake\033[32m{}\033[0m".format(fixed_data[i]))
    elif i in no_mistake:
        print("No mistake\033[34m{}\033[0m".format(corrupted_data[i]))
    elif i in multi_mistake:
        print("2 mistakes\033[33m{}\033[0m".format(corrupted_data[i]))
