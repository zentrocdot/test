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

def update_number(x,y):
    if x > y:
        z = x/y
        if float(z).is_integer():
            z = int(z)                                 
        ret = str(z) + ":1"                   
    elif x <= y:
        z = y/x
        if float(z).is_integer():
            z = int(z)
        ret = "1:" + str(z)    
    return str(ret)

# Define class AspectRatioScript.
class AspectRatioScript(scripts.Script):
    '''Class for calculating the aspect ratio.'''
    
    def title(self):
        '''Class method title.'''
        return "Aspect Ratio Calculator"

    def show(self, is_img2img):
        '''Class method show.'''
        return scripts.AlwaysVisible  # Hide this script in the Scripts dropdown

    def image_resolution(self, is_img2img):
        if is_img2img:
            imgres = [self.i2i_w, self.i2i_h]
        else:
            imgres = [self.t2i_w, self.t2i_h]
        return imgres

    def ui(self, is_img2img):
        '''Class method ui.'''
        # Create a column.
        with gr.Column(
            elem_id=f'{"img" if is_img2img else "txt"}2img_container_aspect_ratio'
        ):
            # Create an accordion. 
            with InputAccordion(
                False, label="Aspect Ratio Calculator", 
                elem_id=f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
            ) as enabled:
                arvalue = gr.Textbox(value="N/A", lines=1, interactive=False, inputs=None,
                    label="Calculated aspect ratio from Width/Height"
                )
                # Create a row.
                with gr.Row(
                    elem_id=f'{"img" if is_img2img else "txt"}2img_container_aspect_ratio'
                ):
                    # Create two numeric fields and one button. 
                    wentry = gr.Number(label="Width", interactive=True, scale=int)
                    hentry = gr.Number(label="Height", interactive=True, scale=int)
                    mybutton = gr.Button("Calculate Aspect Ratio")          
                    with contextlib.suppress(AttributeError):
                        imgres = self.image_resolution()
                        mybutton.click(update_number, inputs=[wentry, hentry], outputs=arvalue)               
          
    # Class method after_component.
    def after_component(self, component, **kwargs):
        '''Class method after_component.

        This method is used to generalize the existing programme code. It is
        detected if one is in the 'txt2img' tab or in the 'img2img' tab in the 
        web UI. Then the corresponding self variables can be used in the same
        programme code for both tabs.
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
