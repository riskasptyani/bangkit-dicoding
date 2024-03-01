import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set_theme(style='dark')

# Bike season berisi total pelanggan dalam kelompok musim
def bike_season_df(df):
    season_df = df.groupby(by="season").agg({
        "cnt": "max"
    }).reset_index() 
    return season_df

# Bike year berisi total pelanggan dalam setiap tahun
def bike_year_df(df):
    year_df = df.groupby(by="year").agg({
        "cnt": "min"
    }).reset_index() 
    return year_df

# Mengimport data dari csv
day_df = pd.read_csv("https://raw.githubusercontent.com/riskasptyani/bangkit-dicoding/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/riskasptyani/bangkit-dicoding/main/data/hour.csv")

# Mengubah tipe data datetime, dan juga merubah beberapa nama kolom pada day_df
datetime_columns = ["dteday"]

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

day_df.info()

day_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "weathersit" : "weather"
}, inplace=True)

day_df.info()

# Mengubah tipe data datetime, dan juga merubah beberapa nama kolom pada hour_df
datetime_columns = ["dteday"]

for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

hour_df.info()

hour_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "hr" : "hour",
    "weathersit" : "weather"
}, inplace=True)

hour_df.info()

# Membuat variabel min_date dan max_date sebagai batasan dalam tanggal dashboard
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Menambahkan logo dan namas
    st.write("Riska's Bike Sharing")
    st.image("dashboard/undraw_Ride_a_bicycle_re_6tjy-removebg-preview.png")
    # Menginisialisasi start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
# Mendeklarasikan tanggal awal dan akhir pada data day dan hour
day_data_df = day_df[(day_df["date"] >= str(start_date)) & 
                       (day_df["date"] <= str(end_date))]

hour_data_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                       (hour_df["date"] <= str(end_date))]

# Menyiapkan berbagai dataframe dengan memanggil func yang dubuat sebelumnya
season_df = bike_season_df(day_data_df)
year_df = bike_year_df(day_data_df)

# Membuat judul Dashboard
st.title('Dashboard Penyewaan Sepeda Thn. 2011 - 2012')

st.markdown("-------")

# pola yang terjadi pada jumlah total penyewaan sepeda berdasarkan Musim
plt.style.use('dark_background')
st.subheader("Penyewaan sepeda berdasarkan Musim")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24,6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="season", y="cnt", data=day_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Jumlah peminjam berdasarkan musim pada data harian", loc="center", fontsize=15)
ax[0].tick_params(axis="x", labelsize=12)

sns.barplot(x="season", y="cnt", data=hour_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Jumlah peminjam berdasarkan musim pada data dalam jam", loc="center", fontsize=15)
ax[1].tick_params(axis="x", labelsize=12)

plt.tight_layout()
st.pyplot(fig)
with st.expander('Penjelasan'):
    st.write(
        """
        1 : Spring
        
        2 : Summer
        
        3 : Fall

        4 : Winter
        """
    )

st.markdown("-------")

# pola yang terjadi pada jumlah total penyewaan sepeda berdasarkan Tahun
plt.style.use('dark_background')
st.subheader("Penyewaan sepeda berdasarkan Tahun")

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(24,6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="year", y="cnt", data=day_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Jumlah peminjam berdasarkan tahun pada data harian", loc="center", fontsize=15)
ax[0].tick_params(axis="x", labelsize=12)

sns.boxplot(x="year", y="cnt", data=hour_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Jumlah peminjam berdasarkan tahun pada data dalam jam", loc="center", fontsize=15)
ax[1].tick_params(axis="x", labelsize=12)

plt.tight_layout()
st.pyplot(fig)
with st.expander('Penjelasan'):
    st.write(
        """
        0 : 2011
        
        1 : 2012

        """
    )

st.markdown("-------")
