'''Extension for AUTOMATIC1111 called sd-webui-predefined_aspect_ratios.

Version 0.0.0.2
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
from modules.ui_components import ToolButton, InputAccordion

# Define module variables.
_width = 512
_height = 512

# Define the module aspect ratio dictionary.
ardict = {"1:1   ": 1.00, "1.19:1": 1.19, "1.25:1": 1.25, "1.3:1 ": 1.30, 
          "1.33:1": 1.33, "1.37:1": 1.37, "1.41:1": 1.41, "1.5:1 ": 1.50, 
          "1.59:1": 1.59, "1.6:1 ": 1.60, "1.66:1": 1.66, "1.75:1": 1.75, 
          "1.77:1": 1.77, "1.78:1": 1.78, "1.85:1": 1.85, "2.35:1": 2.35,
          "2.37:1": 2.37, "2.38:1": 2.38, "2.39:1": 2.39, "2.4 :1": 2.40,
          "2.75:1": 2.75, "2.76:1": 2.76, "3.2:1 ": 3.20, "3.55:1": 3.55,
          "3.58:1": 3.58, "3.6:1 ": 3.60, "12:5  ": 2.40, "18:5  ": 3.60,
          "18:9  ": 2.00, "19.5:9": 2.17, "20:9  ": 2.22, "21:9  ": 2.33,
          "22:9  ": 2.44, "32:9  ": 3.56, "36:10 ": 3.60} 

# Declare the aspect ratio list.
arlist = []

# Create the aspect ratio list.
for key, value in ardict.items():
    arlist.append(key)  

# Define class AspectRatioButton.
class  AspectRatioButton(ToolButton):
    '''Class for calculating the new Width and new Height for
       use in the web UI from the chosen aspect ratio.
    '''
    def __init__(self, ar=1.0, **kwargs):
        '''Class init method.'''
        super().__init__(**kwargs)
        self.ar = ar

    def apply(self, w, h):
        '''Class method apply.'''
        # Initialise height and width.
        w = _width
        h = _height
        # Calculate new width and height.
        if self.ar > 1.0:  # fixed height, change width
            w = self.ar * h
        elif self.ar < 1.0:  # fixed width, change height
            h = w / self.ar
        else:  # set minimum dimension to both
            min_dim = min([w, h])
            w, h = min_dim, min_dim
        print(w, h)  
        # Create a new list.
        retlst = list(map(round, [w, h]))
        # Return the list with width and height.
        return retlst

# Define class AspectRatioScript.
class AspectRatioScript(scripts.Script):
    '''Class for selecting the aspect ratio.'''
    
    def title(self):
        '''Class method title.'''
        return "Aspect Ratio Selector"

    def show(self, is_img2img):
        '''Class method show.'''
        return scripts.AlwaysVisible  # hide this script in the Scripts dropdown

    def ui(self, is_img2img):
        '''Class method ui.'''
        # Loop over the columns.
        with gr.Column(
            elem_id=f'{"img" if is_img2img else "txt"}2img_container_aspect_ratio'
        ):
            with InputAccordion(False, label="Uncommon Aspect Ratios", elem_id=self.elem_id("ra_enable")) as enabled:
                ardd = gr.Dropdown(arlist, label="Aspect Ratios", value="1.0")
                btn = AspectRatioButton(ar=1.0, value="DO")
                with contextlib.suppress(AttributeError):
                    if is_img2img:
                        resolution = [self.i2i_w, self.i2i_h]
                    else:
                        resolution = [self.t2i_w, self.t2i_h]
                    def combine(x):      
                        btn.ar = ardict[x]
                        return btn.apply(512, 512)
                    btn.click(
                        combine,
                        inputs=[ardd]
                        outputs=resolution
                    )
    
    # Class method after_component.
    # This is to generalize the code. Detect if one is in txt2img tab or img2img tab, and then
    # use the corresponding self variables so we can use the same code for both tabs.
    def after_component(self, component, **kwargs):
        '''Class method after_component.'''
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
