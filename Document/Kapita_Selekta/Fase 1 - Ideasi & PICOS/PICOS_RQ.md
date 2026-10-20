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

Dalam konteks penelitian Ilmu Komputer (*Software Engineering & Intelligent Systems*), kerangka **PICOS** diadaptasi secara terstruktur sebagai berikut:

| Komponen PICOS | Formulasi Spesifik Sesuai Judul Tugas Akhir |
| :--- | :--- |
| **P**<br/>*(Platform & Population)* | <ul><li style="margin-bottom: 10px;"><strong>Platform Sistem:</strong><br/>Sistem otomatisasi dokumen berbasis web (<em>FastAPI</em>) dan mesin pemrosesan low-level <em>OpenXML</em> (<em>python-docx</em> / <em>lxml</em>).</li><li style="margin-bottom: 10px;"><strong>Populasi Data:</strong><br/>1.747 sampel paragraf dari 7 pilar struktur naskah akademik serta 5 dokumen uji emas (<em>Gold Datasets</em> P1–P5).</li><li><strong>Target Pengguna:</strong><br/>Mahasiswa dan sivitas akademika Universitas Esa Unggul (UEU).</li></ul> |
| **I**<br/>*(Intervention)* | <p><strong>Rancang bangun Multi-Agent System (MAS) yang mengintegrasikan 3 pilar utama:</strong></p><ol><li style="margin-bottom: 12px;"><strong>Deteksi Struktur Berbasis NLP:</strong><br/>Ekstraksi fitur teks <em>Natural Language Processing</em> menggunakan <em>TF-IDF N-Gram (1, 2)</em> (400 dimensi) yang dikombinasikan dengan 20 fitur metadata <em>OpenXML</em> menggunakan algoritma <em>Random Forest</em> (Agent 1: <em>Inspector</em>).</li><li style="margin-bottom: 12px;"><strong>Validasi Logika Struktur & Penjaminan Mutu:</strong><br/>Audit konsistensi urutan bab monotonik dan mekanisme <em>Two-Tier SQA</em> (Agent 2: <em>Quality Critic</em>) serta siklus pembelajaran mandiri <em>Continuous Active Learning</em>.</li><li><strong>Automated Formatting Engine:</strong><br/>Rekonstruksi tata letak dokumen tingkat rendah non-destruktif berbasis <em>OpenXML</em> murni tanpa ketergantungan MS Word GUI (Agent 3: <em>Formatting Actuator</em>).</li></ol> |
| **C**<br/>*(Comparison)* | <ol><li style="margin-bottom: 12px;"><strong>Komparasi Model Klasifikasi NLP:</strong><br/>Algoritma <em>Random Forest (Balanced)</em> dibandingkan dengan model baseline <em>Logistic Regression (Balanced)</em>.</li><li style="margin-bottom: 12px;"><strong>Komparasi Arsitektur Deteksi:</strong><br/>Pendekatan klasifikasi NLP tunggal (<em>Single-Agent / Pure ML</em>) dibandingkan dengan arsitektur kolaboratif <em>Multi-Agent System</em> yang dilengkapi <em>Quality Critic (5 Lapisan Guardrail)</em>.</li><li><strong>Komparasi Operasional:</strong><br/>Pemformatan manual oleh manusia menggunakan <em>Microsoft Word GUI</em> (durasi 2–4 jam/dokumen).</li></ol> |
| **O**<br/>*(Outcome)* | <ol><li style="margin-bottom: 12px;"><strong>Performa Deteksi Struktur (NLP & ML):</strong><br/><em>Accuracy</em> puncak mencapai <strong>97,22%</strong> (<em>Weighted F1-Score</em>: <strong>0,97</strong>; dengan evolusi terukur: baseline 90,70% &rarr; 93,71% &rarr; 94,84% &rarr; <strong>97,22%</strong> pada 7 Master Datasets &amp; fitur spasial OpenXML).</li><li style="margin-bottom: 12px;"><strong>Keberhasilan Otomatisasi Formatting:</strong><br/>Skor kepatuhan mutu artifak (<em>SQA Tier 2 Acceptance Score</em>) mencapai <strong>100% PASS</strong> terhadap 8 kriteria standar SK Rektor UEU No. 5 Tahun 2018 &amp; standar tabel APA 7.</li><li><strong>Kecepatan Eksekusi:</strong><br/>Rata-rata waktu pemrosesan dokumen utuh di bawah <strong>1,5 detik</strong> (aktual rata-rata: <strong>0,98 detik</strong>).</li></ol> |
| **S**<br/>*(Suspect / Domain)* | <p>Naskah dokumen akademik mentah berformat <code>.docx</code> (Skripsi, Proposal Tugas Akhir, dan Laporan Magang/MBKM) di Universitas Esa Unggul yang mengalami ketidakpatuhan struktur penomoran, hierarki <em>heading</em>, tipografi, dan tata letak halaman.</p> |

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
