import os
import sys
# 设置 Gradio 临时目录
GRADIO_TEMP = "/tmp/gradio_temp" if sys.platform != "win32" else r"C:\Users\seanjob\.hermes\gradio_temp"
os.environ["GRADIO_TEMP_DIR"] = GRADIO_TEMP
os.makedirs(GRADIO_TEMP, exist_ok=True)

import gradio as gr
from pages import page_aigc, page_rag, page_agent
from dotenv import load_dotenv

load_dotenv()

with gr.Blocks(title="白泽造物·文化IP数智活化推演室", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎨 白泽造物 · 文化IP数智活化推演室")
    gr.Markdown("### AI在地文化IP创作与商业决策三合一平台")
    
    with gr.Tabs():
        with gr.TabItem("⚙️ AIGC管线"):
            page_aigc.render()
        with gr.TabItem("🧬 RAG文化基因库"):
            page_rag.render()
        with gr.TabItem("📈 智能商业决策"):
            page_agent.render()

if __name__ == "__main__":
    demo.launch(share=True)