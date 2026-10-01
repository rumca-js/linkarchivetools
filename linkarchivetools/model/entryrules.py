from pathlib import Path
from datetime import datetime
import re

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
        self.set_table("entry_rules")

    def is_url_blocked(self, url, source=None) -> bool:
        rules = self.get_rules_for(url=url,source=source)
        for rule in rules:
            if rule.block:
                return True
        return False

    def is_entry_rule_triggered(self, rule_row, url, source=None) -> bool:
        if not rule_row.enabled:
            return False

        if rule_row.source_id and source is not None:
            if rule_row.source_id != source.id:
                return False

        if not rule_row.trigger_rule_url:
            return False

        if not rule_row.trigger_rule_url.strip():
            return False

        rule_urls = rule_row.trigger_rule_url.split(",")
        for rule_url in rule_urls:
            rule_url = rule_url.strip()

            if self.is_url_match(rule_url, url):
                return True

        return False

    def is_url_match(self, rule_pattern, url):
        return re.search(rule_pattern, url)

    def get_rules_for(self, url=None, entry=None, source=None):
        result = []

        conditions = {"enabled" : True}

        rules = list(self.connection.entry_rules.get_where(conditions, limit=10000))
        for rule_row in rules:
           if not rule_row.enabled:
               continue

           if entry and self.is_entry_rule_triggered(rule_row, url=entry["link"], source=source):
               result.append(rule_row)
           if url and self.is_entry_rule_triggered(rule_row, url=url, source=source):
               result.append(rule_row)

        return result

    def add_entry_rule(self, entry_rule_url, block=True, trust=False, properties=None, name=None, source_id=None):
        entries = self.connection.entry_rules.get_where({"trigger_rule_url" : entry_rule_url})
        entry = next(entries, None)

        if not entry:
            data = properties

            if not data:
                data = {}

            data["trigger_rule_url"] = entry_rule_url
            if name:
                data["rule_name"] = name
            else:
                data["rule_name"] = ""
            data["enabled"] = True
            data["priority"] = 0
            data["rule_name"] = entry_rule_url
            data["trigger_text"] = ""
            data["trigger_text_hits"] = 0
            data["trigger_text_fields"] = ""
            data["block"] = block
            data["trust"] = trust
            data["auto_tag"] = ""
            data["apply_age_limit"] = 0
            data["browser_id"] = 0
            data["script"] = ""
            if source_id:
                data["source_id"] = source_id

            return self.connection.entry_rules.insert_json_data(data)

    def add_entry_rules(self, raw_input):
        entry_rule_urls = read_line_things(raw_input)
        for entry_rule_url in entry_rule_urls:
            self.add_entry_rule(entry_rule_url)

    def set_entry_rules(self, raw_input):
        self.connection.entry_rules.truncate()

        self.add_entry_rules(raw_input)
