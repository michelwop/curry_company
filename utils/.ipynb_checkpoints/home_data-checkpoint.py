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
    
    values = st.sidebar.slider(
        'Selecione uma data limite',
        value=datetime(2022, 3, 13),
        min_value=df['order_date'].min(),
        max_value=df['order_date'].max(),
        format='DD-MM-YYYY')
    
    traffic_density = st.sidebar.multiselect(
        'Escolha a densidade do tráfego',
        df['road_traffic_density'].unique(),
        df['road_traffic_density'].unique())

    st.sidebar.markdown("### Dados Tratados")

    processed_data = pd.read_csv("./dataset/train_processed.csv")

    st.sidebar.download_button(
        label="Download",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )

    return list(traffic_density), values

def create_home(df):
    st.title(':red[Marketplace | Cury Company] :100:')
    
    tab1, tab2, tab3 = st.tabs(["Entregadores", "Restaurantes", "Cliente"])
    
    with tab1:
        st.subheader('Visão Entregadores')  
    
        st.container()
        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            st.metric(label='A menor idade', value=df['delivery_person_age'].min())
    
        with col2:
            st.metric(label='A maior idade', value=df['delivery_person_age'].max())
        
        with col3:
            st.metric(label='A pior condição veículos', value=df['vehicle_condition'].min())
    
        with col4:
            st.metric(label='A melhor condição veículos', value=df['vehicle_condition'].max())
    
        st.container()
        df_aux = df[['delivery_person_ratings', 'road_traffic_density']].groupby('road_traffic_density').count().sort_values(by='delivery_person_ratings', ascending=False).reset_index()
        
        fig = px.pie(df_aux, values='delivery_person_ratings', names='road_traffic_density', title='Contagem de Avaliação padrão por tipo de tráfego.', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)
    
    with tab2:
        st.subheader('Visão Restaurantes')  
    
        st.container()
        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            st.metric(label='Qtd entregadores únicos', value=df['delivery_person'].nunique())
    
        with col2:
            df['distancia(km)'] = df.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']), (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1 )
            st.metric(label='A distância média dos resturantes e dos locais de entrega', value=round(df['distancia(km)'].mean(), 2))
    
        st.container()
        
        cols = ['city', 'time_taken(min)']
        df_aux = df[cols].groupby('city').agg({ 'time_taken(min)' : ['mean', 'std']})    
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.sort_values(by='avg_time', ascending=False).reset_index()
    
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_aux['city'],
           y=df_aux['avg_time'],
            name='O tempo médio de entrega por cidade',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=df_aux['city'],
            y=df_aux['std_time'],
            name='O desvio padrão de entrega por cidade',
            marker_color='lightsalmon'
        ))
        
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(fig)
    
    with tab3:
        st.subheader('Visão Empresa')  
    
        st.container()
        col1, col2, col3, col4 = st.columns(4)
    
        with col1:
            st.metric(label='Qtd entregadores únicos', value=df['delivery_person'].nunique())
    
        with col2:
            df['distancia(km)'] = df.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']), (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1 )
            st.metric(label='A distância média dos resturantes e dos locais de entrega', value=round(df['distancia(km)'].mean(), 2))
    
        st.container()
        
        cols = ['id', 'road_traffic_density']
        df_aux = df.loc[:, cols].groupby('road_traffic_density').count().reset_index()
    
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_aux['road_traffic_density'],
           y=df_aux['id'],
            name='Distribuição dos pedidos por tipo de tráfego',
            marker_color='indianred'
        ))
        
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(fig)
        
        df['week_of_year'] = df['order_date'].dt.strftime('%U')
        cols1 = ['delivery_person', 'week_of_year']
        cols2 = ['id', 'week_of_year']
        
        #Qtd entregadores na semana
        df_aux1 = df[cols1].groupby('week_of_year').nunique().reset_index()
        
        #Pedidos na Semana
        df_aux2 = df[cols2].groupby('week_of_year').count().reset_index()
        
        #Junção de Dataframes
        df_aux = pd.merge(df_aux1, df_aux2, how='inner')
        df_aux['order_by_deliver'] = df_aux['id'] / df_aux['delivery_person']
        
        #Apresentar gráfico de linhas
        st.line_chart(df_aux, x="week_of_year", y=["delivery_person", "id"], color=["#CD5C5C", "#FFA07A"])

    return None