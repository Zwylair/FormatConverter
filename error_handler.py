import sys
import logging
import traceback
import dearpygui.dearpygui as dpg


def format_exception(exception: BaseException) -> str:
    formatted_exception = traceback.format_exception(type(exception), exception, exception.__traceback__)
    return ''.join(formatted_exception).rstrip('\n')


class ErrorHandler(logging.Handler):
    def emit(self, record):
        old_logs = dpg.get_value('error_log_field_value')
        formatted_exc = format_exception(sys.exc_info()[1])
        record.msg = formatted_exc

        dpg.set_value('error_log_field_value', ('\n' if old_logs else '') + formatted_exc)
