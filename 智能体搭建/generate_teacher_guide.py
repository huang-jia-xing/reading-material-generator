def generate_teacher_guide(data):
    """生成教师指南，返回Word文档的二进制数据"""
    if not HAS_DOCX or Document is None:
        # 备用方案：返回纯文本
        guide_text = f"""
教师使用指南

生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
主题：{data.get('core_theme', '自定义主题')}

使用建议：
1. 根据学生阅读水平分配合适版本
2. 鼓励学生挑战更高难度版本
3. 使用配套问题进行阅读评估
"""
        return guide_text.encode('utf-8')

    try:
        doc = Document()
        doc.add_heading('教师使用指南', 0)

        # 添加基本信息
        doc.add_heading('一、课程信息', level=1)
        doc.add_paragraph(f'生成时间：{datetime.now().strftime("%Y年%m月%d日 %H:%M")}')
        doc.add_paragraph(f'主题：{data.get("core_theme", "自定义主题")}')

        # 添加使用建议
        doc.add_heading('二、使用建议', level=1)
        doc.add_heading('1. 分组教学', level=2)
        doc.add_paragraph('基础版：适合阅读困难的学生', style='List Bullet')
        doc.add_paragraph('标准版：适合大多数学生', style='List Bullet')
        doc.add_paragraph('挑战版：适合阅读能力强的学生', style='List Bullet')

        doc.add_heading('2. 教学流程', level=2)
        doc.add_paragraph('课前：分发适合学生水平的阅读材料', style='List Bullet')
        doc.add_paragraph('课中：组织小组讨论，鼓励学生分享', style='List Bullet')
        doc.add_paragraph('课后：使用配套问题进行评估', style='List Bullet')

        doc.add_heading('3. 差异化策略', level=2)
        doc.add_paragraph('允许学生根据自己的进度选择材料', style='List Bullet')
        doc.add_paragraph('鼓励完成基础版的学生尝试挑战版', style='List Bullet')
        doc.add_paragraph('组织跨版本的小组合作', style='List Bullet')

        doc.add_heading('4. 评估建议', level=2)
        doc.add_paragraph('使用配套的阅读理解问题', style='List Bullet')
        doc.add_paragraph('观察学生在讨论中的表现', style='List Bullet')
        doc.add_paragraph('鼓励学生进行自我评估', style='List Bullet')

        # 注意事项
        doc.add_heading('三、注意事项', level=1)
        doc.add_paragraph('1. 建议教师先阅读所有版本的材料', style='List Bullet')
        doc.add_paragraph('2. 根据学生的实际反应调整教学策略', style='List Bullet')
        doc.add_paragraph('3. 鼓励学生提出问题，激发思考', style='List Bullet')

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        print(f"生成教师指南失败: {e}")
        # 返回纯文本备用
        guide_text = f"教师指南生成失败，错误信息：{str(e)}"
        return guide_text.encode('utf-8')