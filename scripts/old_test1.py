#!/usr/bin/python3
'''sd-webui-simple-meta_data_viewer
Extension for AUTOMATIC1111.

Version 0.0.0.1
'''
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=import-error
# pylint: disable=consider-using-from-import
# pylint: disable=trailing-whitespace
# pylint: disable=unused-argument
# pylint: disable=too-many-instance-attributes
# pylint: disable=no-self-use

# Import the Python modules.
import gradio as gr
import modules.sd_models as models
import modules.shared
from modules.ui import create_refresh_button
from pathlib import Path
import json
from modules import script_callbacks
import os

lora_path = getattr(modules.shared.cmd_opts, "lora_dir", os.path.join(models.paths.models_path, "Lora"))
print(lora_path)

lora_list = []

def list_loras():
    global lora_list
    if not os.path.isdir(lora_path):
        print("No valid path")
        return []
    def list_recursive(path: str) -> list[str]:
        out = []
        global_path = os.path.join(lora_path, path)
        for item in os.listdir(global_path):
            if os.path.isfile(os.path.join(global_path, item)):
                out.append(os.path.join(path, item))
            elif os.path.isdir(os.path.join(global_path, item)):
                out.extend(list_recursive(os.path.join(path, item)))
        return out
    lora_list = list_recursive("")

list_loras()

def lora_tiles():
    global lora_list
    if len(lora_list) == 0:
        list_loras()
    return lora_list

def on_ui_tabs():
    # Create a new block.
    with gr.Blocks(analytics_enabled=False) as ui_component:    
        # Create a new row. 
        with gr.Row():
                #input_file = gr.Dropdown(lora_tiles(), label="Lora")
                input_file = gr.Dropdown(list_loras(), label="Lora")
                create_refresh_button(input_file, list_loras,
                                      lambda: {"choices": lora_tiles()},
                                      "metadata_utils_refresh_1")
        with gr.Row():
                json_input = gr.Code(lines=10, label="Metadata as JSON",
                                     language="json")
                input_file.change(
                    fn=on_button_load_metadata_lora,
                    inputs=[input_file], outputs=[json_input]
                )
    return [(ui_component, "Metadata Viewer", "metadata_viewer_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

def get_lora(lora_file):
    if not os.path.isfile(os.path.join(lora_path, lora_file)):
        return None
    return os.path.join(lora_path, lora_file)

def on_button_load_metadata_lora(input_file: str):
    if selected_model := get_lora(input_file):
        if metadata := models.read_metadata_from_safetensors(selected_model):
            return json.dumps(metadata, indent=4, ensure_ascii=False)
        return 'No metadata'
    return 'No Model'
