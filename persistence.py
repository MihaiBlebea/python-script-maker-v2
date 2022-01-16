#!/usr/bin/env python3

import yaml

MODEL_SQL_TEMPLATE = """
import sqlite3

class {model_name}:
    def __init__(self, {params_list}, id = None):
        self.id = id
        {model_fields}

    def __get_conn():
        conn = sqlite3.connect("db.db")
        conn.row_factory = sqlite3.Row
        return conn

    def __to_dict(self):
        model = self.__dict__
        del model["id"]
        return model

    def create_table():
        conn = {model_name}.__get_conn()
        cur = conn.cursor()
        cur.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                {table_columns}
            );\"\"\"
        )

    def save(self):
        conn = {model_name}.__get_conn()
        cur = conn.cursor()
        cur.execute("{insert_query}", list(self.__to_dict().values()))
        conn.commit()
        conn.close()

    def select_by_id(id):
        conn = {model_name}.__get_conn()
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM {table_name} WHERE id = ?", (id,)).fetchall()

        return [User(**row) for row in rows]

    def delete(self):
        conn = {model_name}.__get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM {table_name} WHERE id = ?", (id,))
        conn.commit()
        conn.close()

"""


def main():
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            print(config)
            if "database" not in config:
                print("Could not find database key in config")
                return

            if config["database"] == "sql":
                # add_sqlite()
                return
            
            if config["database"] == "nosql":
                # add_tinydb()
                return

            raise Exception("Database type is not valid: " + config["database"])

        except yaml.YAMLError as err:
            print(f"Encountered error: {err}")


def add_model(name: str, params: list):
    data = MODEL_SQL_TEMPLATE.format(
        model_name=name.title(),
        params_list=", ".join(params),
        model_fields="\n\t\t".join(build_model_properties(params)),
        table_name=name.lower() + "s",
        table_columns=build_create_table_query(params),
        insert_query=build_insert_query(name.lower() + "s", params)
    )

    f = open(f"{name.title()}.py", "w")
    f.write(data.strip())
    f.close()


def build_model_properties(params: list)-> str:
    params = [param.split(":")[0] for param in params]
    return [f"self.{param} = {param}" for param in params]


def build_create_table_query(params: list)-> str:
    results = []
    for param in params:
        key = param.split(":")[0]
        value_type = param.split(":")[1]
        if value_type == "str":
            results.append(f"{key} VARCHAR(255)")
        
        if value_type == "int":
            results.append(f"{key} INTEGER")

        if value_type == "bool":
            results.append(f"{key} INTEGER(1)")

    return ", ".join(results)


def build_insert_query(table_name, params: list)-> str:
    param_names = []
    values = []
    for param in params:
        param_names.append(param.split(":")[0])
        values.append("?")

    return f"INSERT INTO {table_name} ({', '.join(param_names)}) VALUES ({', '.join(values)})"

if __name__ == "__main__":
    add_model("user", [
        "name:str",
        "age:int"
    ])