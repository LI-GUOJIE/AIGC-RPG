import redis
import os
import json
from storydata import StoryData
from templatedata import TemplateData

def get_redis_cli():
    return redis.Redis(host=os.environ.get("REDIS_HOST"), 
                    port=os.environ.get("REDIS_PORT"), 
                    password=os.environ.get("REDIS_PASSWORD"),
                    decode_responses=True, 
                   )

def get_new_story_id(player_template_name):

    # 连接redis
    r = get_redis_cli()

    # 该模板下当前的最大故事ID
    max_num = r.incr("template_max_story:" + player_template_name)

    # 获取该模板下唯一的故事ID
    return player_template_name + "-" + str(max_num)


# 简单粗暴地使用json
def get_story(story_id) -> StoryData:

    # 连接redis
    r = get_redis_cli()

    # 获取json
    json_story = r.get("story_id:" + story_id)

    # 判断是否为空
    if json_story is None:
        return None
    
    # 解析json
    data = json.loads(json_story)
    result = StoryData("", "", None)
    result.__dict__ = data

    # 后增加的属性，需要兼容之前已存储的数据
    result.story_id = story_id
    if 'query_logs' not in data:
        result.query_logs = []
    
    # 处理嵌套类（story中的template）
    temp_data = TemplateData("", "", "", "")
    temp_data.__dict__ = result.temp_data
    result.temp_data = temp_data
    return result


# 简单粗暴地使用json
def set_story(story_id, story_data:StoryData):

    # 连接redis
    r = get_redis_cli()

    # 处理嵌套类（story中的template）
    old_data = story_data.temp_data
    story_data.temp_data = story_data.temp_data.__dict__

    # 序列化
    json_story = json.dumps(story_data.__dict__)
    story_data.temp_data = old_data

    # 存储到redis
    r.set("story_id:" + story_id, json_story, ex=86400*30)

def get_template(temp_name) -> TemplateData:

    # 连接redis
    r = redis.Redis(host=os.environ.get("REDIS_HOST"), 
                    port=os.environ.get("REDIS_PORT"), 
                    password=os.environ.get("REDIS_PASSWORD"),
                    decode_responses=True, 
                   )

    # 获取json
    json_temp = r.get("temp_id:" + temp_name)

    # 判断是否为空
    if json_temp is None:
        return None

    # 解析json
    data = json.loads(json_temp)
    result = TemplateData("", "", "", "")
    result.__dict__ = data
    return result

def set_template(temp_name, temp_data:TemplateData):

    # 连接redis
    r = get_redis_cli()

    # 序列化
    json_temp = json.dumps(temp_data.__dict__)

    # 存储到redis
    r.set("temp_id:" + temp_name, json_temp, ex=86400*30)