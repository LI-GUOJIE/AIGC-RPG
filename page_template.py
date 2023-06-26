from btn_create_template import create_template
from btn_force_create_template import force_create_template
from btn_search_template import search_template
import gradio as gr

# 加载模板管理页面
def load_page_template():
	with gr.Column():
		with gr.Row():
			with gr.Column():
				gr.Markdown("### 初始设置（在创建新故事时生效）\n")

				with gr.Box():
					world_engine_init_template = gr.Textbox(label="世界初始引擎", show_label=True, max_lines=12, lines=12)
					dialog_engine_init_template = gr.Textbox(label="对话初始引擎", show_label=True, max_lines=12, lines=12)
				
			with gr.Column():
				gr.Markdown("### 多轮设置（在多轮对话过程中生效）\n")

				with gr.Box():
					world_engine_update_template = gr.Textbox(label="世界更新引擎", show_label=True, max_lines=12, lines=12)
					dialog_engine_update_template = gr.Textbox(label="对话更新引擎", show_label=True, max_lines=12, lines=12)

		with gr.Row():
			manager_template_name = gr.Textbox(label="模板ID（支持中文）", show_label=True, max_lines=1, lines=1)
			btn_create_template = gr.Button("生成模板（若模板ID已存在则报错）", variant="primary")
			btn_force_create_template = gr.Button("强制更新模板", variant="primary")
			btn_search_template = gr.Button("查找模板", variant="primary")

	# 生成模板
	btn_create_template.click(
		create_template,
		inputs=[manager_template_name, world_engine_init_template, dialog_engine_init_template, world_engine_update_template, dialog_engine_update_template],
		outputs=[world_engine_init_template, dialog_engine_init_template, world_engine_update_template, dialog_engine_update_template],
	)

	# 强制更新模板
	btn_force_create_template.click(
		force_create_template,
		inputs=[manager_template_name, world_engine_init_template, dialog_engine_init_template, world_engine_update_template, dialog_engine_update_template],
		outputs=[world_engine_init_template, dialog_engine_init_template, world_engine_update_template, dialog_engine_update_template],
	)

	# 查找模板
	btn_search_template.click(
		search_template,
		inputs=[manager_template_name],
		outputs=[world_engine_init_template, dialog_engine_init_template, world_engine_update_template, dialog_engine_update_template],
	)