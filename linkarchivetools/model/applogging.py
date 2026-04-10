"""
TODO remove hardcoded values
"""
import traceback
from datetime import datetime
from .basetable import BaseTable


class AppLogging(BaseTable):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    NOTIFICATION = 60

    def __init__(self, connection):
        self.connection = connection
        self.set_table("applogging")

    def create_entry(self, info_text, detail_text="", level=INFO, stack=False):
        if len(info_text) > 1900:
            info_text = info_text[:1900]
        if len(detail_text) > 2900:
            detail_text = detail_text[:2900]

        json_data = {}
        json_data["info_text"] = info_text
        json_data["detail_text"] = detail_text
        json_data["level"] = level
        json_data["date"] = datetime.now()

        self.connection.applogging.insert_json_data(json_data)

        self.cleanup_overflow()

    def cleanup_overflow(self):
        """
        Cleans up
        """
        count_elements = self.connection.applogging.count()
        if count_elements > AppLogging.get_max_log_entries():
            diff = count_elements - AppLogging.get_max_log_entries()

            rows = self.connection.applogging.get_where(order_by=[self.connection.applogging.get_table().c.date.asc()], limit=diff)
            for row in rows:
                self.connection.applogging.delete(id=row.id)

    def get_max_log_entries():
        return 2000

    def debug(self, info_text, detail_text="", stack=False):
        print(info_text)

    def info(self, info_text, detail_text="", stack=False):
        self.create_entry(info_text, detail_text=detail_text, level=AppLogging.INFO, stack=stack)

    def warning(self, info_text, detail_text="", stack=False):
        self.create_entry(info_text, detail_text=detail_text, level=AppLogging.WARNING, stack=stack)

    def error(self, info_text, detail_text="", stack=False):
        print("Error: " + info_text)
        self.create_entry(info_text, detail_text=detail_text, level=AppLogging.ERROR, stack=stack)

    def notify(self, info_text, detail_text="", stack=False):
        self.create_entry(info_text, detail_text=detail_text, level=AppLogging.NOTIFICATION, stack=stack)

    def exc(self, exception_object, info_text="", detail_text="", stack=False):

        error_text = traceback.format_exc()
        print("Exception format")
        print(error_text)

        stack_lines = traceback.format_stack()
        stack_string = "".join(stack_lines)
        print("Stack:")
        print(stack_string)

        if not info_text:
            info_text = ""

        info_text = info_text + "\n" + str(exception_object)
        detail_text = error_text + "\n" + stack_string

        self.create_entry(info_text, detail_text=detail_text, level=AppLogging.ERROR, stack=stack)
