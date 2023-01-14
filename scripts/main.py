import os
import sys
import json
import gradio as gr
import modules.ui
from modules import script_callbacks, sd_models, shared
from modules.ui import setup_progressbar, gr_show
from modules.shared import opts, cmd_opts, state
from webui import wrap_gradio_gpu_call


def on_ui_tabs():
    config_file =  os.path.join('extensions', 'sd_prompt_generator', "json", 'tags.json')
    with open(config_file) as f:
        config = json.load(f)

    with gr.Blocks() as prompt_generator:
        generate_button = gr.Button('Send to txt2img', variant='primary')
        pre_textbox = gr.Textbox(label='Prefix',lines=1,interactive=True)
        post_textbox = gr.Textbox(label='Postfix',lines=1,interactive=True)
        tag_list = []
        tag_checkboxgroup = []
        for tag_group in config.keys():
            with gr.Accordion(label=tag_group, open=True):
                for subgroup in config[tag_group].keys():
                    with gr.Accordion(label=subgroup, open=False):
                        for tag in config[tag_group][subgroup].keys():
                            with gr.Row():
                                tag_checkboxgroup.append(gr.CheckboxGroup(label=tag,choices=["Random",*config[tag_group][subgroup][tag]]))
                                tag_list.append(config[tag_group][subgroup][tag])
        
        tags_textbox = gr.Textbox(value=json.dumps(tag_list), visible=False)
        
        generate_button.click(
            fn = generate,
            _js = "setPrompt",
            inputs = [pre_textbox, post_textbox, tags_textbox, *tag_checkboxgroup]
        )


    return (prompt_generator, "Generator", "prompt_generator"),

script_callbacks.on_ui_tabs(on_ui_tabs)

def generate():
    gr.update()