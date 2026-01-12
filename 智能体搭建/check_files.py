"""
文件存在性验证脚本
运行此脚本检查所有必需文件
"""

import os
import sys


def check_project_structure():
    """检查项目结构"""
    print("🔍 检查项目文件结构...")

    # 定义必需的文件和目录
    required_files = [
        ('run_test.py', '测试脚本'),
        ('local_server.py', '本地服务器'),
        ('requirements.txt', '依赖文件'),
        ('vercel.json', '部署配置'),
        ('package.json', 'Node.js配置'),
        ('api/generate.py', 'API核心代码'),
        ('frontend/index.html', '前端主界面'),
        ('frontend/style.css', '前端样式'),
        ('frontend/script.js', '前端脚本')
    ]

    all_exist = True
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (未找到)")
            all_exist = False

    return all_exist


def get_current_directory_info():
    """获取当前目录信息"""
    print("\n📁 当前工作目录信息:")
    print(f"工作目录: {os.getcwd()}")

    # 列出所有Python文件
    print("\nPython文件列表:")
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    for file in py_files:
        print(f"  - {file}")

    # 列出目录
    print("\n目录列表:")
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    for d in dirs:
        print(f"  - {d}/")


if __name__ == "__main__":
    print("=" * 60)
    print("项目文件完整性检查")
    print("=" * 60)

    get_current_directory_info()
    print("\n" + "=" * 60)

    success = check_project_structure()

    if success:
        print("\n🎉 所有必需文件都存在！")
        print("\n下一步建议:")
        print("1. 运行测试: python run_test.py")
        print("2. 启动服务器: python local_server.py")
        print("3. 创建GitHub仓库")
    else:
        print("\n⚠️ 缺少一些文件，请创建缺失的文件")

    print("=" * 60)