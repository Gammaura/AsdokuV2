# ANALISIS CELAH PENELITIAN (RESEARCH GAP) & REKOMENDASI JUDUL TUGAS AKHIR
## Sintesis Silang Business Requirements Document (BRD) $\times$ Systematic Literature Review (SLR) — Sistem ASDOKU

> **Kode Dokumen:** `GAP-ASDOKU-2026-F5`  
> **Mata Kuliah:** Kapita Selekta  
> **Program Studi / Institusi:** Teknik Informatika, Fakultas Ilmu Komputer (FASILKOM) — Universitas Esa Unggul  
> **Penyusun:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Dosen Pengampu / Pembimbing:** Dosen Kapita Selekta FASILKOM UEU  
> **Regulasi Acuan:** SK Rektor Universitas Esa Unggul No. 5 Tahun 2018 (Pedoman Penulisan Skripsi & Tugas Akhir)  
> **Basis Data Literatur:** 126 Studi Terindeks Scopus (2021–2026) $\rightarrow$ 15 Studi Primer (S01–S15)  
> **Basis Kebutuhan Sistem:** 16 Functional Requirements (FR-01 s/d FR-16), 4 Business Objectives (BO-01 s/d BO-04), & 5 Risk Register (RSK-01 s/d RSK-05)  
> **Dokumen Rujukan Terkait:** [BRD_Business_Requirements_Document.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%203%20-%20Dokumen%20BRD/BRD_Business_Requirements_Document.md), [SLR_Systematic_Literature_Review.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%204%20-%20Dokumen%20SLR/SLR_Systematic_Literature_Review.md), [Evidence_Matrix_Scopus.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%202%20-%20Penelusuran%20Literatur%20&%20Evidence%20Matrix/Evidence_Matrix_Scopus.md), dan [PICOS_RQ.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%201%20-%20Ideasi%20&%20PICOS/PICOS_RQ.md)  
> **Tanggal Analisis:** 21 Oktober 2026  
> **Status Dokumen:** Final (Fase 5 — Analisis Gap & Penetapan Judul: Telah Disinkronisasi Penuh: 420 Dimensi Fitur Hibrida & Akurasi Puncak 97,22%)

---

## PEMISAHAN STRUKTUR ANALISIS (ATURAN KETAT)

Untuk menjamin objektivitas ilmiah sesuai protokol Scopus, seluruh analisis di bawah ini memisahkan secara tegas tiga komponen berikut:

* **(A) Fakta dari BRD/SLR:** Data empiris, parameter teknis, metrik aktual (420 dimensi fitur, 1.747 sampel paragraf, akurasi puncak 97,22%, baseline 93,71%, kepatuhan 100% PASS, waktu eksekusi 0,65–1,45 detik / rata-rata 0,98 detik), serta temuan literatur terverifikasi S01–S15.
* **(B) Interpretasi Pola:** Analisis kritis terhadap mengapa solusi yang ada di literatur Scopus (S01–S15) belum mampu menyelesaikan kebutuhan spesifik pada BRD secara langsung.
* **(C) Usulan Novelty:** Kontribusi arsitektural, algoritmik, dan rekayasa perangkat lunak baru yang dihadirkan oleh sistem **ASDOKU**.

---

## TAHAP 1 — Matriks Silang Functional Requirements (BRD) $\times$ Studi Primer (SLR)

Tabel di bawah ini memetakan seluruh **16 Functional Requirements (FR-01 s/d FR-16)** dari dokumen BRD terhadap solusi eksisting pada **15 Studi Primer Scopus (S01–S15)** beserta referensi pendukung di dalam laporan Scopus AI:

| Kode FR | Deskripsi Kebutuhan Fungsional (Fakta BRD) | Solusi Eksisting pada Literatur SLR (Fakta SLR S01–S15) | Status Pemenuhan | Analisis Kesenjangan: (A) Fakta, (B) Interpretasi, (C) Novelty |
| :---: | :--- | :--- | :---: | :--- |
| **FR-01** | **Web Interface (`app.py`):** Fitur *drag-and-drop* / pemilihan berkas untuk mengunggah dokumen mentah `.docx`. | **S04 (Kumara et al., 2026)** membahas arsitektur perangkat lunak MAS modern; **S14 (Liu et al., 2026)** menyediakan antarmuka observasi interaksi agen. | **SEBAGIAN** | **(A)** Literatur membahas antarmuka sistem agen secara umum.<br/>**(B)** Belum spesifik menangani *stream* biner dokumen `.docx` lokal.<br/>**(C)** Studio Web FastAPI khusus unggah naskah akademik `.docx`. |
| **FR-02** | **Agent 1 (Inspector):** Membaca `.docx` secara non-destruktif & mengekstraksi **420 dimensi fitur hibrida** (400 *TF-IDF N-Gram* + 20 *Metadata OpenXML*). | **S06 (Roldan-Baluis et al., 2022)** mengkaji ekstraksi fitur NLP teks tak terstruktur; **S07 (Saier et al., 2023)** memproses teks penuh arXiv (LaTeX); **S12 (Latha & Reddy, 2026)** mengusulkan arsitektur *metadata-driven*. | **BELUM ADA** | **(A)** S06, S07, dan S12 memproses fitur teks dan metadata secara terpisah atau pada domain non-OpenXML.<br/>**(B)** Belum ada studi yang menggabungkan *TF-IDF N-Gram* dengan atribut spasial DOM *OpenXML* (`is_below_drawing`, `is_above_table`, `doc_pos`).<br/>**(C)** Ekstraksi **420 Fitur Hibrida (NLP + Low-Level OpenXML)** pada **7 Pilar Dataset Akademik UEU** (1.747 sampel). |
| **FR-03** | **Agent 1 (Inspector):** Mengklasifikasikan paragraf ke label struktur dokumen dengan model ML (*Random Forest* vs *Logistic Regression*) & menghasilkan *Draft Blueprint* + *confidence score*. | **S05 (Ali et al., 2024)** membandingkan algoritma ML tradisional untuk aplikasi NLP pada lingkungan terbatas sumber daya; **S09 (Blagec et al., 2022)** merumuskan metrik evaluasi klasifikasi NLP. | **TERPENUHI** | **(A)** S05 dan S09 telah menyediakan metodologi komparasi ML klasik dan metrik *Accuracy* / *F1-Score*.<br/>**(B)** Paradigma komparasi algoritma ML klasik sudah mapan di literatur.<br/>**(C)** Diterapkan pada korpus skripsi Indonesia dengan akurasi puncak **97,22%** (baseline **93,71%**) vs *Logistic Regression* (**88,57%**). |
| **FR-04** | **Agent 1 (Inspector):** Menandai paragraf dengan `is_ambiguous = True` jika skor keyakinan prediksi $<$ 0.70 (70%). | **S12 (Latha & Reddy, 2026)** membahas adaptasi model berbasis metadata; **Ref 90 (Sheng et al., 2025)** mengkaji analisis ketidakpastian (*uncertainty*) pada evaluasi model. | **SEBAGIAN** | **(A)** Konsep *uncertainty* telah dibahas di literatur evaluasi LLM.<br/>**(B)** Belum digunakan sebagai pemicu audit deterministik antar-agen pada struktur dokumen.<br/>**(C)** Penandaan ambiguitas probabilistik ($< 0.70$) sebagai umpan langsung ke *Agent 2*. |
| **FR-05** | **Agent 2 (Quality Critic - SQA Tier 1):** Audit urutan bab monotonik ($\text{Bab I} \rightarrow \text{Bab II} \dots$) & pola *Regex* `^BAB\s+([IVX\d]+)` pada Skripsi dan Laporan Magang (mengatasi **RSK-02**). | **S02 (Gabauer, 2026)** dan **S10 (Muwa et al., 2026)** merumuskan kerangka kerja hibrida yang memadukan model berbasis data dengan perencana/kontrol logika simbolik (*symbolic control*). | **SEBAGIAN** | **(A)** S02 dan S10 menyediakan kerangka konseptual *hybrid neuro/statistical-symbolic*.<br/>**(B)** Belum ada aturan simbolik spesifik untuk memvalidasi sekuens bab monotonik karya ilmiah Indonesia & variasi bab magang.<br/>**(C)** Algoritma audit bab monotonik + *Regex Priority Pattern* pada *Agent 2*. |
| **FR-06** | **Agent 2 (Quality Critic - SQA Tier 1):** *Guardrail* karantina halaman awal (*frontmatter*) & isolasi zona sub-bab 1.7 Sistematika Penulisan agar bebas *false positive* bab baru (mengatasi **RSK-01**). | **S15 (Agarwal & Nene, 2025)** mengusulkan kerangka tata kelola AI 5 lapis; **Ref 117 (Sammartino, 2026)** merekomendasikan agen validasi keluaran. | **BELUM ADA** | **(A)** S15 hanya menyajikan tata kelola regulasi makro 5 lapis.<br/>**(B)** Tidak ada satupun literatur yang menangani anomali kontekstual naskah Indonesia di mana narasi "Bab I, Bab II" di dalam sub-bab 1.7 memicu *false positive* pergantian bab.<br/>**(C)** **5 Lapisan Guardrail Kontekstual** dengan isolasi zona Sistematika Penulisan dan karantina *Frontmatter*. |
| **FR-07** | **Agent 2 (Quality Critic - SQA Tier 1):** Memvalidasi dan mengamankan baris rumus matematika serta *caption* Gambar/Tabel agar tidak salah menjadi sub-bab (mengatasi **RSK-04**). | **S07 (Saier et al., 2023)** mengekstraksi elemen rumus dan sitasi pada korpus ilmiah berbahasa Inggris (*unarXive*). | **SEBAGIAN** | **(A)** S07 mengenali elemen formula pada dokumen LaTeX arXiv.<br/>**(B)** Pada `.docx`, penomoran rumus `(2.1)` sangat mirip dengan sub-bab `2.1` sehingga rawan salah diklasifikasi oleh ML murni.<br/>**(C)** Filter proteksi formula & *caption* berbasis fitur spasial *OpenXML* + *Guardrail Agent 2*. |
| **FR-08** | **Agent 1 & Agent 2 Coordination:** Menjalankan siklus negosiasi *SQA Tier 1* (*Feedback Directives* & re-inspeksi adaptif) hingga menghasilkan *Approved Blueprint* 100% konsisten. | **S01 (Malfa et al., 2025)**, **S03 (Petridis et al., 2025)**, dan **S11 (Zhang et al., 2024)** menekankan otonomi agen sejati, pembagian peran spesialis, dan mekanisme refleksi/koreksi antar-agen. | **TERPENUHI** | **(A)** S01, S03, dan S11 membuktikan efektivitas kolaborasi berbasis peran (*debate/reflection*).<br/>**(B)** Konsep refleksi multi-agen di literatur dapat diadaptasi langsung.<br/>**(C)** Implementasi *Blueprint Verification Loop* deterministik antara *Inspector* dan *Critic*. |
| **FR-09** | **Agent 3 (Formatting Actuator):** Sanitasi total *template* kotor (hapus tag `<w:numPr>` liar untuk cegah **RSK-03**) & rekonstruksi *Cover* resmi berlogo UEU 3.0 cm rata tengah. | **Ref 117 (Sammartino, 2026)** dan **Ref 118 (Geng et al., 2026)** membahas *input sanitization* untuk keamanan eksekusi agen. | **BELUM ADA** | **(A)** Literatur hanya membahas sanitasi *prompt* teks terhadap serangan siber.<br/>**(B)** Belum ada mekanisme sanitasi pohon DOM *OpenXML* (`<w:numPr>`) untuk mencegah penomoran ganda (`1.1 1.1`) sekaligus membangun ulang sampul standar institusi.<br/>**(C)** Mesin **Sanitasi Total DOM OpenXML & Rekonstruksi Cover Otomatis** oleh *Agent 3*. |
| **FR-10** | **Agent 3 (Formatting Actuator):** Membagi dokumen menjadi **3 Section terisolasi** (*Cover*, *Frontmatter*, *Isi Bab*) dengan `link_to_previous = False` untuk *Dual Page Numbering* (Romawi & Latin). | Tidak ditemukan pada **S01–S15** maupun **126 studi Scopus AI** (literatur berfokus pada generasi teks/evaluasi, bukan manipulasi seksi biner XML). | **BELUM ADA** | **(A)** Nihil di dalam 126 paper Scopus AI.<br/>**(B)** Model NLP/LLM tidak mampu memanipulasi atribut `<w:sectPr>` untuk memutus tautan *header/footer* antar-seksi secara non-destruktif.<br/>**(C)** **Automated 3-Section Isolation & Dual Page Numbering Engine** berbasis *low-level OpenXML*. |
| **FR-11** | **Agent 3 (Formatting Actuator):** Menyuntikkan properti *style* resmi dan tag `<w:outlineLvl>` untuk *Heading 1–3* agar langsung muncul di *Navigation Pane* MS Word. | Tidak ditemukan pada **S01–S15**. | **BELUM ADA** | **(A)** Literatur hanya berhenti pada pelabelan teks (*text tagging*).<br/>**(B)** Pelabelan teks tanpa injeksi `<w:outlineLvl>` tidak memperbaiki struktur *Navigation Pane* di MS Word.<br/>**(C)** Injeksi langsung hierarki `<w:outlineLvl>` ke pohon XML dokumen. |
| **FR-12** | **Agent 3 (Formatting Actuator):** Menghasilkan *Dynamic Table of Contents* (Daftar Isi, Gambar, Tabel) dengan *dot leaders* & instruksi `<w:updateFields w:val="true"/>`. | Tidak ditemukan pada **S01–S15**. | **BELUM ADA** | **(A)** Tidak ada studi di korpus Scopus AI yang mengotomatisasi *Complex Field* (`w:fldSimple` / `w:instrText` TOC) pada OpenXML.<br/>**(B)** Karena manipulasi dilakukan *headless* (tanpa GUI Word), diperlukan mekanisme pemicu *auto-compute* halaman saat file dibuka.<br/>**(C)** Generator *Dynamic TOC Field* & injeksi `<w:updateFields w:val="true"/>`. |
| **FR-13** | **Agent 3 (Formatting Actuator):** Menstandarisasi seluruh tabel ke format **APA 7th Edition** (hapus garis vertikal, sisakan 3 garis horizontal utama) & font *Times New Roman*. | Tidak ditemukan pada **S01–S15**. | **BELUM ADA** | **(A)** Nihil pada 15 studi primer Scopus.<br/>**(B)** Pemformatan tabel di naskah mahasiswa masih dilakukan manual satu per satu dan rawan melanggar standar APA 7.<br/>**(C)** **Automated APA 7 Table Border Refactoring** pada elemen `<w:tblBorders>` tanpa mengubah isi sel tabel (*100% non-destructive*). |
| **FR-14** | **Agent 2 (Quality Critic - SQA Tier 2):** Mengaudit berkas fisik `.docx` hasil rekonstruksi *Agent 3* terhadap **8 kriteria mutu SK Rektor UEU** & menginstruksikan auto-remediasi jika gagal. | **S13 (Chou, 2026)** mengkaji agen *Software Quality Assessment* (SQA); **S14 (Liu et al., 2026)** mengusulkan evaluasi *multi-level* (*Mosaic*); **S15 (Agarwal & Nene, 2025)** merumuskan sertifikasi kepatuhan regulasi. | **BELUM ADA** | **(A)** S13 menunjukkan bahwa *LLM-as-a-Judge* tidak konsisten untuk SQA, sedangkan S14 dan S15 memberikan kerangka konseptual evaluasi bertingkat & regulasi.<br/>**(B)** Belum ada agen SQA yang mengaudit berkas fisik `.docx` secara deterministik terhadap regulasi universitas sekaligus melakukan auto-remediasi.<br/>**(C)** **Two-Tier Deterministic SQA Gate** (Tier 1: *Blueprint* & Tier 2: *Physical Artifact 8 Kriteria UEU*) dengan capaian **100% PASS**. |
| **FR-15** | **Active Learning Module:** Menyimpan koreksi deterministik *Agent 2* ke CSV, lalu memicu *continuous retraining* & *hot-reload* model saat mencapai $\ge 5$ sampel (mengatasi **RSK-05**). | **S12 (Latha & Reddy, 2026)** membahas *meta-learning* adaptif; **Ref 124 (Middha et al., 2024)** & **Ref 125 (Yu et al., 2025)** membahas augmentasi data pada bahasa *low-resource*. | **SEBAGIAN** | **(A)** Literatur membahas adaptasi model dan augmentasi data secara terpisah dari agen pengawas.<br/>**(B)** *Active learning* konvensional membutuhkan pelabelan manusia (*human annotation*) yang lambat.<br/>**(C)** **Critic-Driven Autonomous Active Learning** (koreksi simbolik *Agent 2* menjadi label emas otomatis untuk melatih ulang *Agent 1* dengan *0s downtime hot-reload*). |
| **FR-16** | **Web Interface (`alat.html` & `alat.js`):** Menampilkan progres interaktif, konsol log eksekusi agen *real-time*, kartu skor SQA, dan tombol unduh `(Asdoku) - ...`. | **S14 (Liu et al., 2026)** mengusulkan kerangka *Mosaic* untuk mengobservasi proses kerja MAS secara transparan. | **TERPENUHI** | **(A)** S14 menekankan pentingnya observabilitas berorientasi proses pada MAS.<br/>**(B)** Dapat diimplementasikan langsung melalui *live streaming log* dan kartu skor mutu.<br/>**(C)** Visualisasi *Live Execution Terminal Log* dan *SQA Scorecard* pada antarmuka web. |

### Ringkasan Pemetaan Matriks Silang (TAHAP 1):

* **Status TERPENUHI:** 3 Kebutuhan Fungsional (**FR-03, FR-08, FR-16**) — **18,75%**
* **Status SEBAGIAN:** 5 Kebutuhan Fungsional (**FR-01, FR-04, FR-05, FR-07, FR-15**) — **31,25%**
* **Status BELUM ADA (Kandidat Gap Terkuat):** 8 Kebutuhan Fungsional (**FR-02, FR-06, FR-09, FR-10, FR-11, FR-12, FR-13, FR-14**) — **50,00%**

---

## TAHAP 2 — Skoring 3 Kandidat Gap Terkuat & Pemilihan Gap Pemenang

Dari 8 baris berstatus **"BELUM ADA"** pada Tahap 1, ketiganya dikonsolidasikan menjadi **3 Kandidat Gap Utama** yang merepresentasikan celah Metodologis, Dataset, Konteks, dan Performa:

1. **Kandidat Gap 1 (Integrasi End-to-End MAS Hibrida, Two-Tier SQA, & Rekonstruksi Non-Destruktif OpenXML — Mencakup FR-02, FR-06, FR-09 s/d FR-14):**
Belum adanya arsitektur *Multi-Agent System* hibrida yang menyatukan deteksi struktur berbasis fitur hibrida NLP + *OpenXML* (*Agent 1*), validasi logika simbolik *Two-Tier SQA* dengan *5 Lapisan Guardrail* (*Agent 2*), serta aktuator rekonstruksi tata letak `.docx` tingkat rendah secara non-destruktif (*Agent 3*).
2. **Kandidat Gap 2 (Representasi Fitur Hibrida NLP + Spasial OpenXML pada Korpus Bahasa Indonesia — Mencakup FR-02 & FR-07):**
Ketiadaan metode ekstraksi fitur yang menggabungkan 400 dimensi leksikal *TF-IDF N-Gram* dengan 20 fitur metadata spasial *OpenXML* pada 7 pilar dataset akademik berbahasa Indonesia (*low-resource*).
3. **Kandidat Gap 3 (Tata Kelola Two-Tier Deterministic SQA & Critic-Driven Active Learning — Mencakup FR-06, FR-14, & FR-15):**
Kelemahan pendekatan *LLM-as-a-Judge* yang bias dan lambat pada *Software Quality Assessment* multi-agen, sehingga dibutuhkan agen pengawas deterministik dua tingkat (*Blueprint* & *Physical Artifact*) yang sekaligus menggerakkan siklus *Active Learning* mandiri.

### Tabel Skoring Kandidat Gap

| Kandidat Gap | Jenis Gap (SLR) | Novelty (1–10) | Kelayakan (1–10) | Dampak (1–10) | Total Skor (Maks 30) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gap 1: Orkestrasi Tri-Agent Hibrida (NLP + Simbolik Two-Tier SQA) untuk Deteksi Struktur & Rekonstruksi Non-Destruktif OpenXML (`FR-02`, `FR-06`, `FR-09`–`FR-14`)** | **Metodologis, Konteks & Performa (Terpadu)** | **9,5** | **9,5** | **10,0** | **29,0 / 30** *(PEMENANG)* |
| **Gap 2: Ekstraksi 420 Fitur Hibrida (TF-IDF + Metadata Spasial OpenXML) pada 7 Pilar Dataset Akademik Bahasa Indonesia (`FR-02`, `FR-07`)** | **Dataset & Representasi Fitur** | 8,5 | 9,5 | 8,5 | 26,5 / 30 |
| **Gap 3: Mekanisme Two-Tier Deterministic SQA & Critic-Driven Autonomous Active Learning (`FR-06`, `FR-14`, `FR-15`)** | **Evaluasi Mutu (SQA) & Adaptabilitas** | 9,0 | 9,0 | 8,5 | 26,5 / 30 |

### Justifikasi Pemilihan Gap Pemenang (Gap 1 — Skor 29,0/30):

* **(A) Fakta dari BRD & SLR:** Dalam 126 paper Scopus AI (S01–S15), penelitian yang ada terpecah antara sistem keagenan teoritis/evaluasi teks (**Malfa et al., 2025 [S01]**; **Gabauer, 2026 [S02]**; **Chou, 2026 [S13]**) dan ekstraksi korpus ilmiah statis (**Saier et al., 2023 [S07]**; **Li et al., 2022 [S08]**). Di sisi lain, BRD menuntut penyelesaian masalah nyata mahasiswa UEU dari hulu (deteksi struktur dengan akurasi puncak **97,22%**) hingga hilir (dokumen `.docx` lulus audit fisik **100% PASS** dalam waktu rata-rata **0,98 detik**).
* **(B) Interpretasi Pola:** Jika hanya mengambil Gap 2 (hanya deteksi NLP tanpa memformat `.docx`) atau Gap 3 (hanya audit SQA tanpa aktuator *OpenXML*), maka **Business Objective BO-02 (100% PASS kepatuhan SK Rektor UEU)** dan **BO-03 (efisiensi waktu pemrosesan $\le 2,0$ detik menggantikan 2–4 jam kerja manual)** tidak akan tercapai secara utuh.
* **(C) Usulan Novelty:** **Gap 1** adalah *umbrella gap* (celah payung) yang secara otomatis merangkum Gap 2 dan Gap 3 ke dalam satu kesatuan rekayasa sistem yang utuh: **Arsitektur Tri-Agent Hibrida** (*Inspector*, *Quality Critic*, *Formatting Actuator*) yang menjembatani pemahaman bahasa alami (*NLP*) dengan manipulasi struktur fisik *OpenXML* berjaminan mutu *Two-Tier SQA*.

---

## TAHAP 3 — 5 Rekomendasi Judul Tugas Akhir Berdasarkan Gap Pemenang

Seluruh kandidat judul di bawah ini mematuhi aturan ketat: **maksimal 20 kata**, **spesifik**, **tidak klise**, dan menggunakan struktur baku **`[Metode] untuk [Outcome] pada [Objek/Konteks]`**.

| No | Kandidat Judul Tugas Akhir (Maksimal 20 Kata) | Jumlah Kata | Daya Tarik (1–10) | Novelty (1–10) | Kelayakan (1–10) | Total Skor (Maks 30) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | **Rancang Bangun Multi-Agent System Berbasis Natural Language Processing untuk Otomatisasi Deteksi Struktur dan Formatting pada Dokumen Akademik** | **17 Kata** | **9,5** | **9,5** | **10,0** | **29,0** *(PERINGKAT 1)* |
| **2** | **Arsitektur Multi-Agent Hibrida dan Two-Tier SQA Berbasis NLP untuk Otomatisasi Deteksi Struktur dan Formatting pada Dokumen Akademik** | **17 Kata** | **9,5** | **10,0** | **9,0** | **28,5** |
| **3** | **Integrasi Multi-Agent System dan Fitur Hibrida NLP-OpenXML untuk Otomatisasi Deteksi Struktur dan Rekonstruksi Formatting pada Dokumen Akademik** | **17 Kata** | **9,0** | **9,5** | **9,5** | **28,0** |
| **4** | **Orkestrasi Tri-Agent System Berbasis Natural Language Processing untuk Validasi Struktur dan Otomatisasi Formatting Non-Destruktif pada Naskah Akademik** | **17 Kata** | **9,0** | **9,0** | **9,5** | **27,5** |
| **5** | **Kombinasi Klasifikasi NLP dan Kontrol Simbolik Multi-Agent untuk Otomatisasi Deteksi Struktur dan Standarisasi Tata Letak Dokumen Akademik** | **17 Kata** | **8,5** | **9,0** | **9,5** | **27,0** |

### Pemetaan Struktur `[Metode] untuk [Outcome] pada [Objek/Konteks]` pada Kelima Judul:

1. **Judul 1:** `[Rancang Bangun Multi-Agent System Berbasis Natural Language Processing]` **untuk** `[Otomatisasi Deteksi Struktur dan Formatting]` **pada** `[Dokumen Akademik]`.
2. **Judul 2:** `[Arsitektur Multi-Agent Hibrida dan Two-Tier SQA Berbasis NLP]` **untuk** `[Otomatisasi Deteksi Struktur dan Formatting]` **pada** `[Dokumen Akademik]`.
3. **Judul 3:** `[Integrasi Multi-Agent System dan Fitur Hibrida NLP-OpenXML]` **untuk** `[Otomatisasi Deteksi Struktur dan Rekonstruksi Formatting]` **pada** `[Dokumen Akademik]`.
4. **Judul 4:** `[Orkestrasi Tri-Agent System Berbasis Natural Language Processing]` **untuk** `[Validasi Struktur dan Otomatisasi Formatting Non-Destruktif]` **pada** `[Naskah Akademik]`.
5. **Judul 5:** `[Kombinasi Klasifikasi NLP dan Kontrol Simbolik Multi-Agent]` **untuk** `[Otomatisasi Deteksi Struktur dan Standarisasi Tata Letak]` **pada** `[Dokumen Akademik]`.

---

## TAHAP 4 — Analisis Final & Rekomendasi

### 1. Analisis Mengapa Judul Peringkat 1 Paling Kuat (Kaitan ke Gap & Novelty)

* **(A) Fakta dari BRD & SLR:** Judul Peringkat 1 (*"Rancang Bangun Multi-Agent System Berbasis Natural Language Processing untuk Otomatisasi Deteksi Struktur dan Formatting pada Dokumen Akademik"*) memiliki keselarasan 100% dengan rumusan masalah **RQ 1.1, RQ 1.2, dan RQ 1.3** pada dokumen Fase 1 (PICOS) dan BRD, sekaligus menjawab langsung kritik **Malfa et al. (2025) [S01]** serta **Gabauer (2026) [S02]** di SLR.
* **(B) Interpretasi Pola:** Judul ini memiliki keseimbangan sempurna antara **kejelasan akademik tingkat S1 Teknik Informatika** (*Kelayakan 10/10*) dan **kedalaman kontribusi riset** (*Novelty 9,5/10*). Istilah *"Multi-Agent System"* dan *"Natural Language Processing"* sebagai `[Metode]` langsung memayungi inovasi di balik layar (420 fitur hibrida, *Random Forest* 97,22%, *Two-Tier SQA*, dan *Active Learning*), sementara frasa *"Otomatisasi Deteksi Struktur dan Formatting"* sebagai `[Outcome]` secara eksplisit membedakan penelitian ini dari penelitian NLP biasa yang hanya mengklasifikasikan teks tanpa mampu memformat berkas fisik `.docx`.
* **(C) Usulan Novelty:** Judul ini mengunci dua kutub kebaruan sekaligus: **otonomi kolaborasi multi-agen** di tingkat kecerdasan buatan dan **rekonstruksi tata letak non-destruktif** di tingkat rekayasa perangkat lunak (*OpenXML*), dengan pembuktian empiris **100% PASS** pada 5 *Gold Datasets* dalam waktu rata-rata **0,98 detik**.

---

### 2. Alternatif Versi Judul: Versi Akademik (Jurnal/Paper) vs Versi Praktis (Industri/Produk)

Apabila hasil Tugas Akhir ini dipublikasikan ke jurnal internasional terindeks Scopus/SINTA atau dihilirisasi menjadi produk perangkat lunak kampus, berikut adalah adaptasi judulnya:

* **Versi Akademik (Publikasi Jurnal Scopus / IEEE / Springer):**
  > **"Arsitektur Multi-Agent Hibrida dan Two-Tier SQA Berbasis Fitur NLP-OpenXML untuk Deteksi Struktur dan Rekonstruksi Dokumen Akademik"** *(16 Kata)*  
  > *(Versi Bahasa Inggris untuk Jurnal Internasional: "A Hybrid NLP-Symbolic Multi-Agent System with Two-Tier Quality Assurance for Automated Structure Detection and Non-Destructive Academic Document Formatting")*  
  > **Alasan:** Menonjolkan terminologi teoretis dari SLR Scopus (**Gabauer, 2026 [S02]**; **Liu et al., 2026 [S14]**) yaitu *Hybrid Multi-Agent*, *Two-Tier SQA*, dan *NLP-OpenXML Features*.

* **Versi Praktis / Industri (Implementasi Produk Kampus / SaaS EdTech — ASDOKU):**
  > **"ASDOKU: Platform Web Multi-Agent Berbasis NLP untuk Otomatisasi Standarisasi dan Penjaminan Mutu Format Dokumen Karya Ilmiah"** *(16 Kata)*  
  > **Alasan:** Menonjolkan nilai guna bisnis (*value proposition* dari BRD: kecepatan $\le 2$ detik, bebas ribet mengatur margin/daftar isi manual, dan jaminan kepatuhan 100% terhadap standar institusi).

---

### 3. Rekomendasi Final & Paragraf Pembuka Latar Belakang (Bab I Skripsi)

#### Rekomendasi Judul Final Tugas Akhir:

> **"Rancang Bangun Multi-Agent System Berbasis Natural Language Processing untuk Otomatisasi Deteksi Struktur dan Formatting pada Dokumen Akademik"**  
> *(Atau varian susunan kata identik pada BRD/PICOS: **"Rancang Bangun Multi-Agent System untuk Otomatisasi Deteksi Struktur dan Formatting Dokumen Akademik Berbasis Natural Language Processing"** — keduanya berjumlah 16–17 kata, 100% konsisten dengan seluruh dokumen Fase 1, Fase 2, BRD, dan SLR).*

#### Kalimat & Paragraf Pembuka Latar Belakang (Siap Pakai untuk Bab I Skripsi):

> **"Penyusunan karya ilmiah akhir seperti Skripsi, Proposal Tugas Akhir, dan Laporan Kerja Praktik menuntut kepatuhan mutlak terhadap regulasi tata letak dan tipografi institusi, sebagaimana diatur secara ketat dalam Surat Keputusan Rektor Universitas Esa Unggul Nomor 5 Tahun 2018 serta standar tabel *APA 7th Edition*. Namun, dalam praktiknya, ketiadaan sistem otomatisasi yang mampu memahami struktur semantik naskah menyebabkan mahasiswa dan dosen pembimbing harus menghabiskan waktu rata-rata 2 hingga 4 jam per dokumen hanya untuk memperbaiki kesalahan teknis pemformatan secara manual di Microsoft Word—mulai dari kerusakan hierarki penomoran sub-bab, ketiadaan *Heading Styles* pada *Navigation Pane*, kegagalan isolasi nomor halaman ganda (*Romawi* dan *Latin*), hingga inkonsistensi format tabel. Di sisi lain, perkembangan riset *Natural Language Processing* (NLP) dan *Multi-Agent Systems* (MAS) pada rentang tahun 2021–2026 menunjukkan bahwa model klasifikasi tunggal yang bekerja secara terisolasi rentan mengalami kesalahan prediksi kontekstual pada dokumen semi-terstruktur dan tidak memiliki kapabilitas untuk merekonstruksi struktur fisik *OpenXML* (`.docx`) secara non-destruktif (Malfa et al., 2025; Gabauer, 2026). Untuk menjembatani celah tersebut, penelitian ini mengusulkan rancang bangun sistem otomatisasi cerdas bernama ASDOKU yang mengintegrasikan ekstraksi 420 dimensi fitur hibrida (400 fitur leksikal *TF-IDF N-Gram* dan 20 fitur metadata spasial *OpenXML*) ke dalam arsitektur kolaboratif *Tri-Agent System* (*Inspector Agent*, *Quality Critic Agent*, dan *Formatting Actuator Agent*) yang dikawal oleh mekanisme penjaminan mutu *Two-Tier Software Quality Assurance* (SQA)."**

---

> **Pernyataan Pengesahan Fase 6A:**  
> Berkas analisis gap dan rekomendasi judul ini disusun secara sistematis mengacu pada sintesis silang BRD dan SLR untuk mata kuliah Kapita Selekta dan menjadi dasar perumusan Bab 1 Proposal Tugas Akhir Program Studi Teknik Informatika, Fakultas Ilmu Komputer, Universitas Esa Unggul.
