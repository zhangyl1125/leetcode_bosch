# 反转字符串

""""
["h","e","l","l","o"] → ["o","l","l","e","h"] 过程
"""
class Solution:
    def reverseString(self,s:list[str])->None:
        """
        不返回任何值，直接在原列表上修改顺序
        """
        left,right = 0,len(s)-1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

if __name__ == "__main__":
    s = ["h","e","l","l","o"]
    Solution().reverseString(s) #  原地修改s，不用接收返回值
    print(s)