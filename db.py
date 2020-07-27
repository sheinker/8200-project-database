import os
import shelve
import db_api
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any, Dict, List, Type
from pathlib import Path




@dataclass_json
@dataclass
class DBField(db_api.DBField):
    def __init__(self, name, type):
        self.name = name
        self.type = type


@dataclass_json
@dataclass
class SelectionCriteria(db_api.SelectionCriteria):
    def __init__(self, field_name, operator, value):
        self.field_name = field_name
        self.operator = operator
        self.value = value


@dataclass_json
@dataclass
class DBTable(db_api.DBTable):
    def __init__(self, name, fields, key_field_name):
        self.name = name
        self.fields = fields
        self.key_field_name = key_field_name

        self.path_file = os.path.join('db_files', self.name + '.db')
        table = shelve.open(self.path_file)
        try:
            table_values = {}
            for field in fields:
                table_values[fields] = ''
            table[key_field_name] = table_values
        finally:
            table.close()

    def count(self):
        table_file = shelve.open(os.path.join('db_files', self.name + '.db'))
        try:
            count_rows = len(table_file.keys())
        finally:
            table_file.close()
        return count_rows

    def insert_record(self, values: Dict[str, Any]):
        if values is None or len(values) > len(self.fields) or values[self.key_field_name] is None:
            raise ValueError
        else:
            table_file = shelve.open(os.path.join('db_files', self.name + '.db'), writeback=True)
            try:
                if table_file[values[self.key_field_name]]:
                    table_file.close()
                else:
                    table_file[values[self.key_field_name]] = values
            finally:
                table_file.close()

    def delete_record(self, key):
        table = shelve.open(os.path.join('db_files', self.name + '.db'), writeback=True)
        try:
            if key is None or key not in table:
                raise ValueError
            else:
                table.pop(key)
        finally:
            table.close()




    def delete_records(self, criteria):
        for record in criteria:
            self.delete_record(record)

    def get_record(self, key: Any) -> Dict[str, Any]:
        # if key is None or key not in table:
        #     raise ValueError
        # else:
        # table = shelve.open(os.path.join('db_files', self.name + '.db'), writeback=True)



    def update_record(self, key: Any, values: Dict[str, Any]):
        raise NotImplementedError


@dataclass_json
@dataclass
class DataBase(db_api.DataBase):
    tables: Dict[str, DBTable]

    def create_table(self, table_name, fields, key_field_name):
        if table_name not in self.tables:
            self.tables[table_name] = DBTable(table_name, fields, key_field_name)
            return self.tables[table_name]
        else:
            raise ValueError

    def num_tables(self):
        return len(self.tables)

    def get_table(self, table_name):
        return self.tables.get(table_name)

    def delete_table(self, table_name):
        if table_name in self.tables:
            os.remove(db_api.DB_ROOT.joinpath(f"{table_name}.dir"))
            self.tables.pop(table_name)
        else:
            raise ValueError

    def get_tables_names(self):
        return list(self.tables.keys())

    def query_multiple_tables(self, tables, fields_and_values_list, fields_to_join_by):
        pass

    # def query_multiple_tables(
    #         self,
    #         tables: List[str],
    #         fields_and_values_list: List[List[SelectionCriteria]],
    #         fields_to_join_by: List[str]
    # ) -> List[Dict[str, Any]]:
    #     raise NotImplementedError
