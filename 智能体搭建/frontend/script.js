// frontend/script.js
// 分层阅读材料生成系统 - 前端交互逻辑

// ==================== 使用限制管理器 ====================
const UsageManager = {
    MAX_USES_PER_DAY: 10,
    MAX_USES_PER_MONTH: 50,

    checkUsage: function() {
        const today = new Date().toISOString().split('T')[0];
        const month = new Date().toISOString().substring(0, 7);

        const todayCount = localStorage.getItem(`usage_${today}`) || 0;
        const monthCount = localStorage.getItem(`usage_${month}`) || 0;

        if (todayCount >= this.MAX_USES_PER_DAY) {
            return {
                allowed: false,
                reason: '今日使用次数已达上限（10次），请明天再试或联系管理员获取更多次数。'
            };
        }

        if (monthCount >= this.MAX_USES_PER_MONTH) {
            return {
                allowed: false,
                reason: '本月使用次数已达上限（50次），请联系管理员获取更多使用权限。'
            };
        }

        return { allowed: true };
    },

    recordUsage: function() {
        const today = new Date().toISOString().split('T')[0];
        const month = new Date().toISOString().substring(0, 7);

        const todayCount = parseInt(localStorage.getItem(`usage_${today}`) || '0');
        const monthCount = parseInt(localStorage.getItem(`usage_${month}`) || '0');

        localStorage.setItem(`usage_${today}`, todayCount + 1);
        localStorage.setItem(`usage_${month}`, monthCount + 1);

        // 更新显示
        this.updateUsageDisplay();
    },

    updateUsageDisplay: function() {
        const today = new Date().toISOString().split('T')[0];
        const month = new Date().toISOString().substring(0, 7);

        const todayCount = localStorage.getItem(`usage_${today}`) || 0;
        const monthCount = localStorage.getItem(`usage_${month}`) || 0;

        const usageDisplay = document.getElementById('usageDisplay');
        if (usageDisplay) {
            usageDisplay.innerHTML = `
                <small>今日已用: ${todayCount}/${this.MAX_USES_PER_DAY} | 本月已用: ${monthCount}/${this.MAX_USES_PER_MONTH}</small>
            `;
        }
    }
};

// ==================== 主题管理器（本地存储） ====================
const ThemeManager = {
    saveTheme: function(title, content, grade) {
        const themes = JSON.parse(localStorage.getItem('saved_themes') || '[]');
        themes.push({
            title: title || '未命名主题',
            content,
            grade,
            date: new Date().toLocaleString('zh-HK'),
            id: Date.now() // 使用时间戳作为唯一ID
        });

        // 最多保存10个主题
        if (themes.length > 10) {
            themes.shift();
        }

        localStorage.setItem('saved_themes', JSON.stringify(themes));
        this.updateThemeList();
        return true;
    },

    loadThemes: function() {
        return JSON.parse(localStorage.getItem('saved_themes') || '[]');
    },

    deleteTheme: function(id) {
        let themes = this.loadThemes();
        themes = themes.filter(theme => theme.id !== id);
        localStorage.setItem('saved_themes', JSON.stringify(themes));
        this.updateThemeList();
    },

    updateThemeList: function() {
        const themeList = document.getElementById('themeList');
        if (!themeList) return;

        const themes = this.loadThemes();

        if (themes.length === 0) {
            themeList.innerHTML = '<div class="empty-state">暂无保存的主题</div>';
            return;
        }

        let html = '<div class="theme-list-header">已保存的主题：</div>';
        themes.forEach(theme => {
            html += `
                <div class="theme-item" data-id="${theme.id}">
                    <div class="theme-title">${theme.title}</div>
                    <div class="theme-info">
                        <span>${theme.grade}</span>
                        <span>${theme.date}</span>
                    </div>
                    <div class="theme-actions">
                        <button onclick="ThemeManager.useTheme(${theme.id})" class="btn-small btn-primary">使用</button>
                        <button onclick="ThemeManager.deleteTheme(${theme.id})" class="btn-small btn-danger">删除</button>
                    </div>
                </div>
            `;
        });

        themeList.innerHTML = html;
    },

    useTheme: function(id) {
        const themes = this.loadThemes();
        const theme = themes.find(t => t.id === id);

        if (theme) {
            document.getElementById('originalText').value = theme.content;
            document.getElementById('targetGrade').value = theme.grade;

            // 滚动到顶部
            document.querySelector('.input-section').scrollIntoView({ behavior: 'smooth' });

            // 显示成功提示
            alert(`已加载主题：${theme.title}`);
        }
    }
};

// ==================== API调用管理器 ====================
const APIManager = {
    // 测试模式下，使用模拟数据
    TEST_MODE: true,

    // API配置
    config: {
        local: 'http://localhost:5000/api/generate',
        vercel: 'https://your-project.vercel.app/api/generate'
    },

    // 获取当前API地址
    getApiUrl: function() {
        if (this.TEST_MODE || window.location.hostname === 'localhost') {
            return this.config.local;
        }
        return this.config.vercel;
    },

    // 调用后端API
    callBackendAPI: async function(data) {
        try {
            const response = await fetch(this.getApiUrl(), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/zip'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API请求失败 (${response.status}): ${errorText}`);
            }

            return await response.blob();

        } catch (error) {
            console.error('API调用错误:', error);

            // 如果是本地开发，提供友好提示
            if (this.getApiUrl().includes('localhost')) {
                throw new Error('无法连接到本地服务器。请确保已运行：python local_server.py');
            }

            throw error;
        }
    },

    // 模拟Coze API调用（实际使用时需要替换）
    callCozeAPI: async function(data) {
        // 模拟延迟
        await new Promise(resolve => setTimeout(resolve, 1500));

        // 模拟返回的数据结构
        return {
            leveled_texts: {
                basic: {
                    title: `${data.target_grade} - ${data.original_text.substring(0, 20)}...`,
                    content: this.generateSimulatedContent(data.original_text, 'basic'),
                    word_count: Math.floor(data.original_text.length * 0.7),
                    reading_level: '基础'
                },
                standard: {
                    title: `${data.target_grade} - ${data.original_text.substring(0, 20)}...`,
                    content: this.generateSimulatedContent(data.original_text, 'standard'),
                    word_count: data.original_text.length,
                    reading_level: '标准'
                },
                advanced: {
                    title: `${data.target_grade} - ${data.original_text.substring(0, 20)}...`,
                    content: this.generateSimulatedContent(data.original_text, 'advanced'),
                    word_count: Math.floor(data.original_text.length * 1.3),
                    reading_level: '挑战'
                }
            },
            comprehension_questions: {
                basic_questions: [
                    {
                        question: "这篇文章主要讲了什么？",
                        type: "choice",
                        options: ["选项A", "选项B", "正确答案", "选项D"],
                        answer: "正确答案",
                        explanation: "从文章第一段可以找到答案"
                    }
                ],
                standard_questions: [
                    {
                        question: "作者通过这篇文章想表达什么？",
                        type: "short_answer",
                        answer: "参考答案：作者想表达...",
                        explanation: "需要从文章整体来理解"
                    }
                ],
                advanced_questions: [
                    {
                        question: "结合你的生活经验，谈谈对这篇文章的看法。",
                        type: "open_ended",
                        answer: "参考答案：这篇文章让我想到...",
                        explanation: "这是一个开放性问题"
                    }
                ]
            },
            support_materials: {
                basic_materials: {
                    vocabulary_list: [
                        {
                            word: "关键词",
                            pinyin: "guān jiàn cí",
                            definition: "文章中最重要的词语",
                            example: "这句话中的关键词是..."
                        }
                    ]
                }
            },
            core_theme: data.original_text.substring(0, 50)
        };
    },

    generateSimulatedContent: function(originalText, level) {
        if (level === 'basic') {
            return originalText.substring(0, 200) + " [基础版内容已简化]";
        } else if (level === 'standard') {
            return originalText.substring(0, 400) + " [标准版内容]";
        } else {
            return originalText + " [挑战版内容已扩展，包含更深层的分析和思考。]";
        }
    }
};

// ==================== 主程序逻辑 ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('分层阅读系统已加载');

    // 初始化组件
    initComponents();

    // 初始化使用次数显示
    UsageManager.updateUsageDisplay();

    // 初始化主题列表
    ThemeManager.updateThemeList();

    // 设置示例按钮
    setupExampleButtons();
});

function initComponents() {
    const generateBtn = document.getElementById('generateBtn');
    const originalText = document.getElementById('originalText');
    const targetGrade = document.getElementById('targetGrade');
    const versionCount = document.getElementById('versionCount');

    if (generateBtn) {
        generateBtn.addEventListener('click', handleGenerate);
    }

    // 自动保存主题（每10秒检查一次）
    if (originalText) {
        let saveTimeout;
        originalText.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                if (originalText.value.trim().length > 10) {
                    const title = originalText.value.substring(0, 30) + '...';
                    ThemeManager.saveTheme(title, originalText.value, targetGrade.value);
                }
            }, 10000); // 10秒后自动保存
        });
    }
}

function setupExampleButtons() {
    const examples = {
        '中文示例': `香港是一個國際大都會，位於中國的南方。香港有美麗的維多利亞港、高聳的摩天大樓和豐富的文化遺產。香港也是一個重要的金融中心，被稱為「東方之珠」。`,
        '英文示例': `Hong Kong is an international metropolis located in the south of China. It has a beautiful Victoria Harbour, towering skyscrapers, and rich cultural heritage. Hong Kong is also an important financial center, known as the "Pearl of the Orient".`,
        '科學示例': `水有三種狀態：固態、液態和氣態。水的固態是冰，液態是水，氣態是水蒸氣。水的狀態變化與溫度有關。當溫度低於0°C時，水會結冰；當溫度高於100°C時，水會變成水蒸氣。`
    };

    const exampleContainer = document.getElementById('exampleButtons');
    if (exampleContainer) {
        Object.entries(examples).forEach(([name, text]) => {
            const button = document.createElement('button');
            button.className = 'btn-example';
            button.textContent = name;
            button.onclick = () => {
                document.getElementById('originalText').value = text;
                document.getElementById('targetGrade').value = '四年級';
            };
            exampleContainer.appendChild(button);
        });
    }
}

async function handleGenerate() {
    const originalText = document.getElementById('originalText');
    const targetGrade = document.getElementById('targetGrade');
    const versionCount = document.getElementById('versionCount');

    // 验证输入
    if (!originalText.value.trim()) {
        alert('請輸入原文內容！');
        originalText.focus();
        return;
    }

    // 检查使用限制
    const usageCheck = UsageManager.checkUsage();
    if (!usageCheck.allowed) {
        alert(usageCheck.reason);
        return;
    }

    // 显示加载状态
    showLoading(true);

    try {
        // 保存当前主题
        const title = originalText.value.substring(0, 50);
        ThemeManager.saveTheme(title, originalText.value, targetGrade.value);

        // 构建请求数据
        const requestData = {
            original_text: originalText.value,
            target_grade: targetGrade.value,
            version_count: parseInt(versionCount.value) || 3
        };

        console.log('发送请求数据:', requestData);

        // 1. 调用Coze API（测试模式下使用模拟数据）
        let cozeData;
        if (APIManager.TEST_MODE) {
            cozeData = await APIManager.callCozeAPI(requestData);
            console.log('模拟Coze数据:', cozeData);
        } else {
            // 实际调用Coze API的代码
            // cozeData = await callRealCozeAPI(requestData);
            cozeData = await APIManager.callCozeAPI(requestData); // 暂时使用模拟
        }

        // 2. 调用后端生成文件
        console.log('调用后端API生成文件...');
        const zipBlob = await APIManager.callBackendAPI(cozeData);

        // 3. 记录使用次数
        UsageManager.recordUsage();

        // 4. 提供下载
        const url = window.URL.createObjectURL(zipBlob);
        const downloadLink = document.getElementById('downloadLink');

        if (downloadLink) {
            downloadLink.href = url;
            downloadLink.download = `分层阅读材料_${Date.now()}.zip`;
            downloadLink.style.display = 'inline-block';

            // 显示结果
            showLoading(false);
            showResult(true);

            // 自动下载
            setTimeout(() => {
                downloadLink.click();
            }, 500);
        }

    } catch (error) {
        console.error('生成失败:', error);

        // 显示错误信息
        const statusText = document.getElementById('statusText');
        if (statusText) {
            statusText.textContent = `生成失败: ${error.message}`;
        }

        // 如果是本地开发，提供额外提示
        if (APIManager.getApiUrl().includes('localhost')) {
            alert(`本地服务器连接失败。\n\n请确保已运行：\npython local_server.py\n\n然后刷新页面重试。`);
        }

        showLoading(false);
        showResult(false, error.message);
    }
}

function showLoading(show) {
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');

    if (show) {
        if (progressSection) progressSection.style.display = 'block';
        if (resultSection) resultSection.style.display = 'none';

        // 模拟进度
        simulateProgress();
    } else {
        if (progressSection) progressSection.style.display = 'none';
    }
}

function simulateProgress() {
    const progressFill = document.getElementById('progressFill');
    const statusText = document.getElementById('statusText');

    if (!progressFill || !statusText) return;

    let progress = 0;
    const steps = [
        '正在分析文本...',
        '正在提取核心信息...',
        '正在生成分层文本...',
        '正在设计阅读理解问题...',
        '正在生成词汇表和任务卡...',
        '正在打包文件...',
        '准备下载...'
    ];

    const interval = setInterval(() => {
        progress += 10 + Math.random() * 5;
        if (progress > 95) progress = 95;

        progressFill.style.width = progress + '%';

        // 更新状态文本
        const stepIndex = Math.min(Math.floor(progress / 14), steps.length - 1);
        statusText.textContent = steps[stepIndex];

        if (progress >= 95) {
            clearInterval(interval);
        }
    }, 300);
}

function showResult(success, errorMessage = '') {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');

    if (!resultSection || !resultContent) return;

    if (success) {
        resultContent.innerHTML = `
            <div class="success-message">
                <h3>✅ 生成完成！</h3>
                <p>分层阅读材料已成功生成并打包。</p>
                <p>请点击下方链接下载：</p>
                <a id="downloadLink" class="download-btn" href="#" download>
                    ⬇️ 下载分层阅读材料.zip
                </a>
                <p class="file-info">文件大小：约 2-5 MB | 包含：阅读文章、问题、词汇表、教师指南</p>
            </div>
        `;
    } else {
        resultContent.innerHTML = `
            <div class="error-message">
                <h3>❌ 生成失败</h3>
                <p>${errorMessage || '未知错误'}</p>
                <button onclick="location.reload()" class="btn-retry">🔄 重新尝试</button>
                <button onclick="showTroubleshooting()" class="btn-help">❓ 查看帮助</button>
            </div>
        `;
    }

    resultSection.style.display = 'block';
}

function showTroubleshooting() {
    alert(`常见问题解决方法：

1. 本地服务器未启动：
   运行：python local_server.py

2. 网络连接问题：
   检查网络连接，或稍后重试

3. 使用次数超限：
   每人每天最多10次，每月最多50次

4. 浏览器问题：
   尝试使用 Chrome 或 Edge 浏览器

如需帮助，请联系系统管理员。`);
}

// 全局暴露函数（用于HTML中的onclick调用）
window.ThemeManager = ThemeManager;
window.UsageManager = UsageManager;