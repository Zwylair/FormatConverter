import copy
import time
import json
import magic
from tabulate import tabulate
import dearpygui.dearpygui as dpg
import custom_mimetypes
from funcs import *


def unfold_directories(fps: list[str]) -> list[str]:
    """ unfold a directory -> and add all subfiles to filelist """

    all_fps = copy.copy(fps)
    for i in fps:
        if os.path.isdir(i):
            all_fps.remove(i)

            for root, dirs, files in os.walk(i):
                for file in files:
                    all_fps.append(os.path.join(root, file))
    return all_fps


def remove_unsupported_files(fps: list[str]) -> list[str]:
    """ removes from list unsupported files by its mimetypes """

    out_fps = copy.copy(fps)
    mime_engine = magic.Magic(mime=True)

    for filepath in fps:
        with open(filepath, 'rb') as file:
            mime_type = mime_engine.from_buffer(file.read(1024))

        if mime_type is None:
            mime_type = custom_mimetypes.define_mimetype(filepath)

        if mime_type is None or mime_type not in ALL_SUPPORTED_IMPORT:
            out_fps.remove(filepath)
    return out_fps


def check_for_different_media_types(fps: list[str]) -> bool:
    """ we can process only one type of media at the time, so, we need to define the type of processing media,
    and say "there isn't only one type if media" import error info """

    mime_engine = magic.Magic(mime=True)

    with open(fps[0], 'rb') as file:
        mime_type = mime_engine.from_buffer(file.read(1024))
    first_got_media_type = mime_type.split('/')[0]

    for filepath in fps:
        with open(filepath, 'rb') as file:
            mime_type = mime_engine.from_buffer(file.read(1024))
        got_media_type = mime_type.split('/')[0]

        if got_media_type != first_got_media_type:
            return True
    return False


def show_output_format_chooser():
    def submit_callback():
        if dpg.get_value('output_format'):
            dpg.delete_item('output_format_chooser_window')

    #

    dpg.delete_item('different_media_types_window')
    with dpg.window(tag='output_format_chooser_window', width=200, height=125, no_resize=True, no_close=True):
        output_media_type = {
            'audio': SUPPORTED_AUDIO_OUTPUT,
            'image': SUPPORTED_IMAGE_OUTPUT,
            'video': SUPPORTED_VIDEO_OUTPUT
        }[dpg.get_value('input_media_type')]

        dpg.add_combo(output_media_type, width=50, label='Choose output format', source='output_format')
        dpg.add_button(label='Submit', callback=submit_callback)


def drop_handler(fps: list[str]):
    fps = unfold_directories(fps)
    fps = remove_unsupported_files(fps)

    mime_engine = magic.Magic(mime=True)
    headers = ['Name', 'Weight', 'Extension', 'Status', 'Export format']
    shorted_filenames_dict = {}
    data = []

    # we can process only one type of media at the time, so, we need to define the type of processing media,
    # and say "there isn't only one type if media" import error info
    if check_for_different_media_types(fps):
        dpg.delete_item('different_media_types_window')
        with dpg.window(tag='different_media_types_window', width=350, height=150, no_resize=True, no_close=True):
            dpg.add_text('You have been dropped files, that have different media\n'
                         'types (not only audio, for example).\n\n'
                         'Drop the files with one media type only')
        return

    with open(fps[0], 'rb') as file:
        mime_type = mime_engine.from_buffer(file.read(1024))
    dpg.set_value('input_media_type', mime_type.split('/')[0])

    show_output_format_chooser()

    # wait for closed format output window
    while True:
        try:
            dpg.get_item_label('output_format_chooser_window')
            time.sleep(0.3)
        except BaseException:
            break

    export_format = dpg.get_value('output_format')

    for filepath in fps:
        table_filename = get_strf_name(filepath)
        shorted_filenames_dict[table_filename] = filepath
        weight = get_strf_weight(os.path.getsize(filepath))
        extension = os.path.splitext(filepath)[1]
        extension = extension.lstrip('.')[:9]

        data.append([table_filename, weight, extension, 'Waiting', export_format])

    dpg.set_value('shorted_filenames_dict', json.dumps(shorted_filenames_dict))
    dpg.set_value('table_headers', json.dumps(headers))
    dpg.set_value('table_data', json.dumps(data))
    dpg.set_value('log_field_value', tabulate(data, headers, tablefmt=TABLEFMT))
