# 分层阅读材料生成系统

专为港澳小学教师设计的分层阅读材料生成工具。

## 功能特点

- 一键生成分层阅读材料（基础版、标准版、挑战版）
- 自动生成Word文档和配套练习
- 完全免费，无需注册
- 支持本地保存常用主题

## 使用方法

1. 访问系统网址：https://your-vercel-app.vercel.app
2. 输入原文或主题
3. 选择年级和版本数量
4. 点击生成，等待片刻
5. 下载生成的ZIP文件

## 本地开发

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行本地测试：`python tests/test_local.py`
4. 启动本地服务器：`python local_server.py`
5. 打开frontend/index.html

## 部署

使用Vercel一键部署。

## 技术栈

- 前端：HTML, CSS, JavaScript
- 后端：Python (Flask), Vercel Serverless Functions
- AI：Coze工作流

## 许可证

仅供教育使用。