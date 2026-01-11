def generate_mock_data(user_input):
    """生成模拟数据，用于演示和测试"""

    # 根据用户输入生成不同版本的内容
    original_text = user_input.get('original_text', '')
    target_grade = user_input.get('target_grade', '三年级')
    version_count = user_input.get('version_count', 3)

    # 基础版本的内容生成逻辑
    mock_data = {
        'leveled_texts': {},
        'comprehension_questions': {},
        'support_materials': {}
    }

    # 生成基础版
    if version_count >= 1:
        mock_data['leveled_texts']['basic'] = {
            'title': '基础阅读材料',
            'content': generate_basic_version(original_text),
            'word_count': len(generate_basic_version(original_text)),
            'reading_level': '基础'
        }

        mock_data['comprehension_questions']['basic_questions'] = [
            {
                'question': '这篇文章主要讲了什么？',
                'type': 'choice',
                'options': ['选项A', '选项B', '正确答案', '选项D'],
                'answer': '正确答案',
                'explanation': '从文章第一句可以找到答案。'
            }
        ]

        mock_data['support_materials']['basic_materials'] = {
            'vocabulary_list': [
                {
                    'word': '重要',
                    'pinyin': "zhong yao",
                    'definition': '具有重大意义的',
                    'example': '这是一个重要的决定。'
                }
            ],
            'task_card': {
                'reading_goals': ['理解文章大意', '找出关键信息'],
                'mind_map_structure': '中心主题 → 主要事件 → 重要人物',
                'reading_strategies': ['先看标题', '找出关键词']
            }
        }

    # 生成标准版
    if version_count >= 2:
        mock_data['leveled_texts']['standard'] = {
            'title': '标准阅读材料',
            'content': generate_standard_version(original_text),
            'word_count': len(generate_standard_version(original_text)),
            'reading_level': '标准'
        }

        mock_data['comprehension_questions']['standard_questions'] = [
            {
                'question': '作者通过这篇文章想表达什么？',
                'type': 'short_answer',
                'answer': '参考答案：作者想表达...',
                'explanation': '需要从文章整体来理解作者的意图。'
            }
        ]

        mock_data['support_materials']['standard_materials'] = {
            'vocabulary_list': [
                {
                    'word': '表达',
                    'pinyin': 'biǎo dá',
                    'definition': '表示思想、感情',
                    'example': '他用文字表达情感。'
                }
            ],
            'task_card': {
                'reading_goals': ['分析文章结构', '理解作者意图'],
                'mind_map_structure': '中心思想 → 分论点 → 论据 → 结论',
                'reading_strategies': ['边读边做笔记', '分析段落关系']
            }
        }

    # 生成挑战版
    if version_count >= 3:
        mock_data['leveled_texts']['advanced'] = {
            'title': '挑战阅读材料',
            'content': generate_advanced_version(original_text),
            'word_count': len(generate_advanced_version(original_text)),
            'reading_level': '挑战'
        }

        mock_data['comprehension_questions']['advanced_questions'] = [
            {
                'question': '结合你的生活经验，谈谈对这篇文章的看法。',
                'type': 'open_ended',
                'answer': '参考答案：这篇文章让我想到...',
                'explanation': '这是一个开放性问题，鼓励学生联系实际。'
            }
        ]

        mock_data['support_materials']['advanced_materials'] = {
            'vocabulary_list': [
                {
                    'word': '深刻',
                    'pinyin': 'shēn kè',
                    'definition': '达到事情本质的',
                    'example': '他的见解很深刻。'
                }
            ],
            'task_card': {
                'reading_goals': ['批判性思考', '联系实际应用'],
                'mind_map_structure': '主题 → 分析 → 评价 → 应用',
                'reading_strategies': ['批判性阅读', '与已有知识联系']
            }
        }

    return mock_data


def generate_basic_version(text):
    """生成基础版本文本"""
    # 简化文本，使用短句
    sentences = text.split('。')
    simplified = []
    for sentence in sentences[:3]:  # 只取前3句
        if sentence.strip():
            simplified.append(sentence.strip() + '。')

    return ' '.join(simplified)[:200]  # 限制长度


def generate_standard_version(text):
    """生成标准版本文本"""
    return text[:400]  # 保持原样，限制长度


def generate_advanced_version(text):
    """生成挑战版本文本"""
    # 增加一些复杂词汇和句式
    enhanced = text
    replacements = {
        '的': '之',
        '和': '与',
        '因为': '由于',
        '所以': '因此'
    }

    for old, new in replacements.items():
        enhanced = enhanced.replace(old, new)

    return enhanced[:600]