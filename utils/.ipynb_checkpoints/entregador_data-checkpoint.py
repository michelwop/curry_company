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
    st.markdown( '# Visão Entregadores' )
    
    with st.container():
        st.title('Métricas')
        col1, col2, col3, col4 = st.columns (4)
        with col1:
            maior_idade = df['delivery_person_age'].max()
            col1.metric('Maior de Idade', maior_idade)
    
        with col2:
            menor_idade = df['delivery_person_age'].min()
            col2.metric('Maior de Idade', menor_idade)
            
        with col3:
            melhor_condicao = df['vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_condicao)
        
        with col4:
            pior_condicao = df['vehicle_condition'].min()
            col4.metric('Pior Condição', pior_condicao)
    
    with st.container():
        st.title('Avaliações')
        col1, col2 = st.columns (2)
        with col1:
            st.subheader('Avaliação Média por Entregador')
            st.dataframe(df[['delivery_person_ratings', 'delivery_person']]
                         .groupby('delivery_person').mean()
                         .sort_values(by='delivery_person_ratings', ascending=False).reset_index())
    
        with col2:
            st.subheader('Avaliação Média por Trânsito')
            st.dataframe(df[['delivery_person_ratings', 'road_traffic_density']]
                         .groupby('road_traffic_density').mean()
                         .sort_values(by='delivery_person_ratings', ascending=False).reset_index())
            
            st.subheader('Avaliação Média por clima')
            st.dataframe(df[['delivery_person_ratings', 'weatherconditions']]
                         .groupby('weatherconditions').mean()
                         .sort_values(by='delivery_person_ratings', ascending=False).reset_index())
    
    with st.container():
        st.title('Avaliações')
        col1, col2 = st.columns (2)
        with col1:
            st.subheader('Top entregadores mais rápidos')
            df_aux = df[['delivery_person', 'city', 'time_taken(min)']].groupby(['city', 'delivery_person']).mean().sort_values(by='time_taken(min)', ascending=True).reset_index()
            df_aux1 = df_aux.loc[df_aux['city'] == 'Metropolitian', :].head(10)
            df_aux2 = df_aux.loc[df_aux['city'] == 'Urban', :].head(10)
            df_aux3 = df_aux.loc[df_aux['city'] == 'Semi-Urban', :].head(10)
    
            df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
            st.dataframe(df2)
                
        with col2:
            st.subheader('Top entregadores mais lentos')
            df_aux = df[['delivery_person', 'city', 'time_taken(min)']].groupby(['city', 'delivery_person']).mean().sort_values(by='time_taken(min)', ascending=False).reset_index()
            df_aux1 = df_aux.loc[df_aux['city'] == 'Metropolitian', :].head(10)
            df_aux2 = df_aux.loc[df_aux['city'] == 'Urban', :].head(10)
            df_aux3 = df_aux.loc[df_aux['city'] == 'Semi-Urban', :].head(10)
    
            df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
            st.dataframe(df2)

    return None