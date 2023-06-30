import requests
import os
import json
import const
import copy

# 参考revertGPT构造Chatbot
class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str,
    ) -> None:
        self.api_key: str = api_key
        self.session = requests.Session()
        
    # 最简单的查询
    def query(
        self,
        story_id:str,
        conversations:list,
        is_davinci:bool,
        output_query_logs:list,
    ):
        try:
            # 使用davinci模型
            if is_davinci:

                # 转换语句
                query_convs = ""
                for conv in conversations:
                    query_convs += conv['content'] + '\n'

                # 带超时的访问
                rsp = self.session.post(
                    os.environ.get("API_DAVINCI_URL"),
                    headers={"Content-Type": "application/json"},
                    verify = False,
                    json={
                        "auth": self.api_key,
                        "conversation": query_convs,
                    },
                    timeout=const.default_timeout,
                )

                # 解析返回值
                for line in rsp.iter_lines():
                    processed_line = json.loads(line)
                    rsp_content = processed_line['data']['choices'][0]['text']

                    # insert query log
                    output_query_logs.append({
                            "Request to GPT": copy.deepcopy(query_convs),
                            "Response from GPT": rsp_content,
                        })
                    return rsp_content, True
            else:

                # 带超时的访问
                rsp = self.session.post(
                    os.environ.get("API_TURBO_URL"),
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
                            "Request to GPT": copy.deepcopy(conversations),
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
        except Exception as errInfo:
            print(f"chatbot finish, story_id:{story_id}, response:")
            print("AI接口访问失败，其他错误, errInfo:")
            print(errInfo)
            return "AI接口访问失败，字数太多，或其他原因", False

# 初始化全局变量
chatbot = Chatbot(api_key=os.environ.get("API_KEY"))