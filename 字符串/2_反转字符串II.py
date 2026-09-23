"""
反转字符串 II

给定一个字符串和一个整数 k，每 2k 个字符反转前 k 个字符。

示例:
输入: s = "abcdefg", k = 2
输出: "bacdfeg"
"""
# 思路：
"""
01
    每次跳 2k
    i = 0, 2k, 4k ...
    每次处理一大组
02
    找前 k 个
    left = i
    right = min(i+k-1, n-1)
03
    局部反转
    只交换这一小段
    别的字符别动
04
    继续下一组
    i += 2k
    直到遍历完
"""
class Solution:
    def reverseStr(self,s:str,k:int)->str:
        """
        1. 使用range(start, end, step)来确定需要调换的初始位置
        2. 对于字符串s = 'abc'，如果使用s[0:999] ===> 'abc'。字符串末尾如果超过最大长度，则会返回至字符串最后一个值，这个特性可以避免一些边界条件的处理。
        3. 用切片整体替换，而不是一个个替换.
        """
        def reverse_substring(text):
            left,right = 0,len(text) - 1
            while left < right:
                text[left],text[right] =text[right],text[left]
                left +=1
                right -=1
            return text
        
        res = list(s)

        for cur in range(0,len(res),2*k):   # range(起始, 终止, 步长)
            res[cur:cur+k] = reverse_substring(res[cur:cur+k])

        return ''.join(res)

    
"""
    res 现在是修改完成的字符列表，例如 ['b','a','c','d','f','e','g']
    ''.join(列表)`：把列表里面所有字符拼接成一个完整字符串.
"""

if __name__ == "__main__":
    s = "abcdefghijk"
    k = 2
    solution = Solution()
    print(solution.reverseStr(s, k)) # bacdfeghjik