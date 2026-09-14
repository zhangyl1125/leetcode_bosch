# 题意：给定两个数组，编写一个函数来计算它们的交集。

class Solution:
    def intersection(self, nums1: list[int], nums2: list[int]) -> list[int]:
        # 使用哈希表存储一个数组中的所有元素
        table = {}
        for num in nums1:
            table[num] = table.get(num, 0) + 1


        # 使用集合存储结果
        res = set()
        for num in nums2:
            if num in table:
                res.add(num)
                del table[num]  # 删除已匹配的元素，避免重复添加

        return list(res)