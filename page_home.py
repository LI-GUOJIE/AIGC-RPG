from page_player import load_page_player
from page_template import load_page_template
import gradio as gr

# 静态主页
with gr.Blocks(title="AIRPG", css="footer {visibility: hidden}", theme="default") as demo:
    with gr.Tab("模板管理页面"):
        load_page_template()
    with gr.Tab("玩家页面"):
        load_page_player()