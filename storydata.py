class StoryData:
    
    def __init__(
        self,
        player_template_name,
    ) -> None:
        self.template_id       = player_template_name  # 模板ID
        self.world_record_txt  = ''                    # 世界状态长篇记录，只增不减
        self.dialog_record_txt = ''                    # 对话长篇记录，只增不减
        self.conversation      = []                    # 会话长篇记录，只增不减
        self.latest_dialog     = []                    # 最后一轮对话，每次更新世界后清零
        self.summary           = ''                    # 世界状态摘要
        self.user_input        = ''                    # 用户输入

    def get_str_latest_dialog(self):
        result = ""
        for d in self.latest_dialog:
            result += d['content'] + '\n'
        return result