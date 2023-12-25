import os.path
import subprocess
from dpg_funcs.drop_handler import *


def process_button_callback():
    # if the sounds weren't dropped stop
    if dpg.get_value('log_field_value') == LOG_FIELD_DEFAULT:
        return

    def update_log():
        dpg.set_value('log_field_value', tabulate(data, headers, tablefmt=TABLEFMT))

    dpg.disable_item('process_button')  # prevent breakage of the code

    mime_engine = magic.Magic(mime=True)
    input_media_format = dpg.get_value('input_media_type')
    shorted_filenames_dict = json.loads(dpg.get_value('shorted_filenames_dict'))
    headers = json.loads(dpg.get_value('table_headers'))
    data = json.loads(dpg.get_value('table_data'))
    export_format = dpg.get_value('output_format')
    loaded_files = []

    # every loaded file
    for line_index, line in enumerate(data):
        shorted_filename, weight, ext, status = line

        data[line_index] = [shorted_filename, weight, ext, 'Processing', export_format]
        update_log()

        #

        full_filename = shorted_filenames_dict[shorted_filename]
        export_filename = os.path.splitext(full_filename)[0] + f'.{export_format}'
        with open(full_filename, 'rb') as file:
            mime_type = mime_engine.from_buffer(file.read(1024))

        try:
            match input_media_format:
                case 'audio':
                    importer: AudioImporter = SUPPORTED_AUDIO_IMPORTERS[mime_type]
                    importer.__init__(full_filename)

                    exporter: AudioExporter = SUPPORTED_AUDIO_EXPORTERS[export_format]
                    exporter.__init__(importer.decoded_audio, export_filename, export_format)
                case 'video':
                    ...
                case 'image':
                    ...

            data[line_index] = [shorted_filename, weight, ext, 'Done', export_format]
            update_log()
        except BaseException:
            data[line_index] = [shorted_filename, weight, ext, 'Error', export_format]
            update_log()

    # # mixing
    # out_audio = loaded_files[0]
    # for i in loaded_files[1:]:
    #     out_audio = out_audio + i
    #
    # date_strf = datetime.now().strftime("%Y.%m.%d %H-%M")
    # output_fn = f'c:\\output\\{len(loaded_files)} files mixed [{date_strf}].{export_format}'

    dpg.enable_item('process_button')
