# 快乐数
#
# 解题思路：
# 1. 不断求出当前数字各位数字的平方和，并把这个平方和作为下一个数字。
# 2. 如果最终得到 1，就是快乐数；如果某个中间结果重复出现，说明进入了循环，不可能得到 1。
# 3. 用集合 record 保存已经出现过的结果，重复时返回 False，得到 1 时返回 True。
#
# 高频语法：
# - class 用来定义类，def 用来定义函数或方法。
# - self 表示当前对象；n: int -> bool 是类型注解，表示参数 n 通常是整数、返回值通常是布尔值。
# - set() 创建空集合；in 用于判断元素是否存在，add() 用于向集合中添加元素。
# - while True 表示不断循环；if/else 表示条件分支，return 会立即结束当前方法并返回结果。
# - divmod(n, 10) 同时返回除法的商和余数；n, r = ... 是序列解包。
# - ** 表示幂运算，+= 表示先相加再赋值。
# - if __name__ == '__main__' 表示只有直接运行本文件时，下面的测试代码才会执行。
# - Solution() 用于创建对象，.isHappy(...) 用于调用对象的方法，print() 用于输出结果。

class Solution:  # 定义 Solution 类，用于封装快乐数的判断方法。
    def isHappy(self, n: int) -> bool:  # 定义判断快乐数的方法，参数 n 是待判断的数字。
        record = set()  # 创建空集合，保存已经出现过的中间结果。

        while True:  # 持续计算下一个结果，直到得到 1 或发现循环。
            n = self.get_sum(n)  # 求出 n 各位数字的平方和，并更新 n。
            if n == 1:  # 如果结果等于 1，说明 n 是快乐数。
                return True  # 返回 True，结束方法。

            if n in record:  # 如果结果已经出现过，说明计算进入了循环。
                return False  # 返回 False，说明 n 不是快乐数。
            else:  # 如果结果没有出现过，就执行下面的记录操作。
                record.add(n)  # 把当前结果加入集合，避免之后重复计算。

    def get_sum(self, n: int) -> int:  # 定义计算各位数字平方和的辅助方法。
        new_num = 0  # 初始化平方和为 0。
        while n:  # 只要 n 为真，就一直循环
        # 等价于 while n != 0:  当 n 不为 0 时，继续拆分 n 的每一位数字。
            n,r = divmod(n, 10)  # 求 n 除以 10 的商和余数，余数 r 就是当前个位数字。
            new_num += r ** 2  # 将当前数字的平方累加到平方和中。
        return new_num  # 返回各位数字的平方和。

if __name__ == '__main__':  
    solution = Solution()  # 创建 Solution 类的对象。
    print(solution.isHappy(19))  # 调用方法判断 19，并输出 True。
    print(solution.isHappy(2))   # 调用方法判断 2，并输出 False。