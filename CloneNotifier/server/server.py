from flask import Flask, send_from_directory
from flask_cors import CORS

import os
import mimetypes

app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求

# 定义处理 script.js 文件的路由
@app.route('/api/script.js')
def get_script():
    # 获取当前文件所在目录的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # 使用 Flask 提供的 send_from_directory 函数发送文件
    return send_from_directory(os.path.join(base_dir, 'result', 'js'), 'script.js')

# 定义处理其他可能路径的路由，例如 /api/result/20240425/index.html
@app.route('/api/result/<path:file_path>')
def get_result_file(file_path):
    # 获取当前文件所在目录的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # 构建请求文件的完整路径
    requested_path = os.path.join(base_dir, 'result', file_path)
    # 检查文件是否存在
    if os.path.exists(requested_path):
        # 使用 Flask 提供的 send_from_directory 函数发送文件
        return send_from_directory(os.path.join(base_dir, 'result'), file_path)
    else:
        return 'File not found', 404

# 定义处理 script.js 文件的路由
@app.route('/api/diff/<path:file_path>')
def get_diff(file_path):
    # 获取当前文件所在目录的绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    # 使用 Flask 提供的 send_from_directory 函数发送文件
    return send_from_directory(os.path.join(base_dir, 'diff'), file_path, mimetype=mime_type)

if __name__ == '__main__':
    app.run(port=8080)
