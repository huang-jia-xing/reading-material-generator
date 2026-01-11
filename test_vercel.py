"""
Vercel部署测试脚本
在Vercel部署完成后运行此脚本验证功能
"""

import requests
import time
import sys


def test_vercel_deployment(domain):
    """测试Vercel部署"""
    print(f"🔍 测试Vercel部署: {domain}")

    tests = [
        ("首页访问", f"{domain}", 200),
        ("API健康检查", f"{domain}/health", 200),
        ("前端文件", f"{domain}/index.html", 200),
        ("CSS文件", f"{domain}/style.css", 200),
    ]

    all_passed = True
    for name, url, expected_code in tests:
        try:
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code == expected_code else "❌"
            print(f"{status} {name}: {url} (状态码: {response.status_code})")
            if response.status_code != expected_code:
                all_passed = False
        except Exception as e:
            print(f"❌ {name}: {url} (错误: {e})")
            all_passed = False

    return all_passed


def test_api_function(domain):
    """测试API功能"""
    print("\n🔄 测试API功能...")

    api_url = f"{domain}/api/generate"
    test_data = {
        "leveled_texts": {
            "basic": {
                "title": "Vercel部署测试",
                "content": "这是一篇测试文章，用于验证Vercel部署是否成功。",
                "word_count": 25,
                "reading_level": "基础"
            }
        },
        "comprehension_questions": {},
        "support_materials": {},
        "core_theme": "部署测试"
    }

    try:
        response = requests.post(
            api_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            file_size = len(response.content)
            print(f"✅ API功能正常，返回文件大小: {file_size} 字节")

            # 保存测试文件
            with open("vercel_test_output.zip", "wb") as f:
                f.write(response.content)
            print("📁 测试文件已保存: vercel_test_output.zip")

            return True
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ API调用异常: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python test_vercel.py <你的Vercel域名>")
        print("示例: python test_vercel.py https://reading-material-system.vercel.app")
        return

    domain = sys.argv[1].rstrip('/')

    print("=" * 60)
    print("Vercel部署验证测试")
    print("=" * 60)

    # 测试基础访问
    if not test_vercel_deployment(domain):
        print("\n❌ 基础访问测试失败，请检查部署")
        return

    # 测试API功能
    if not test_api_function(domain):
        print("\n⚠️ API功能测试失败，可能是前端API地址未更新")
        print("请确保 frontend/script.js 中的API地址已更新为Vercel域名")
        return

    print("\n" + "=" * 60)
    print("🎉 Vercel部署验证成功！")
    print("\n下一步:")
    print(f"1. 访问 {domain} 进行手动测试")
    print("2. 测试完整的前端交互流程")
    print("3. 准备演示材料")
    print("=" * 60)


if __name__ == "__main__":
    main()