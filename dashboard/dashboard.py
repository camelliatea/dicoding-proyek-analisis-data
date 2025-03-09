import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Set Layout
st.set_page_config(
    page_title='Bike Sharing Dashboard',
    page_icon='bar_chart',
    layout='wide')

# Load Data
main_data = pd.read_csv('https://raw.githubusercontent.com/camelliatea/dicoding-proyek-analisis-data/refs/heads/main/dashboard/main_data.csv')
main_data['date'] = pd.to_datetime(main_data['date'])

# Helper function untuk menyiapkan DataFrame
def create_daily_users(df):
    daily_users_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_users_df

def create_monthly_users(df):
    monthly_users_df = df.resample(rule='M', on='date').agg({
        'registered': 'sum',
        'casual': 'sum',
        'count': 'sum'
    }).reset_index()
    monthly_users_df['date'] = monthly_users_df['date'].dt.strftime('%b-%y')
    return monthly_users_df

def create_season_users(df):
    season_users_df = df.groupby('season')[['registered', 'casual', 'count']].sum().reset_index()
    return season_users_df

def create_weather_users(df):
    weather_users_df = df.groupby('weather')[['registered', 'casual', 'count']].mean().reset_index()
    return weather_users_df

def create_workingday_users(df):
    workingday_users_df = df.groupby('workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_users_df

def create_temp_df(df):
    temp_df = df.groupby(by='temp').agg({
        'count': 'mean'
    }).reset_index()
    return temp_df

def create_atemp_df(df):
    atemp_df = df.groupby(by='atemp').agg({
        'count': 'mean'
    }).reset_index()
    return atemp_df

def create_hum_df(df):
    hum_df = df.groupby(by='humidity').agg({
        'count': 'mean'
    }). reset_index()
    return hum_df

def create_windspeed_df(df):
    windspeed_df = df.groupby(by='windspeed').agg({
        'count': 'mean'
    }). reset_index()
    return windspeed_df

def create_casual_users(df):
    casual_users_df = df.groupby('date').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_users_df

def create_registered_users(df):
    registered_users_df = df.groupby('date').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_users_df

def create_weekday_users(df):
    weekday_users_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_users_df

def create_total_bins(df):
    users_bins = df.groupby('count_bins').agg({
        'count': 'count'
    }).reset_index()
    return users_bins

def create_casual_bins(df):
    casual_bins = df.groupby('casual_bins').agg({
        'casual': 'count'
    }).reset_index()
    return casual_bins

def create_registered_bins(df):
    registered_bins = df.groupby('registered_bins').agg({
        'registered': 'count'
    }).reset_index()
    return registered_bins

# Setting Sidebar
min_date = main_data['date'].min()
max_date = main_data['date'].max()

with st.sidebar:
    # menambahkan logo perusahaan 'Blue Bike' (fiksi)
    st.image('dashboard/bluebike_logo.png')

    # mengatur filter
    st.header('Filter: ')
    # mengambil start_Date dan end_date dari date_input
    try:
        start_date, end_date = st.date_input(
            label='Date Filter', 
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
    )
    except ValueError:
        st.error("You must pick a start and end date")
        st.stop()
    
    st.header ('created by: ')
    st.write('Elita Camellia')

# menghubungkan filter dengan dataframe utama
main_df = main_data[
    (main_data['date'] >= str(start_date)) & 
    (main_data['date'] <= str(end_date))
]

# menetapkan main_df le helper function
daily_users_df = create_daily_users(main_df)
monthly_users_df = create_monthly_users(main_df)
season_users_df = create_season_users(main_df)
weather_users_df = create_weather_users(main_df)
weekday_users_df = create_weekday_users(main_df)
workingday_users_df = create_workingday_users(main_df)
temp_df = create_temp_df(main_df)
atemp_df = create_atemp_df(main_df)
hum_df =  create_hum_df(main_df)
windspeed_df = create_windspeed_df(main_df)
casual_users_df = create_casual_users(main_df)
registered_users_df = create_registered_users(main_df)
users_bins = create_total_bins(main_df)
casual_bins = create_casual_bins(main_df)
registered_bins = create_registered_bins(main_df)


# Membentuk User Interface (UI) mainpage
st.header('Blue Bike Dashboard')
st.markdown('###')

## Subheader untuk Rentals Summary
st.subheader('Bikers Summary')

col1, col2, col3 = st.columns(3)

with col1:
    daily_users_df = daily_users_df['count'].sum()
    st.metric('Total Bikers', value=daily_users_df)

with col2:
    registered_users_df = registered_users_df['registered'].sum()
    st.metric('Registered Bikers', value=registered_users_df)

with col3:
    casual_users_df = casual_users_df['casual'].sum()
    st.metric('Casual Bikers', value=casual_users_df)

# Chart
## Monthly Bikers
st.markdown('###')

with st.container():
    st.subheader('Monthly Bikers')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        monthly_users_df['date'],
        monthly_users_df['count'],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=9)
    st.pyplot(fig)

col4, col5 = st.columns(2)

with col4:
    with st.container():
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(
            monthly_users_df['date'],
            monthly_users_df['casual'],
            marker='o', 
            linewidth=2,
            color="#90CAF9"
        )
        ax.tick_params(axis='y', labelsize=11)
        ax.tick_params(axis='x', labelsize=9)
        ax.set_title('Casual', loc='center', fontsize=20)
        st.pyplot(fig)

with col5:
    with st.container():
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(
            monthly_users_df['date'],
            monthly_users_df['registered'],
            marker='o', 
            linewidth=2,
            color="#90CAF9"
        )
        ax.tick_params(axis='y', labelsize=11)
        ax.tick_params(axis='x', labelsize=9)
        ax.set_title('Registered', loc='center', fontsize=20)
        st.pyplot(fig)

## Season Chart
st.markdown('###')
st.subheader('Bikers by Season')

with st.container():
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='count', 
        y='season', 
        data=season_users_df.sort_values(by='season', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

col6, col7 = st.columns(2)

with col6:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='season', 
        y='registered', 
        data=season_users_df.sort_values(by='season', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Registered', loc='center', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

with col7:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='season', 
        y='casual', 
        data=season_users_df.sort_values(by='season', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Casual', loc='center', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

##  Weather Chart
st.markdown('###')
st.subheader('Bikers by Weather')

with st.container():
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='count', 
        y='weather', 
        data=weather_users_df.sort_values(by='weather', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

col8, col9 = st.columns(2)

with col8:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='weather', 
        y='registered', 
        data=weather_users_df.sort_values(by='weather', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Registered', loc='center', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

with col9:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='weather', 
        y='casual', 
        data=weather_users_df.sort_values(by='weather', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title('Casual', loc='center', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

## Weekday Bikers
st.markdown('###')
st.subheader('Bikers by Day')

col10, col11 = st.columns(2)
with col10:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='weekday', 
        y='count', 
        data=weekday_users_df.sort_values(by='weekday', ascending=True), 
        palette=colors,
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

with col11:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#D3D3D3', '#90CAF9']

    sns.barplot(
        x='workingday', 
        y='count', 
        data=workingday_users_df.sort_values(by='workingday', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    st.pyplot(fig)

## Environmental
st.markdown('###')
st.subheader('Environmental Conditions')

col12, col13= st.columns(2)

with col12:
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.scatter(
        temp_df['temp'], 
        temp_df['count'], 
        color='blue', 
        marker='o')
    ax.set_ylabel('Average')
    ax.set_xlabel('Temperature')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Temperature', loc='center', fontsize=20)
    st.pyplot(fig)

with col13:
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.scatter(
        atemp_df['atemp'], 
        atemp_df['count'], 
        color='blue', 
        marker='o')
    ax.set_ylabel('Average')
    ax.set_xlabel('Feeling Temperature')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Feeling Temperature', loc='center', fontsize=20)
    st.pyplot(fig)

col14, col15 = st.columns(2)

with col14:
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.scatter(
        hum_df['humidity'], 
        hum_df['count'], 
        color='blue', 
        marker='o')
    ax.set_ylabel('Average')
    ax.set_xlabel('Humidity')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Humidity', loc='center', fontsize=20)
    st.pyplot(fig)

with col15:
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.scatter(
        windspeed_df['windspeed'], 
        windspeed_df['count'], 
        color='blue', 
        marker='o')
    ax.set_ylabel('Average')
    ax.set_xlabel('Wind Speed')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Wind Speed', loc='center', fontsize=20)
    st.pyplot(fig)

## Clustering
st.markdown('###')
st.subheader('Clustering')

col16, col17, col18= st.columns(3)

with col16:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#D3D3D3', '#D3D3D3','#90CAF9']

    sns.barplot(
        x='count_bins', 
        y='count', 
        data=users_bins.sort_values(by='count_bins', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Total Bikers by Activity Level', loc='center', fontsize=20)
    st.pyplot(fig)

with col17:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#90CAF9','#D3D3D3', '#D3D3D3']

    sns.barplot(
        x='casual_bins', 
        y='casual', 
        data=casual_bins.sort_values(by='casual_bins', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Casual Bikers by Activity Level', loc='center', fontsize=20)
    st.pyplot(fig)

with col18:
    fig, ax = plt.subplots(figsize=(16, 8))

    colors = ['#D3D3D3', '#D3D3D3', '#90CAF9']

    sns.barplot(
        x='registered_bins', 
        y='registered', 
        data=registered_bins.sort_values(by='registered_bins', ascending=True), 
        palette=colors, 
        ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.set_title('Registered Bikers by Activity Level', loc='center', fontsize=20)
    st.pyplot(fig)