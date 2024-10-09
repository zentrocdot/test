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
from modules.ui_components import ToolButton, InputAccordion

# Define module variables.
_width = 512
_height = 512
     
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
            with InputAccordion(
                False, label="Utilised Aspect Ratios (Landscape Orientation)", 
                elem_id=f'{"img" if is_img2img else "txt"}2img_row_aspect_ratio'
            ) as enabled:
                #arval = gr.Dropdown(arlist, label="Aspect Ratios", value="1:1")

                arvalue = gr.Number(label="Aspect ratio calculated from W/H", value=0, interactive=False, render=True)
                with gr.Row(
                    elem_id=f'{"img" if is_img2img else "txt"}2img_container_aspect_ratio'
                ):
                  rst = AspectRatioButton(ar=1.0, value="Reset")
                  btn = AspectRatioButton(ar=1.0, value="Apply")
                  chg = AspectRatioButton(ar=1.0, value="Change Orientation")
                  mybutton = gr.Button("Test", tooltip="")
                          
                  with contextlib.suppress(AttributeError):
                    if is_img2img:
                        imgres = [self.i2i_w, self.i2i_h]
                    else:
                        imgres = [self.t2i_w, self.t2i_h]
                    def update_button(arstr):      
                        btn.ar = ardict[arstr]
                        return btn.apply(_width, _height)
                    btn.click(
                        update_button,
                        inputs=[arval],
                        outputs=imgres
                    )
                    def update_rst(arstr):      
                        rst.ar = 1.0
                        return rst.apply(_width, _height)
                    rst.click(
                        update_rst,
                        inputs=[arval],
                        outputs=imgres
                    )
                    def update_chg(arstr):      
                        chg.ar = 1/ardict[arstr]
                        return chg.apply(_width, _height)
                    chg.click(
                        update_chg,
                        inputs=[arval],
                        outputs=imgres
                    )
                    def lala(x,y):
                        print("x=", x, "y=", y)   
                        ret = x/y      
                        #btn.prtval      
                        #print("START")      
                        #print(self.t2i_w, self.t2i_h)
                        #print(self.i2i_w, self.i2i_h)
                        #print("END")
                        #return (x,y)     
                        return ret    
                    
                    test1 = mybutton.click(lala, inputs=imgres, outputs=arvalue)       
                    print(test1)        
          
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
