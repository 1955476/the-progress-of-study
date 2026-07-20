import torch #构建主流大模型的库
import torch.nn as nn
import math

# --- 占位符模块，将在后续小节实现 ---
class MultiHeadAttention(nn.Module):
    """
    多头注意力机制模块
    """
    #d_model --> 一个token的向量长度  num_heads --> 代表分成几个头
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        #校验: 总向量长度必须能平分给所有头
        assert d_model % num_heads == 0  #d_model 必须能被num_heads整除

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        """
        这里的W_q...是线性层对象(训练出的可学习矩阵)
        通过 层(输入)
        W_q(Q) 训练出含有查询特征的矩阵
        """
        #定义Q， K， V 和输出的线性变换层
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model) #输出融合层:将注意力头融合后筛选出关键信息，除去冗杂信息，然后拼接成一个新向量输出

    """
    多头注意力的标准形状
    [batch, heads, seq_len, d_k]
    batch: 一次送多少条句子 -->一次同时塞给大模型多少条句子
    heads: 多少个注意力头
    seq_len: 一条句子有几个字
    d_k: 单个头里向量的长度
    
    下面的QKV都是含有这四个参数
    Q --> 通过可学习矩阵，将原来的数据打包成一堆突出每个单词q特征的句子
    batch: 一次推送多少个句子
    heads: 多少个查询角度
    seq_len: 每个句子单词数量
    当句子长于这个长度会被截断
    当句子短会被mask填充，但是再注意力处理会对mask的注意力降到极低
    d_k: 每个注意力头分配多少维度
    其余同理
    """
    def scaled_dot_product_attention(self,  Q, K, V, mask = None):
        #1、计算注意力得分
        """
        先将K矩阵的最后两个维度交换
        从每个句子来看，就是将seq_len 和 d_k 交换
        例子:
        全部数据 : 里面有一个句子，每个句子三个词，每个词的每个注意力头分配64维度
        Q 的后两个维度依次是 seq_len 和 d_k
        K 交换后后两个维度是 d_k 和 seq_len
        Q * KT 就是将Q的每个词的多个查询向量 去乘 每个词的多个标签向量 就实现了查询
        Q[3 * 64] * T[64 * 3]
        """
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        """
        attn_scores = [batch, heads, seq_q, seq_k] 
        seq_q 代表每一个查询单词 行
        seq_k 代表所有匹配单词 列
        """

        #应用掩码
        if mask is not None:
            #将掩码中位置为0的位置设置为一个非常小的负数，这样softmax后接近0
            attn_scores = attn_scores.masked_fill(mask == 0, -1e9) #将mask等于true的位置替换成-1e9

        #3、计算注意力权重(softmax)
        attn_probs = torch.softmax(attn_scores, dim=-1) #代表处理的维度是-1 就是seq_k 代表处理每个单词匹配的其他单词

        """
        split_heads是将原来形状为(batch_size, seq_length, d_model)拆解成(batch_size, num_heads, seq_length, d_k)
        这个.view函数就是将最后d_model拆为num_heads * d_k 然后交换最后两个维度 --> 以方便到注意力计算时方便
        
         batch_size, num_heads, seq_length, d_k = x.size()
         这里的x是原来的三维矩阵，将x的三个维度值分别自左向右赋值给三个变量
        """
        def split_heads(self, x):
            #将输入x的形状从(batch_size, seq_length, d_model)
            #变换为(batch_size, num_heads, seq_length, d_k)
            batch_size, num_heads, seq_length, d_k = x.size()
            return x.transpose(1,2).contiguous().view(batch_size, seq_length, self.d_model)

             #4、加权求和
            output = torch.matmul(attn_probs, V)

        def combine_heads(self, x):
            # 将输入 x 的形状从 (batch_size, num_heads, seq_length, d_k)
            # 变回 (batch_size, seq_length, d_model)
            batch_size, num_heads, seq_length, d_k = x.size()
            """
            transpose底层不会交换内存位置，只是逻辑上变了位置
            但是view的处理要求必须是紧挨着的
            所以通过.contiguous()来将逻辑上的位置交换转变成实际内存上的，就是按照逻辑重新复制一份
            """
            return x.transpose(1, 2).contiguous().view(batch_size, seq_length, self.d_model)

        def forward(self, Q, K, V, mask=None):
            # 1. 对 Q, K, V 进行线性变换
            """
            参数的QKV是都是原来的通用语义矩阵
            经过处理后就有不同语义
            """
            Q = self.split_heads(self.W_q(Q))
            K = self.split_heads(self.W_k(K))
            V = self.split_heads(self.W_v(V))

            # 2. 计算缩放点积注意力
            attn_output = self.scaled_dot_product_attention(Q, K, V, mask)

            # 3. 合并多头输出并进行最终的线性变换
            output = self.W_o(self.combine_heads(attn_output))
            return output

class PositionWiseFeedForward(nn.Module):
    """
    位置前馈网络模块(FNN)
    将每个单词的内部多层含义，提炼出来
    """
    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionWiseFeedForward, self).__init__();
        self.linear1 = nn.Linear(d_model, d_ff)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()

        def forward(self, x):
            #x:(batch_size, seq_len, d_model)
         x = self.linear1(x)
         x = self.relu(x)
         x = self.dropout(x)
         x = self.linear2(x)
         # 最终输出形状: (batch_size, seq_len, d_model)
         return x


"""
残差连接：保留原始信息，给网络开一条直达通道，方便深层训练；
层归一化：统一特征数值大小，让训练更稳定、好收敛。
"""

"""
首先类的定义
class 类名(继承的父类(支持多继承)):
......

nn.Module --> 所有神经网络层/模型的基类
继承才能拥有前向传播、参数管理等神经网络功能
"""
class PositionalEncoding(nn.Module):
    """
    位置编码模块
    """
    """
    为输入序列的词嵌入向量添加位置编码
    """
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        #训练时随机删掉一部分特征维度，不让模型死记训练数据的细节；
        self.dropout = nn.Dropout(p=dropout)

        #创建一个足够长的位置编码矩阵
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))

        #pe(position encoding) 的大小为 (max_len, d_model)
        pe = torch.zeros(max_len, d_model)

        #偶数位的使用sin,奇数维度使用cos
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        #将pe注册为buffer, 这样它就不会被是为模型参数，但会随模型移动
        self.register_buffer('pe', pe.unsqueeze(0))

    #forword是父类方法 这里是对父类方法的重写
    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return self.dropout

#--- 编码器核心层 ---
class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout):
        #super(子类, self) 找到该子类的直接父类，返回父类对象
        super(EncoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention() #待实现
        self.feed_forward = PositionWiseFeedForward() #待实现
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

        def forward(self, x, mask):
            #1、多头自注意力
            attn_output = self.self_attn(x, x, x, mask)
            x = self.norm1(x + dropout(attn_output))

            #2、前馈网络
            ff_output = self.feed_forward(x)
            x = self.norm2(x + self.dropout(ff_output))

            return x

#--- 解码器核心层 ---
class DecoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout):
        super(DecoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention() #待实现
        self.cross_attn = MultiHeadAttention() #待实现
        self.feed_forward = PositionWiseFeedForward() #待实现
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, encoder_output, src_mask, tgt_mask):
        #1、掩码多头自注意力(对自己)
        attn_output = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn_output))

        #2、交叉注意力(对编码器输出)
        cross_attn_output = self.cross_attn(x, encoder_output, encoder_output, src_mask)
        x = self.norm2(x + self.dropout(cross_attn_output))

        #3、前馈网络
        ff_output = self.feed_forward(x)
        x = self.norm3(x + self.dropout(ff_output))

        return x





