from shops_database import Table as ShopsTable
from products_database import Table as ProductsTable
from markers_database import Table as MarkersTable
from tools import sql_result_to_pandas
import plotly.express as px


def sales_revenue_distribution(st, table_df, shops_table_df,
                               products_table_df):
    map_df = table_df.merge(
        shops_table_df,
        left_on='id',
        right_on='way_id',
        suffixes=(None, "_x")
    ).merge(
        products_table_df,
        left_on='id_x',
        right_on='shop_id',
        suffixes=(None, "_y")
    ).groupby(['id', 'name', 'geometry'],
              as_index=False).sum()[['id',
                                     'name',
                                     'geometry',
                                     'Sales',
                                     'Revenue']]

    map_df['lat'] = map_df['geometry'].str.split(' ').str[-1].str[:-1].astype(
        float)
    map_df['lon'] = map_df['geometry'].str.split(' ').str[1].str[1:].astype(
        float)

    with st.sidebar:
        value = st.radio("Choose what to display",
                         ('Sales', 'Revenue'))

    st.markdown(
        '## :chart_with_upwards_trend: Sales & Revenue distribution')
    fig = px.scatter_mapbox(map_df, lat='lat', lon='lon',
                            size=value, color=value, hover_name='name',
                            opacity=1, center=dict(lat=51.1266, lon=71.429),
                            zoom=11.5, mapbox_style="carto-positron", height=700)
    st.plotly_chart(fig, use_container_width=True)


def sunburst(st, products_table_df):
    st.markdown("## :sunny: Sunburst chart of categories")

    products_table_df = products_table_df.fillna('')
    fig = px.sunburst(products_table_df, path=['category_0', 'category_1'],
                      values='Sales', labels={'labels': 'Category',
                                              'Sales': 'Sales',
                                              'parent': 'Parent category',
                                              'id': 'Full category'})
    st.plotly_chart(fig, use_container_width=True)


def metrics(st, products_table_df):
    st.markdown("## :currency_exchange: Malls metrics")

    max_price = products_table_df['Max price'].max()
    min_price = products_table_df['Min price'].min()
    average_price = products_table_df['Average price'].mean()//1000
    total_sales = products_table_df['Sales'].sum()
    total_revenue = products_table_df['Revenue'].sum()
    revenue_potential = products_table_df['Revenue potential'].mean()//1000
    lost_profit = products_table_df['Lost profit'].mean()//1000
    lost_profit_percent = products_table_df['Lost profit percent'].mean()//1000
    sales_per_day_average = products_table_df['Sales per day average'].mean(
    )//1000

    column_1, column_2, column_3 = st.columns(3)
    column_1.metric("Max price", f"{max_price}", "10 %")
    column_2.metric("Min price", f"{min_price}", "8.55 %")
    column_3.metric("Average price", f"{average_price}", "0.12 %")

    column_1.metric("Sales", f"{total_sales}", "-0.88 %")
    column_2.metric("Revenue", f"{total_revenue}", "-0.86 %")
    column_3.metric("Revenue potential", f"{revenue_potential}", "40 %")

    column_1.metric("Lost profit", f"{lost_profit}", "-10%")
    column_2.metric("Lost profit percent", f"{lost_profit_percent}", "8.55 %")
    column_3.metric("Sales per day average",
                    f"{sales_per_day_average}", "13.45 %")


def malls_page(st):
    st.markdown(
        "# :department_store: Interactive map of places - Malls report")

    table = MarkersTable().select()
    table_df = sql_result_to_pandas(table, 'markers')
    shops_table = ShopsTable().select()
    shops_table_df = sql_result_to_pandas(shops_table, 'nodes')
    products_table = ProductsTable().select()
    products_table_df = sql_result_to_pandas(products_table, 'products')

    with st.sidebar:
        chart_type = st.selectbox("Choose what to display",
                                  ('Sales & Revenue distribuion',
                                   'Metrics',
                                   'Sunburst'))

    if chart_type == 'Sales & Revenue distribuion':
        sales_revenue_distribution(st, table_df, shops_table_df,
                                   products_table_df)
    elif chart_type == 'Sunburst':
        sunburst(st, products_table_df)
    else:
        metrics(st, products_table_df)
