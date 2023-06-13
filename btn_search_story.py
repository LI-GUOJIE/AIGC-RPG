import gradio as gr
import redis_cli

# 获取上回故事内容
def search_story(story_id):
    
    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "", "故事ID不存在：" + story_id, "故事ID不存在：" + story_id

    # 返回内容
    return story_data['template_id'], \
        story_data['world_record_txt'], \
        story_data['dialog_record_txt']