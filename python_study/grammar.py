print("Hello World")

# type --- 查看数据类型
# isinstance(数据,数据类型)  --- 返回值为bool

#the define of string
#1、双引号定义
s1 = "hello"  #不能换行
#2、单引号定义   #不能换行
s2 = 'hello'

#problem:
msg = 'It\'s very good'  #用转义字符解决问题

#3、三引号定义  #可定义多行字符串
s3 = """"
hello：
the gate of python
"""

#concatente strings （拼接字符串)
s1 = "人生苦短"
s2 = "我用python"

# the plus sign only can concatenate the string date type (通过加号拼接字符串)
print("吉多.范罗多姆" + s1 + s2)

# the function can convert an int data  type to the string data type
a = 18
s3 = str(a)

#formatted string
s1 = "Tom"
s2 = "Amy"
print("my name is %s and my frind name is %s" %(s1,s2))

#the other way(the f at the head is important)
name = "Tom"
hobby = "python coding"
print(f"my name is {name}, my hobby is {hobby}")

#input and output
s = input("请输入你的姓名：")  #the function that gets the message from the keyboard
print(f"欢迎你{s}")  #the function that present the information on the screen


#the airthematic opretors  算数运算符
# +
# -
# *
# /
# // --->  integer division
# %
# ** --->x to the power of n (幂指)

#assignment opetators(赋值运算符)
# =
# +=
# -=
# *=
# /=
# %=
# =
# **=

#comparison operators
#==
#!=
#>
#>=
#<
#<=

#logical operators
#and
#or
#not -->negation (取反)




