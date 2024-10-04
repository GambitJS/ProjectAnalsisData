import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul dashboard
st.title('Bike Sharing Dashboard')

# Membaca data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])


# Sidebar untuk pilihan dataset
selected_dataset = st.sidebar.selectbox("Select Dataset", ["Daily Data", "Hourly Data"])

if selected_dataset == "Daily Data":
    df = day_df
    time_column = 'dteday'
else:
    df = hour_df
    time_column = 'hr'


# Filter berdasarkan rentang tanggal (untuk data harian)
if selected_dataset == "Daily Data":
    start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
    end_date = st.sidebar.date_input("End Date", df['dteday'].max())
    filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Filter berdasarkan jam (untuk data per jam)
elif selected_dataset == "Hourly Data":
    selected_hour = st.sidebar.select_slider("Select Hour", options=df['hr'].unique())
    filtered_df = df[df['hr'] == selected_hour]
else:
    filtered_df = df

# Menampilkan DataFrame (opsional)
if st.checkbox("Show Data"):
    st.write(filtered_df)


# Visualisasi 1: Pola peminjaman berdasarkan hari (atau jam)
st.header('Bike Usage Trend')
plt.figure(figsize=(10, 6))
if selected_dataset == "Daily Data":
    sns.lineplot(x='dteday', y='cnt', data=filtered_df)
else:
    sns.barplot(x=time_column, y='cnt', data=filtered_df)
st.pyplot(plt)


# Visualisasi 2: Perbandingan casual vs registered
st.header("Casual vs. Registered Users")
if selected_dataset == "Daily Data": # Bar plot untuk data harian
    plt.figure(figsize=(10, 6))
    sns.barplot(x='weekday', y='cnt', hue='workingday', data=filtered_df)
    st.pyplot(plt)

    plt.figure(figsize=(10,6))
    sns.barplot(data=filtered_df, x='weekday', y='cnt', hue='holiday')
    st.pyplot(plt)

elif selected_dataset == "Hourly Data":  # Line plot untuk data per jam, misal perbandingan dalam satu hari
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='hr', y='casual', data=filtered_df, label="casual")
    sns.lineplot(x='hr', y='registered', data=filtered_df, label="registered")
    plt.legend()
    st.pyplot(plt)



# Visualisasi 3: Pengaruh cuaca
st.header("Bike Rentals Based on Weather")

plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=filtered_df)
st.pyplot(plt)