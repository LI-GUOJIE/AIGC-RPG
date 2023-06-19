from page_home import demo

def Run(port):
    # 加载静态页面
    demo.launch(debug=True, share=True, server_name="0.0.0.0", server_port=port)

if __name__ == "__main__":
    Run(20036)