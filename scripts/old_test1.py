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
import os
import json
import gradio as gr
import modules.sd_models as models
import modules.shared
from modules.ui import create_refresh_button
#from pathlib import Path
from modules import script_callbacks

lora_path = getattr(modules.shared.cmd_opts, "lora_dir", os.path.join(models.paths.models_path, "Lora"))

def fast_lora_scan(dir, ext):  # dir: str, ext: list
    subfolders, files = [], []
    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.name)
    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    files.sort(reverse=False)
    return files

def get_lora_list():
    return fast_lora_scan(lora_path, [".safetensors"])

def on_ui_tabs():
    # Create a new block.
    with gr.Blocks(analytics_enabled=False) as ui_component:    
        # Create a new row. 
        with gr.Row():
            input_file = gr.Dropdown(fast_lora_scan(lora_path, [".safetensors"]), label="Lora")
            create_refresh_button(input_file, get_lora_list,
                                  lambda: {"choices": fast_lora_scan(lora_path, [".safetensors"])},
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
