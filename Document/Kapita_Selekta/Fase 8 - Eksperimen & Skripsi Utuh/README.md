# FASE 8: EKSPERIMEN, SKRIPSI UTUH & SIDANG AKHIR
## Verifikasi Empiris, Uji Similaritas Turnitin, dan Penyusunan Skripsi Lengkap (Bab I–V)

> **Mata Kuliah:** Skripsi / Tugas Akhir  
> **Program Studi:** Teknik Informatika, FASILKOM — Universitas Esa Unggul  
> **Status:** Siap Dieksekusi

---

## 1. Rangkuman Bukti Empiris & Metrik Eksperimen

Hasil eksperimen yang telah dicapai pada sistem ASDOKU:
* **Model Klasifikasi:** Random Forest Classifier (Class Weight: Balanced, Estimators: 100).
* **Dimensi Fitur:** 420 Fitur Hibrida (400 Fitur TF-IDF N-Gram 1,2 + 20 Fitur Metadata OpenXML).
* **Puncak Akurasi:** **97.22%** (*Weighted F1-Score*: **0.97**; evolusi bertahap dari baseline 90.70% $\rightarrow$ 93.71% $\rightarrow$ 94.84% $\rightarrow$ **97.22%**).
* **Komparasi Baseline:** Mengungguli Logistic Regression (*Accuracy*: 88.57%, *F1*: 0.88).
* **Evaluasi Mutu Dokumen:** Skor kepatuhan SQA Tier 2 mencapai **100.0% PASS** terhadap 8 kriteria SK Rektor UEU No. 5 Tahun 2018 pada seluruh 5 Dokumen Emas (*Gold Datasets* P1–P5).
* **Latency Eksekusi:** Waktu pemrosesan rata-rata **0.98 detik** per naskah lengkap (di bawah batas ambang SLA 1.5 detik).

---

## 2. Struktur Naskah Skripsi Lengkap (Bab I s/d Bab V)

* **Halaman Awal:** Judul Resmi, Lembar Pengesahan, Pernyataan Keaslian, Abstrak (Bahasa Indonesia & English), Kata Pengantar, Daftar Isi (otomatis terintegrasi), Daftar Tabel, Daftar Gambar.
* **Bab I: Pendahuluan**
* **Bab II: Tinjauan Pustaka** (Sintesis PRISMA SLR Scopus P01–P15).
* **Bab III: Metodologi Penelitian** (Tri-Agent Design, Two-Tier SQA, Active Learning, OpenXML Non-Destructive Engine).
* **Bab IV: Hasil dan Pembahasan**
  - Analisis Hasil Ekstraksi Fitur & Matriks Korelasi Fitur Spasial.
  - Analisis Confusion Matrix & Evaluasi Klasifikasi per Kategori Elemen.
  - Pengujian Lapisan Guardrail Agent 2 (Kasus Anomali Sub-bab 1.7 & Laporan Magang).
  - Evaluasi Kepatuhan Fisik Dokumen (Tier 2 SQA Audit).
  - Evaluasi Efisiensi Waktu Pemrosesan & Throughput Server FastAPI.
  - Implikasi Hasil terhadap Teori dan Praktik Penulisan Dokumen Akademik.
* **Bab V: Kesimpulan dan Saran**
  - Kesimpulan terhadap RQ 1.1, RQ 1.2, RQ 1.3.
  - Saran Pengembangan Lanjutan (Integrasi LLM reasoning lanjutan, dukungan format PDF/LaTeX).

---

## 3. Target Pra-Sidang

1. **Uji Plagiarisme / Similaritas Turnitin:** Target $\le 20\%$ (tanpa menyertakan bibliografi/daftar pustaka dan kutipan langsung).
2. **Uji Fungsional & Kerapian Dokumen:** Seluruh artifak `.docx` hasil olahan sistem wajib lulus uji cetak dan uji *Navigation Pane* di Microsoft Word versi desktop.
3. **Simulasi Sidang Akhir:** Penguasaan materi pembuktian algoritma dan demonstrasi live aplikasi.
