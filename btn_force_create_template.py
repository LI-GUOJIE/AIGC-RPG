import redis_cli
from templatedata import TemplateData

# 加载世界引擎更新模板
def force_create_template(manager_template_name,
                    world_engine_init_template,
                    dialog_engine_init_template,
                    world_engine_update_template,
                    dialog_engine_update_template,
):
    
    # 检查模板名是否为空
    if len(manager_template_name) < 1:
        return "模板名为", \
            "模板名为空", \
            "模板名为空", \
            "模板名为空"
    
    # 检查模板内容是否为空
    if len(world_engine_init_template) < 1 or len(dialog_engine_init_template) < 1 or \
        len(world_engine_update_template) < 1 or len(dialog_engine_update_template) < 1:
        return "您提交的某个模板是空值", \
            "您提交的某个模板是空值", \
            "您提交的某个模板是空值", \
            "您提交的某个模板是空值" 
    
    # 如果存在同名模板，则打印新旧两份模板内容
    old_world_engine_init_template     = ""  
    old_dialog_engine_init_template    = ""    
    old_world_engine_update_template   = ""    
    old_dialog_engine_update_template  = ""     

    # 初始化模板
    temp_data = redis_cli.get_template(manager_template_name)
    if temp_data is not None:
        old_world_engine_init_template     = temp_data.world_engine_init_template
        old_dialog_engine_init_template    = temp_data.dialog_engine_init_template
        old_world_engine_update_template   = temp_data.world_engine_update_template 
        old_dialog_engine_update_template  = temp_data.dialog_engine_update_template
    temp_data = TemplateData(
        world_engine_init_template,
        dialog_engine_init_template,
        world_engine_update_template,
        dialog_engine_update_template,
    )
    redis_cli.set_template(manager_template_name, temp_data)

    return "强制更新模板：" + manager_template_name + "\n被覆盖的内容：" + old_world_engine_init_template, \
        "强制更新模板：" + manager_template_name + "\n被覆盖的内容：" + old_dialog_engine_init_template, \
        "强制更新模板：" + manager_template_name + "\n被覆盖的内容：" + old_world_engine_update_template, \
        "强制更新模板：" + manager_template_name + "\n被覆盖的内容：" + old_dialog_engine_update_template
