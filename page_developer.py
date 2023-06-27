import gradio as gr
from btn_update_developer_info import update_developer_info

# 加载玩家页面
def load_page_developer():
	with gr.Column():
		with gr.Row():
			story_id = gr.Textbox(label="故事ID（[创建新故事时]自动生成的）", show_label=True, max_lines=1, lines=1)
			btn_update_developer_info = gr.Button("更新", variant="primary")
			
		# developer_txt = gr.Textbox(label="", show_label=False, max_lines=16, lines=16)
		developer_txt = gr.Code(language="json", show_label=False)

	# 根据故事线查找对应的内容
	btn_update_developer_info.click(
		update_developer_info,
		inputs=[story_id],
		outputs=[developer_txt],
	)