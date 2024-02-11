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
    st.markdown( '# Visão Restaurantes' )

    with st.container():
        st.title("Métricas")
    
        col1, col2, col3, col4, col5, col6 = st.columns(6)
    
        with col1:
            qtd_entregadores = df['delivery_person'].nunique()
            col1.metric( "Entregadores únicos", qtd_entregadores)
    
        with col2:
            df['distancia(km)'] = df.apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']), (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1 )
            avg_distance = df['distancia(km)'].mean()
            col2.metric( "Distância média das entregas", round(avg_distance, 2))
    
        with col3:
            cols = ['time_taken(min)', 'festival']
            df_aux = df[cols].groupby(['festival']).agg({ 'time_taken(min)' : 'mean'})
            
            df_aux.columns = ['avg_time']
            df_aux1 = df_aux.reset_index()        
            df_aux1 = df_aux1['avg_time'][df_aux1['festival'] == 'Yes']
    
            #col3.metric( "Tempo médio de entrega em festivais", round(df_aux1, 2))
            col3.metric( "Tempo médio de entrega em festivais", df_aux1)
    
        with col4:
            cols = ['time_taken(min)', 'festival']
            df_aux = df[cols].groupby(['festival']).agg({ 'time_taken(min)' : 'std'})
            
            df_aux.columns = ['std_time']
            df_aux1 = df_aux.reset_index()        
            df_aux1 = df_aux1['std_time'][df_aux1['festival'] == 'Yes']
    
            col4.metric( "Desvio padrão de entrega em festivais", round(df_aux1, 2))
    
        with col5:
            cols = ['time_taken(min)', 'festival']
            df_aux = df[cols].groupby(['festival']).agg({ 'time_taken(min)' : 'mean'})
            
            df_aux.columns = ['avg_time']
            df_aux1 = df_aux.reset_index()        
            df_aux1 = df_aux1['avg_time'][df_aux1['festival'] == 'No']
    
            col5.metric( "Tempo médio de entregas sem festivais", round(df_aux1, 2))
    
        with col6:
            cols = ['time_taken(min)', 'festival']
            df_aux = df[cols].groupby(['festival']).agg({ 'time_taken(min)' : 'std'})
            
            df_aux.columns = ['std_time']
            df_aux1 = df_aux.reset_index()        
            df_aux1 = df_aux1['std_time'][df_aux1['festival'] == 'No']
    
            col6.metric( "Desvio padrão de entrega sem festivais", round(df_aux1, 2)) 
    
    with st.container():
        st.markdown("""---""")
        st.title("Tempo Médio de entrega por cidade")
        col1, col2 = st.columns(2)
    
        with col1:
            cols = ['city', 'time_taken(min)']
            df_aux = df.loc[:, cols].groupby( 'city' ).agg({ 'time_taken(min)' : ['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
    
            fig = px.bar(df_aux, x=df_aux['city'], y=df_aux['avg_time'])
            st.plotly_chart(fig, use_container_width=True)
            
           
        with col2:
            cols = ['city', 'time_taken(min)', 'type_of_order']            
            df_aux = df.loc[:, cols].groupby( ['city', 'type_of_order'] ).agg({ 'time_taken(min)' : ['mean', 'std']})
            
            df_aux.columns = ['avg_time', 'std_time']
                   
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe( df_aux )
        
    with st.container():
        st.markdown("""---""")
        st.title("Distribuição do Tempo")
        
        cols = ['delivery_location_latitude',
                'delivery_location_longitude',
                'restaurant_latitude',
                'restaurant_longitude']
        
        df['distance'] = df.loc[:, cols].apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']), (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1 )
        avg_distance = df.loc[:, ['city', 'distance']].groupby( 'city' ).mean().reset_index()
        fig = go.Figure(data=[ go.Pie(labels=avg_distance['city'], values=avg_distance['distance'], pull=[0, 0.3, 0])])
        st.plotly_chart(fig)    
    
    
    with st.container():
        df_aux = ( df.loc[:, ['city', 'time_taken(min)', 'road_traffic_density']]
                   .groupby( ['city', 'road_traffic_density'] )
                   .agg( {'time_taken(min)': ['mean', 'std']} ) )
        
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        fig = px.sunburst(
            df_aux,
            path=['city', 'road_traffic_density'],
            values='avg_time',
            color='std_time',
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(df_aux['std_time'] ) )
        
        st.plotly_chart( fig )
    
    return None