import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca dataset
df = pd.read_csv('StudentPerformanceFactors.csv')

# Judul Dashboard
st.title('Dashboard Analisis Performa Siswa')

# Tampilkan informasi dataset lengkap pada awalnya
st.subheader('Informasi Dataset Lengkap')
st.write(df)

# Sidebar untuk memilih kolom yang akan ditampilkan
st.sidebar.subheader('Filter Data')
selected_columns = st.sidebar.multiselect(
    "Pilih Kolom untuk Ditampilkan",
    df.columns.tolist(),
    default=df.columns.tolist()
)

# Tampilkan dataset berdasarkan kolom yang dipilih
st.subheader('Dataset Berdasarkan Pilihan Kolom')
filtered_df = df[selected_columns]
st.write(filtered_df)

# Menampilkan info statistik deskriptif
st.subheader('Statistik Deskriptif')
Exam_Score_101 = (df['Exam_Score'] > 100).sum()
df.loc[df['Exam_Score'] == 101, 'Exam_Score'] = 100
st.write(df.describe().T)

# Mengisi missing values dengan mode
df['Teacher_Quality'].fillna(df['Teacher_Quality'].mode()[0], inplace=True)
df['Parental_Education_Level'].fillna(df['Parental_Education_Level'].mode()[0], inplace=True)
df['Distance_from_Home'].fillna(df['Distance_from_Home'].mode()[0], inplace=True)

# Informasi siswa dengan nilai tertinggi
st.subheader('Informasi Siswa dengan Exam Skor Tertinggi')
top_students = df[df['Exam_Score'] == 100]
if not top_students.empty:
    st.write(top_students)
else:
    st.write("Tidak ada siswa dengan nilai Exam Score 100.")

# Pilihan jenis visualisasi
st.sidebar.subheader('Pilih Jenis Visualisasi')
plot_type = st.sidebar.selectbox(
    "Pilih Jenis Visualisasi",
    ["Heatmap Korelasi", "Histogram", "Scatter Plot"]
)

# Visualisasi berdasarkan pilihan
if plot_type == "Heatmap Korelasi":
    st.subheader('Heatmap Korelasi Antar Fitur')
    numeric_df = df.select_dtypes(include=['int'])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
    st.pyplot(plt)

elif plot_type == "Histogram":
    st.sidebar.subheader('Pilih Kolom Histogram')
    hist_column = st.sidebar.selectbox("Pilih Kolom", df.select_dtypes(include=['int', 'float']).columns)
    st.subheader(f'Distribusi {hist_column}')
    plt.figure(figsize=(10, 5))
    df[hist_column].hist(bins=10)
    plt.title(f"Distribusi {hist_column}")
    plt.xlabel(hist_column)
    plt.ylabel("Frekuensi")
    st.pyplot(plt)

elif plot_type == "Scatter Plot":
    st.sidebar.subheader('Pilih Kolom Scatter Plot')
    x_axis = st.sidebar.selectbox("Pilih Kolom X", df.select_dtypes(include=['int', 'float']).columns)
    y_axis = st.sidebar.selectbox("Pilih Kolom Y", df.select_dtypes(include=['int', 'float']).columns)
    hue_column = st.sidebar.selectbox("Pilih Kolom Hue", df.columns, index=0)
    st.subheader(f'Hasil Scatter Plot: {x_axis} vs {y_axis}')
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_column, palette='viridis')
    plt.title(f"Scatter Plot {x_axis} vs {y_axis}")
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    st.pyplot(plt)

# Statistik Kustom
st.sidebar.subheader('Statistik Kustom')
stat_column = st.sidebar.selectbox("Pilih Kolom untuk Statistik", df.select_dtypes(include=['int', 'float']).columns)
if stat_column:
    st.subheader(f'Statistik Kustom untuk {stat_column}')
    st.write({
        "Rata-rata": df[stat_column].mean(),
        "Median": df[stat_column].median(),
        "Standar Deviasi": df[stat_column].std()
    })