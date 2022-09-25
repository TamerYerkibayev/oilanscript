import streamlit as st
from shillelagh.backends.apsw.db import connect


class Table():
    def __init__(
            self):
        pass

    def select(self):
        connection = connect(":memory:")

        @st.cache(ttl=600)
        def run_query(query):
            cursor = connection.cursor()

            rows = []
            for row in cursor.execute(query):
                rows.append(row)

            return rows

        sheet_url = st.secrets['spreadsheets']["products"]
        rows = run_query(
            f"""
            SELECT * FROM "{sheet_url}";
            """)

        return rows

    def select_by_node_id(self, shop_id):
        connection = connect(":memory:")

        @st.cache(ttl=600)
        def run_query(query):
            cursor = connection.cursor()

            rows = []
            for row in cursor.execute(query):
                rows.append(row)

            return rows

        sheet_url = st.secrets['spreadsheets']["products"]
        rows = run_query(
            f"""
            SELECT * FROM "{sheet_url}"
            WHERE shop_id={shop_id};
            """)

        return rows

    def select_by_id(self, id):
        connection = connect(":memory:")

        @st.cache(ttl=600)
        def run_query(query):
            cursor = connection.cursor()

            rows = []
            for row in cursor.execute(query):
                rows.append(row)

            return rows

        sheet_url = st.secrets['spreadsheets']["products"]
        rows = run_query(
            f"""
            SELECT * FROM "{sheet_url}"
            WHERE id={id};
            """)

        return rows
