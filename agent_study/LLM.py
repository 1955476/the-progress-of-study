import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

#指定模型ID
model_id = "Qwen/Qwen1.5-0.5B-Chat"

#设置设备，优先使用GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

#加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_id)

#加载模型，并将其移动到指定设备
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

print("米星和分词器加载完成")

#准备对话输入
"""
先要将整个messages转换成指定大模型分词器所能识别的形式，才能传给分词器转换为tokenID
"""
"""
整个上下文
"""
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role":"user", "content":"你好，请介绍你自己"}
]

"""
将messages转换成指定大模型的对话模板 这样才知道读取哪里，将哪里转化成tokenID
"""
#使用分词器的模板格式化输入
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False, #是否转化为张量
    add_generation_prompt=True #是否后面加提示词 就是加上assistant的相关标记，让大模型知道该自己回答了
)

#编码输入文本
model_inputs = tokenizer([text], return_tensors="pt").to(device)

print("编码后的输入文本:")
print(model_inputs)

#使用模型生成回答
#max_new_tokens 控制模型最大生成多少个新的Token
"""
指定模型在生成自己输出是最多生成多少token
"""
generated_ids = model.generate(
    model_inputs.input_id,
    max_new_tokens=512
)

#截出输出部分
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids,generated_ids)
]

#解码生成的 Token ID
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("\n模型的回答:")
print(response)

