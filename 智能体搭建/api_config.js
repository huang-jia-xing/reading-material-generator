// Coze API 配置
const COZE_CONFIG = {
    // Coze Bot ID（需要替换为实际的Bot ID）
    BOT_ID: "your_bot_id_here",

    // Coze API 端点（根据Coze文档更新）
    API_ENDPOINT: "https://api.coze.cn/v1/workflow/run",

    // API密钥（从Coze平台获取）
    API_KEY: "your_api_key_here",

    // 版本名称映射
    VERSION_NAMES: {
        basic: "基础版",
        standard: "标准版",
        advanced: "挑战版",
        extension: "拓展版"
    }
};

// 调用Coze工作流API
async function callCozeWorkflow(userInput) {
    const payload = {
        bot_id: COZE_CONFIG.BOT_ID,
        user_input: {
            original_text: userInput.original_text,
            target_grade: userInput.target_grade,
            version_count: userInput.version_count
        },
        stream: false
    };

    try {
        const response = await fetch(COZE_CONFIG.API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${COZE_CONFIG.API_KEY}`
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API调用失败: ${response.status}`);
        }

        const data = await response.json();
        return processCozeResponse(data);

    } catch (error) {
        console.error('Coze API调用错误:', error);
        throw error;
    }
}

// 处理Coze返回的数据
function processCozeResponse(cozeData) {
    // 这里需要根据Coze的实际返回格式进行调整
    // 假设Coze返回的数据结构为：
    // {
    //   "output": {
    //     "leveled_texts": {...},
    //     "comprehension_questions": {...},
    //     "support_materials": {...}
    //   }
    // }

    return cozeData.output || cozeData;
}

// 导出配置
export { COZE_CONFIG, callCozeWorkflow, processCozeResponse };