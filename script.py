import gradio as gr
import modules.shared as shared

params = {
        "display_name": "Novelist",
        "is_tab": True,
        "activate": True,
        "selectText": [0, 0],
        "selectGen": [0, 0],
        "selectNotepad": [0, 0],
}

loadedFileName = ""

loadedData = {
    "Chapters" : [
        {
            "title": "Chapter 1",
            "text": "This is the first chapter of the book",
            "summary": "This is the summary of the first chapter",
            "active": False
        }
    ],
    "Memories": [],
}

current_chapter = 0

# def get_chapter_selector():
#     return (d.Title for d in loadedData["Chapters"])
# #    loadedData["Chapters"].map((e) => e["Title"])


file_nameJSON = "novelist.json"

def get_chapter_selector():
    return (d["title"] for d in loadedData["Chapters"])


def ui():
    with gr.Row():
        with gr.Column():
            with gr.Group():

                chapter_title = gr.Textbox(lines=1, max_lines=1, elem_classes=['textbox', 'add_scrollbar'],
                                           label="Chapter Title", placeholder="Enter chapter title here",
                                           interactive=True,
                                           readonly= current_chapter >= len(loadedData["Chapters"]) ,
                                           value = loadedData["Chapters"][current_chapter]["title"] if current_chapter >= len(loadedData["Chapters"]) else "",
                                           )

                chapter_textbox = gr.Textbox(lines=10, label="Text", placeholder="Enter text here ,,, or somewhere!!!! t4est test test.")

                with gr.Row():
                    chapter_generate = gr.Button("Generate", variant="primary", elem_classes="small-button" )
                    chapter_summarize = gr.Button("Summarize", variant="primary", elem_classes="small-button")
                    # chapter_active = gr.Checkbox(label="Active for generation",
                    #     checked= loadedData["Chapters"][current_chapter]["active"]) if current_chapter in range(len(loadedData["Chapters"])) else False

                chapter_summary = gr.Textbox(lines=10, label="Summary", placeholder="")

        with gr.Column():
            with gr.Tab("Novel"):

                with gr.Group("Novel file:"):
                    with gr.Row():
                        gr.File(file_types=[".json"], file_count="single", label="Load Novel", type="file",
                                        interactive=True, height="1em")

                    with gr.Row():
                        gr.Button("Save Novel", variant="secondary", elem_classes="small-button")
                        gr.Button("Save As", variant="secondary", elem_classes="small-button")

                with gr.Group("Chapters:") as chapter_group:

                    chapter_list = gr.Radio(
                        choices= get_chapter_selector(),
                        type="index",
                        value=current_chapter,
                        label="Chapters",
                        interactive=True,
                        elem_classes=['textbox', 'add_scrollbar'],
                        )

                    with gr.Row():
                        add_chapter_button = gr.Button("Add Chapter", variant="secondary", elem_classes="small-button")
                        delete_chapter_button = gr.Button("Delete Chapter", variant="secondary", elem_classes="small-button", icon="trash")

            with gr.Tab("Ideas"):
                with gr.Row():
                    idea_textbox = gr.Textbox(lines=10, label="Text", placeholder="")
                with gr.Row():
                    idea_save = gr.Button("Generate", variant="primary")


            with gr.Tab("Memories"):
                memory_title = gr.Textbox(lines=1, label="Memory Title", placeholder="Enter memory title here")
                memory_textbox = gr.Textbox(lines=25, label="Text", placeholder="Enter text here ,,, or somewhere!!!! t4est test test.")

    @add_chapter_button.click(inputs=[], outputs=chapter_list)
    def add_chapter():
        no = len(loadedData["Chapters"])
        loadedData["Chapters"].append({
            "title": "Chapter {0}".format(no+1),
            "text": "",
            "summary": ""
        })

        print(loadedData["Chapters"])

        return chapter_list.update(
                choices=get_chapter_selector(),
                value=str(current_chapter)
            )



    @chapter_list.input(inputs=[chapter_list], outputs=[chapter_title, chapter_textbox, chapter_summary])
    def chapter_change(idx):
        global current_chapter
        current_chapter = idx
        print("Chapter changed to {0}".format(current_chapter))

        return [
            chapter_title.update(value=loadedData["Chapters"][current_chapter]["title"]),
            chapter_textbox.update(value=loadedData["Chapters"][current_chapter]["text"]),
            chapter_summary.update(value=loadedData["Chapters"][current_chapter]["summary"])
        ]


    @chapter_title.input(inputs=[chapter_title], outputs=[chapter_list])
    def chapter_title_change(txt):
        loadedData["Chapters"][current_chapter]["title"] = txt
        return chapter_list.update(
            choices=get_chapter_selector()
        )

    # def chapter_title_change():
    #     nope = 1
    #
    # chapter_title.change(chapter_title_change)
