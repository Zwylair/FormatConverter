# process = subprocess.Popen(['converters\\rles\\ConsoleApp2.exe', 'C:\\Users\\Zwylair\\Desktop\\file.rle2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, error = process.communicate()

import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
import dnd_setup
import dpg_funcs
from settings import *

dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='Format Converter v1.0.0', width=633, height=500)

with dpg.value_registry():
    dpg.add_string_value(tag='shorted_filenames_dict')
    dpg.add_string_value(tag='table_headers')
    dpg.add_string_value(tag='table_data')
    dpg.add_string_value(tag='file_format', default_value='mp3')
    dpg.add_string_value(tag='log_field_value', default_value=LOG_FIELD_DEFAULT)
    dpg.add_string_value(tag='input_media_type')
    dpg.add_string_value(tag='output_format')

#

with dpg.font_registry():
    with dpg.font('bin/ubuntu_regular.ttf', 14, default_font=True, id='ubuntu'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    with dpg.font('bin/ubuntu_mono-regular.ttf', 12, default_font=False, id='ubuntu_mono'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font('ubuntu')

#

with dpg.window(no_title_bar=True, no_resize=True, no_close=True, no_move=True) as window:
    dpg.add_input_text(default_value=LOG_FIELD_DEFAULT, tag='log', source='log_field_value',
                       readonly=True, multiline=True, width=600, height=420)

    with dpg.group(horizontal=True):
        dpg.add_combo([], label='Output format', source='file_format', width=50)
        dpg.add_button(label='Process', tag='process_button', callback=dpg_funcs.process_button_callback)
        dpg.add_text(default_value='Drag&Drop the sounds', color=(90, 90, 90))

dpg.bind_item_font('log', 'ubuntu_mono')
dpg.set_primary_window(window, True)
dnd_setup.setup(dpg_funcs.drop_handler)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
