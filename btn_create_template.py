import redis_cli
from templatedata import TemplateData

# 生成模板世界引擎更新模板
def create_template(manager_template_name,
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
    
    # 初始化模板
    temp_data = redis_cli.get_template(manager_template_name)
    if temp_data is not None:
        return "存在同名模板，如果想要覆盖，请点击[强制更新模板]按钮：" + manager_template_name, \
            "存在同名模板，如果想要覆盖，请点击[强制更新模板]按钮：" + manager_template_name, \
            "存在同名模板，如果想要覆盖，请点击[强制更新模板]按钮：" + manager_template_name, \
            "存在同名模板，如果想要覆盖，请点击[强制更新模板]按钮：" + manager_template_name
    temp_data = TemplateData(
        world_engine_init_template,
        dialog_engine_init_template,
        world_engine_update_template,
        dialog_engine_update_template,
    )
    redis_cli.set_template(manager_template_name, temp_data)

    return "生成模板成功：" + manager_template_name, \
        "生成模板成功：" + manager_template_name, \
        "生成模板成功：" + manager_template_name, \
        "生成模板成功：" + manager_template_name

