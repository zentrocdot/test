'''sd-webui-calc_aspect_ratio
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
import contextlib
import gradio as gr
import modules.scripts as scripts
from modules.ui_components import InputAccordion
   
# Define class MetaDataViewer.
class MetaDataViewer(scripts.Script):
    '''Class for calculating the aspect ratio.'''
    
    def title(self):
        '''Class method title.'''
        return "Aspect Ratio Calculator"

    def show(self, is_img2img):
        '''Class method show.'''
        return scripts.AlwaysVisible  # hide this script in the Scripts dropdown

    def ui(self, is_img2img):
        '''Class method ui.'''
        # Create a block.
        with gr.Blocks() as ui_component:
            with gr.Tab("Checkpoint"):
                with gr.Row():
                    #input_file = gr.Dropdown(models.checkpoint_tiles(), label="Checkpoint")
                    #create_refresh_button(input_file, models.list_models,
                    #                  lambda: {"choices": models.checkpoint_tiles()}, "metadata_utils_refresh_1")

                    button = gr.Button(value="Set Metadata", variant="primary")

                gr.HTML("<p style=\"text-align:center;color:red\">Warning! Changing the metadata of "
                    "your checkpoint also changes it's hash</p>")
                      
          
    # Class method after_component.
    def after_component(self, component, **kwargs):
        '''Class method after_component.

        This method is used to generalize the existing programme code. It is
        detected if one is in the txt2img tab or in the img2img tab. Then the
        corresponding self variables can be used in the same programme code 
        for both tabs.
        '''
        if kwargs.get("elem_id") == "txt2img_width":
            self.t2i_w = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.t2i_h = component
        if kwargs.get("elem_id") == "img2img_width":
            self.i2i_w = component
        if kwargs.get("elem_id") == "img2img_height":
            self.i2i_h = component
        if kwargs.get("elem_id") == "img2img_image":
            self.image = [component]
        if kwargs.get("elem_id") == "img2img_sketch":
            self.image.append(component)
        if kwargs.get("elem_id") == "img2maskimg":
            self.image.append(component)
        if kwargs.get("elem_id") == "inpaint_sketch":
            self.image.append(component)
        if kwargs.get("elem_id") == "img_inpaint_base":
            self.image.append(component)
