import gradio as gr
import modules.shared as shared

params = {
        "display_name": "Novelist",
        "is_tab": True,
        "activate": True,
    }

text = ""

file_nameJSON = "novelist.json"


def ui():
    text = gr.Textbox(lines=10, label="Text", placeholder="Enter text here ,,, or somewhere!!!! t4est test test.")
    text.change(lambda x: params.update({"text": x}), text, None)
    return gr.Group([text])
