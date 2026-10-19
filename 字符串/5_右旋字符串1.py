def reverse(chars, left, right):
    # 反转闭区间 [left, right] 内的字符
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1


k = int(input())
chars = list(input())
n = len(chars)
k %= n

reverse(chars, 0, n - 1)  # 整体反转
reverse(chars, 0, k - 1)  # 反转前 k 个字符
reverse(chars, k, n - 1)  # 反转剩余字符

print("".join(chars))