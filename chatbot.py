import requests
import os
import json
import const

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
        story_id:str,
        conversations:list,
        output_query_logs:list,
    ):
        try:
            # 带超时的访问
            rsp = self.session.post(
                self.url,
                headers={"Content-Type": "application/json"},
                verify = False,
                json={
                    "auth": self.api_key,
                    "conversation": conversations,
                },
                timeout=const.default_timeout,
            )

            # 解析返回值
            for line in rsp.iter_lines():
                processed_line = json.loads(line)
                rsp = processed_line['data']['choices'][0]['message']
                rsp_content = rsp['content']

                # insert query log
                output_query_logs.append({
                        "Request to GPT": conversations,
                        "Response from GPT": rsp,
                    })
                return rsp_content, True
            
        # 超时
        except requests.Timeout:
            print(f"chatbot finish, story_id:{story_id}, response:")
            print("AI接口访问失败，响应超时")
            return "AI接口访问失败，响应超时", False
        
        # 链接异常
        except requests.ConnectionError:
            print(f"chatbot finish, story_id:{story_id}, response:")
            print("AI接口访问失败，连接错误")
            return "AI接口访问失败，连接错误", False
        
        # 其他异常
        except:
            print(f"chatbot finish, story_id:{story_id}, response:")
            print("AI接口访问失败，其他错误")
            return "AI接口访问失败，其他错误", False

# 初始化全局变量
chatbot = Chatbot(api_key=os.environ.get("API_KEY"), url=os.environ.get("API_URL"))