import redis_cli

# 发送用户输入内容
def update_dialog(story_id, user_input):
    
    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事不存在：" + story_id
    
    # 调用对话引擎
    errmsg, ok = story_data.update_dialog(user_input)
    if ok == False:
        return errmsg

    # 存盘
    redis_cli.set_story(story_id, story_data)

    # 返回缓存中的内容
    return story_data.dialog_record_txt