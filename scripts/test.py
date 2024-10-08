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
_ar_values_0 = (1.0, 2.0, 3/2, 4/3, 5/3, 5/4, 6/5,
                 7/5, 14/9, 15/9, 16/9, 16/10)
_ar_values_1 = (1.0, 0.5, 2/3, 3/4, 3/5, 4/5, 5/6,
                            5/7, 9/14, 9/15, 9/16, 10/16)
_ar_labels_0 = ("1:1", "2:1", "3:2", "4:3", "5:3", "5:4", "6:5",
                            "7:5", "14:9", "15:9", "16:9", "16:10")
_ar_labels_1 = ("1:1", "1:2", "2:3", "3:4", "3:5", "4:5", "5:6",
                            "5:7", "9:14", "9:15", "9:16", "10:16")

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
        # Create a new list.
        retlst = list(map(round, [w, h]))
        # Return the list with width and height.
        return retlst

    #def reset(self, w, h):
    #    '''Class method reset.'''
    #    return [self.res, self.res]

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
            ardd = gr.Dropdown(
                ["1.19:1", "1.25:1"], label="Uncommon Aspect Ratios", value="")
            use_prompt_button = gr.Button("Use Aspect Ratio", variant="primary", elem_id="use-prompt-button", tooltip="")
            #btns = [AspectRatioButton(ar=1.0, value="1:1")]
            with contextlib.suppress(AttributeError):
                if is_img2img:
                    resolution = [self.i2i_w, self.i2i_h]
                else:
                    resolution = [self.t2i_w, self.t2i_h]
                use_prompt_button.click(
                        use_prompt_button.apply,
                        inputs=resolution,
                        outputs=resolution
                )
            
          with gr.Accordion(open=True, label='SD1.5', visible=True): 
            
            with gr.Row(
                elem_id=f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
            ):
                # Aspect ratio buttons line 1.
                btns = [AspectRatioButton(ar=1.0, value="1:1")]
                with contextlib.suppress(AttributeError):
                    for b in btns:
                        if is_img2img:
                            resolution = [self.i2i_w, self.i2i_h]
                        else:
                            resolution = [self.t2i_w, self.t2i_h]
                        b.click(
                            b.apply,
                            inputs=resolution,
                            outputs=resolution
                        )
            # Loop over the row 1.
            with gr.Row(
                elem_id=f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
            ):
                # Aspect ratio buttons line 1.
                btns = [
                    AspectRatioButton(ar=ar, value=label)
                    for ar, label in zip(
                        #self.ar_values_0,
                        #elf.ar_labels_0
                        _ar_values_0,
                        _ar_labels_0
                    )
                ]
                with contextlib.suppress(AttributeError):
                    for b in btns:
                        if is_img2img:
                            resolution = [self.i2i_w, self.i2i_h]
                        else:
                            resolution = [self.t2i_w, self.t2i_h]
                        b.click(
                            b.apply,
                            inputs=resolution,
                            outputs=resolution
                        )
            # Loop over the row 2.
            with gr.Row(
                elem_id=f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
            ):
                # Aspect ratio buttons line 2.
                btns = [
                    AspectRatioButton(ar=ar, value=label)
                    for ar, label in zip(
                        #self.ar_values_1,
                        #self.ar_labels_1
                        _ar_values_1,
                        _ar_labels_1
                    )
                ]
                with contextlib.suppress(AttributeError):
                    for b in btns:
                        if is_img2img:
                            resolution = [self.i2i_w, self.i2i_h]
                        else:
                            resolution = [self.t2i_w, self.t2i_h]
                        b.click(
                            b.apply,
                            inputs=resolution,
                            outputs=resolution
                        )
    
    # Class method after_component.
    # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
    # so we can use the same code for both tabs
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
