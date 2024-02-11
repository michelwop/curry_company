import pandas as pd
import plotly.express as px
import folium
from datetime import datetime
import time
from haversine import haversine
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import plotly.graph_objects as go


def create_sidebar(df):
    image_path = "./img/"
    image = Image.open(image_path + "food_delivery.png")
    st.sidebar.image(image)
    
    st.sidebar.markdown( "# Cury Company" )
    st.sidebar.markdown( "Fastest Delivery in Town" )
    st.sidebar.markdown( """---""" )
    
    date_slider = st.sidebar.slider(
        'Selecione uma data limite', 
        value=datetime(2022, 3, 13),
        min_value=datetime(2022, 2, 11),
        max_value=datetime(2022, 4, 6),
        format='DD-MM-YYYY')
    
    traffic_options = st.sidebar.multiselect(
       'Escolha a densidade do tráfego',
        df['road_traffic_density'].unique(),
        default=df['road_traffic_density'].unique())
    
    st.sidebar.markdown( """---""" )
    st.sidebar.markdown( "#### Powered by Comunidade DS" )
    
    return list(traffic_options), date_slider

def create_home(df):
    st.markdown( '# Visão Cliente' )
    tab1, tab2, tab3 = st.tabs(["Visão Gerencial", "Visão Tática", "Visão Geográfica"])
    
    with tab1:
        with st.container():
            st.header( 'Ordens por Dia' )
            cols = ['id', 'order_date']
            df1 = df.loc[:, cols].groupby('order_date').count().reset_index()
            fig = px.bar(df1, x='order_date', y='id')
            st.plotly_chart(fig, use_container_width=True)
        
        with st.container():
            col1, col2 = st.columns (2)
            with col1:
                st.header('Venda por Densidade de Tráfego')
                cols = ['id', 'road_traffic_density']
                df.loc[:, cols].groupby('road_traffic_density').count().reset_index()
                fig = px.pie(df, values='id', names='road_traffic_density')
                st.plotly_chart(fig, use_container_width=True)
        
            with col2:
                st.header('Densidade de Tráfego por Cidade')
                cols = ['id', 'city', 'road_traffic_density']
                df_aux = df[cols].groupby(['city', 'road_traffic_density']).count().reset_index()
                fig = px.scatter(df_aux, x='city', y='road_traffic_density', size='id', color='city')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        with st.container():
            st.header('Ordens Semanal')
            df['week_of_year'] = df['order_date'].dt.strftime('%U')
            cols = ['id', 'week_of_year']
            df1 = df.loc[:, cols].groupby('week_of_year').count().reset_index()
            fig = px.line(df1, x='week_of_year', y='id')
            st.plotly_chart(fig, use_container_width=True)
    
            cols1 = ['delivery_person', 'week_of_year']
            cols2 = ['id', 'week_of_year']
    
            st.header('Ordens por Entregadores Semanal')
            #Qtd entregadores na semana
            df_aux1 = df[cols1].groupby('week_of_year').nunique().reset_index()
            
            #Pedidos na Semana
            df_aux2 = df[cols2].groupby('week_of_year').count().reset_index()
            
            #Junção de Dataframes
            df_aux = pd.merge(df_aux1, df_aux2, how='inner')
            df_aux['order_by_deliver'] = df_aux['id'] / df_aux['delivery_person']
            
            #Apresentar gráfico de linhas
            fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        with st.container():
            st.header('Localização')
            cols = ['city', 'road_traffic_density', 'delivery_location_latitude', 'delivery_location_longitude']
            df_aux = df[cols].groupby(['city', 'road_traffic_density']).median().reset_index()
    
            map = folium.Map()        
            for i in range(0,len(df_aux)):
               folium.Marker(
                  location=[df_aux.iloc[i]['delivery_location_latitude'],
                            df_aux.iloc[i]['delivery_location_longitude']],
                  popup=df_aux.iloc[i][['city','road_traffic_density']],
               ).add_to(map)
    
            map.fit_bounds([[df_aux['delivery_location_latitude'].min(), df_aux['delivery_location_longitude'].min()],
                            [df_aux['delivery_location_latitude'].max(), df_aux['delivery_location_longitude'].max()]])
            
            folium_static (map, width=1024, height=600)
    return None