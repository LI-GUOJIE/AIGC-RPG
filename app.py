from page_home import demo

def Run():
    # 加载静态页面
    demo.launch(debug=True, share=True, server_name="0.0.0.0", server_port=20035)

if __name__ == "__main__":
    Run()