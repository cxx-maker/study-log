# def dedupe(items):
#     """去重并保留顺序"""
#     result = []
#     for i in items:
#         if i not in result:
#             result.append(i)
#     return result
          
# if __name__ == '__main__':
    
#     print(dedupe([3, 1, 3, 2, 1, 5]))
def dedupe_fast(items):
    """去重并保留顺序（O(n) 版本）"""
    result = []
    seen = set()
    for x in items:
        #判断 + 记录 + 收集
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result

print(dedupe_fast([3, 1, 3, 2, 1, 5]))

#字符串反转
def reverse_v1(s):
    """使用切片"""
    return s[::-1]
def reverse_v2(s):
    """用循环逐字符拼接"""
    result = ""
    for ch in s :
        result = ch + result
    return result

print(reverse_v1("hello"))
print(reverse_v2("hello"))

def is_palindrome(s):
    """判断是否是回文"""
    s = s.lower().replace(" ", "")
    return s == reverse_v1(s)
print(is_palindrome("A man a plan a canal Panama"))
print(is_palindrome("hello"))