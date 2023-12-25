import os.path
from typing import Literal
from error_handler import ErrorHandler
from dpg_funcs.drop_handler import *

logger = logging.getLogger(__name__)
handler = ErrorHandler(logging.ERROR)
logger.addHandler(handler)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.DEBUG)


def choose_media_importer(input_media_format: Literal['audio', 'video', 'image'], mimetype: str):
    return {
        'audio': AUDIO_IMPORTERS,
        'video': VIDEO_IMPORTERS,
        'image': IMAGE_IMPORTERS,
    }[input_media_format][mimetype]


def choose_media_exporter(input_media_format: Literal['audio', 'video', 'image'], export_format: str):
    return {
        'audio': AUDIO_EXPORTERS,
        'image': IMAGE_EXPORTERS,
        'video': VIDEO_EXPORTERS
    }[input_media_format][export_format]


def process_button_callback():
    # if there weren't dropped any media
    if dpg.get_value('log_field_value') == LOG_FIELD_DEFAULT:
        return

    logger.debug('starting')
    dpg.disable_item('process_button')  # prevent breakage of the code

    def update_log():
        dpg.set_value('log_field_value', tabulate(data, table_headers, tablefmt=TABLEFMT))

    input_media_format = dpg.get_value('input_media_type')
    export_format = dpg.get_value('output_format')
    shorted_filenames_dict = json.loads(dpg.get_value('shorted_filenames_dict'))
    table_headers = json.loads(dpg.get_value('table_headers'))
    data = json.loads(dpg.get_value('table_data'))
    mime_engine = magic.Magic(mime=True)
    max_datalist_index = len(data) - 1
    merge_obj: pydub.AudioSegment | None = None

    # every loaded file (from table data)
    for line_index, line in enumerate(data):
        shorted_filename, weight, operation, status = line
        data[line_index] = [shorted_filename, weight, operation, 'Processing']

        full_filename = shorted_filenames_dict[shorted_filename]
        export_filename = os.path.splitext(full_filename)[0] + ('-merged' if operation == 'merge' else '')

        # if export_filename exists, check for 'export_filename (1)', 'export_filename (2)' etc...
        count = 0
        while True:
            new_export_name = export_filename + (f' ({count})' if count else '') + f'.{export_format}'
            count += 1

            if not os.path.exists(new_export_name):
                export_filename = new_export_name
                break

        logger.debug('')
        logger.debug(f'start file processing: {full_filename}')
        update_log()

        with open(full_filename, 'rb') as file:
            mime_type = mime_engine.from_buffer(file.read(1024))

        try:
            importer = choose_media_importer(input_media_format, mime_type)(full_filename)
            exporter = choose_media_exporter(input_media_format, export_format)(importer.decoded_media, export_filename, export_format)

            logger.debug(f'got importer: {importer.__class__.__name__}')
            logger.debug(f'got exporter: {exporter.__class__.__name__}')
            logger.debug(f'operation: {operation}')

            if operation == 'convert':
                exporter.export()

                data[line_index] = [shorted_filename, weight, operation, 'Done']
                update_log()

            elif operation == 'merge':
                exporter.decoded_media = merge_obj

                if input_media_format == 'audio':
                    if merge_obj is None:
                        merge_obj = importer.decoded_media

                        data[line_index] = [shorted_filename, weight, operation, 'Loaded']
                        update_log()
                        continue
                    merge_obj += importer.decoded_media

                    if line_index == max_datalist_index:
                        exporter.export()

                elif input_media_format == 'video':
                    ...

                elif input_media_format == 'image':
                    ...  # if x > y: 10:2 ;; if y > x: 2:10

                #

                # make whole filelist status to "done" if the export was done or just put "Loaded"
                if line_index == max_datalist_index:
                    data = list(map(lambda i: [i[0], i[1], i[2], 'Done'], data))
                else:
                    data[line_index] = [shorted_filename, weight, operation, 'Loaded']
                logger.debug('operation done')
                update_log()

        except Exception as err:
            logger.error(err)

            data[line_index] = [shorted_filename, weight, operation, 'Error']
            update_log()

    logger.debug('quota done')
    dpg.enable_item('process_button')
