from chatbot import chatbot
from storydata import StoryData
import redis_cli

# 加载世界引擎初始模板，并初始化会话
def new_story(player_template_name, not_ignore_system, is_davinci, is_summary):
    ignore_system = not not_ignore_system

    # 检查模板名是否为空
    if len(player_template_name) < 1:
        return player_template_name, "模板ID为空", "模板ID为空"

    # 获取模板
    temp_data = redis_cli.get_template(player_template_name)
    if temp_data is None:
        return player_template_name, "模板不存在", "模板不存在"

    # 获取新的故事ID
    story_id = redis_cli.get_new_story_id(player_template_name)

    # 初始化故事
    story_data = redis_cli.get_story(story_id)
    if story_data is not None:
        return story_id, "故事ID异常", "故事ID异常"
    
    # 初始化世界状态
    story_data = StoryData(story_id, player_template_name, temp_data)
    errmsg, ok = story_data.new_story(ignore_system, is_davinci, is_summary)
    if ok == False:
        return story_id, errmsg, errmsg

    # 存储
    redis_cli.set_story(story_id, story_data)
    
    # 渲染页面
    return story_id, story_data.world_record_txt, story_data.dialog_record_txt

