# CRC
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
    remainder_list = []
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
        remainder_list.append(remainder)
        if not np.all(remainder == 0):
            errors += 1
            error_index.append(i)
    return errors, error_index, remainder_list


print("Generated Data:")
print(data)
print("-------------------")

# 生成多项式
poly = np.array([1, 0, 1, 1], dtype=np.uint8)

crc_data = crc_generator(data, poly)
print("CRC Checks:")
print(crc_data[:, -len(poly) + 1:])
print("-------------------")

disturbed_data = disturb(crc_data)
print("Disturbed data:")
print(disturbed_data)
print("-------------------")

error_item, _, remainder = crc_check(disturbed_data, poly)
for i in range(num):
    if i in _:
        print("\033[31m{}\033[0m".format(crc_data[i]))
    else:
        print("\033[32m{}\033[0m".format(crc_data[i]))
print("-------------------")

for i in range(num):
    if i in _:
        print("\033[31m{}\033[0m".format(remainder[i]))
    else:
        print("\033[32m{}\033[0m".format(remainder[i]))

print(f"Error item: {error_item}, Accuracy: {((num - error_item) / num)*100 :.2f}%")
