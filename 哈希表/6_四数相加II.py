# 核心：A + B + C + D = 0⇔ (A + B) = - (C + D)
# 先做 A+B 统计表，再去查 - (C+D)

class Solution:
    def fourSumCount(self,nums1,nums2,nums3,nums4):
        # 使用字典进行存储nums1和nums2的所有可能的和，并统计每个和出现的次数
        record = {}# {两数之和： 出现次数}
        for a in nums1:
            for b in nums2:
                # 如果当前算出来的和（比如 3）已经在字典里，就把它的出现次数加 1
                if a+b in record:
                    record[a+b] += 1
                else:
                    # 如果是第一次出现，就记录出现次数为 1：
                    record[a+b] = 1
    
        # 如果-(a+b)存在与nums3和nums4的和中，则说明存在四个数的和为0，统计出现次数
        count = 0
        for c in nums3:
            for d in nums4:
                key = -c-d
                if key in record:
                    # 如果我需要的那个互补数（key）在账本里出现过，那账本里记了它出现过几次，我就把总成功数 count 加上几。”
                    count += record[key]
        return count

if __name__ == '__main__':
    solution = Solution()
    print(solution.fourSumCount([1,2],[2,3],[3,4],[4,5]))  # 输出 0
    print(solution.fourSumCount([-1,5],[-2,-3],[3,4],[4,-5]))  # 输出 1
    print(solution.fourSumCount([1,-2],[2,3],[-3,4],[-4,5]))  # 输出1