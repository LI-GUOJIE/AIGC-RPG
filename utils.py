import re


key_words = {
    "{世界摘要}": 'summary',
    "{最新对话}": 'latest_dialog',
    "{用户输入}": 'user_input',
}


# 从输出内容里获取摘要
def get_summary(text):
    print("get_summary")
    print(text)
    match = re.search(f"【摘要】.**", text, re.DOTALL)
    if match:
        new_text = match.group(1).strip()
        print("get_summary success:")
        print(new_text)
        return new_text
    else:
        # 找不到匹配内容
        print("get_summary failed:")
        return text


# 添加默认的最后一轮对话记录（早期探索阶段）
def add_default_latest_dialog(prompt, story_data):
    if prompt.find("{最新对话}") < 0:
        str_latest_dialog = "【对话】\n"
        for dialog in story_data['latest_dialog']:
            str_latest_dialog += dialog + '\n'
        return str_latest_dialog + prompt
    return prompt


# 添加默认世界状态（早期探索阶段）
def add_default_summary(prompt, story_data):
    if prompt.find("{世界摘要}") < 0:
        return "【世界】\n" + story_data['summary'] + '\n' + prompt
    return prompt
    

# 添加摘要属性，让GPT必须返回摘要信息
def add_summary_property(prompt):
    if prompt.find("摘要：") < 0:
        return prompt + "\n在末尾对最新的世界状态做一个总结，大约100句话，并严格遵守以下格式：\n【摘要：】"
    return prompt

    
# 替换模板中的关键词
def replace_key_words(prompt, story_data):
    for k, v in key_words.items():
        prompt = prompt.replace(k, story_data[v])
    return prompt