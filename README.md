# DECIPHERAHP AI - Sistem Pendukung Keputusan Pricing Cerdas

**DECIPHERAHP AI** adalah aplikasi berbasis web yang membantu pengusaha dan pebisnis menentukan harga produk optimal dengan memadukan metode Analytic Hierarchy Process (AHP) dan kecerdasan buatan (AI). Aplikasi ini memberikan rekomendasi harga yang kompetitif dengan mempertimbangkan berbagai faktor internal dan eksternal.

## Fitur Utama

✅ **Perhitungan Harga Komprehensif**:
- Mempertimbangkan biaya produksi, pemasaran, dan margin keuntungan
- Analisis harga kompetitor (rata-rata, tertinggi, terendah)
- Prediksi tren harga menggunakan regresi linear

📊 **Metode AHP (Analytic Hierarchy Process)**:
- Pembobotan kriteria secara pairwise comparison
- Perhitungan konsistensi rasio
- Integrasi faktor lingkungan (daya beli, persaingan, dll)

📈 **Visualisasi Data Interaktif**:
- Grafik perbandingan harga
- Posisi harga vs kompetitor
- Sensitivitas margin keuntungan
- Analisis break-even point

📄 **Laporan Otomatis**:
- Generate PDF report profesional
- Rekomendasi strategi pricing
- Analisis kompetitif

## Teknologi yang Digunakan

- **Python** (numpy, pandas, scikit-learn)
- **Streamlit** (framework web app)
- **Matplotlib** (visualisasi data)
- **FPDF** (generasi PDF)
- **Lottie** (animasi interaktif)

## Cara Menggunakan

1. Isi data produk di sidebar (biaya produksi, pemasaran, margin)
2. Masukkan data kompetitor (harga pesaing)
3. Atur parameter lingkungan (daya beli, persaingan, dll)
4. Lihat hasil analisis di dashboard utama
5. Download laporan PDF untuk dokumentasi

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```
   streamlit run streamlit_app.py
   ```

## Kontribusi

Kontribusi terbuka untuk:
- Penyempurnaan algoritma AHP
- Penambahan fitur analisis baru
- Perbaikan antarmuka pengguna

Dikembangkan oleh [DeYu22] |
