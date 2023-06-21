from storydata import StoryData

# # 从输出内容里获取摘要
# def get_summary(text:str) -> str:
#     idx = text.find("【摘要】")
#     if idx < 1:
#         return text
#     return text[idx+len("【摘要】"):]

# # 从输出内容里删除摘要
# def del_summary(text:str) -> str:
#     idx = text.find("【摘要】")
#     if idx < 1:
#         return text
#     return text[:idx]
    
# # 添加默认的最后一轮对话记录（早期探索阶段）
# def add_default_latest_dialog(prompt:str, story_data:StoryData) -> str:
#     if prompt.find("{最近一轮对话}") < 0:
#         return story_data.str_latest_dialog() + prompt
#     return prompt

# # 添加默认世界状态（早期探索阶段）
# def add_default_summary(prompt:str, story_data:StoryData) -> str:
#     if prompt.find("{世界摘要}") < 0:
#         return "【世界】\n" + story_data.summary + '\n' + prompt
#     return prompt

# # 添加摘要属性，让GPT必须返回摘要信息
# def add_summary_property(prompt:str) -> str:
#     if prompt.find("【摘要】") < 0:
#         return prompt + "\n另外，在末尾对最新的世界状态做一个摘要，大约100句话，并严格遵守以下格式：\n【摘要】"
#     return prompt