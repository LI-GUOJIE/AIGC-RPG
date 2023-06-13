from chatbot import chatbot
import redis_cli

# 发送用户输入内容
def update_dialog(story_id, user_input):
    
    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事不存在：" + story_id
    
    # 检查模板ID
    temp_name = story_data['template_id']
    temp_data = redis_cli.get_template(temp_name)
    if temp_data is None:
        return "故事对应的模板不存在：" + story_id

    # 插入用户输入内容
    story_data['conversation'].append({"role": 'user',"content": user_input})

    # 命令式调用引擎
    response = chatbot.ask(story_id, "system", temp_data['dialog_engine_update_template'])

    # 将本回合新增对话追加到缓存
    new_content = user_input + "\n" + response
    story_data['dialog_record_txt'] += "\n" + new_content
    redis_cli.set_story(story_id, story_data)

    # 返回缓存中的内容
    return story_data['dialog_record_txt']