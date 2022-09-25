from shops_database import Table as ShopsTable
from products_database import Table as ProductsTable
from tools import sql_result_to_pandas
import plotly.express as px
import pandas as pd
import numpy as np


def sales_revenue_charts(st, products_table_df):
    products_table_df = products_table_df.groupby(
        ['shop_id'], as_index=False).sum()

    sales_columns = products_table_df.columns[products_table_df.columns.str.contains(
        ' Sales')]
    revenue_columns = products_table_df.columns[products_table_df.columns.str.contains(
        ' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    df = pd.DataFrame(
        index=dates,
        data=np.c_[
            products_table_df[sales_columns].T.values,
            products_table_df[revenue_columns].T.values
        ],
        columns=[
            'Sales',
            'Revenue'
        ]
    )

    with st.sidebar:
        chart_type = st.radio(
            "Choose what to display",
            ('Sales', 'Revenue'))

    if chart_type == 'Sales':
        st.markdown("## :chart_with_upwards_trend: Sales chart")

        fig = px.line(
            df,
            x=df.index,
            y=df[df.columns[0]],
            markers=True,
            labels={
                'Sales': 'Sales',
                'index': 'Date'
            })
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("## :chart: Revenue chart")

        fig = px.line(
            df,
            x=df.index,
            y=df[df.columns[1]],
            markers=True,
            labels={
                'Revenue': 'Revenue',
                'index': 'Date'
            })

        st.plotly_chart(fig, use_container_width=True)


def metrics(st, products_table_df):
    st.markdown("## :currency_exchange: Malls metrics")

    max_price = products_table_df['Max price'].max()
    min_price = products_table_df['Min price'].min()
    average_price = products_table_df['Average price'].mean()//10000
    total_sales = products_table_df['Sales'].sum()
    total_revenue = products_table_df['Revenue'].sum()
    revenue_potential = products_table_df['Revenue potential'].mean()//10000
    lost_profit = products_table_df['Lost profit'].mean()//10000
    lost_profit_percent = products_table_df['Lost profit percent'].mean(
    )//10000
    sales_per_day_average = products_table_df['Sales per day average'].mean(
    )//10000

    column_1, column_2, column_3 = st.columns(3)

    column_1.metric("Max price", f"{max_price} $", "10 %")
    column_2.metric("Min price", f"{min_price} $", "8.55 %")
    column_3.metric("Average price", f"{average_price} $", "0.12 %")

    column_1.metric("Sales", f"{total_sales}", "-0.88 %")
    column_2.metric("Revenue", f"{total_revenue} $", "-0.86 %")
    column_3.metric("Revenue potential", f"{revenue_potential}", "40 %")

    column_1.metric("Lost profit", f"{lost_profit} $", "-10%")
    column_2.metric("Lost profit percent", f"{lost_profit_percent}", "8.55 %")
    column_3.metric("Sales per day average",
                    f"{sales_per_day_average}", "13.45 %")


def charts_by_period(st, products_table_df):
    products_table_df = products_table_df.groupby(
        ['shop_id'], as_index=False).sum()

    sales_columns = products_table_df.columns[products_table_df.columns.str.contains(
        ' Sales')]
    revenue_columns = products_table_df.columns[products_table_df.columns.str.contains(
        ' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    df = pd.DataFrame(
        index=dates,
        data=np.c_[
            products_table_df[sales_columns].T.values,
            products_table_df[revenue_columns].T.values
        ],
        columns=[
            'Sales',
            'Revenue'
        ]
    )

    column_1, column_2 = st.columns(2)

    with st.sidebar:
        chart_type = st.radio(
            "Choose a period",
            ('Month', 'Day'))

    if chart_type == 'Month':
        df = df.groupby(df.index.strftime("%B")).sum()

        column_1.markdown("## :chart_with_upwards_trend: Sales by month")

        fig = px.bar(
            df,
            x=df.index,
            y=df[df.columns[0]],
            labels={
                'Sales': 'Sales',
                'index': 'Month'
            })
        column_1.plotly_chart(fig, use_container_width=True)

        column_2.markdown("## :chart: Revenue by month")

        fig = px.bar(
            df,
            x=df.index,
            y=df[df.columns[1]],
            labels={
                'Revenue': 'Revenue',
                'index': 'Month'
            })

        column_2.plotly_chart(fig, use_container_width=True)
    else:
        df = df.groupby(df.index.strftime(
            "%a")).sum().iloc[[1, 5, 6, 4, 0, 2, 3], :]

        column_1.markdown("## :chart_with_upwards_trend:  Sales by day")

        fig = px.bar(
            df,
            x=df.index,
            y=df[df.columns[0]],
            labels={
                'Sales': 'Sales',
                'index': 'Day'
            })
        column_1.plotly_chart(fig, use_container_width=True)

        column_2.markdown("## :chart: Revenue by day")

        fig = px.bar(
            df,
            x=df.index,
            y=df[df.columns[1]],
            labels={
                'Revenue': 'Revenue',
                'index': 'Day'
            })

        column_2.plotly_chart(fig, use_container_width=True)


def pie_chart(st, products_table_df):
    with st.sidebar:
        chart_type = st.radio(
            "Choose what to display",
            ('Sales', 'Revenue'))

    if chart_type == 'Sales':
        st.markdown("## :chart_with_upwards_trend: Sales pie chart")
        fig = px.pie(
            products_table_df,
            values=products_table_df['Sales'],
            names=products_table_df['category_1'],
            labels={
                'Sales': 'Sales',
                'category_1': 'Category'
            })

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("### :chart: Revenue pie chart")
        fig = px.pie(
            products_table_df,
            values=products_table_df['Revenue'],
            names=products_table_df['category_1'],
            labels={
                'Revenue': 'Revenue',
                'category_1': 'Category'
            })

        st.plotly_chart(fig, use_container_width=True)


def shops_page(st, id):
    st.markdown(
        "# :shopping_bags: Interactive map of places - Shops report")

    table = ShopsTable().select_by_seller_id(id)
    table_df = sql_result_to_pandas(table, 'nodes')
    node_id = table_df['id'].iloc[0]

    products_table = ProductsTable().select_by_node_id(node_id)
    products_table_df = sql_result_to_pandas(products_table, 'products')

    with st.sidebar:
        option = st.selectbox(
            'Choose a chart?',
            ('Sales & Revenue charts', 'Metrics', 'Charts by period', 'Pie chart'))

        st.write('You selected:', option)

    if option == 'Sales & Revenue charts':
        sales_revenue_charts(st, products_table_df)
    elif option == 'Metrics':
        metrics(st, products_table_df)
    elif option == 'Charts by period':
        charts_by_period(st, products_table_df)
    elif option == 'Pie chart':
        pie_chart(st, products_table_df)
