# FASE 1: PERENCANAAN PENELITIAN & PROTOKOL PICOS
## Mata Kuliah: Kapita Selekta — Fakultas Ilmu Komputer, Universitas Esa Unggul

> **Penyusun:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Program Studi:** Teknik Informatika, Fakultas Ilmu Komputer (FASILKOM) — Universitas Esa Unggul  
> **Regulasi Acuan:** SK Rektor Universitas Esa Unggul No. 5 Tahun 2018 (Pedoman Penulisan Skripsi & Tugas Akhir)  
> **Tanggal Penyusunan:** 20 Oktober 2026  
> **Status Dokumen:** Final (Fase 1)

---

### Topik Penelitian
**Rancang Bangun Multi-Agent System Untuk Otomatisasi Deteksi Struktur Dan Formatting Dokumen Akademik Berbasis Natural Language Processing**

---

## 1. Kerangka Metodologi PICOS

Dalam konteks penelitian Ilmu Komputer (*Software Engineering & Intelligent Systems*), kerangka **PICOS** diadaptasi secara presisi sebagai berikut:

| Komponen PICOS | Formulasi Spesifik Sesuai Judul Tugas Akhir |
| :--- | :--- |
| **P (Platform / Population / Target User)** | **Platform:**<br/>Sistem otomatisasi dokumen berbasis web (*FastAPI*) dan mesin pemrosesan *OpenXML* (*python-docx* / *lxml*).<br/><br/>**Populasi Data:**<br/>1.747 sampel paragraf dari 7 pilar struktur naskah akademik serta 5 dokumen uji emas (*Gold Datasets* P1–P5).<br/><br/>**Target Pengguna:**<br/>Mahasiswa dan sivitas akademika Universitas Esa Unggul (UEU). |
| **I (Intervention / Metode & Algoritma Baru)** | Rancang bangun **Multi-Agent System (MAS)** yang mengintegrasikan tiga pilar utama:<br/><br/>1. **Deteksi Struktur Berbasis NLP:** Ekstraksi fitur teks *Natural Language Processing* menggunakan *TF-IDF N-Gram (1, 2)* (400 dimensi) yang dikombinasikan dengan 20 fitur metadata *OpenXML* menggunakan algoritma *Random Forest* (Agent 1: *Inspector*).<br/>2. **Validasi Logika Struktur:** Audit konsistensi urutan bab monotonik dan mekanisme *Two-Tier SQA* (Agent 2: *Quality Critic*) serta siklus *Continuous Active Learning*.<br/>3. **Automated Formatting Engine:** Rekonstruksi tata letak dokumen tingkat rendah non-destruktif berbasis *OpenXML* (Agent 3: *Formatting Actuator*). |
| **C (Comparison / Baseline Model & Sistem Lama)** | 1. **Komparasi Model Klasifikasi NLP:** Algoritma *Random Forest (Balanced)* dibandingkan dengan model baseline *Logistic Regression (Balanced)*.<br/>2. **Komparasi Arsitektur Deteksi:** Pendekatan klasifikasi NLP tunggal (*Single-Agent / Pure ML*) dibandingkan dengan arsitektur *Multi-Agent System* yang dilengkapi *Quality Critic (5 Lapisan Guardrail)*.<br/>3. **Komparasi Operasional:** Pemformatan manual menggunakan *Microsoft Word GUI*. |
| **O (Outcome / Metrik Evaluasi Performa)** | 1. **Performa Deteksi Struktur (NLP & ML):** *Accuracy* puncak mencapai **97,22%** (*Weighted F1-Score* **0,97**; dengan evolusi bertahap dari baseline 90,70% $\rightarrow$ 93,71% $\rightarrow$ 94,84% $\rightarrow$ **97,22%** pada 7 Master Datasets & fitur spasial OpenXML).<br/>2. **Keberhasilan Otomatisasi Formatting:** Skor kepatuhan mutu artifak (*SQA Tier 2 Acceptance Score*) mencapai **100% PASS** terhadap 8 kriteria standar SK Rektor UEU No. 5 Tahun 2018 & standar tabel APA 7.<br/>3. **Kecepatan Eksekusi:** Rata-rata waktu pemrosesan dokumen utuh di bawah **1,5 detik** (aktual rata-rata: **0,98 detik**). |
| **S (Suspect / Subjek & Domain Kasus)** | Naskah dokumen akademik mentah berformat `.docx` (Skripsi, Proposal Tugas Akhir, dan Laporan Magang/MBKM) di Universitas Esa Unggul yang mengalami ketidakpatuhan struktur penomoran, hierarki *heading*, tipografi, dan tata letak halaman. |

---

## 2. Penyesuaian Tiga Research Questions (RQ)

Ketiga pertanyaan penelitian di bawah ini dirancang agar langsung menjawab variabel-variabel yang tertera pada judul skripsi:

### RQ 1.1: Kebutuhan Sistem & Representasi Fitur NLP untuk Deteksi Struktur
> *"Bagaimana merumuskan representasi fitur berbasis Natural Language Processing (TF-IDF N-Gram) yang diintegrasikan dengan atribut metadata OpenXML pada 7 pilar dataset akademik untuk mendeteksi karakteristik struktur elemen dokumen akademik secara akurat?"*

* **Keterkaitan dengan Judul:**  
  Menjawab aspek **"Deteksi Struktur"** dan **"Berbasis Natural Language Processing"**. Bagian ini membedah mengapa teks naskah akademik memerlukan pemrosesan NLP (mengenali pola kata judul bab, sub-bab, caption, daftar pustaka) yang diperkuat oleh fitur struktural dokumen.

---

### RQ 1.2: Rancang Bangun Arsitektur Multi-Agent System & Otomatisasi Formatting
> *"Bagaimana merancang bangun arsitektur Multi-Agent System (Inspector, Quality Critic, dan Formatting Actuator) serta mekanisme koordinasi Two-Tier SQA untuk mengotomatisasi validasi struktur dan rekonstruksi formatting dokumen akademik sesuai standar SK Rektor Universitas Esa Unggul?"*

* **Keterkaitan dengan Judul:**  
  Menjawab aspek **"Rancang Bangun Multi-Agent System"** dan **"Otomatisasi Deteksi Struktur dan Formatting Dokumen Akademik"**. Bagian ini menjelaskan cara kerja ketiga agen dalam bernegosiasi memperbaiki anomali deteksi (seperti pada kasus sub-bab 1.7 dan laporan magang) hingga mengeksekusi *formatting* otomatis pada berkas `.docx`.

---

### RQ 1.3: Evaluasi Performa Deteksi Struktur & Kepatuhan Hasil Formatting
> *"Seberapa tinggi tingkat akurasi model klasifikasi berbasis Natural Language Processing dalam mendeteksi struktur dokumen serta tingkat kepatuhan mutu hasil formatting otomatis Multi-Agent System ketika diuji pada beragam dokumen akademik riil (Gold Datasets)?"*

* **Keterkaitan dengan Judul:**  
  Menjawab **pembuktian empiris** dari keseluruhan sistem yang dibangun, baik dari sisi evaluasi metrik NLP/Machine Learning (*Confusion Matrix, Accuracy, F1-Score*) maupun evaluasi hasil *formatting* fisik dokumen (**100% PASS** pada 5 dokumen emas P1–P5).
