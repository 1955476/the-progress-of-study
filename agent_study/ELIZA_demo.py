import re  #导入处理正则表达式的库
import random #导入随机数标准库

"""
1、将用户的输入去匹配规则库里的正则表达式
2、将句子中的匹配部分进行人称转化
3、随机选择一个回答的句子，并将修改过人称的部分放到替换部分，将回复返回
"""

#定义规则库
rules = {
    r"I need (.*)": [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r"Why don't you (.*)\?": [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}",
        "Do you really want me to {0}?"
    ],
    r".*": [
        "Please tell me more about your more.",
        "Let's change focus a bit ... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

#定义代码转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}

"""
def 函数名(形参1, 形参2, ...):
函数体代码块
return 返回值 # 可选，无return默认None 代表没有空结果
"""
def swap_pronouns(phrase):
    """
    对输入语句代词转换
    """
    words = phrase.lower().split()  #先小写然后分割（按照空格）
    #这里的.get(key,default) --> key 代表查找值，找到后替换为value default 指没找到替换的默认值
    swapped_words = [pronoun_swap.get(word,word) for word in words]
    """
    等价于
    swapped_words = []
    for word in words:
    new_word = pronoun_swap,get(word,word)
    swapped_words.append(new_word)
    """

    """
    [pronoun_swap.get(word,word) for word in words] --> 列表推导式
    语法规则: [ 表达式 for 循环变量 in 可迭代对象]
    代表将遍历这个可迭代对象，每个对象执行表达式，然后将返回值放到列表中
    """

    return " ".join(swapped_words)
"""
str.join(可迭代对象) --> str:分割字符串
作用:用当前字符串作为分隔符，把序列里的所有元素拼接成一整段新字符串
"""

def respond(user_input):
    """
    .items()
    以键值对的方式遍历
    """
    for pattern,responses in rules.items():
        """
        re.search(正则, 待匹配文本, 标志位)
        search 代表匹配待匹配文本的任意位置
        match 只匹配开头位置
        
        正则: 代表要匹配的表达式
        标志位: 开启特殊规则(比如: 开启大小写忽略等),多个规则用 | 
        底层代表的是二进制位开关
         0 代表关闭
         1 代表打开
         当开启某个特殊规则，特定位置的二进制位就变成1
         
         match的类型是Match对象
         match.group(0) 完整匹配的字符串
         match.group(1) 第1个捕获括号内容  第一个捕获的内容
         match.groups() 所有捕获分组组成的元组  就是将匹配的所有内容，组合成元组返回
         match.span() 匹配内容的起始、结束下标
        """
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            #捕获匹配到的部分
            """
            三元条件表达式
            变量 = 针织表达式 if 判断条件 else 假值表达式
            """
            captured_group = match.group(1) if match.groups() else ''
            #进行代词转换
            swapped_group = swap_pronouns(captured_group)
            #从模板中随机选择一个并格式化
            response = random.choice(responses).format(swapped_group)
            return response
    return random.choice(rules[r".*"])

    #主聊天循环
if __name__ == '__main__': #代表检查当前文件是否为本文件，如果是本文件就执行(以防止被当作模块导入执行下面代码)
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break

        response = respond(user_input)
        print(f"Therapist: {response}")


