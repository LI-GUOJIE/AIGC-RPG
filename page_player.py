from btn_search_story import search_story
from btn_new_story import new_story
from btn_update_dialog import update_dialog
from btn_update_world import update_world
import gradio as gr

# 加载玩家页面
def load_page_player():
	with gr.Column():
		with gr.Row():
			with gr.Box():
				player_template_name = gr.Textbox(label="模板ID（管理员预设的)", show_label=True, max_lines=1, lines=1)
				btn_new_story = gr.Button("创建新故事", variant="primary")
				
			with gr.Box():
				story_id = gr.Textbox(label="故事ID（[创建新故事时]自动生成的）", show_label=True, max_lines=1, lines=1)
				btn_search_story = gr.Button("续写故事", variant="primary")
						
		with gr.Row():
			with gr.Box():
				world_record_txt = gr.Textbox(label="世界状态记录", show_label=True, max_lines=25, lines=25)
				btn_update_world = gr.Button("更新到世界记录", variant="primary")
				
			with gr.Column():
				dialog_record_txt = gr.Textbox(label="对话记录", show_label=True, max_lines=20, lines=20)

				with gr.Box():
					gr.Markdown("### 用户输入\n")
					dialog_input = gr.Textbox(show_label=False, max_lines=1, lines=1)
					btn_update_dialog = gr.Button("发送", variant="primary")

	# 创新新故事
	btn_new_story.click(
		new_story,
		inputs=[player_template_name],
		outputs=[story_id, world_record_txt, dialog_record_txt],
	)              

	# 根据故事线找回所有内容，包括模板和状态记录
	btn_search_story.click(
		search_story,
		inputs=[story_id],
		outputs=[player_template_name, world_record_txt, dialog_record_txt],
	)              

	# 更新世界状态
	btn_update_world.click(
		update_world,
		inputs=[story_id],
		outputs=[world_record_txt, dialog_record_txt],
	)         

	# 发送用户输入内容
	btn_update_dialog.click(
		update_dialog,
		inputs=[story_id, dialog_input],
		outputs=[dialog_record_txt],
	)