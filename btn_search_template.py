import redis_cli

# 加载世界引擎更新模板
def search_template(manager_template_name):
    
    # 查找模板
    temp_data = redis_cli.get_template(manager_template_name)
    if temp_data is None:
        return "模板不存在：" + manager_template_name, \
            "模板不存在：" + manager_template_name, \
            "模板不存在：" + manager_template_name, \
            "模板不存在：" + manager_template_name
    
    return temp_data['world_engine_init_template'], \
        temp_data['dialog_engine_init_template'] , \
        temp_data['world_engine_update_template'] , \
        temp_data['dialog_engine_update_template']
