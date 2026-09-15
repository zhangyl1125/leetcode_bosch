# 只要有一种字母不够，就失败
# 核心思路
# 先统计，再检查
# 常见理解法：先数 magazine 里每个字母有几个，再看 ransomNote 需不需要超量。

class Solution:
    def CanConstruct(self,ransomNote:str,magazine:str)->bool:
        # 用于统计 ransomNote 中每个字母的数量
        ransom_count = [0] * 26 
        # 用于统计 magazine 中每个字母的数量
        magazine_count = [0] * 26  

        # 统计 ransomNote 中每个字母的数量
        for c in ransomNote:
            # ord() 函数返回字符的 ASCII 编码值。如ord('a') 返回 97，ord('b') 返回 98，以此类推。通过 ord(c) - ord('a') 可以将字母映射到 0-25 的索引范围。
            # ransom_count[0]：表示赎金信里一共需要多少个字母 'a'（下标 0 存的就是 'a' 的出现次数）。
            ransom_count[ord(c) - ord('a')] += 1  

        # 统计 magazine 中每个字母的数量
        for c in magazine:
            # magazine_count[1]：表示杂志里一共能提供多少个字母 'b'（下标 1 存的就是 'b' 的出现次数）。
            magazine_count[ord(c) - ord('a')] += 1  
        # 检查 ransomNote 中每个字母的数量是否不超过 magazine 中的数量
        return all(ransom_count[i] <= magazine_count[i] for i in range(26))  # 检查 ransomNote 中每个字母的数量是否不超过 magazine 中的数量

if __name__ == '__main__':
    solution = Solution()
    print(solution.CanConstruct("a","b"))  # 输出 False
    print(solution.CanConstruct("aa","ab"))  # 输出 False
    print(solution.CanConstruct("aa","aab"))  # 输出 True