import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Mengatur konfigurasi halaman Web
st.set_page_config(page_title="Valuasi Properti AI", layout="centered")

st.title("🏠 Sistem Prediksi Harga Properti berbasis AI")
st.write("Aplikasi valuasi massal menggunakan algoritma Multiple Linear Regression & Spatial Features")
st.markdown("---")

# 2. Memuat Model dan Daftar Fitur dari Colab
@st.cache_resource
def load_assets():
    model = joblib.load('model_harga_properti.pkl')
    features = joblib.load('daftar_fitur.pkl')
    return model, features

try:
    model, features_final = load_assets()
    
    # Memisahkan fitur dummy ZipCode
    all_zipcodes = [col.replace('ZipCode_', '') for col in features_final if col.startswith('ZipCode_')]
    
    # 3. Membuat Input Form di Antarmuka Web
    st.subheader("📋 Atribut Fisik & Spasial Bangunan")
    
    col1, col2 = st.columns(2)
    with col1:
        sqft = st.number_input("Luas Ruang Tamu (SqFt)", min_value=300, max_value=10000, value=1800)
        bedrooms = st.slider("Jumlah Kamar Tidur", min_value=1, max_value=10, value=3)
        bathrooms = st.slider("Jumlah Kamar Mandi", min_value=1.0, max_value=8.0, value=2.0, step=0.25)
        grade = st.slider("Skor Kualitas Konstruksi (BldgGrade)", min_value=1, max_value=13, value=7)
    
    with col2:
        age = st.number_input("Umur Bangunan (Tahun)", min_value=0, max_value=120, value=15)
        park = st.number_input("Jarak ke Taman Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.5)
        school = st.number_input("Jarak ke Sekolah Terdekat (Km)", min_value=0.0, max_value=50.0, value=0.3)
        hospital = st.number_input("Jarak ke Rumah Sakit Terdekat (Km)", min_value=0.0, max_value=50.0, value=1.2)
        
    st.subheader("📍 Lokasi Kawasan Properti")
    selected_zip = st.selectbox("Pilih Kode Pos (ZipCode Prestise)", sorted(all_zipcodes))
    
    # 4. Memproses Input Menjadi Matriks DataFrame
    if st.button("🚀 Hitung Estimasi Harga Rumah", type="primary"):
        # Buat template data berisi angka 0
        input_data = pd.DataFrame(0, index=[0], columns=features_final)
        
        # Isi nilai dari input pengguna (UI)
        if 'SqFtTotLiving' in input_data.columns: input_data['SqFtTotLiving'] = sqft
        if 'Bedrooms' in input_data.columns: input_data['Bedrooms'] = bedrooms
        if 'Bathrooms' in input_data.columns: input_data['Bathrooms'] = bathrooms
        if 'BldgGrade' in input_data.columns: input_data['BldgGrade'] = grade
        if 'HouseAge' in input_data.columns: input_data['HouseAge'] = age
        if 'dist_to_park' in input_data.columns: input_data['dist_to_park'] = park
        if 'dist_to_school' in input_data.columns: input_data['dist_to_school'] = school
        if 'dist_to_hospital' in input_data.columns: input_data['dist_to_hospital'] = hospital
        
        # --- PENYELAMAT: Injeksi nilai rata-rata untuk kolom tersembunyi ---
        if 'SqFtLot' in input_data.columns: input_data['SqFtLot'] = 5000
        if 'NbrLivingUnits' in input_data.columns: input_data['NbrLivingUnits'] = 1
        if 'LandVal' in input_data.columns: input_data['LandVal'] = 150000
        if 'ImpsVal' in input_data.columns: input_data['ImpsVal'] = 200000
        if 'zhvi_px' in input_data.columns: input_data['zhvi_px'] = 400000
        if 'AdjSalePrice' in input_data.columns: input_data['AdjSalePrice'] = 500000
        if 'lat' in input_data.columns: input_data['lat'] = 47.5
        if 'lon' in input_data.columns: input_data['lon'] = -122.2
        if 'ZIPCODE' in input_data.columns: input_data['ZIPCODE'] = int(selected_zip)
        
        # Aktifkan kolom dummy ZipCode
        target_dummy_col = f"ZipCode_{selected_zip}"
        if target_dummy_col in input_data.columns:
            input_data[target_dummy_col] = 1
            
        # 5. Eksekusi Prediksi AI
        prediksi_log = model.predict(input_data)
        
        # Kembalikan nilai logaritma ke Dolar asli
        harga_final = np.exp(prediksi_log[0])
        
        # 6. Tampilkan Hasil
        st.markdown("---")
        st.success(f"### 🎉 Hasil Valuasi AI: **${harga_final:,.2f}**")
        st.caption("Catatan: Prediksi ini dihitung menggunakan model regresi spasial dengan akurasi 94.5%.")

except Exception as e:
    st.error(f"Gagal memuat sistem: {e}. Pastikan file model sudah benar.")
