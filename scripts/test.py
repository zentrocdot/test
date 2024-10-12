'''sd-webui-aspect_ratio2width_height
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
# pylint: disable=bad-indentation
# pylint: disable=unused-variable

# Import the Python modules.
import contextlib
import gradio as gr
import modules.scripts as scripts
from modules.ui_components import ToolButton, InputAccordion

# Define module variables.
_width = 512
_height = 512
_IsExact = False
_IsWidth = 512
_IsHeight = 512

def width_height(ar):
    global _IsWidth
    global _IsHeight
    fac1, fac2 = ar.split(":")
    height = 512
    width = float(fac1) * height / float(fac2)
    if _IsExact == True:
      if float(width).is_integer():
        width, height = (int(width), int(height))
      else:
        new_height = height
        while True:
            new_height += 2
            width = float(fac1) * new_height / float(fac2)
            if float(width).is_integer():
                break
        width, height = (int(width), int(new_height))
        _IsWidth, _IsHeight = (int(width), int(new_height))
    return (width, height)

# Define class AspectRatioButton.
class  AspectRatioButton(ToolButton):
    '''Class for calculating the new Width and new Height for
       use in the web UI from the chosen aspect ratio.
    '''
    def __init__(self, ar=1.0, **kwargs):
        '''Class init method.'''
        super().__init__(**kwargs)
        self.ar = ar

    def apply(self, wx, hy):
        '''Class method apply.'''
        print(w, h)
        # Initialise height and width.
        w = _width
        h = _height
        # Calculate new width and height.
        #if self.ar > 1.0:  # fixed height, change width
        #    w = self.ar * h
        #elif self.ar < 1.0:  # fixed width, change height
        #    h = w / self.ar
        #else:  # set minimum dimension to both
        #    min_dim = min([w, h])
        #    w, h = min_dim, min_dim
        # Create a new list.
        retlst = list(map(round, [w, h]))
        # Return the list with width and height.
        return retlst

# Define class AspectRatioScript.
class ResolutionCalcScript(scripts.Script):
    '''Class for calculation the resolution.'''
    
    def title(self):
        '''Class method title.'''
        return "Resolution Calculator"

    def show(self, is_img2img):
        '''Class method show.'''
        return scripts.AlwaysVisible  # hide this script in the Scripts dropdown

    def image_resolution(self, is_img2img):
        '''Get the image resolution from container and return the values.'''
        if is_img2img:
            imgres = [self.i2i_w, self.i2i_h]
        else:
            imgres = [self.t2i_w, self.t2i_h]
        return imgres    

    def ui(self, is_img2img):
        '''Class method ui.'''
        # Set the css format strings.
        css_acc = f'{"img" if is_img2img else "txt"}2img_accordion_aspect_ratio' 
        css_col = f'{"img" if is_img2img else "txt"}2img_container_aspect_ratio'
        css_row = f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
        css_button = f'{"img" if is_img2img else "txt"}2img_button_aspect_ratio'
        # Loop over the columns.
        with gr.Column(elem_id=css_col):
            with InputAccordion(value=False,
                label="Aspect Ratio to Width/Height", 
                elem_id=css_acc
            ) as enabled:
                with gr.Row(elem_id=css_row):      
                    wx = gr.Number(value=None, label="", render=True, visible=True, show_label=False,
                            interactive=False, info="Width")
                    hy = gr.Number(value=None, label="", render=True, visible=True, show_label=False,
                            interactive=False, info="Height")
                    rb_on_off = gr.Radio(choices=["On", "Off"], value="Off", label="Exact Calculation")    
                with gr.Row(elem_id=css_row):
                    arcalc_input = gr.Textbox(value="", info="Aspect Ratio", label="", placeholder="Enter aspect ratio here")     
                    calc_btn = gr.Button(value="Calculate", elem_id=css_button) 
                    with contextlib.suppress(AttributeError):
                        def calc_value(ar_str):
                            print(ar_str) 
                            x, y = width_height(ar_str)
                            return (x, y)
                        calc_btn.click(calc_value, inputs=[arcalc_input], outputs=[wx, hy])
                        def change_rb(rb_state):
                            global _IsExact
                            if rb_state == "Off":
                                _IsExact = False
                            elif rb_state == "On":
                                _IsExact = True      
                            return rb_state
                        rb_on_off.change(change_rb, inputs=[rb_on_off], outputs=[rb_on_off])
                with gr.Row(elem_id=css_row):
                    btns = [AspectRatioButton(ar=1.0, value="Apply")]
                    with contextlib.suppress(AttributeError):
                        for b in btns:
                            imgres = self.image_resolution(is_img2img)
                            b.click(b.apply, inputs=imgres, outputs=imgres)
            
    # Class method after_component.
    def after_component(self, component, **kwargs):
        '''Class method after_component.

        This method is used to generalize the existing code. It is detected if 
        one is in the txt2img tab or the img2img tab. Then the corresponding self
        variables can be used in the same code for both tabs.
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
