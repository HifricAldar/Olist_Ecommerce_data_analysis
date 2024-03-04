import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Dashboard E-Commerce Olist", page_icon=":bar_chart:", layout="wide")

df = pd.read_csv("https://raw.githubusercontent.com/HifricAldar/Olist_Ecommerce_data_analysis/main/Dashboard/olist_ecommerce_cleaned.csv")

st.markdown("<h1 class='labels-for-title'>Dashboard E-Commerce Olist</h1>", unsafe_allow_html=True)

def customer_place():
    top_cities = df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False).head(10)

    fig = px.bar(top_cities, 
                x=top_cities.values, 
                y=top_cities.index,  
                orientation='h', 
                labels={'x': 'Jumlah Pelanggan', 'y': 'Kota'}, 
                title='Top 10 Kota dengan Jumlah Pelanggan Terbanyak',
                color_discrete_sequence=['skyblue']) 
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#5e697a',
        xaxis=dict(showgrid=False),
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

def payment_method():
    payment_counts_df = df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False).reset_index()
    payment_counts_df.columns = ["payment_type", "order_count"]

    fig = px.pie(payment_counts_df, 
                values='order_count', 
                names='payment_type', 
                title='Jumlah Pesanan Unik berdasarkan Jenis Pembayaran',
                hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

def top_product_category():
    top_products = df.groupby(by="product_category_name_english").order_id.nunique().sort_values(ascending=False).head(5)

    fig = go.Figure(data=[go.Bar(
        y=top_products.index,
        x=top_products.values,
        orientation='h',
        marker=dict(color='skyblue')
    )])
    fig.update_layout(title='Top 5 Kategori Produk Paling Banyak Dibeli', 
                      yaxis_title='Produk', 
                      xaxis_title='Jumlah Pesanan',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='#5e697a',
                      xaxis=dict(showgrid=False),
                      font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

def order_days():
    orders_per_day = df['order_day_of_week'].value_counts()
    explode = [0] * len(orders_per_day)
    explode[orders_per_day.values.argmax()] = 0.1

    fig = go.Figure(data=[go.Pie(
        labels=orders_per_day.index,
        values=orders_per_day,
        pull=[0.1 if i == orders_per_day.values.argmax() else 0 for i in range(len(orders_per_day))],
    )])
    fig.update_layout(
        title='Jumlah Pesanan per Hari dalam Seminggu',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.02,
            xanchor="left",
            x=0.01
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
def weekly_sales_per_years():
    orders_copy = df.copy()
    orders_copy['order_purchase_timestamp'] = pd.to_datetime(orders_copy['order_purchase_timestamp'])
    orders_copy['year'] = orders_copy['order_purchase_timestamp'].dt.year
    orders_copy['week'] = orders_copy['order_purchase_timestamp'].dt.week

    weekly_sales_per_year = orders_copy.groupby(['year', 'week']).size().reset_index(name='total_sales')
    fig = go.Figure()

    for year in range(2016, 2019):
        data_year = weekly_sales_per_year[weekly_sales_per_year['year'] == year]
        fig.add_trace(go.Scatter(
            x=data_year['week'],
            y=data_year['total_sales'],
            mode='lines+markers',
            name=str(year)
        ))

    fig.update_layout(
        title='Total Pembelian per Minggu untuk Setiap Tahun',
        xaxis_title='Minggu dalam Tahun',
        yaxis_title='Total Pembelian per Minggu',
        xaxis=dict(
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#5e697a',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

top_left_corner, top_middle, top_right_corner = st.columns((1,1,1))
with top_left_corner:
    order_days()
with top_middle:
    customer_place()
with top_right_corner:
    payment_method()
bottom_left_corner, bottom_right_corner = st.columns((1,1))
with bottom_left_corner:
    weekly_sales_per_years()
with bottom_right_corner:
    top_product_category()


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
