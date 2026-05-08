# 🎨 白泽造物 · 文化IP数智活化推演室

**在地文化IP创作与商业决策三合一平台**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-6.10%2B-orange)](https://gradio.app)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-green)](https://langchain.com)

---

## 📌 项目简介

白泽造物（杭州）数字文化有限公司旗下产品。针对「在地文化IP的智能创作与商业决策」场景，构建了一套融合 **AIGC管线**、**RAG知识库** 与 **Agent商业决策** 的完整 Demo。

核心目标：让AI帮助社区/街道/村委等基层单位，把在地文化资源变成可体验、可传播、可变现的IP产品。

## 🚀 核心功能

### ⚙️ AI文化IP视觉生成管线
- 基于 ComfyUI + FLUX.1 模型 + 在地文化LoRA 实现高质量图像生成
- 支持「虫小绿IP」「触身历史」「非遗技艺」等在地文化IP定制化提示词
- 三种艺术风格：国风原味 / AI时尚 / 跨界融合
- 提供模拟生成模式（无 ComfyUI 环境时自动降级）

### 🧬 在地文化IP知识库
- 使用 LangChain + HuggingFace Embeddings + FAISS 向量化在地文化IP文本
- 语义检索并自动注入「白泽造物·在地文化基因片段」标记
- 内置示例数据（触身历史、虫小绿、农发城市厨房、非遗政策等），支持上传自定义文档

### 📈 白泽造物·IP活化智能决策
- 基于 LangChain + 大模型构建多链 Agent
- 自动完成：商业策略分析 → 预算估算（三档方案）→ 营销方案生成
- 输出推荐适配的白泽造物产品线（触身历史课程包/数智展示包/工作坊/年度顾问）

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| AIGC 管线 | ComfyUI, FLUX.1, LoRA, PIL |
| RAG 知识库 | LangChain, FAISS, HuggingFace Embeddings |
| Agent 框架 | LangChain, ChatOpenAI（兼容硅基流动/DeepSeek API） |
| 前端界面 | Gradio 6.10 |
| 语言 | Python 3.10+ |

## 📦 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的账号/baize-ip-demo.git
cd baize-ip-demo
```

### 2. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置 API 密钥
复制 `.env.example` 为 `.env`，填入你的 API 密钥：
```
OPENAI_API_KEY=sk-xxxxxx
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct
```

### 4. 启动 ComfyUI（可选，用于 AIGC 真实生成）
- 下载 ComfyUI 并启动
- 将 `modules/aigc_pipeline/workflow.json` 导入 ComfyUI 并导出为 API 格式
- 确保 FLUX.1 模型与 LoRA 放置在正确目录

### 5. 运行 Demo
```bash
python main.py
```
浏览器打开 http://127.0.0.1:7860 即可体验三模块功能。

## 🎯 使用示例

### AIGC 管线
- 输入：虫小绿IP形象 → 选择风格国风原味
- 输出：生成国风IP风格图像

### RAG 知识库
- 点击「使用示例数据」构建向量库
- 提问：触身历史课程怎么设计？
- 回答：检索相关在地文化片段并带白泽造物基因标记

### Agent 决策
- 输入：虫小绿IP如何在社区场景做商业化？
- 输出：包含商业策略、预算三档方案、营销方案的完整报告

## 🔮 愿景

AI 正在让在地文化IP从静态资源变成可自我进化的活态资产。白泽造物的角色不是「守护者」，而是「活化者」——用AI降低文化IP的创作门槛和商业化成本，让每一段在地记忆都能被看见、被体验、被传承。

## 📄 许可证
MIT

## 📧 联系
白泽造物（杭州）数字文化有限公司
