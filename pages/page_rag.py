import gradio as gr
from modules.rag_engine.knowledge_base import CulturalIPKnowledgeBase
import os

kb = CulturalIPKnowledgeBase()
sample_data_path = os.path.join(os.path.dirname(__file__), "..", "modules", "rag_engine", "data", "sample_ip.txt")

def build_with_sample():
    try:
        docs = kb.load_documents(sample_data_path)
        kb.build_vector_store(docs)
        kb.save_store("./cultural_ip_store")
        return "知识库构建完成！已加载示例文化IP数据。"
    except Exception as e:
        return f"构建失败：{str(e)}"

def build_from_file(file):
    if file is None:
        return "请上传文件"
    try:
        docs = kb.load_documents(file.name)
        kb.build_vector_store(docs)
        kb.save_store("./cultural_ip_store")
        return f"知识库构建完成！已加载 {len(docs)} 个文档片段。"
    except Exception as e:
        return f"构建失败：{str(e)}"

def answer_question(question, history):
    # history 格式为 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    if not kb.vector_store:
        try:
            kb.load_store("./cultural_ip_store")
        except:
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": "请先构建知识库（使用示例数据或上传文件）"})
            return "", history
    try:
        context = kb.get_context_with_gene(question, k=3)
        answer = f"🔍 **基于白泽造物知识库的回答**\n\n检索到的在地文化IP片段：\n\n{context}"
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        return "", history
    except Exception as e:
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": f"查询出错：{str(e)}"})
        return "", history

def render():
    with gr.Blocks() as page:
        gr.Markdown("## 🧬 在地文化IP知识库")
        gr.Markdown("白泽造物·在地文化基因库，支持语义检索与AI问答")
        
        with gr.Tab("📤 构建知识库"):
            file_input = gr.File(label="上传文化IP文档（TXT格式）")
            build_btn = gr.Button("构建向量库")
            build_output = gr.Textbox(label="构建结果")
            
            build_btn.click(
                fn=build_from_file,
                inputs=file_input,
                outputs=build_output
            )
            
            use_sample_btn = gr.Button("使用示例数据")
            use_sample_btn.click(
                fn=build_with_sample,
                inputs=[],
                outputs=build_output
            )
        
        with gr.Tab("💬 文化IP问答"):
            # 移除 type 参数，让 Gradio 使用默认格式（新版）
            chatbot = gr.Chatbot(label="对话历史", height=400)
            msg = gr.Textbox(label="输入问题", placeholder="例如：虫小绿IP有哪些活化方式？")
            clear = gr.Button("清空")
            
            msg.submit(
                fn=answer_question,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            clear.click(lambda: None, None, chatbot, queue=False)
            
            gr.Examples(
                examples=[
                    ["虫小绿IP如何商业化？"],
                    ["触身历史课程怎么设计？"],
                    ["非遗数字化有哪些政策支持？"],
                    ["社区文化IP怎么做线上传播？"],
                    ["AI如何帮在地文化IP变现？"]
                ],
                inputs=msg
            )
    return page