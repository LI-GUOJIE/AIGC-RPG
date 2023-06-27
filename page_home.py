from page_player import load_page_player
from page_template import load_page_template
from page_developer import load_page_developer
import gradio as gr

# 静态主页
with gr.Blocks(title="AIRPG", css="footer {visibility: hidden}", theme="default") as demo:
    with gr.Tab("玩家页面"):
        load_page_player()
    with gr.Tab("开发者页面"):
        load_page_developer()
    with gr.Tab("模板管理页面"):
        load_page_template()