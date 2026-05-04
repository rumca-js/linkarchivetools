from pathlib import Path
from datetime import datetime
from .sourcedata import SourceData
from .sources import Sources
from .basetable import BaseTable


def read_line_things(input_text):
    sources = [
        line.strip()
        for line in input_text.splitlines()
        if line.strip()
    ]

    sources = set(sources)
    sources = list(sources)

    return sources


class EntryRules(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("entryrules")

    def is_url_blocked(self, url):
        conditions = {"block" : True, "enabled" : True}
        rules = self.connection.entry_rules.get_where(conditions)
        for rule in rules:
            if rule.trigger_rule_url == url:
                return True

    def is_entry_rule_triggered(self, url) -> bool:
        rules = self.connection.entry_rules.get_where({"trigger_rule_url" : url})
        rules = next(rules, None)
        if rules:
            return True
        return False

    def get_rule_urls(self):
        urls = []

        conditions = {"enabled" : True}

        rules = self.connection.entry_rules.get_where(conditions, limit=10000)
        for rule in rules:
            if not rule.enabled:
                continue

            urls.append(rule.trigger_rule_url)

        return urls

    def get_rules_for(self, url=None, entry=None):
        result = []

        conditions = {"enabled" : True}

        rules = self.connection.entry_rules.get_where(conditions, limit=10000)
        for rule in rules:
           if not rule.enabled:
               continue

           if entry and self.is_entry_rule_triggered(entry["link"]):
               result.append(rule)
           if url and self.is_entry_rule_triggered(url):
               result.append(rule)

        return result

    def add_entry_rule(self, entry_rule_url):
        entries = self.connection.entry_rules.get_where({"trigger_rule_url" : entry_rule_url})
        entry = next(entries, None)

        if not entry:
            data = {}
            data["trigger_rule_url"] = entry_rule_url
            data["enabled"] = True
            data["priority"] = 0
            data["rule_name"] = entry_rule_url
            data["trigger_text"] = ""
            data["trigger_text_hits"] = 0
            data["trigger_text_fields"] = ""
            data["block"] = True
            data["trust"] = False
            data["auto_tag"] = ""
            data["apply_age_limit"] = 0
            data["browser_id"] = 0

            return self.connection.entry_rules.insert_json_data(data)

    def add_entry_rules(self, raw_input):
        entry_rule_urls = read_line_things(raw_input)
        for entry_rule_url in entry_rule_urls:
            self.add_entry_rule(entry_rule_url)

    def set_entry_rules(self, raw_input):
        self.connection.entry_rules.truncate()

        entry_rule_urls = read_line_things(raw_input)
        for entry_rule_url in entry_rule_urls:
            self.add_entry_rule(entry_rule_url)
