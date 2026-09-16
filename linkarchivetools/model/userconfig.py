from datetime import datetime

from .basetable import BaseTable
from .entries import Entries


class UserConfig(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("readlater")

    def get_user(self, user_id):
        user_table = self.connection.get_table("user")
        return user_table.get_where({"id" : user_id})

    def get_config(self, user_id):
        for row in self.get_table().get_where({"user_id" : user_id}):
            return row

    def add_config(self, user_id):
        json_data = {}

        user = self.get_config(user_id)
        if not user:
            return

        json_data["username"] = user.username
        json_data["karma"] = 0
        json_data["birth_date"] = None
        json_data["display_style"] = ""
        json_data["display_type"] = ""
        json_data["show_icons"] = True
        json_data["small_icons"] = False
        json_data["thumbnails_as_icons"] = False
        json_data["entries_direct_links"] = False
        json_data["highlight_bookmarks"] = False
        json_data["click_behavior_modal_window"] = False
        json_data["links_per_page"] = 0
        json_data["sources_per_page"] = 0
        json_data["debug_mode"] = False
        json_data["user_id"] = user_id

        return self.get_table().insert_json_data(json_data=json_data)

    def add_user(self, username="testuser", password="testpassword"):
        user_table = self.connection.get_table("user")

        data = {
                "username" : username,
                "password" : password,
                "first_name" : "",
                "last_name" : "",
                "email" : "testemail@test.com",
                "is_superuser" : False,
                "is_staff" : False,
                "is_active" : True,
                "date_joined" : datetime.now(),
                }
        id = user_table.insert_json_data(data)
        return id
