# 切片拼接实现右旋字符串
k = int(input())
s = input()

# 右旋超过字符串长度时，取余得到实际需要移动的位数
k %= len(s)
# 后 k  个字符放在前面，其余的字符放到后面
print(s[-k:] + s[:-k])
print(s)

if __name__ == "__main__":
    k = 2
    s = "abcdefg"
    k %= len(s)
    print(s[-k:] + s[:-k])  # 预期输出：fgabcde

