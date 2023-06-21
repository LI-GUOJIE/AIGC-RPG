import requests
import os
import json

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
        
    # 最简单的查询
    def query(
        self,
        conversations,
    ):
        rsp = self.session.post(
            self.url,
            headers={"Content-Type": "application/json"},
            verify = False,
            json={
                "auth": self.api_key,
                "conversation": conversations,
            },
        )
        try:
            for line in rsp.iter_lines():
                processed_line = json.loads(line)
                rsp = processed_line['data']['choices'][0]['message']
                rsp_content = rsp['content']
                return rsp_content
        except:
            return "AI模型提供方发生报错"

# 初始化全局变量
chatbot = Chatbot(api_key=os.environ.get("API_KEY"), url=os.environ.get("API_URL"))