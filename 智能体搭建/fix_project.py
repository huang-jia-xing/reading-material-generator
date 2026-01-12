"""
项目修复脚本 - 自动检查和修复常见问题
"""

import os
import shutil


def fix_project_structure():
    """修复项目结构"""
    print("🔧 正在检查和修复项目结构...")

    # 确保必要的目录存在
    directories = ['api', 'frontend', 'tests']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录: {directory}")

    # 检查并修复文件位置
    files_to_check = ['local_server.py', 'run_test.py']
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ 文件存在: {file}")
        else:
            print(f"❌ 文件不存在: {file}")

            # 尝试在其他位置查找
            found = False
            for root, dirs, files in os.walk('.'):
                if file in files:
                    src = os.path.join(root, file)
                    print(f"💡 在其他位置找到: {src}")
                    shutil.copy(src, file)
                    print(f"✅ 已复制到根目录: {file}")
                    found = True
                    break

            if not found:
                print(f"⚠️  未找到文件: {file}，可能需要手动创建")

    # 验证修复结果
    print("\n📋 修复后文件检查:")
    required_files = ['local_server.py', 'run_test.py', 'api/generate.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (仍不存在)")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("项目结构修复工具")
    print("=" * 60)
    fix_project_structure()
    print("=" * 60)