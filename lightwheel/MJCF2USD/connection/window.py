import os
import xml.etree.ElementTree as ET
import omni.kit.commands
import omni.ui as ui
import omni.usd
from .mjcf2usd_utils import get_xmls,mjcf_to_usd
from .option_widget import string_filed_builder
import time

class MJCF2USDWindow(ui.Window):
    
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)
        self._models = {
            "usd_success":[],
            "usd_failed":[],
            "convert_time":[],
        }
        self._xmls = []
        self._stage = omni.usd.get_context().get_stage()
        self.frame.set_build_fn(self._build_fn)
        self.label_style_red = {
                    "font_size":18,
                    "font_weight":"bold",
                    "color":0xFF0000FF,
                    }
        self.label_style_green = {
            "font_size":18,
            "font_weight":"bold",
            "color":0xFF66CD00,
            }


    def _build_fn(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=10):
                self._build_window()
                
    def destroy(self) -> None:
        return super().destroy()    
    
    
    def _build_window(self):
        self._stage = omni.usd.get_context().get_stage()
        with self.frame:
            with ui.VStack(spacing=4,height=0):
                
                    
                self._mjcf_location_label = ui.Label("[1] : Select MJCF Location",
                         style=self.label_style_red)

                self._models["mjcf_root_path"] = string_filed_builder(
                    tooltip="Select MJCF or folder containing MJCFs to convert",
                    default_val="No MJCF or folder containing MJCFs be selected",
                    folder_dialog_title="Select MJCF File or Folder containing MJCFs",
                    folder_button_title="Select File or Folder",
                    read_only=False,
                )            
                    
                self._usd_location_label = ui.Label("[2] : Select USD Location",
                         style=self.label_style_red)
                
                self._models["usd_root_path"] = string_filed_builder(
                    tooltip="Select the storage location of USDs (default is the same as the MJCF location)",
                    default_val="None, default is the same as the MJCF location",
                    folder_dialog_title="Select the storage location of USDs",
                    folder_button_title="Select Folder",
                    read_only=False,
                )  


                
                with ui.HStack(height=0):
                    self._modify_xml_checkbox = ui.CheckBox(
                        width=20,
                        height=20,
                        style={
                            "margin": 2,
                            "color": 0xFF000000,
                            "background_color": 0xFFFFFFFF,
                            "border_radius": 2,
                            "border_width": 1,
                            "border_color": 0xFF808080,
                        }
                    )
                    ui.Spacer(width=10)                    
                    ui.Label(
                        "Save Temp MJCF XML",
                        style=self.label_style_green
                    )
                    
                self._mjcf2usd_button = ui.Button(
                    "MJCFs to USDs",
                    clicked_fn=self._on_xmls2usd,
                    enabled=False,
                    style={
                        "font_size": 14,
                        "font_weight": "bold",
                        "color": 0xFF000000,
                        "background_color": 0xFFE0E0E0,
                        "border_radius": 4,  # 圆角
                        "border_width": 1,
                        "border_color": 0xFF808080,
                        "margin": 2,
                        "padding": 4,
                        ":hover": {
                            "background_color": 0xFFD0D0D0,
                            "border_color": 0xFF606060,
                        },
                        ":pressed": {
                            "background_color": 0xFFC0C0C0,
                            "translate": [1, 1],
                        },
                        "transition": {
                            "background_color": 0.2,
                            "scale": 0.02,
                            "translate": 0.02,
                        }
                    }
                )

                self._mjcf2usd_label = ui.Label("[3] : Begin to convert MJCFs to USDs",
                         style=self.label_style_green)
                
                self._mjcf2usd_label.visible = False
                
                self._message_label = ui.Label(
                    "No MJCFs found",
                    style=self.label_style_red,
                )
                
                def _on_mjcf_location_changed(model):
                    value = model.get_value_as_string()
                    if "\\" in value or "/" in value:
                        self._xmls = get_xmls(value)
                        if self._xmls:
                            self._mjcf_location_label.style = self.label_style_green
                            self._usd_location_label.style = self.label_style_green
                            self._mjcf2usd_label.style = self.label_style_green
                            self._mjcf2usd_button.enabled = True
                            xml_text = "\n".join(self._xmls)
                            self._message_label.text = f"Found {len(self._xmls)} MJCFs:\n{xml_text}"
                            self._message_label.style = self.label_style_green
                        else:
                            self._message_label.text = "No MJCFs found"
                            self._message_label.style = self.label_style_red
                            self._mjcf_location_label.style = self.label_style_red
                            self._usd_location_label.style = self.label_style_red
                            self._mjcf2usd_label.style = self.label_style_red
                            self._mjcf2usd_button.enabled = False
                            # self._mjcf2usd_progress_bar.visible = False
                            self._mjcf2usd_label.visible = False
                    else:
                        self._mjcf_location_label.style = self.label_style_red
                        self._usd_location_label.style = self.label_style_red
                        self._mjcf2usd_label.style = self.label_style_red
                        self._mjcf2usd_button.enabled = False
                        # self._mjcf2usd_progress_bar.visible = False
                        self._mjcf2usd_label.visible = False
                    
                self._models["mjcf_root_path"].add_value_changed_fn(_on_mjcf_location_changed)

          
    def xmls2usd(self):
        self._models["convert_time"] = []
        for i ,xml in enumerate(self._xmls):
            time_start = time.time()
            if 'None' in self._models["usd_root_path"].get_value_as_string():
                parent_dir = os.path.dirname(xml)
                model_name = os.path.basename(parent_dir)
                usd_name = str(model_name) + '.usd'
                usd_path = os.path.join(parent_dir, usd_name)
            else:
                parent_dir = os.path.dirname(xml)
                model_name = os.path.basename(parent_dir)
                usd_name = str(model_name) + '.usd'
                
                filepath = os.path.join(self._models["usd_root_path"].get_value_as_string(),model_name)
                if not os.path.exists(filepath):
                    os.mkdir(filepath)
                    
                usd_path = os.path.join(filepath,usd_name)
                
            need_modify_xml = self._modify_xml_checkbox.model.get_value_as_bool()
            mjcf_to_usd(xml, usd_path,need_modify_xml)
            if os.path.exists(usd_path):
                self._models["usd_success"].append(usd_path)
            else:
                self._models["usd_failed"].append(xml)
            time_end = time.time()
            self._models["convert_time"].append(time_end-time_start)
            time_total = sum(self._models["convert_time"])
            time_average = time_total/len(self._xmls)
            time_left = time_average*(len(self._xmls)-i-1)
            # self._message_label.text = f"Converting MJCFs to USDs: {i+1}/{len(self._xmls)}" + \
            # f" Time left: {time_left:.2f} seconds"
        success_text = "\n".join(self._models["usd_success"])
        failed_text = "\n".join(self._models["usd_failed"])
        self._message_label.text += f"\n[Total time]: {time_total:.2f} seconds" + \
            f"\n[Success number]: {len(self._models['usd_success'])}" + \
            f"\n[Failed number]: {len(self._models['usd_failed'])}" + \
            f"\n\n[Success files]: \n{success_text}" + \
            f"\n\n[Failed files]: \n{failed_text}"
            
    def _on_xmls2usd(self):
        self._mjcf2usd_label.visible = True
        # self._mjcf2usd_progress_bar.visible = True
        self._mjcf2usd_button.enabled = False
        # self._mjcf2usd_progress_bar.model.set_value(0)
        self.xmls2usd()
        self._models["convert_time"] = []
        self._models["usd_success"] = []
        self._models["usd_failed"] = []
        self._mjcf2usd_button.enabled = True
        
        
        