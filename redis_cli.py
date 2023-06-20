import redis
import os
import json
from storydata import StoryData

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
    
    print("get_story:")
    data = json.loads(json_story)
    print(data)
    result = StoryData("")
    result.__dict__ = data
    return result

# 简单粗暴地使用json
def set_story(story_id, story_data:StoryData):

    # 连接redis
    r = get_redis_cli()

    # 序列化
    json_story = json.dumps(story_data.__dict__)

    # 存储到redis
    r.set("story_id:" + story_id, json_story, ex=86400*30)

def get_template(temp_name):

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
    return json.loads(json_temp)

def set_template(temp_name, temp_data):

    # 连接redis
    r = get_redis_cli()

    # 序列化
    json_temp = json.dumps(temp_data)

    # 存储到redis
    r.set("temp_id:" + temp_name, json_temp, ex=86400*30)