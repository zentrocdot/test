#!/usr/bin/python3
'''sd-webui-meta_data_viewer
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
from metadata_util_lib import write_metadata
import metadata_utils_file_utils as file_utils
from pathlib import Path
import json
from modules import script_callbacks

def on_ui_tabs():
    # Create a new block.
    with gr.Blocks(analytics_enabled=False) as ui_component:    
        # Create a new row. 
        with gr.Row():
                input_file = gr.Dropdown(file_utils.lora_tiles(), label="Lora")
                create_refresh_button(input_file, file_utils.list_loras,
                                      lambda: {"choices": file_utils.lora_tiles()},
                                      "metadata_utils_refresh_1")
        with gr.Row():
                json_input = gr.Code(lines=10,
                                     label="Metadata as JSON",
                                     language="json")
                input_file.change(
                    fn=on_button_load_metadata_lora,
                    inputs=[input_file],
                    outputs=[json_input]
                )
    return [(ui_component, "Metadata Viewer", "metadata_viewer_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)

'''
def on_button_load_metadata(input_file: str):
    if selected_model := models.get_closet_checkpoint_match(input_file):
        if metadata := models.read_metadata_from_safetensors(selected_model.filename):
            return json.dumps(metadata, indent=4, ensure_ascii=False)
        return 'No metadata'
    return 'Model not found'
'''    

def on_button_load_metadata_lora(input_file: str):
    if selected_model := file_utils.get_lora(input_file):
        if metadata := models.read_metadata_from_safetensors(selected_model):
            return json.dumps(metadata, indent=4, ensure_ascii=False)
        return 'No metadata'
    return 'Model not found'
