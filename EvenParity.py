# 偶校验
import numpy as np
import random

# 生成100个数据, 每个数据8个二进制位
data = np.random.randint(0, 2, (100, 8))


# 计算监督码 (偶校验)
def parity_check(data):
    return np.sum(data, axis=1) % 2

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
    for i in range(100):
        if (np.sum(received[i]) + parity[i]) % 2 != 0:
            errors += 1
            error_index.append(i)
        else:
            if int(''.join(map(str, original[i])), 2) != int(''.join(map(str, received[i])), 2):
                false_positives += 1
                false_positives_index.append(i)
    return errors, false_positives


parity_errors, parity_false_positives = calculate_error_rates(data, corrupted_data)


print("Original Data:")
print(data)
print("-------------------")
print("Parity:")
print(parity)
print("-------------------")
print("Corrupted Data:")
for i in range(100):
    if i in error_index:
        print("\033[31m{}\033[0m".format(corrupted_data[i]))
    elif i in false_positives_index:
        print("\033[32m{}\033[0m".format(corrupted_data[i]))
    elif i in error_index and i in false_positives_index:
        print("\033[33m{}\033[0m".format(corrupted_data[i]))
    else:
        print(corrupted_data[i])
print("-------------------")
print(f"Parity Check Errors: {parity_errors}, False Positives: {parity_false_positives}")
print(f"Accuracy: {(1 - (parity_errors + parity_false_positives) / 100)*100 :.2f}%")
