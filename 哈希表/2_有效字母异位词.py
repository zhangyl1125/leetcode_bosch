"""
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1: 输入: s = "anagram", t = "nagaram" 输出: true

示例 2: 输入: s = "rat", t = "car" 输出: false

**说明:** 你可以假设字符串只包含小写字母。

"""
"""
## 1. `ord()`函数

`ord(字符)`：返回字符的 ASCII 编码数字。

- `ord('a') = 97`，`ord('b')=98` … `ord('z')=122`

"""
class Solution:
    def isAnagram(self,s:str,t:str)->bool:
        record = [0] *26
        for i in s:
            # 遍历`s`每一个字母，对应数组位置**计数 + 1**，统计`s`中每个小写字母出现多少次。
            record[ord(i)-ord('a')] += 1
        for i in t:
            # 遍历`t`每一个字母，对应数组位置**计数‑1**，相当于抵消掉 t 里面出现的字母。
            record[ord(i)-ord('a')] -= 1
        for i in range(26):
            if record[i] != 0:
                return False
        return True

if __name__ == '__main__':
    s = "anagram"
    t = "nagaram"
    solution = Solution()
    print(solution.isAnagram(s,t))