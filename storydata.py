from chatbot import chatbot
from template import Template
import const

class StoryData:
    
    def __init__(
        self,
        player_template_name,
        temp_data:Template,
    ) -> None:
        self.template_id       = player_template_name  # 模板ID
        self.temp_data         = temp_data             # 模板数据
        self.world_record_txt  = ''                    # 世界状态长篇记录，只增不减
        self.dialog_record_txt = ''                    # 对话长篇记录，只增不减
        self.conversation      = []                    # 会话长篇记录，只增不减
        self.latest_dialog     = ''                    # 最新一轮对话内容
        self.summary           = ''                    # 世界状态摘要，每次世界状态发生变动后更新
        

    # 检查token是否达到上限()
    def is_token_touch_limit(self) -> bool:
        return len(self.world_record_txt) > const.default_token_limit
    

    # 更新摘要
    def update_summary(self, world_news):

        # 组织报文。如果有summary，说明不是第一次调用，直接用summary
        if len(self.summary) > 0:
            prompt = "【世界】\n" + self.summary + '\n\n'
        else:
            prompt = "" + self.world_record_txt + '\n\n'
        prompt += "【世界新闻】\n" + world_news + '\n\n'
        prompt += const.default_summary_template

        # 发送请求
        response = chatbot.query([{
            'role': 'system',
            'content': prompt
        }])

        # 更新摘要
        self.summary = response


    # 替换模板中的关键词
    def replace_key_words(self, prompt):
        prompt = prompt.replace("{世界摘要}", self.summary)
        prompt = prompt.replace("{最近一轮对话}", self.latest_dialog)
        return prompt

    
    # 利用摘要发起查询
    def query_with_summary(self, temp) -> str:

        # 记录 input to ChatGPT
        temp = self.replace_key_words(temp)
        self.conversation.append({'role': 'system',
                                  'content': temp})
        
        # 如果接近token上限，改用摘要
        conversations = self.conversation
        if self.is_token_touch_limit():

            # 组织摘要 【世界】+【对话（如果存在）】+【模板】
            prompt = "【世界】\n" + self.summary + '\n\n'
            if len(self.latest_dialog) > 0:
                prompt += "【对话】\n" + self.latest_dialog + '\n\n'
            prompt += temp

            # 使用新的方式
            conversations = [{
                        'role': 'system',
                        'content': prompt
                    }]
            
        # 发送请求
        print("query_with_summary conversations:")
        print(conversations)
        response = chatbot.query(conversations)

        # 记录 ouput from ChatGPT
        print("query_with_summary response:")
        print(response)
        self.conversation.append({'role': 'assistant',
                                'content': response})
    
        return response
        
    # 调用世界初始引擎
    def new_story(self):

        # ======================================= 生成初始世界状态 =======================================
        # 记录 input to ChatGPT
        self.conversation = [{'role': 'system',
                              'content': self.replace_key_words(self.temp_data.world_engine_init_template)}]

        # 生成世界初始状态
        self.world_record_txt = chatbot.query(self.conversation)

        # 更新摘要
        if self.is_token_touch_limit():
            self.update_summary(self.world_record_txt)

        # 记录 ouput from ChatGPT
        self.conversation.append({'role': 'assistant',
                                  'content': self.world_record_txt})

        # ======================================= 生成初始对话内容 =======================================
        # 记录 input to ChatGPT
        self.conversation.append({'role': 'system',
                                  'content': self.replace_key_words(self.temp_data.dialog_engine_init_template)})

        # 生成初始的NPC向玩家打招呼的内容
        self.dialog_record_txt = chatbot.query(self.conversation)

        # 记录 ouput from ChatGPT
        self.conversation.append({'role': 'assistant',
                                  'content': self.dialog_record_txt})

        # 新的一轮对话开始
        self.latest_dialog = self.dialog_record_txt


    # 更新对话
    def update_dialog(self, user_input):

        # 记录 input to ChatGPT
        self.conversation.append({'role': 'user',
                                  'content': user_input}) 

        # 将用户发言插入到对话记录、新一轮对话中
        self.dialog_record_txt += '\n' + user_input
        self.latest_dialog += '\n' + user_input

        # 调用对话更新引擎
        response = self.query_with_summary(self.temp_data.dialog_engine_update_template)
        
        # 将NPC发言插入到对话记录、新一轮对话中
        self.dialog_record_txt += '\n' + response
        self.latest_dialog += '\n' + response


    # 更新世界
    def update_world(self):

        # ======================================= 更新世界状态 =======================================
        # 调用世界更新引擎
        response = self.query_with_summary(self.temp_data.world_engine_update_template)

        # 将新的剧情插入到世界记录
        self.world_record_txt += '\n\n' + response

        # 更新摘要
        if self.is_token_touch_limit():
            self.update_summary(response)

        # ======================================= 重启多轮对话 =======================================
        # 清除上一轮对话
        self.latest_dialog = ""

        # 调用对话更新引擎
        response = self.query_with_summary(self.temp_data.dialog_engine_update_template)

        # 将NPC发言插入到对话记录中
        self.dialog_record_txt += '\n\n' + response

        # 新的一轮对话开始
        self.latest_dialog = response

