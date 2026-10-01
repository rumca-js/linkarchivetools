from datetime import datetime

from .basetable import BaseTable


class EntryTransitionHistoryTable(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("entrytransitionhistory")

    def get_transition(self, entry_from, entry_to):
        transitions = self.get_where({"entry_from_id" : entry_from.id, "entry_to_id" : entry_to.id})
        for transition in transitions:
            return transition

    def transition(self, entry_from, entry_to):
        transition = self.get_transition(entry_from, entry_to)
        if transition:
            json_data = {}
            json_data["counter"] = transition.counter

            status = self.get_table().update_json_data(id=transition.id, json_data=json_data)
            return status
        else:
            json_data = {}

            json_data["counter"] = 1
            json_data["entry_from_id"] = entry_from.id
            json_data["entry_to_id"] = entry_to.id

            status = self.get_table().insert_json_data(json_data=json_data)
            return status


class EntryVisitHistoryTable(BaseTable):
    def __init__(self, connection):
        self.connection = connection
        self.set_table("entryvisithistory")

    def get_entry_visit(self, entry):
        visits = self.get_where({"entry_id" : entry.id})
        for visit in visits:
            return visit

    def get_last_visit_entry(self):
        table = self.get_table().get_table()

        visits = self.get_where({}, order_by=[table.c.date_last_visit.desc()])
        for visit in visits:
            return visit

    def visited(self, entry):
        last_entry = self.get_last_visit_entry()

        visit = self.get_entry_visit(entry)
        if not visit:
            counter = 1

            json_data = {}
            json_data["visits"] = counter
            json_data["date_last_visit"] = datetime.now() # TODO local time?
            json_data["entry_id"] = entry.id

            status = self.get_table().insert_json_data(json_data=json_data)
        else:
            counter = visit.visits

            json_data = {}
            json_data["visits"] = counter
            json_data["date_last_visit"] = datetime.now() # TODO local time?

            status = self.get_table().update_json_data(json_data=json_data)

        if last_entry and entry:
            transitions = EntryTransitionHistoryTable(self.connection)
            transitions.transition(last_entry, entry)

        return status
