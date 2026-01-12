"""
本地开发服务器 - 优化修复版
用于测试和演示
"""

from flask import Flask, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 导入文件生成模块 - 修复变量定义问题
try:
    from api.generate import generate_reading_materials
    GENERATE_FUNCTION_AVAILABLE = True
    print("✅ 成功导入文件生成模块")
except ImportError as import_error:
    print(f"❌ 导入失败: {import_error}")
    print("请在项目根目录运行此脚本")
    # 在except块中定义变量，避免未定义错误
    GENERATE_FUNCTION_AVAILABLE = False
    generate_reading_materials = None

@app.route('/')
def home():
    """主页"""
    return """
    <html>
    <head>
        <title>分层阅读系统 - 本地服务器</title>
        <style>
            body { font-family: 'Microsoft JhengHei', sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #f5f7fa; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .btn { display: inline-block; background: #4a6fa5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 分层阅读材料生成系统 - 本地服务器</h1>
            
            <div class="card">
                <h2>✅ 服务器运行正常</h2>
                <p>本地API服务器已启动并正在运行。</p>
                <p><strong>API端点：</strong> http://localhost:5000/api/generate</p>
                <p><strong>前端页面：</strong> <code>frontend/index.html</code></p>
            </div>
            
            <div class="card">
                <h2>📚 使用说明</h2>
                <ol>
                    <li>用浏览器打开 <strong>frontend/index.html</strong> 文件</li>
                    <li>在界面中输入教学主题</li>
                    <li>点击生成按钮</li>
                    <li>系统会自动调用本地API生成文件</li>
                </ol>
            </div>
            
            <div class="card">
                <h2>🔧 快速测试</h2>
                <p>点击下方按钮测试API功能：</p>
                <a href="/test" class="btn">测试API</a>
            </div>
            
            <div class="card">
                <h2>⚠️ 注意事项</h2>
                <ul>
                    <li>确保已安装依赖：<code>pip install -r requirements.txt</code></li>
                    <li>如果前端无法连接，请检查浏览器控制台</li>
                    <li>生成的文件会自动下载到浏览器默认下载目录</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/test')
def test_page():
    """测试页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API测试</title>
        <script>
            async function testAPI() {
                const testData = {
                    leveled_texts: {
                        basic: {
                            title: "测试文章",
                            content: "这是一个测试内容。",
                            word_count: 5,
                            reading_level: "基础"
                        }
                    },
                    comprehension_questions: {},
                    support_materials: {},
                    core_theme: "测试"
                };
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(testData)
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'test_output.zip';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        alert('✅ API测试成功！文件已下载');
                    } else {
                        const errorText = await response.text();
                        alert('❌ API测试失败: ' + response.status + ' - ' + errorText);
                    }
                } catch (error) {
                    alert('❌ 请求失败: ' + error.message);
                }
            }
        </script>
    </head>
    <body>
        <h1>API功能测试</h1>
        <button onclick="testAPI()">测试API生成文件</button>
        <br><br>
        <a href="/">返回主页</a>
    </body>
    </html>
    """

@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate():
    """API端点：生成阅读材料"""
    if request.method == 'OPTIONS':
        # 处理预检请求
        return '', 200

    try:
        # 检查生成功能是否可用
        if not GENERATE_FUNCTION_AVAILABLE or generate_reading_materials is None:
            return {'error': '文件生成模块未正确加载'}, 500

        # 获取请求数据
        data = request.get_json()
        print(f"📥 收到生成请求，主题: {data.get('core_theme', '未知')}")

        if not data:
            return {'error': '没有提供数据'}, 400

        # 生成文件
        print("🔄 正在生成文件...")
        zip_data = generate_reading_materials(data)
        print(f"✅ 文件生成完成，大小: {len(zip_data)} 字节")

        # 保存到临时文件（用于调试）
        temp_file = "temp_generated.zip"
        with open(temp_file, "wb") as f:
            f.write(zip_data)
        print(f"💾 临时文件保存至: {temp_file}")

        # 返回文件
        return send_file(
            temp_file,
            as_attachment=True,
            download_name='分层阅读材料.zip',
            mimetype='application/zip'
        )

    except Exception as exception:
        print(f"❌ 生成失败: {exception}")
        import traceback
        traceback.print_exc()
        return {'error': str(exception)}, 500

@app.route('/health')
def health():
    """健康检查端点"""
    return {'status': 'healthy', 'service': 'reading-material-generator'}

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 启动分层阅读材料生成系统 - 本地服务器")
    print("=" * 60)
    print("📁 工作目录:", os.getcwd())
    print("🌐 服务器地址: http://localhost:5000")
    print("🔌 API端点: http://localhost:5000/api/generate")
    print("📚 前端文件: frontend/index.html")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)

    # 启动服务器
    app.run(debug=True, host='0.0.0.0', port=5000)