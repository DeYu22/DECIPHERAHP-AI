# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
from streamlit_lottie import st_lottie
import json
import requests
import time
import pandas as pd
from fpdf import FPDF
import base64
from datetime import datetime
import tempfile
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="💰 DECIPHERAHP AI - Sistem Pendukung Keputusan Pricing Cerdas Berbasis AHP & Artificial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk membuat PDF
def create_pdf(results, nama_produk, biaya_produksi, biaya_pemasaran, margin_wish, 
               harga_kompetitor, tingkat_persaingan, daya_beli, biaya_sewa, faktor_eksternal):
    
    pdf = FPDF()
    pdf.add_page()
    
    # =============================================
    # HEADER DENGAN KOP
    # =============================================
    def add_header():
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(70, 110, 200)  # Warna biru
        pdf.cell(0, 10, "DECIPHERAHP AI - LAPORAN ANALISIS PRICING", 0, 1, 'C')
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Jl M Yakub Lubis Gg Dame | Telp: 081264653043", 0, 1, 'C')
        pdf.cell(0, 5, "Email: dedeeyusuf16@gmail.com | Website: https://lynk.id/yusufmdn_", 0, 1, 'C')
        pdf.ln(5)
        pdf.set_line_width(0.5)
        pdf.set_draw_color(70, 110, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
    add_header()
    
    # =============================================
    # INFORMASI DASAR
    # =============================================
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. Informasi Dasar Produk", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Tabel informasi produk
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(60, 8, "Nama Produk", 1, 0, 'L', 1)
    pdf.cell(0, 8, nama_produk if nama_produk else "-", 1, 1)
    pdf.cell(60, 8, "Biaya Produksi", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {biaya_produksi:,.2f}", 1, 1)
    pdf.cell(60, 8, "Biaya Pemasaran", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {biaya_pemasaran:,.2f}", 1, 1)
    pdf.cell(60, 8, "Margin Keuntungan", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"{margin_wish*100:.0f}%", 1, 1)
    pdf.ln(10)
    
    # =============================================
    # DATA KOMPETITOR
    # =============================================
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "2. Data Kompetitor", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    for i, harga in enumerate(harga_kompetitor, 1):
        pdf.cell(40, 8, f"Harga Kompetitor {i}", 1, 0, 'L', 1)
        pdf.cell(0, 8, f"Rp {harga:,.2f}", 1, 1)
    
    pdf.cell(40, 8, "Rata-rata Harga", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['harga_rata_kompetitor']:,.2f}", 1, 1)
    pdf.cell(40, 8, "Harga Tertinggi", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['harga_tertinggi_kompetitor']:,.2f}", 1, 1)
    pdf.ln(15)
    
    # =============================================
    # VISUALISASI DATA
    # =============================================
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "3. Visualisasi Analisis", 0, 1)
    
    # Grafik 1: Perbandingan Harga
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    harga_labels = ['Harga Dasar', 'Rata-Rata', 'Rekomendasi', 'Tertinggi']
    harga_values = [results["harga_dasar"], results["harga_rata_kompetitor"], 
                   results["harga_final"], results["harga_tertinggi_kompetitor"]]
    colors = ['#667eea', '#9f7aea', '#38a169', '#e53e3e']
    ax1.bar(harga_labels, harga_values, color=colors)
    ax1.set_title("Perbandingan Harga")
    ax1.set_ylabel("Harga (Rp)")
    plt.tight_layout()
    
    # Simpan grafik ke temporary file
    img1_path = "temp_chart1.png"
    plt.savefig(img1_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Tambahkan ke PDF
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, "Grafik Perbandingan Harga", 0, 1)
    pdf.image(img1_path, x=10, w=190)
    pdf.ln(5)
    
    # Grafik 2: Posisi vs Kompetitor
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    competitor_labels = [f"Kompetitor {i+1}" for i in range(len(harga_kompetitor))] + ["Anda"]
    competitor_prices = harga_kompetitor + [results["harga_final"]]
    colors = ['#a0aec0']*len(harga_kompetitor) + ['#38a169']
    ax2.bar(competitor_labels, competitor_prices, color=colors)
    ax2.set_title("Posisi Harga vs Kompetitor")
    ax2.set_ylabel("Harga (Rp)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img2_path = "temp_chart2.png"
    plt.savefig(img2_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    pdf.cell(0, 8, "Grafik Posisi Harga vs Kompetitor", 0, 1)
    pdf.image(img2_path, x=10, w=190)
    pdf.ln(10)
    
    # Hapus file temporary
    os.remove(img1_path)
    os.remove(img2_path)
    
    # =============================================
    # HASIL ANALISIS
    # =============================================
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "4. Hasil Analisis", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    # Tabel hasil analisis
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(60, 8, "Harga Dasar", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['harga_dasar']:,.2f}", 1, 1)
    pdf.cell(60, 8, "Harga Rekomendasi", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['harga_final']:,.2f}", 1, 1)
    pdf.cell(60, 8, "Prediksi Tren Harga", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['harga_prediksi']:,.2f}", 1, 1)
    pdf.cell(60, 8, "Margin per Unit", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"Rp {results['margin_per_unit']:,.2f}", 1, 1)
    pdf.cell(60, 8, "Break-Even Volume", 1, 0, 'L', 1)
    pdf.cell(0, 8, f"{results['break_even_volume']:,.0f} unit/bulan", 1, 1)
    pdf.ln(15)
    
    # =============================================
    # REKOMENDASI STRATEGI
    # =============================================
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "5. Rekomendasi Strategi", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    if results["harga_final"] < results["harga_rata_kompetitor"] * 0.9:
        pdf.set_fill_color(230, 255, 230)  # Hijau muda
        pdf.cell(0, 8, "STRATEGI: HARGA AGRESIF", 1, 1, 'C', 1)
        pdf.multi_cell(0, 6, "\n".join([
            "Keunggulan harga Anda:",
            "- Potensi menarik lebih banyak pelanggan",
            "- Meningkatkan volume penjualan",
            "- Menguasai market share",
            "",
            "Pertimbangan:",
            "- Pastikan margin masih sehat",
            "- Monitor reaksi kompetitor"
        ]))
    elif results["harga_final"] > results["harga_rata_kompetitor"] * 1.2:
        pdf.set_fill_color(255, 250, 230)  # Kuning muda
        pdf.cell(0, 8, "STRATEGI: HARGA PREMIUM", 1, 1, 'C', 1)
        pdf.multi_cell(0, 6, "\n".join([
            "Fokus pada:",
            "- Meningkatkan persepsi nilai produk",
            "- Pengalaman pelanggan yang unik",
            "- Segmentasi pasar premium",
            "",
            "Pertimbangan:",
            "- Siapkan diferensiasi produk",
            "- Bangun brand image yang kuat"
        ]))
    else:
        pdf.set_fill_color(230, 240, 255)  # Biru muda
        pdf.cell(0, 8, "STRATEGI: HARGA KOMPETITIF", 1, 1, 'C', 1)
        pdf.multi_cell(0, 6, "\n".join([
            "Strategi yang bisa dilakukan:",
            "- Promosi 'Harga Terbaik di Kelasnya'",
            "- Program loyalitas pelanggan",
            "- Bundling produk",
            "",
            "Pertimbangan:",
            "- Monitor harga kompetitor",
            "- Pertahankan kualitas produk"
        ]))
    
    pdf.ln(10)
    
    # =============================================
    # FOOTER
    # =============================================
    def add_footer():
        pdf.set_y(-20)
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, f"Dicetak oleh Price DECIPHERAHP AI pada {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'L')
        pdf.cell(0, 5, f"Halaman {pdf.page_no()}", 0, 0, 'R')
    
    pdf.set_auto_page_break(auto=True, margin=15)
    add_footer()
    
    return pdf

def create_download_link(pdf, filename):
    try:
        # Menggunakan temporary file untuk memastikan format konsisten
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, 'rb') as f:
                pdf_bytes = f.read()
        
        # Encode ke base64
        b64 = base64.b64encode(pdf_bytes).decode('latin-1')
        
        # Hapus file temporary
        os.unlink(tmp.name)
        
        # Buat link download dengan styling
        href = f'''
        <div style="text-align:center; margin:20px 0;">
            <a href="data:application/pdf;base64,{b64}" 
               download="{filename}" 
               style="display: inline-block; 
                      padding: 12px 24px; 
                      background-color: #667eea; 
                      color: white; 
                      text-decoration: none; 
                      border-radius: 5px; 
                      font-weight: bold;
                      font-size: 16px;
                      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                      transition: all 0.3s ease;">
               📥 Unduh Laporan Lengkap
            </a>
        </div>
        '''
        return href
    except Exception as e:
        st.error(f"Gagal membuat file PDF: {str(e)}")
        return ""

# Animasi Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_sk5h1kfn.json")

# CSS Kustom
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(195deg, #42424a 0%, #191919 100%);
        color: white;
    }

    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        transition: transform 0.3s;
    }

    .metric-box:hover {
        transform: translateY(-5px);
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
    }

    .st-bb {
        background-color: transparent;
    }

    .st-bj {
        background-color: rgba(255,255,255,0.8);
    }

    .title-text {
        font-size: 2.5rem;
        background: -webkit-linear-gradient(#667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    .ahp-explanation {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #666;
    }
    
    .download-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 20px;
        text-align: center;
    }
    
    .download-btn:hover {
        background-color: #5a67d8;
        color: white;
    }
    
    .strategy-box {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header dengan Animasi
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<h1 class="title-text fade-in">💰 DECIPHERAHP AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-size:1.2rem;color:#666">Sistem Pendukung Keputusan Pricing Cerdas Berbasis AHP & Artificial Intelligence</p>', unsafe_allow_html=True)
with col2:
    st_lottie(lottie_animation, height=150, key="header-animation")

# Progress Bar Animasi
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(101):
    progress_bar.progress(i)
    status_text.text(f"Memuat sistem... {i}%")
    time.sleep(0.02)

status_text.empty()
progress_bar.empty()

# =============================================
# 1. INPUT DATA - SIDEBAR
# =============================================
with st.sidebar:
    st.markdown("## 📋 Data Produk")
    nama_produk = st.text_input("Nama Produk", placeholder="Masukkan nama produk", key="nama_produk")

    col1, col2 = st.columns(2)
    with col1:
        biaya_produksi = st.number_input("Biaya Produksi (Rp)", min_value=0, value=None, placeholder="Masukkan biaya produksi",
                                       help="Total biaya produksi per unit produk")
    with col2:
        biaya_pemasaran = st.number_input("Biaya Pemasaran (Rp)", min_value=0, value=None, placeholder="Masukkan biaya pemasaran",
                                        help="Biaya marketing dan distribusi per unit")

    margin_wish = st.slider("Margin Keuntungan (%)", 0, 100, 20, 
                           help="Persentase keuntungan yang diinginkan") / 100

    st.markdown("## 🏪 Data Kompetitor")
    jumlah_kompetitor = st.slider("Jumlah Kompetitor", 1, 10, 1, 
                                help="Banyaknya pesaing langsung di pasar")

    harga_kompetitor = []
    for i in range(jumlah_kompetitor):
        harga = st.number_input(f"Harga Kompetitor {i+1} (Rp)", min_value=0, value=None,
                              placeholder=f"Masukkan harga kompetitor {i+1}",
                              key=f"harga_{i}",
                              help=f"Harga jual kompetitor {i+1} di pasar")
        harga_kompetitor.append(harga)

    st.markdown("## 🌍 Faktor Lingkungan")
    
    with st.expander("📝 Penjelasan Parameter"):
        st.markdown("""
        ### Metode AHP (Analytic Hierarchy Process)
        AHP adalah metode pengambilan keputusan yang mengurai masalah kompleks menjadi hierarki dan mengevaluasi kriteria secara pairwise comparison.
        
        **Parameter yang digunakan:**
                    
        - **Jumlah Kompetitor (1-10):** Banyaknya pemain di pasar
          - 1-3: Monopoli/oligopoli
          - 4-6: Pasar kompetitif
          - 7-10: Pasar sangat padat
                    
        - **Tingkat Persaingan (1-10):** Semakin tinggi nilai, semakin ketat persaingan pasar
          - 1-3: Pasar niche dengan sedikit kompetitor
          - 4-6: Persaingan moderat
          - 7-10: Pasar sangat kompetitif dengan banyak pemain
        
        - **Daya Beli (1-10):** Kemampuan finansial target pasar
          - 1-3: Daya beli rendah (harga sensitif)
          - 4-6: Daya beli menengah
          - 7-10: Daya beli tinggi (premium market)
        
        - **Faktor Eksternal (1-10):** Pengaruh eksternal seperti regulasi, musim, dll
          - 1-3: Pengaruh minimal
          - 4-6: Pengaruh sedang
          - 7-10: Pengaruh signifikan (resiko tinggi)
        
        **Matriks Pairwise Comparison:**
        Kriteria dibandingkan berpasangan dengan skala 1-9 untuk menentukan bobot relatif.
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        tingkat_persaingan = st.slider("Tingkat Persaingan (1-10)", 1, 10, 5, 
                                     help="1: Monopoli, 10: Pasar sangat kompetitif") / 10
    with col2:
        daya_beli = st.slider("Daya Beli (1-10)", 1, 10, 4,
                            help="1: Daya beli rendah, 10: Daya beli tinggi") / 10

    biaya_sewa = st.number_input("Biaya Sewa/Bulan (Rp)", min_value=0, value=None, placeholder="Masukkan biaya sewa",
                               help="Biaya operasional tetap per bulan")
    faktor_eksternal = st.slider("Faktor Eksternal (1-10)", 1, 10, 4,
                               help="1: Pengaruh minimal, 10: Pengaruh sangat signifikan") / 10

# Hitung semua analisis
@st.cache_data
def calculate_results(biaya_produksi, biaya_pemasaran, margin_wish, harga_kompetitor,
                     tingkat_persaingan, daya_beli, biaya_sewa, faktor_eksternal):
    
    # Validasi input
    if None in [biaya_produksi, biaya_pemasaran, biaya_sewa] or None in harga_kompetitor:
        return None

    # Proses perhitungan
    harga_rata_kompetitor = np.mean(harga_kompetitor)
    harga_tertinggi_kompetitor = max(harga_kompetitor)

    criteria = ["Biaya Produksi", "Margin", "Permintaan", "Kompetitor", "Lokasi", "Eksternal"]
    pairwise_matrix = np.array([
        [1, 2, 1/3, 1/4, 1/5, 1/2],
        [1/2, 1, 1/4, 1/5, 1/6, 1/3],
        [3, 4, 1, 1/2, 1/3, 2],
        [4, 5, 2, 1, 1/2, 3],
        [5, 6, 3, 2, 1, 4],
        [2, 3, 1/2, 1/3, 1/4, 1]
    ])

    eigenvalues, eigenvectors = np.linalg.eig(pairwise_matrix)
    max_index = np.argmax(np.real(eigenvalues))
    weights = np.real(eigenvectors[:, max_index])
    weights = weights / np.sum(weights)

    # Hitung Consistency Ratio (CR)
    n = len(pairwise_matrix)
    lambda_max = np.max(np.real(eigenvalues))
    CI = (lambda_max - n) / (n - 1)
    RI = 1.24  # Random Index untuk n=6
    CR = CI / RI

    harga_dasar = (biaya_produksi + biaya_pemasaran) * (1 + margin_wish)

    faktor_lingkungan = (
        (weights[2] * daya_beli) +
        (weights[3] * (harga_rata_kompetitor/harga_dasar)) -
        (weights[4] * (biaya_sewa/5000000)) -
        (weights[5] * faktor_eksternal)
    )

    harga_final = min(harga_dasar * (1 + faktor_lingkungan), 1.3 * harga_tertinggi_kompetitor)
    harga_final = max(harga_final, biaya_produksi + biaya_pemasaran)

    margin_per_unit = harga_final - biaya_produksi - biaya_pemasaran
    break_even_volume = np.ceil(biaya_sewa / margin_per_unit) if margin_per_unit > 0 else float('inf')

    # Prediksi tren
    X = np.arange(len(harga_kompetitor)).reshape(-1, 1)
    y = np.array(harga_kompetitor)
    model = LinearRegression().fit(X, y)
    harga_prediksi = model.predict([[len(harga_kompetitor)]])[0]

    return {
        "harga_dasar": harga_dasar,
        "harga_final": harga_final,
        "harga_rata_kompetitor": harga_rata_kompetitor,
        "harga_tertinggi_kompetitor": harga_tertinggi_kompetitor,
        "harga_prediksi": harga_prediksi,
        "break_even_volume": break_even_volume,
        "margin_per_unit": margin_per_unit,
        "weights": weights,
        "criteria": criteria,
        "consistency_ratio": CR,
        "pairwise_matrix": pairwise_matrix
    }

# Validasi input sebelum menghitung
input_valid = all([
    biaya_produksi is not None,
    biaya_pemasaran is not None,
    biaya_sewa is not None,
    all(h is not None for h in harga_kompetitor)
])

if input_valid:
    results = calculate_results(biaya_produksi, biaya_pemasaran, margin_wish, harga_kompetitor,
                              tingkat_persaingan, daya_beli, biaya_sewa, faktor_eksternal)
else:
    results = None

# =============================================
# 2. TAMPILAN UTAMA
# =============================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Visualisasi", "💡 Rekomendasi"])

with tab1:
    display_name = nama_produk if nama_produk else "Produk Anda"
    st.markdown(f'<h2 style="color:#667eea">Analisis Harga {display_name}</h2>', unsafe_allow_html=True)

    if results is None:
        st.markdown("""
        <div class="empty-state">
            <h3>🛑 Data Belum Lengkap</h3>
            <p>Silakan lengkapi semua data input di sidebar untuk melihat analisis harga</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Metrics Row 1
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Harga Dasar</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">Rp {results["harga_dasar"]:,.2f}</p>'
                       '<p style="font-size:0.8rem;color:#666">Biaya produksi + pemasaran + margin</p>'
                       '</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Harga Kompetitor Rata-rata</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">Rp {results["harga_rata_kompetitor"]:,.2f}</p>'
                       '<p style="font-size:0.8rem;color:#666">Rata-rata harga {jumlah_kompetitor} kompetitor</p>'
                       '</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Harga Final Rekomendasi</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">Rp {results["harga_final"]:,.2f}</p>'
                       '<p style="font-size:0.8rem;color:#666">Dengan pertimbangan AHP</p>'
                       '</div>', unsafe_allow_html=True)

        # Metrics Row 2
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Break-Even Volume</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">{results["break_even_volume"]:,.0f} unit/bulan</p>'
                       '<p style="font-size:0.8rem;color:#666">Untuk menutup biaya sewa</p>'
                       '</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Margin per Unit</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">Rp {results["margin_per_unit"]:,.2f}</p>'
                       '<p style="font-size:0.8rem;color:#666">Keuntungan per produk</p>'
                       '</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-box">'
                       '<h3 style="color:#667eea">Prediksi Tren Harga</h3>'
                       f'<p style="font-size:24px;font-weight:bold;color:#333">Rp {results["harga_prediksi"]:,.2f}</p>'
                       '<p style="font-size:0.8rem;color:#666">Berdasarkan tren kompetitor</p>'
                       '</div>', unsafe_allow_html=True)

        # Strategi Rekomendasi
        if results["harga_final"] < results["harga_rata_kompetitor"] * 0.9:
            st.markdown('<div class="strategy-box" style="background-color: #e6ffed;">'
                       '<h3 style="color:#2d3748">🚀 Rekomendasi Strategi: Harga Agresif</h3>'
                       '<p><b>Keunggulan harga Anda:</b></p>'
                       '<ul>'
                       '<li>Potensi menarik lebih banyak pelanggan</li>'
                       '<li>Meningkatkan volume penjualan</li>'
                       '<li>Menguasai market share</li>'
                       '</ul>'
                       '<p><b>Pertimbangan:</b></p>'
                       '<ul>'
                       '<li>Pastikan margin masih sehat</li>'
                       '<li>Monitor reaksi kompetitor</li>'
                       '</ul>'
                       '</div>', unsafe_allow_html=True)
        elif results["harga_final"] > results["harga_rata_kompetitor"] * 1.2:
            st.markdown('<div class="strategy-box" style="background-color: #fffaf0;">'
                       '<h3 style="color:#2d3748">👑 Rekomendasi Strategi: Harga Premium</h3>'
                       '<p><b>Fokus pada:</b></p>'
                       '<ul>'
                       '<li>Meningkatkan persepsi nilai produk</li>'
                       '<li>Pengalaman pelanggan yang unik</li>'
                       '<li>Segmentasi pasar premium</li>'
                       '</ul>'
                       '<p><b>Pertimbangan:</b></p>'
                       '<ul>'
                       '<li>Siapkan diferensiasi produk</li>'
                       '<li>Bangun brand image yang kuat</li>'
                       '</ul>'
                       '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="strategy-box" style="background-color: #ebf8ff;">'
                       '<h3 style="color:#2d3748">⚖️ Rekomendasi Strategi: Harga Kompetitif</h3>'
                       '<p><b>Strategi yang bisa dilakukan:</b></p>'
                       '<ul>'
                       '<li>Promosi "Harga Terbaik di Kelasnya"</li>'
                       '<li>Program loyalitas pelanggan</li>'
                       '<li>Bundling produk</li>'
                       '</ul>'
                       '<p><b>Pertimbangan:</b></p>'
                       '<ul>'
                       '<li>Monitor harga kompetitor</li>'
                       '<li>Pertahankan kualitas produk</li>'
                       '</ul>'
                       '</div>', unsafe_allow_html=True)
        
        # Tombol Download PDF
        if st.button("📥 Generate PDF Report", key="generate_pdf"):
            if results:
                with st.spinner('Membuat laporan PDF...'):
                    try:
                        pdf = create_pdf(results, nama_produk, biaya_produksi, biaya_pemasaran, margin_wish,
                                      harga_kompetitor, tingkat_persaingan, daya_beli, biaya_sewa, faktor_eksternal)
                        
                        filename = f"Laporan_Analisis_Harga_{nama_produk.replace(' ','_') if nama_produk else 'Produk'}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                        
                        download_link = create_download_link(pdf, filename)
                        if download_link:
                            st.success("Laporan PDF berhasil dibuat!")
                            st.markdown(download_link, unsafe_allow_html=True)
                        else:
                            st.error("Gagal membuat link download")
                    except Exception as e:
                        st.error(f"Terjadi error saat membuat PDF: {str(e)}")
            else:
                st.error("Data belum lengkap untuk membuat laporan PDF")
                
with tab2:
    display_name = nama_produk if nama_produk else "Produk Anda"
    st.markdown(f'<h2 style="color:#667eea">Visualisasi Analisis {display_name}</h2>', unsafe_allow_html=True)

    if results is None:
        st.markdown("""
        <div class="empty-state">
            <h3>📊 Data Belum Tersedia</h3>
            <p>Lengkapi semua data input di sidebar untuk melihat visualisasi</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Buat visualisasi
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # Grafik 1: Bobot Kriteria
        ax1.bar(results["criteria"], results["weights"], color=['#667eea','#764ba2','#6b46c1','#805ad5','#9f7aea','#b794f4'])
        ax1.set_title("Bobot Kriteria AHP", fontsize=14, pad=20)
        ax1.set_xlabel("Kriteria", fontsize=12)
        ax1.set_ylabel("Bobot", fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Grafik 2: Perbandingan Harga
        harga_labels = ['Harga Dasar', 'Rata-Rata Kompetitor', 'Harga Final', 'Kompetitor Tertinggi']
        harga_values = [results["harga_dasar"], results["harga_rata_kompetitor"], results["harga_final"], results["harga_tertinggi_kompetitor"]]
        colors = ['#667eea', '#9f7aea', '#38a169', '#e53e3e']
        ax2.bar(harga_labels, harga_values, color=colors)
        ax2.set_title("Perbandingan Harga", fontsize=14, pad=20)
        ax2.set_ylabel("Harga (Rp)", fontsize=12)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        # Grafik 3: Sensitivitas Margin
        margins = np.linspace(max(0, margin_wish - 0.2), margin_wish + 0.2, 10)
        harga_finals = []
        for m in margins:
            h_dasar = (biaya_produksi + biaya_pemasaran) * (1 + m)
            faktor_lingkungan = (
                (results["weights"][2] * daya_beli) +
                (results["weights"][3] * (results["harga_rata_kompetitor"]/h_dasar)) -
                (results["weights"][4] * (biaya_sewa/5000000)) -
                (results["weights"][5] * faktor_eksternal)
            )
            h_final = min(h_dasar * (1 + faktor_lingkungan), 1.3 * results["harga_tertinggi_kompetitor"])
            harga_finals.append(h_final)

        ax3.plot(margins * 100, harga_finals, marker='o', color='#805ad5', linewidth=2, markersize=8)
        ax3.axhline(results["harga_rata_kompetitor"], color='#e53e3e', linestyle='--', label='Harga Rata Kompetitor')
        ax3.set_title("Sensitivitas Harga terhadap Margin", fontsize=14, pad=20)
        ax3.set_xlabel("Margin Keuntungan (%)", fontsize=12)
        ax3.set_ylabel("Harga Final (Rp)", fontsize=12)
        ax3.legend()
        ax3.grid(linestyle='--', alpha=0.7)

        # Grafik 4: Posisi Harga vs Kompetitor
        competitor_labels = [f"Kompetitor {i+1}" for i in range(jumlah_kompetitor)] + ["Anda"]
        competitor_prices = harga_kompetitor + [results["harga_final"]]
        colors = ['#a0aec0']*jumlah_kompetitor + ['#38a169']
        ax4.bar(competitor_labels, competitor_prices, color=colors)
        ax4.set_title("Posisi Harga vs Kompetitor", fontsize=14, pad=20)
        ax4.set_ylabel("Harga (Rp)", fontsize=12)
        ax4.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        st.pyplot(fig)
        
        # Tambahkan penjelasan AHP
        st.markdown("""
        <div class="ahp-explanation">
        <h3>Detail Metode Analytic Hierarchy Process (AHP)</h3>
        
        <h4>Matriks Perbandingan Berpasangan</h4>
        <p>Berikut matriks perbandingan kriteria yang digunakan dalam perhitungan:</p>
        """, unsafe_allow_html=True)
        
        # Tampilkan matriks pairwise comparison
        st.table(pd.DataFrame(
            results["pairwise_matrix"],
            columns=results["criteria"],
            index=results["criteria"]
        ).style.format("{:.2f}"))
        
        st.markdown(f"""
        <h4>Konsistensi Rasio (CR): {results['consistency_ratio']:.3f}</h4>
        <p>Nilai CR < 0.1 menunjukkan perbandingan yang konsisten. CR saat ini {'memenuhi' if results['consistency_ratio'] < 0.1 else 'tidak memenuhi'} syarat konsistensi.</p>
        
        <h4>Interpretasi Skala Perbandingan</h4>
        <ul>
            <li><b>1</b>: Kedua kriteria sama pentingnya</li>
            <li><b>3</b>: Kriteria sedikit lebih penting</li>
            <li><b>5</b>: Kriteria lebih penting</li>
            <li><b>7</b>: Kriteria sangat penting</li>
            <li><b>9</b>: Kriteria mutlak lebih penting</li>
            <li><b>Nilai kebalikan</b>: Untuk kepentingan sebaliknya</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    display_name = nama_produk if nama_produk else "Produk Anda"
    st.markdown(f'<h2 style="color:#667eea">Rekomendasi Bisnis untuk {display_name}</h2>', unsafe_allow_html=True)

    if results is None:
        st.markdown("""
        <div class="empty-state">
            <h3>💡 Rekomendasi Belum Tersedia</h3>
            <p>Silakan lengkapi semua data input di sidebar untuk mendapatkan rekomendasi</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Strategi Pemasaran")
            if daya_beli > 0.5:
                st.markdown("""
                <div class="strategy-box" style="background-color: #e6ffed;">
                <h4>Targetkan Digital Marketing</h4>
                <ul>
                <li><b>Iklan Instagram/Facebook</b>: Fokus pada konten visual menarik</li>
                <li><b>Kolaborasi dengan micro-influencer</b>: Pilih influencer yang sesuai niche</li>
                <li><b>Konten edukasi produk</b>: Tekankan manfaat dan diferensiasi produk</li>
                <li><b>Retargeting ads</b>: Targetkan pengunjung yang belum konversi</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="strategy-box" style="background-color: #fffaf0;">
                <h4>Fokus pada Offline Marketing</h4>
                <ul>
                <li><b>Spanduk di lokasi strategis</b>: Area dengan lalu lintas tinggi</li>
                <li><b>Promosi mulut ke mulut</b>: Berikan insentif referral</li>
                <li><b>Kerjasama dengan warung/toko</b>: Program konsinyasi atau diskon</li>
                <li><b>Event lokal</b>: Partisipasi dalam bazar atau pameran</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 💰 Manajemen Harga")
            if tingkat_persaingan > 0.7:
                st.markdown("""
                <div class="strategy-box" style="background-color: #fff5f5;">
                <h4>Persaingan Tinggi!</h4>
                <ul>
                <li><b>Paket diskon</b>: Bundling atau volume discount</li>
                <li><b>Program loyalitas</b>: Poin atau membership</li>
                <li><b>Bundling produk</b>: Gabungkan dengan produk komplementer</li>
                <li><b>Harga dinamis</b>: Sesuai waktu atau musim</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="strategy-box" style="background-color: #e6ffed;">
                <h4>Pasar Masih Terbuka</h4>
                <ul>
                <li><b>Kualitas produk</b>: Pertahankan standar tinggi</li>
                <li><b>Reputasi merek</b>: Bangun testimoni positif</li>
                <li><b>Pelayanan</b>: Respons cepat dan ramah</li>
                <li><b>Diferensiasi</b>: Cari unique selling point</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 📦 Strategi Produk")
            if results["harga_final"] > results["harga_rata_kompetitor"]:
                st.markdown("""
                <div class="strategy-box" style="background-color: #fffaf0;">
                <h4>Produk Premium</h4>
                <ul>
                <li><b>Kemasan premium</b>: Desain mewah dan berkualitas</li>
                <li><b>Sertifikasi</b>: Tambahkan sertifikat kualitas</li>
                <li><b>Garansi</b>: Berikan jaminan kepuasan</li>
                <li><b>Eksklusivitas</b>: Batas edisi atau limited stock</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="strategy-box" style="background-color: #ebf8ff;">
                <h4>Produk Value-for-Money</h4>
                <ul>
                <li><b>Efisiensi produksi</b>: Optimalkan biaya</li>
                <li><b>Kuantitas</b>: Skala ekonomi untuk harga lebih baik</li>
                <li><b>Minimalisir biaya</b>: Tanpa mengurangi kualitas</li>
                <li><b>Standarisasi</b>: Konsistensi produk</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("### 📊 Analisis Break-Even")
            st.markdown(f"""
            <div class="strategy-box" style="background-color: #f0f9ff;">
            <h4>Target Penjualan</h4>
            <p><b>{results["break_even_volume"]:,.0f} unit/bulan</b> ({np.ceil(results["break_even_volume"]/30):.0f} unit/hari)</p>
            
            <h4>Margin per unit</h4>
            <p>Rp {results["margin_per_unit"]:,.2f}</p>
            
            <h4>Strategi pencapaian:</h4>
            <ul>
            <li>Fokus pada channel penjualan terbaik</li>
            <li>Optimalkan konversi penjualan</li>
            <li>Tingkatkan average order value</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

            if results["break_even_volume"] > 1000:
                st.markdown("""
                <div class="strategy-box" style="background-color: #fff5f5;">
                <h4>Target break-even terlalu tinggi!</h4>
                <p>Pertimbangkan:</p>
                <ul>
                <li><b>Menaikkan harga</b>: Dengan nilai tambah</li>
                <li><b>Menurunkan biaya</b>: Efisiensi operasional</li>
                <li><b>Pasar baru</b>: Ekspansi wilayah atau segmen</li>
                <li><b>Diversifikasi</b>: Tambah lini produk</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#666;font-size:0.9rem">
    © 2025 DECIPHERAHP AI - Dibangun dengan Streamlit | <a href="#" style="color:#667eea">Bantuan</a> | <a href="#" style="color:#667eea">Kebijakan Privasi</a>
</div>
""", unsafe_allow_html=True)