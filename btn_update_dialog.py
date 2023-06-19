from chatbot import chatbot
import redis_cli
import utils

# 发送用户输入内容
def update_dialog(story_id, user_input):
    
    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事不存在：" + story_id
    
    # 检查模板ID
    temp_name = story_data.template_id
    temp_data = redis_cli.get_template(temp_name)
    if temp_data is None:
        return "故事对应的模板不存在：" + story_id

    # 插入用户输入内容
    story_data.latest_dialog.append({"role": 'user',"content": user_input})
    story_data.user_input = user_input # 仅作记录
    story_data.conversation.append({"role": 'user',"content": user_input}) # 仅作记录

    # 命令式调用引擎
    prompt = temp_data['dialog_engine_update_template']
    prompt = utils.add_default_latest_dialog(prompt, story_data)
    prompt = utils.add_default_summary(prompt, story_data)
    response = chatbot.ask(story_data, "system", prompt)

    # 将本回合新增对话追加到缓存（这里如果不重新获取story_data，ask中的结果将被覆盖）
    story_data.latest_dialog.append({"role": 'user',"content": user_input})
    new_content = user_input + "\n" + response # 仅作记录
    story_data.dialog_record_txt += "\n" + new_content  # 仅作记录
    redis_cli.set_story(story_id, story_data)

    # 返回缓存中的内容
    return story_data.dialog_record_txt