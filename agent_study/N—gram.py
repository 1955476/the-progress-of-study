"""
N-gram模型
通过计算当前单词在规定上下文长度N中出现的概率来预测下一个单词的概率
缺点:
1、数据的稀疏性:如果一个词从未在语料库中出现过，那么它的概率为0
2、泛化能力差:不能举一反三，不理解语言的语义
"""
import collections

#先定义语料库
"""
正常语句并非没有标点，没有标点会导致错误
但是这里演示通过人为控制来避免错误
"""
corpus = "datawhale agent learns datawhale agent works"
tokens = corpus.split()
total_tokens = len(tokens)

#计算 P（datawhale)
count_datawhale = corpus.count("datawhale")
p_datawhale = count_datawhale / total_tokens
print(f"第一步:P(datawhale) = {count_datawhale}/{total_tokens} = {p_datawhale:.3f}")

#计算P(agent | datawhale)
#先计算P(agent)
"""
zip()里面可以迭代多个序列，返回一个元组序列
例如:
zip(["a", "b", "c"], [1, 2, 3])
返回:
[("a", 1), ("b", 2), ("c", 3)]
"""
bigrams = zip(tokens, tokens[1:]) #通过错位来打包所有的2-gram
#Counter()参数是可迭代对象，返回一个字典，键是元素，值是元素出现的次数
bigram_counts = collections.Counter(bigrams)
count_datawhale_agent = bigram_counts[("datawhale", "agent")]
#计算P(agent | datawhale)
p_agent_datawhale = count_datawhale_agent / count_datawhale
print(f"第二步:P(agent | datawhale) = {count_datawhale_agent}/{count_datawhale} = {p_agent_datawhale:.3f}")

#计算P(learns | agent)
count_agent_learns = bigram_counts[("agent", "learns")]
count_agent = tokens.count("agent")
p_learns_agent = count_agent_learns / count_agent
print(f"第三步:P(learns | agent) = {count_agent_learns}/{count_agent} = {p_learns_agent:.3f}")

#进行连乘算出概率
p_sentence = p_datawhale * p_agent_datawhale * p_learns_agent
print(f"最后: P('datawhale agent learns') ≈ {p_datawhale:.3f} * {p_agent_datawhale:.3f} * {p_learns_agent:.3f} = {p_sentence:.3f}")

