import redis_cli
import json

# 获取上回故事内容
def update_developer_info(story_id):
    
    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事ID不存在"

    # 处理嵌套类（story中的template）
    story_data.temp_data = story_data.temp_data.__dict__
    
    # 优化可读性
    output = json.dumps(story_data.__dict__, indent=2, ensure_ascii=False)

    # 返回内容
    return output