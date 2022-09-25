from search_logs_database import Table
from tools import sql_result_to_pandas
import plotly.express as px
import pandas as pd


def hourly_activity(st, table_df):
    st.markdown("## :hourglass: Activity by hours")
    df = table_df.groupby(table_df['datetime'].dt.hour).count()
    fig = px.bar(df, x=df.index, y=df[df.columns[1]],
                 labels={'user_id': 'Activity', 'index': 'Hour'})

    st.plotly_chart(fig, use_container_width=True)


def monthly_activity(st, table_df):
    st.markdown("## :hourglass: Activity by month")
    df = table_df.groupby(table_df['datetime'].dt.strftime("%B")).count()
    fig = px.bar(df, x=df.index, y=df[df.columns[1]],
                 labels={'user_id': 'Activity', 'index': 'Month'})

    st.plotly_chart(fig, use_container_width=True)


def daily_activity(st, table_df):
    st.markdown("## :hourglass: Activity by days")
    df = table_df.groupby(table_df['datetime'].dt.strftime("%A")).count()
    fig = px.bar(df, x=df.index, y=df[df.columns[1]],
                 labels={'user_id': 'Activity', 'index': 'Day'})

    st.plotly_chart(fig, use_container_width=True)


def product_demand(st, table_df):
    st.markdown("## :scroll: Search history")
    products = tuple(table_df.groupby('query', as_index=False).count(
    ).sort_values('id', ascending=False)['query'].values.tolist())
    product = st.selectbox('Choose a product',
                           products)

    df = table_df[table_df['query'] == product].sort_values(['datetime'])
    df['datetime'] = df['datetime'].dt.round('H')
    df = df.groupby(df['datetime']).count()

    fig = px.line(df, x=df.index,
                  y=df[df.columns[1]], markers=True,
                  labels={'user_id': 'Activity', 'datetime': 'Date'})

    st.plotly_chart(fig, use_container_width=True)


def search_logs_page(st):
    st.markdown("# :mag: Interactive map of places - Search logs report")

    table = Table().select()
    table_df = sql_result_to_pandas(table, 'search_logs')
    table_df['datetime'] = table_df['date'] + ' ' + table_df['time']
    table_df['datetime'] = pd.to_datetime(table_df['datetime'])

    with st.sidebar:
        option = st.selectbox('Choose a chart?',
                              ('Hourly activity',
                               'Monthly activity',
                               'Daily activity',
                               'Product demand'))
        st.write('You selected:', option)

    if option == 'Hourly activity':
        hourly_activity(st, table_df)
    elif option == 'Monthly activity':
        monthly_activity(st, table_df)
    elif option == 'Daily activity':
        daily_activity(st, table_df)
    else:
        product_demand(st, table_df)
