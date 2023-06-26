class TemplateData:
    
    def __init__(
        self,
        temp_name:str,
        world_engine_init_template:str,
        dialog_engine_init_template:str,
        world_engine_update_template:str,
        dialog_engine_update_template:str,
    ) -> None:
        self.temp_name                      = temp_name                        # 模板名称
        self.world_engine_init_template     = world_engine_init_template       # 世界初始引擎
        self.dialog_engine_init_template    = dialog_engine_init_template      # 对话初始引擎
        self.world_engine_update_template   = world_engine_update_template     # 世界更新引擎
        self.dialog_engine_update_template  = dialog_engine_update_template    # 对话更新引擎