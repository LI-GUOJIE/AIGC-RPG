import requests
import os
import json
import utils
from storydata import StoryData

# 参考revertGPT构造Chatbot
class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str,
        url: str,
    ) -> None:
        self.api_key: str = api_key
        self.url: str = url
        self.session = requests.Session()

    def ask(
        self,
        story_data:StoryData,
        role,
        prompt,
    ):
        """
        Ask a question
        """

        # Add conversation（会话历史仅用于备份）
        final_prompt = utils.replace_key_words(prompt, story_data)
        story_data.conversation.append({"role": role,"content": final_prompt})
        print("final_prompt:")
        print(final_prompt)
        print("story_data.conversation:")
        print(story_data.conversation)

        # Get response
        rsp = self.session.post(
            self.url,
            headers={"Content-Type": "application/json"},
            verify = False,
            json={
                "auth": self.api_key,
                "conversation": [{"role": role,"content": final_prompt}],
            },
        )
        print("response:")
        print(rsp)

        try:
            for line in rsp.iter_lines():

                # 解析数据
                processed_line = json.loads(line)
                print("processed_line:")
                print(processed_line)

                rsp = processed_line['data']['choices'][0]['message']
                rsp_role = rsp['role']
                rsp_content = rsp['content']

                # 保存结果到对话
                story_data.conversation.append({"role": rsp_role,"content": rsp_content})
                return rsp_content
        except:
            return "AI模型提供方发生报错"

# 初始化全局变量
chatbot = Chatbot(api_key=os.environ.get("API_KEY"), url=os.environ.get("API_URL"))