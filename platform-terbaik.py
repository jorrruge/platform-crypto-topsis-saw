import streamlit as st
import pandas as pd

# Load the CSV files
file_ahp = "AHP Crypto.csv"
file_topsis = "TOPSIS Crypto.csv"
file_saw = "SAW Crypto.csv"
file_average = "AVERAGE Crypto.csv"

# Function to load CSV file
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error membaca file {file_path}: {e}")
        return pd.DataFrame()

# Streamlit App
st.title("Dashboard Penilaian Platform Cryptocurrency")

# Load Data
bobot_df = load_csv(file_ahp)
topsis_df = load_csv(file_topsis)
saw_df = load_csv(file_saw)
average_df = load_csv(file_average)

# AHP dan Average
st.header("1. Penilaian Berdasarkan AHP dan Average")
if not bobot_df.empty and not average_df.empty:
    st.write("### Data Bobot AHP")
    st.dataframe(bobot_df)

    st.write("### Data Average")
    st.dataframe(average_df)

    # Dropdown untuk memilih kriteria
    selected_kriteria = st.selectbox("Pilih Kriteria untuk Penilaian:", average_df.columns[1:])

    if selected_kriteria:
        # Mengambil bobot dari file AHP
        if selected_kriteria in bobot_df[bobot_df.columns[0]].values:
            bobot_kriteria = bobot_df.loc[bobot_df[bobot_df.columns[0]] == selected_kriteria, bobot_df.columns[1]].values[0]
        else:
            bobot_kriteria = 1  # Default jika tidak ada bobot yang ditemukan

        # Menghitung nilai akhir dengan pembobotan
        average_df["Nilai Akhir"] = average_df[selected_kriteria] * bobot_kriteria
        sorted_average_df = average_df.sort_values(by="Nilai Akhir", ascending=False)

        st.write(f"### Peringkat Alternatif Berdasarkan: {selected_kriteria}")
        st.dataframe(sorted_average_df[[average_df.columns[0], "Nilai Akhir"]])

# TOPSIS
st.header("2. Penilaian Berdasarkan TOPSIS")
if not topsis_df.empty:
    st.write("### Data TOPSIS")
    st.dataframe(topsis_df)

    # Alternatif nilai tertinggi
    best_topsis = topsis_df.iloc[topsis_df.iloc[:, 1].idxmax()]
    st.write("### Alternatif Terbaik Berdasarkan TOPSIS:")
    st.write(best_topsis)

# SAW
st.header("3. Penilaian Berdasarkan SAW")
if not saw_df.empty:
    st.write("### Data SAW")
    st.dataframe(saw_df)

    # Alternatif nilai tertinggi
    best_saw = saw_df.iloc[saw_df.iloc[:, 1].idxmax()]
    st.write("### Alternatif Terbaik Berdasarkan SAW:")
    st.write(best_saw)
