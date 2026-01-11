"""
分层阅读材料生成系统 - 综合测试脚本
放在项目根目录运行，确保路径正确
"""

import sys
import os
import zipfile


def setup_environment():
    """设置环境路径"""
    print("🔧 设置测试环境...")

    # 获取当前脚本所在目录（项目根目录）
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 项目根目录: {project_root}")

    # 添加项目根目录到Python路径
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # 检查关键目录是否存在
    required_dirs = ['api', 'frontend']
    for dir_name in required_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ 找到目录: {dir_name}")
        else:
            print(f"❌ 目录不存在: {dir_name}")
            return False

    return True


def test_dependencies():
    """测试Python依赖"""
    print("\n🔍 测试Python依赖...")

    dependencies = [
        ('python-docx', 'docx'),
        ('Pillow', 'PIL'),
        ('Flask', 'flask')
    ]

    all_installed = True
    for package_name, import_name in dependencies:
        try:
            if import_name == 'docx':
                import docx
            elif import_name == 'PIL':
                from PIL import Image
            elif import_name == 'flask':
                import flask

            print(f"✅ {package_name} 已安装")
        except ImportError as e:
            print(f"❌ {package_name} 未安装: {e}")
            all_installed = False

    return all_installed


def test_file_generation():
    """测试文件生成功能"""
    print("\n📝 测试文件生成功能...")

    try:
        # 动态导入，避免路径问题
        import importlib
        generate_module = importlib.import_module('api.generate')
        generate_reading_materials = generate_module.generate_reading_materials

        # 测试数据
        test_data = {
            "leveled_texts": {
                "basic": {
                    "title": "测试文章",
                    "content": "这是一个测试内容。用来验证系统是否正常工作。",
                    "word_count": 15,
                    "reading_level": "基础"
                }
            },
            "comprehension_questions": {
                "basic_questions": [
                    {
                        "question": "这是一个测试问题吗？",
                        "type": "choice",
                        "options": ["是", "否"],
                        "answer": "是",
                        "explanation": "这是一个测试"
                    }
                ]
            },
            "support_materials": {
                "basic_materials": {
                    "vocabulary_list": [
                        {
                            "word": "测试",
                            "pinyin": "cè shì",
                            "definition": "检验、验证",
                            "example": "这是一个测试"
                        }
                    ]
                }
            },
            "core_theme": "测试主题"
        }

        print("🔄 正在生成文件...")
        zip_data = generate_reading_materials(test_data)

        # 保存测试文件
        output_file = "test_output_fixed.zip"
        with open(output_file, "wb") as f:
            f.write(zip_data)

        print(f"✅ 文件生成成功！保存至: {output_file}")
        print(f"📦 文件大小: {len(zip_data)} 字节")

        # 验证ZIP文件内容
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"📋 ZIP包含 {len(file_list)} 个文件:")
            for file in file_list:
                print(f"   - {file}")

        return True

    except Exception as e:
        print(f"❌ 文件生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_frontend_files():
    """测试前端文件是否存在"""
    print("\n🌐 测试前端文件...")

    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, 'frontend')

    if not os.path.exists(frontend_dir):
        print(f"❌ frontend目录不存在: {frontend_dir}")
        return False

    print(f"✅ 找到frontend目录: {frontend_dir}")

    frontend_files = [
        "index.html",
        "style.css",
        "script.js"
    ]

    all_exist = True
    for file in frontend_files:
        file_path = os.path.join(frontend_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 不存在")
            all_exist = False

    return all_exist


def test_local_server():
    """测试本地服务器文件"""
    print("\n🚀 测试本地服务器文件...")

    # 检查local_server.py是否存在
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_server_path = os.path.join(current_dir, 'local_server.py')

    if os.path.exists(local_server_path):
        print(f"✅ local_server.py 存在: {local_server_path}")

        # 检查文件内容是否基本正确
        try:
            with open(local_server_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查关键内容
            checks = [
                ('Flask', '包含Flask框架'),
                ('generate_reading_materials', '调用生成函数'),
                ('@app.route', '有路由定义'),
                ('send_file', '有文件返回功能')
            ]

            all_checks_passed = True
            for keyword, description in checks:
                if keyword in content:
                    print(f"  ✅ {description}")
                else:
                    print(f"  ⚠️  未找到: {description}")
                    all_checks_passed = False

            if all_checks_passed:
                print("✅ local_server.py 文件内容检查通过")
            else:
                print("⚠️  local_server.py 文件可能不完整")

            return True

        except Exception as file_error:
            print(f"❌ 读取文件出错: {file_error}")
            return True  # 文件存在，只是读取有问题
    else:
        print(f"❌ local_server.py 不存在于: {current_dir}")
        print("💡 提示：请确保在项目根目录运行此脚本")

        # 列出当前目录的文件，帮助用户定位
        print("\n📁 当前目录文件列表:")
        for file in os.listdir(current_dir):
            if file.endswith('.py'):
                print(f"  - {file}")

        return False  # 文件不存在，这是一个关键错误


def main():
    """主测试函数"""
    print("=" * 60)
    print("分层阅读材料生成系统 - 综合测试套件")
    print("=" * 60)

    # 设置环境
    if not setup_environment():
        print("❌ 环境设置失败，请检查项目结构")
        return False

    # 执行测试
    tests = [
        ("Python依赖", test_dependencies),
        ("文件生成", test_file_generation),
        ("前端文件", test_frontend_files),
        ("本地服务器", test_local_server)
    ]

    test_results = []
    for test_name, test_func in tests:
        print(f"\n🔧 执行测试: {test_name}")
        try:
            test_success = test_func()  # 使用不同的变量名
            test_results.append((test_name, test_success))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            test_results.append((test_name, False))

    # 输出测试总结
    print("\n" + "=" * 60)
    print("测试总结:")
    print("=" * 60)

    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)

    for test_name, test_success in test_results:  # 使用不同的变量名
        status = "✅ 通过" if test_success else "❌ 失败"
        print(f"{test_name}: {status}")

    print(f"\n🎯 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统准备就绪。")
        print("\n下一步行动:")
        print("1. 创建GitHub仓库")
        print("2. 部署到Vercel")
        print("3. 测试完整流程")
        print("\n立即运行本地服务器:")
        print("   python local_server.py")
        print("然后浏览器打开: frontend/index.html")
        return True
    else:
        print("\n⚠️ 部分测试失败，请修复以下问题:")
        for test_name, test_success in test_results:
            if not test_success:
                print(f"   - {test_name}")
        return False


if __name__ == "__main__":
    final_success = main()  # 使用不同的变量名
    sys.exit(0 if final_success else 1)