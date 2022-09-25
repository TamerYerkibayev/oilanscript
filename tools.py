import pandas as pd
import numpy as np

ways_columns = [
    'id', 'addr_street', 'addr_housenumber',
    'building_levels', 'image_link', 'geometry', 'name']

nodes_columns = [
    'id', 'name', 'shop', 'seller_id', 'way_id'
]

products_columns = [
    'id', 'SKU', 'Name', 'Category', 'Brand', 'Seller', 'Color', 'Balance',
    'Comments', 'Final Price', 'Max price', 'Min price',
    'Average price', 'Sales', 'Revenue', 'Revenue potential',
    'Lost profit', 'Lost profit percent', 'url', 'thumb',
    'Days in stock', 'Days with sales', 'Average if in stock',
    'Rating', 'Basic Sale', 'Basic Sale Price', 'Promo Sale',
    'Base price', 'SPP', 'SPP Price', 'FBS', 'Category position',
    'Sales per day average', '09.08.2021 Sales', '10.08.2021 Sales',
    '11.08.2021 Sales', '12.08.2021 Sales', '13.08.2021 Sales',
    '14.08.2021 Sales', '15.08.2021 Sales', '16.08.2021 Sales',
    '17.08.2021 Sales', '18.08.2021 Sales', '19.08.2021 Sales',
    '20.08.2021 Sales', '21.08.2021 Sales', '22.08.2021 Sales',
    '23.08.2021 Sales', '24.08.2021 Sales', '25.08.2021 Sales',
    '26.08.2021 Sales', '27.08.2021 Sales', '28.08.2021 Sales',
    '29.08.2021 Sales', '30.08.2021 Sales', '31.08.2021 Sales',
    '01.09.2021 Sales', '02.09.2021 Sales', '03.09.2021 Sales',
    '04.09.2021 Sales', '05.09.2021 Sales', '06.09.2021 Sales',
    '07.09.2021 Sales', '09.08.2021 Revenue', '10.08.2021 Revenue',
    '11.08.2021 Revenue', '12.08.2021 Revenue', '13.08.2021 Revenue',
    '14.08.2021 Revenue', '15.08.2021 Revenue', '16.08.2021 Revenue',
    '17.08.2021 Revenue', '18.08.2021 Revenue', '19.08.2021 Revenue',
    '20.08.2021 Revenue', '21.08.2021 Revenue', '22.08.2021 Revenue',
    '23.08.2021 Revenue', '24.08.2021 Revenue', '25.08.2021 Revenue',
    '26.08.2021 Revenue', '27.08.2021 Revenue', '28.08.2021 Revenue',
    '29.08.2021 Revenue', '30.08.2021 Revenue', '31.08.2021 Revenue',
    '01.09.2021 Revenue', '02.09.2021 Revenue', '03.09.2021 Revenue',
    '04.09.2021 Revenue', '05.09.2021 Revenue', '06.09.2021 Revenue',
    '07.09.2021 Revenue', 'category_0', 'category_1', 'category_2',
    'category_3', 'category_4', 'category_5', 'shop_id']

markers_columns = ["id", "name", "geometry"]

search_logs_columns = ["id", "user_id", "query", "date", "time"]


def sql_result_to_pandas(sql_result: list, table_name: str):
    if table_name == 'ways':
        return pd.DataFrame(sql_result, columns=ways_columns)

    if table_name == 'nodes':
        return pd.DataFrame(sql_result, columns=nodes_columns)

    if table_name == 'markers':
        return pd.DataFrame(sql_result, columns=markers_columns)

    if table_name == 'search_logs':
        return pd.DataFrame(sql_result, columns=search_logs_columns)

    return pd.DataFrame(sql_result, columns=products_columns)


def pandas_to_sales(table: pd.DataFrame):
    sales_columns = table.columns[table.columns.str.contains(' Sales')]
    revenue_columns = table.columns[table.columns.str.contains(' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    return pd.DataFrame(
        index=dates,
        data=np.c_[
            table[sales_columns].values.flatten(),
            table[revenue_columns].values.flatten()],
        columns=['sales', 'revenue']
    )


def pandas_to_shop_sales_grouped(table: pd.DataFrame, column_to_group: str):
    table = table.groupby([column_to_group], as_index=False).sum()
    sales_columns = table.columns[table.columns.str.contains(' Sales')]
    revenue_columns = table.columns[table.columns.str.contains(' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    return [
        pd.DataFrame(
            index=dates,
            data=table[sales_columns].T.values,
            columns=table[column_to_group]
        ),
        pd.DataFrame(
            index=dates,
            data=table[revenue_columns].T.values,
            columns=table[column_to_group]
        )
    ]


def pandas_to_shop_total_sales(table: pd.DataFrame, id: int, shops_table: pd.DataFrame):
    table = table.groupby(['shop_id'], as_index=False).sum()
    table = table[table['shop_id'] == id]
    sales_columns = table.columns[table.columns.str.contains(' Sales')]
    revenue_columns = table.columns[table.columns.str.contains(' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    return pd.DataFrame(
        index=dates,
        data=np.c_[
            table[sales_columns].T.values,
            table[revenue_columns].T.values
        ],
        columns=np.r_[
            shops_table[shops_table['id'] == id]['name'] + ' sales',
            shops_table[shops_table['id'] == id]['name'] + ' revenue'
        ]

    )


def pandas_to_shop_total_sales_grouped(table: pd.DataFrame, shops_table: pd.DataFrame):
    table = table.groupby(['shop_id'], as_index=False).sum()
    sales_columns = table.columns[table.columns.str.contains(' Sales')]
    revenue_columns = table.columns[table.columns.str.contains(' Revenue')]
    dates = sorted(
        pd.to_datetime(
            sales_columns.str.split(' ').str[0],
            dayfirst=True)
    )

    return [
        pd.DataFrame(
            index=dates,
            data=table[sales_columns].T.values,
            columns=shops_table['id']
        ),
        pd.DataFrame(
            index=dates,
            data=table[revenue_columns].T.values,
            columns=shops_table['id']
        )
    ]
