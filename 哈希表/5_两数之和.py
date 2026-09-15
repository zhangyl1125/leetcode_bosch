"""
1.题目想要的：
不是返回数字，是返回下标
例如 2 + 7 = 9，所以返回的是它们在数组里的位置：[0, 1]。

2.使用算法哈希法
边走边查 map。
时间复杂度：O(n)
"""
class Solution:
    def twosum(self,nums:list[int],target:int)->list[int]:
        record = {} # {数字: 对应下标}

        for index,value in enumerate(nums):
            # 遍历当前的所有的元素，并在map中查找是否存在 target - value  匹配的key
            if target - value in record:
                return [record[target - value],index]   # 如果找到了，record[target - value] 是之前那个互补数的下标，index 是当前数的下标，直接返回这两个下标。
            # 如果没找到匹配对，就把访问过的元素和下标存入map中
            record[value] = index   # record[数字] = 下标;如果没找到，就把当前数字作为 key、当前下标作为 value 存进字典，方便后面的数字来找它。
        return []

if __name__ == '__main__':
    solution = Solution()
    print(solution.twosum([2,7,11,15],9))  # 输出 [0, 1]
    print(solution.twosum([3,2,4],6))      # 输出 [1, 2]
    print(solution.twosum([3,3],6))        # 输出 [0, 1]

"""
record[value] = index 的本质是：“我没能和前面的人配成对，那我就把自己的【号码】和【站位】登记在册，方便后面的人来找我。”

为什么是 record[数字] = 下标，而不是反过来？

题目要查的是： “列表里有没有某个数字？”

字典（哈希表）的特性： 查 key 的速度极快（接近瞬间完成）。

因此设计为： 把数字当作 key，把下标当作 value。这样后续只需要执行 if target - value in record，就能秒查前面有没有出现过这个互补数。

具体例子演练

假设：

列表：nums = [3, 8, 6]

目标值：target = 9

我们来看代码一步一步是怎么跑的：

第一轮：来到第一个元素

当前情况：index = 0, value = 3

算差值：我需要找一个 9 - 3 = 6

查字典：record 目前是空的 {}，里面没有 6，配对失败。

执行 record[value] = index：

把当前数字 3 当作 key，当前下标 0 当作 value 存进去：record[3] = 0。

现在的字典：{3: 0}

含义：备忘录上记着——“数字 3 在 0 号位”。

第二轮：来到第二个元素

当前情况：index = 1, value = 8

算差值：我需要找一个 9 - 8 = 1

查字典：record 是 {3: 0}，里面没有 1，配对失败。

执行 record[value] = index：

把当前数字 8 和下标 1 存进去：record[8] = 1。

现在的字典：{3: 0, 8: 1}

含义：备忘录现在记着——“数字 3 在 0 号位，数字 8 在 1 号位”。

第三轮：来到第三个元素

当前情况：index = 2, value = 6

算差值：我需要找一个 9 - 6 = 3

查字典：查一下 3 in record？找到了！

取结果：

从字典里查出之前 3 的下标：record[3] 得到 0。

当前 6 的下标就是 index = 2。

直接返回 [0, 2]，程序结束。
"""
