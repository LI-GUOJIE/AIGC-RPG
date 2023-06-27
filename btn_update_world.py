import redis_cli

# 更新世界状态
def update_world(story_id, not_ignore_system):
    ignore_system = not not_ignore_system

    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事不存在：" + story_id, "故事不存在：" + story_id
    
    # 更新世界状态
    errmsg, ok = story_data.update_world(ignore_system)
    if ok == False:
        return errmsg, errmsg

    # 存盘
    redis_cli.set_story(story_id, story_data)

    # 返回缓存中的内容
    return story_data.world_record_txt, story_data.dialog_record_txt
