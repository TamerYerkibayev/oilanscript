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

        sheet_url = st.secrets['spreadsheets']["ways"]
        rows = run_query(
            f"""
            SELECT * FROM "{sheet_url}";
            """)

        return rows
