"""
给定一个字符串 s，它包含小写字母和数字字符，请编写一个函数，将字符串中的字母字符保持不变，而将每个数字字符替换为number。

例如，对于输入字符串 "a1b2c3"，函数应该将其转换为 "anumberbnumbercnumber"。
a5b → anumberb
"""
# 思路要从后往前填写：因为 1 个数字会膨胀成 6 个字符。如果从前面不停插入，后面的元素可能被反复搬动。

"""
01
    先数数字
    每出现 1 个数字
    最终长度多 5
02
    先扩容
    因为 "number" 长 6
    原数字只占 1 位
03
    双指针
    j 指向旧串末尾
    i 指向新串末尾
04
    从后往前填
    数字写入 number
    字母原样拷贝

"""
# 步骤一原字符串转换成字符列表   --->   Python 字符串不能原地改字符，所以先变成字符列表。
# 步骤二统计一个数字字符
# 步骤三进行扩容

class Solution(object):
    def substitute_numbers(self, s):
        # 统计出现数字的个数
        # 遍历字符串每一个字符；if char.isdigit() 就计数==是字符就返回true,然后累加所有1-> 统计一共有多少个数字
        count = sum(1 for char in s if char.isdigit())
        # 举例：统计完成：有 3 个数字，所以新长度 = 6 + 3×5 = 21。
        # 计算扩充后字符串的大小，x->number,没有一个数字就要增加五个字符
        expanded_length = len(s) + count * 5
        # Python 字符串不可变，不能直接扩容修改。所以用列表 list（可变）
        res = [''] * expanded_length

        # 初始化双指针；
        # old_index：原始字符串最后一个字符下标（从后往前读，初始 = 5，"a1b2c3" 下标 0~5）
        # new_index：新数组 res 最后一个下标（初始 = 20）
        new_index = expanded_length - 1
        old_index = len(s) - 1

        #循环条件：原始指针没有越界，>=0 就继续循环。
        while old_index >= 0:
            if s[old_index].isdigit():
                    res[new_index-5:new_index+1] = "number"
                    new_index -= 6
            else:
                res[new_index] = s[old_index]
                new_index -= 1
            old_index -= 1

        # - `''`：**空字符串**
        # - `.join(可迭代对象)`：是**字符串的内置方法**
        return ''.join(res) # 把序列里的所有元素拼接成一整个新字符串，元素之间用「分隔符」隔开

if __name__ == "__main__":
    s = "a1b2c3"
    solution = Solution()
    print(solution.substitute_numbers(s))