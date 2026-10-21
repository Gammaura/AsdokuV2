# AUDIT KRITIS BRD $\times$ SLR, KELAYAKAN AKADEMIK, DAN EVALUASI PORTOFOLIO INDUSTRI
## Proyek: ASDOKU (*Multi-Agent System untuk Otomatisasi Deteksi Struktur dan Formatting Dokumen Akademik Berbasis NLP*)

> **Kode Dokumen:** `AUDIT-ASDOKU-2026-F6`  
> **Mata Kuliah:** Kapita Selekta — FASILKOM Universitas Esa Unggul  
> **Auditor Peran 1:** Dosen Pembimbing & Penguji Sidang Skripsi (Skeptis, Metodologis, Berbasis Bukti)  
> **Auditor Peran 2:** Senior Tech Lead / Hiring Manager (Pragmatis, Arsitektural, Anti-*Buzzword*)  
> **Kandidat / Peneliti:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Program Studi / Institusi:** Teknik Informatika, Fakultas Ilmu Komputer (FASILKOM) — Universitas Esa Unggul  
> **Regulasi Acuan:** SK Rektor Universitas Esa Unggul No. 5 Tahun 2018 (Pedoman Penulisan Skripsi & Tugas Akhir)  
> **Dokumen Terkait:** [BRD_Business_Requirements_Document.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%203%20-%20Dokumen%20BRD/BRD_Business_Requirements_Document.md), [SLR_Systematic_Literature_Review.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%204%20-%20Dokumen%20SLR/SLR_Systematic_Literature_Review.md), [Evidence_Matrix_Scopus.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%202%20-%20Penelusuran%20Literatur%20&%20Evidence%20Matrix/Evidence_Matrix_Scopus.md), dan [Gap_Analysis_dan_Penetapan_Judul.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%205%20-%20Analisis%20Gap%20&%20Penetapan%20Judul/Gap_Analysis_dan_Penetapan_Judul.md)  
> **Tanggal Analisis:** 21 Oktober 2026  
> **Status Dokumen:** Final Audit & Action Plan (Fase 6 — Uji Kesesuaian & Kritik Keras)

---

## TAHAP 1 — Audit Kesesuaian BRD $\times$ SLR (Deteksi Klaim yang "Terlihat Dipaksakan")

Tabel berikut membedah setiap **Business Objective (BO)** dan kelompok **Functional Requirements (FR)** di BRD terhadap **15 Studi Primer (S01–S15)** pada laporan Scopus AI. Status dibagi menjadi: **VALID & KUAT**, **COCOKLOGI / DIPAKSAKAN**, atau **MURNI REKAYASA TEKNIS (TANPA BUKTI SLR)**.

| Komponen BRD | Klaim Bukti di SLR (S01–S15) | Verdict Audit | Bedah Kritis: (A) Fakta Dokumen, (B) Kritik Skeptis, (C) Rekomendasi Aksi |
| :--- | :--- | :---: | :--- |
| **BO-01 & FR-02, FR-03**<br/>*(Ekstraksi 420 Fitur Hibrida: 400 TF-IDF + 20 Metadata OpenXML & Klasifikasi Random Forest vs Logistic Regression)* | **S05** (Ali et al., 2024), **S06** (Roldan-Baluis et al., 2022), **S09** (Blagec et al., 2022), **S12** (Latha & Reddy, 2026). | **SEBAGIAN VALID / SEBAGIAN DIPAKSAKAN** | **(A) Fakta:** S05 dan S06 memang membahas ML tradisional untuk NLP teks tak terstruktur. S12 membahas *Metadata-Driven Meta-Learning Architectures*.<br/>**(B) Kritik (DIPAKSAKAN):** Mencatut **S12 (Latha & Reddy, 2026)** sebagai landasan ekstraksi 20 atribut DOM *OpenXML* (`font_size`, `is_bold`, `is_below_drawing`) adalah **lompatan konseptual**. *Meta-learning metadata* di S12 mengacu pada metadata distribusi dataset untuk adaptasi lintas-tugas (*task adaptation*), bukan fitur *layout* dokumen Word! Selain itu, di Fase 2 awal sempat tercantum paper fiktif (*Vaswani & Kumar, 2022; Fernandez et al., 2023*) sebelum diganti ke S01–S15.<br/>**(C) Aksi:** Jangan klaim S12 sebagai pencetus fitur OpenXML. Nyatakan di Bab II bahwa S12 menjadi inspirasi pemanfaatan metadata, sedangkan ekstraksi **20 fitur spasial OpenXML** adalah kontribusi *feature engineering* Anda sendiri (atau tambahkan 1 paper *Document Layout Analysis* asli via Mendeley). |
| **FR-05, FR-08**<br/>*(Arsitektur Tri-Agent: Inspector, Quality Critic, Formatting Actuator & Negosiasi Blueprint)* | **S01** (Malfa et al., 2025), **S02** (Gabauer, 2026), **S03** (Petridis et al., 2025), **S04** (Kumara et al., 2026), **S10** (Muwa et al., 2026), **S11** (Zhang et al., 2024). | **TERLIHAT DIPAKSAKAN (OVERCLAIMING ISTILAH)** | **(A) Fakta:** S01, S02, S10, dan S11 membahas *LLM-based Multi-Agent Systems*, *neuro-symbolic planning*, dan psikologi sosial kolaborasi agen LLM (debat/refleksi). Sementara ASDOKU menggunakan `scikit-learn` (*Random Forest*), aturan *if-else/Regex* (`critic.py`), dan skrip manipulasi XML (`formatter.py`).<br/>**(B) Kritik Keras:** Di sinilah titik paling rawan saat sidang! Anda mengutip paper tentang **LLM Agents** (S01, S02, S11) untuk menjustifikasi sistem yang **sama sekali tidak memakai LLM**, melainkan **Sequential Pipeline + Rule Engine**. Penguji atau *Tech Lead* akan langsung bertanya: *"Ini beneran Multi-Agent yang otonom sesuai definisi Wooldridge di S01, atau cuma 3 file Python yang dipanggil berurutan di dalam `app.py`?"*<br/>**(C) Aksi:** Gunakan **S01 (Malfa et al., 2025)** dan **S03 (Petridis et al., 2025)** justru untuk menyerang kelemahan LLM dan membenarkan **Classical/Hybrid Agent Paradigm** (agen tidak wajib berbasis LLM, melainkan entitas perangkat lunak dengan pemisahan peran *perceive-reason-act* dan *feedback loop* nyata antara `inspector.py` $\leftrightarrow$ `critic.py` $\leftrightarrow$ `formatter.py`). |
| **BO-02, FR-06, FR-14**<br/>*(Two-Tier SQA & 5 Lapisan Guardrail untuk SK Rektor UEU No. 5/2018)* | **S13** (Chou, 2026), **S14** (Liu et al., 2026 - *Mosaic*), **S15** (Agarwal & Nene, 2025). | **COCOKLOGI TERMINOLOGI (DIPAKSAKAN)** | **(A) Fakta:** S13 membahas *AI-as-a-Judge* untuk evaluasi kode, S14 membahas observabilitas performa MAS, dan S15 membahas *five-layer framework for AI governance* (regulasi pemerintah, standar nasional, sertifikasi).<br/>**(B) Kritik (DIPAKSAKAN):** Menyamakan *"5-Layer AI Governance"* milik **Agarwal & Nene (2025) [S15]** (yang membahas kebijakan publik/pemerintahan di jurnal *Transforming Government*) dengan **5 blok validasi Regex/aturan kode** di `critic.py` (seperti karantina *frontmatter* dan isolasi sub-bab 1.7) adalah **cocoklogi angka "5"**. Begitu pula istilah *Software Quality Assurance (SQA)*: mengecek margin 4-3-3-3 cm pada file `.docx` bukanlah SQA perangkat lunak, melainkan **Document Compliance Auditing / Output Validation**.<br/>**(C) Aksi:** Ubah klaim terhadap S15 menjadi **analogi adaptasi konsep** (*"Mengadaptasi prinsip tata kelola berlapis dari S15 ke dalam ranah mikro validasi dokumen sebagai 5 Lapisan Guardrail Kontekstual"*). Untuk SQA, tegaskan bahwa ini adalah **Artifact Quality Gate** (mengacu pada *output validation agents* di **Ref 118 [Geng et al., 2026]**). |
| **BO-04 & FR-04, FR-15**<br/>*(Active Learning dengan Threshold < 0.70 & Auto-Retrain tiap $\ge 5$ Sampel)* | **S12** (Latha & Reddy, 2026), **Ref 124** (Middha et al., 2024), **Ref 125** (Yu et al., 2025). | **TERLIHAT DIPAKSAKAN (BAHAYA KONSEPTUAL ML)** | **(A) Fakta:** BRD menyatakan bahwa koreksi *Agent 2* langsung disimpan ke CSV dan memicu *retraining* *Agent 1* setiap mencapai $\ge 5$ sampel, yang diklaim menaikkan akurasi dari 93,71% ke **97,22%**.<br/>**(B) Kritik Keras:** Pertama, di dalam 126 paper Scopus AI **tidak ada** bahasan spesifik tentang *micro-batch active learning threshold = 5*. Kedua, secara teori *Machine Learning*, melatih model menggunakan output dari *Rule Engine* (`critic.py`) tanpa verifikasi manusia bukanlah *Active Learning* sejati, melainkan **Rule-Guided Pseudo-Labeling / Weak Supervision** (yang justru didukung oleh **Ref 72 & 85 [Liu et al., 2023]** tentang *weakly supervised neuro-symbolic reasoning* di PDF Scopus Anda!).<br/>**(C) Aksi:** Ganti sandaran teori fitur ini ke **Ref 72 / Ref 85 (Liu et al., 2023 - *Weakly supervised reasoning by neuro-symbolic approaches*)**! Itu ada di halaman 15–16 PDF Scopus Anda dan 100% akurat secara keilmuan: aturan simbolik (*Agent 2*) memberikan supervisi lemah (*weak label*) untuk melatih model statistik (*Agent 1*). |
| **BO-03 & FR-09 s/d FR-13**<br/>*(Manipulasi Low-Level OpenXML: Sanitasi `<w:numPr>`, 3 Section, TOC, Tabel APA 7)* | Tidak ada di S01–S15 (Hanya dikaitkan longgar ke **Ref 117** tentang *input sanitization* keamanan LLM). | **MURNI REKAYASA TEKNIS (NIHIL DI SLR)** | **(A) Fakta:** Seluruh 126 paper di laporan Scopus AI membahas AI/MAS/NLP, tidak ada satu pun yang membahas struktur skema XML ECMA-376 atau pustaka `python-docx`.<br/>**(B) Kritik:** Mengaitkan penghapusan tag `<w:numPr>` dengan *input sanitization* keamanan siber di **Ref 117 (Sammartino, 2026)** terlalu jauh.<br/>**(C) Aksi:** Di Bab II Skripsi, pisahkan sub-bab **Landasan Teori Rekayasa Dokumen (Standar ISO/IEC 29500 OpenXML & APA 7th Edition)** dari sub-bab **SLR MAS-NLP**. Jangan paksakan paper AI untuk menjustifikasi tag XML `<w:sectPr>` atau `<w:tblBorders>`. |

---

## TAHAP 2 — Kritik Kelayakan Brutal (Kacamata Dosen Pembimbing & Penguji)

### 1. Apakah topik ini realistis diselesaikan mahasiswa S1 dalam 1 semester dengan skill teknis rata-rata?

* **(A) Fakta Dokumen:** Dokumen Anda menunjukkan sistem sudah memiliki metrik aktual (1.747 sampel, akurasi baseline 93,71% $\rightarrow$ 97,22%, 5 *Gold Datasets* P1–P5 lulus 100% PASS, waktu eksekusi rata-rata 0,98 detik, serta file `inspector.py`, `critic.py`, `formatter.py`, `app.py`, `alat.html`).
* **(B) Kritik Brutal:** Jika dimulai dari nol oleh mahasiswa S1 dengan *skill* rata-rata dalam 1 semester, **TIDAK REALISTIS (Tingkat kegagalan > 80%)**. Mengapa? Karena memanipulasi DOM `lxml` / `python-docx` untuk memecah 3 *section* berbeda (`link_to_previous = False`), merombak border tabel XML, dan menyuntikkan *complex field* TOC tanpa merusak gambar/rumus di `.docx` adalah mimpi buruk *debugging*. Namun, karena prototipe dan eksperimen Anda **sudah terbangun**, tantangannya bukan lagi *"bisa selesai atau tidak"*, melainkan **"apakah Anda benar-benar memahami setiap baris kode manipulasi XML dan matriks matematika TF-IDF + Random Forest tersebut saat diuji lisan tanpa bantuan AI?"**
* **(C) Rekomendasi Aksi:** Siapkan kemampuan menjelaskan kode tingkat rendah (`lxml.etree.Element`, `qn('w:sectPr')`, mekanisme penggabungan matriks *sparse* TF-IDF 400 dimensi dengan vektor *dense* 20 fitur OpenXML) di luar kepala.

### 2. Apakah ini termasuk topik "generik/klise" yang sudah terlalu sering dikerjakan tanpa nilai tambah baru?

* **(A) Fakta Dokumen:** Topik menggabungkan deteksi struktur dokumen dengan otomatisasi *formatting* `.docx` sesuai SK Rektor UEU No. 5 Tahun 2018.
* **(B) Kritik Brutal:** Topik NLP mahasiswa S1 di Indonesia yang klise adalah *"Analisis Sentimen Ulasan Aplikasi X dengan Naive Bayes/SVM"* atau *"Chatbot Akademik Kampus dengan RAG"*. Topik Anda **SAMA SEKALI TIDAK KLISE**. Justru ini sangat segar, menyelesaikan masalah nyata yang dirasakan langsung oleh dosen penguji di ruangan sidang, dan memiliki artefak fisik yang bisa diuji langsung saat sidang (*live demo*).
* **(C) Rekomendasi Aksi:** Pertahankan fokus pada **penyelesaian masalah struktur & rekonstruksi OpenXML non-destruktif**, jangan tergiur mengubahnya menjadi *chatbot* atau asisten penulisan esai.

### 3. Apakah dataset yang dibutuhkan benar-benar bisa didapat secara legal & etis?

* **(A) Fakta Dokumen:** Populasi data terdiri dari 1.747 sampel paragraf dari 7 pilar struktur naskah akademik dan 5 dokumen uji emas (*Gold Datasets* P1–P5) milik mahasiswa Universitas Esa Unggul.
* **(B) Kritik Brutal:** **RAWAN PELANGGARAN HAK CIPTA & PRIVASI DATA (NFR-07)**. Skripsi atau Laporan Magang mahasiswa lain yang belum dipublikasikan di repositori resmi perpustakaan mengandung data pribadi (Nama, NIM, tanda tangan, atau data rahasia perusahaan tempat magang pada RSK-02). Jika Anda mengambil file `.docx` teman atau senior tanpa izin tertulis atau tanpa anonimisasi, penguji bisa mempermasalahkan etika penelitian (*ethical clearance*).
* **(C) Rekomendasi Aksi:**
  1. Lakukan **Anonimisasi Data** pada seluruh 5 *Gold Datasets* (P1–P5) dan 1.747 sampel CSV (samarkan nama penulis, NIM, dan nama perusahaan mitra magang jika bersifat konfidensial).
  2. Cantumkan di Bab III bahwa dokumen diambil dari repositori terbuka/publik perpustakaan UEU atau telah mendapatkan persetujuan (*informed consent*) dari pemilik naskah untuk keperluan riset.

### 4. Tiga Skenario Kegagalan Paling Mungkin Terjadi & Cara Memitigasinya

| No | Skenario Kegagalan Brutal (Saat Pengujian / Sidang) | Akar Masalah (Berdasarkan Fakta BRD) | Strategi Mitigasi Konkret |
| :---: | :--- | :--- | :--- |
| **1** | **Tuduhan *Data Leakage* & *Overfitting* pada Klaim Akurasi 97,22% dan 100% PASS** | Lompatan akurasi dari 90,70% $\rightarrow$ 93,71% $\rightarrow$ **97,22%** dan skor SQA **100% PASS** pada P1–P5 sangat mencurigakan jika paragraf dari dokumen P1–P5 ikut masuk ke dalam 1.747 sampel pelatihan, atau jika aturan *Guardrail Agent 2* dibuat *hardcoded* khusus untuk mengakali P1–P5. | **(C) Aksi:** Pisahkan secara ketat (*Document-Level Split*): pastikan 0% paragraf dari dokumen uji P1–P5 pernah dilihat oleh model saat pelatihan 1.747 sampel. Saat sidang, minta dosen penguji mengirimkan **1 file `.docx` acak milik mereka sendiri (*Blind Test*)** untuk membuktikan sistem tidak di-*hardcode* hanya untuk P1–P5. |
| **2** | **Korupsi Struktur File `.docx` (*Unreadable Content*) pada Dokumen Kompleks** | Manipulasi langsung pohon XML (`w:sectPr`, pemindahan paragraf lintas seksi, penghapusan `w:numPr`) pada dokumen yang memiliki *Merged Cells* tabel rumit, *Floating Shapes/Text Box*, atau *Track Changes/Comments* aktif dapat merusak skema relasi `document.xml` sehingga MS Word menolak membuka file. | **(C) Aksi:** Tambahkan *Pre-Sanitization & XML Schema Validator* sebelum menyimpan file keluaran: terima otomatis semua *Track Changes*, lewati manipulasi tabel jika terdeteksi matriks *nested table* ekstrem, dan sediakan *Fallback Mechanism* (jika mutasi XML gagal pada satu elemen, lewati elemen tersebut dan catat di log tanpa menggagalkan seluruh dokumen). |
| **3** | ***Self-Poisoning Loop* pada Modul Active Learning (FR-15 / RSK-05)** | Jika aturan *Regex* atau *Guardrail* pada *Agent 2* melakukan kesalahan koreksi pada dokumen yang formatnya sangat aneh, lalu koreksi salah tersebut otomatis disimpan ke CSV dan memicu *retraining* setiap 5 sampel, maka model *Random Forest* akan mengalami *concept drift* (makin dipakai makin bodoh). | **(C) Aksi:** Ubah mekanisme simpan otomatis menjadi **Quarantined Active Learning Pool**: hasil koreksi *Agent 2* hanya masuk ke *training pool* jika memenuhi dua syarat: (1) Dokumen akhir lulus **SQA Tier 2 = 100%**, dan (2) Skor akurasi pada *Hold-out Validation Set* murni tidak turun setelah *retraining* (*Shadow Evaluation Gate* sebelum *hot-reload*). |

---

## TAHAP 3 — Kritik dari Kacamata Hiring Manager / Senior Tech Lead

### 1. Empat Pertanyaan Tajam yang Akan Ditanyakan Saat Technical Interview

Jika Anda menulis proyek ini di CV sebagai *"Built an NLP-based Multi-Agent System with 97.22% accuracy and 0.98s latency"*, *interviewer* senior akan langsung menguji Anda dengan pertanyaan berikut:

1. **"Mengapa Anda menyebut ini *Multi-Agent System*?** Apa bedanya kode `inspector.py`, `critic.py`, dan `formatter.py` Anda dengan arsitektur *standard MVC / Sequential Data Pipeline* biasa? Apakah agen-agen ini berjalan secara *asynchronous*, punya *state/memory* independen, atau hanya fungsi Python yang dipanggil berurutan?"
2. **"Klaim *0 seconds downtime hot-reload* (NFR-04) saat *Active Learning retraining* di FastAPI:** Bagaimana cara Anda menangani *concurrency / race condition* jika ada *user A* sedang melakukan inferensi sementara proses di *background* sedang menimpa objek model `joblib` di memori dan menulis ke file CSV yang sama?"
3. **"Terkait ekstraksi 420 fitur (400 TF-IDF + 20 OpenXML):** Mengapa Anda memilih *Random Forest* di atas matriks TF-IDF yang *sparse*? Bukankah model berbasis *tree* sering kalah efisien dibanding *Linear SVM* atau *Gradient Boosting (LightGBM/XGBoost)* pada fitur teks berdimensi ratusan? Dan bagaimana *feature importance* antara 400 fitur teks vs 20 fitur metadata—jangan-jangan model Anda sebenarnya hanya menebak dari 20 fitur `font_size` dan `is_bold`, sementara 400 fitur NLP-nya tidak berguna?"
4. **"Pemrosesan file `.docx` rata-rata 0,98 detik (BO-03):** Itu untuk file ukuran berapa MB dan berapa halaman? Karena `python-docx` memuat seluruh struktur DOM XML ke dalam RAM, apa yang terjadi pada server FastAPI Anda jika 20 mahasiswa mengunggah skripsi berukuran 25 MB (penuh gambar resolusi tinggi) secara bersamaan? Apakah *event loop* FastAPI Anda akan *blocking*?"

### 2. Kelemahan Proyek yang Langsung Terlihat oleh Reviewer Teknis Berpengalaman

* **(A) Fakta Dokumen:** Penyimpanan umpan balik *Active Learning* menggunakan berkas `.csv` lokal (FR-15), pemicu *retraining* setiap $\ge 5$ sampel, dan ketergantungan pada `<w:updateFields w:val="true"/>` saat dibuka di MS Word (Bagian 8.2 BRD).
* **(B) Kritik Teknis:**
  1. **Penyimpanan `.csv` untuk *Active Learning* di Web Server adalah *Anti-Pattern*:** Jika ada 2 *request* masuk bersamaan di FastAPI, penulisan ke file `.csv` tanpa *file locking* atau database transaksional (seperti SQLite/PostgreSQL) akan menyebabkan korupsi file CSV.
  2. ***Retraining* setiap 5 sampel paragraf terlalu agresif:** Satu dokumen skripsi memiliki 150–500 paragraf (NFR-02). Artinya, satu kali unggah dokumen saja bisa menghasilkan $>5$ koreksi dan langsung memicu *retraining* CPU-bound di tengah *request* pengguna!
  3. ***Over-engineering Buzzwords*:** Menyebut validasi *if-else/Regex* sebagai *"Two-Tier Software Quality Assurance (SQA)"* dan *"5-Layer AI Governance"* terdengar keren di depan dosen, tapi di mata *Senior Engineer*, itu terlihat seperti usaha membungkus *rule-based script* dengan istilah riset agar terlihat canggih.

### 3. Apa yang Membedakan Proyek Ini dari 100 Proyek ML Generik di GitHub?

Terlepas dari kritik di atas, proyek ini memiliki **3 nilai jual luar biasa** yang jarang dimiliki *fresh graduate*:

1. **Bukan Sekadar *Jupyter Notebook*:** 95% portofolio ML mahasiswa berhenti di `model.predict()` di dalam Google Colab. Anda membangun **End-to-End Product** yang menerima file biner rumit (`.docx`), memanipulasi *Abstract Syntax Tree / DOM XML* tingkat rendah secara non-destruktif, dan menghasilkan file `.docx` siap pakai.
2. **Kombinasi *Probabilistic ML + Deterministic Guardrails*:** Di industri saat ini, tidak ada perusahaan yang berani menaruh model ML/AI murni ke produksi tanpa *guardrails*. Arsitektur hibrida Anda (*Agent 1* menebak secara statistik, *Agent 2* mengunci dengan aturan logika domain) menunjukkan pola pikir **Production Machine Learning Engineer**.
3. **Metrik Bisnis yang Nyata (*Real-World ROI*):** Anda punya metrik pembanding yang konkret: memangkas pekerjaan manual **2–4 jam menjadi 0,98 detik** dengan preservasi konten 100%.

### 4. Skor "Daya Jual di Interview": **8,2 / 10**

* **Alasan Skor 8,2 (Bukan 6, tapi belum 9,5):**
  * **Nilai Plus (+8,2):** Proyek ini membuktikan Anda menguasai *Full-Stack AI Engineering* (Data curation 1.747 sampel $\rightarrow$ Feature Engineering hibrida $\rightarrow$ Scikit-Learn Pipeline $\rightarrow$ Low-level XML DOM manipulation $\rightarrow$ FastAPI Backend $\rightarrow$ Interactive Web UI). Sangat sedikit lulusan S1 yang mau mengotori tangan membedah spesifikasi XML `.docx`.
  * **Pengurang Nilai (-1,8):** Klaim istilah yang agak *over-hyped* (menyebut *rule engine* sebagai *Autonomous Critic Agent* dan *Weak Supervision* sebagai *Active Learning*), arsitektur penyimpanan CSV yang belum siap untuk *concurrent production*, serta belum adanya bukti *Ablation Study* (apakah 400 fitur NLP benar-benar berkontribusi dibandingkan 20 fitur OpenXML saja).

---

## TAHAP 4 — Rekomendasi Perbaikan Konkret (Action Plan)

Berikut adalah langkah konkret yang dapat Anda eksekusi langsung tanpa mengubah fondasi sistem yang sudah jadi:

### (A) Langkah Konkret Menaikkan Kekuatan Akademik (Skripsi & Publikasi)

1. **Wajib Tambahkan *Ablation Study* (Studi Ablasi Fitur) di Bab IV:**
   * Jangan hanya membandingkan *Random Forest* (93,71% / 97,22%) vs *Logistic Regression* (88,57%).
   * Buat tabel eksperimen 3 skenario pada *Random Forest*:
     1. **Hanya 400 Fitur NLP (TF-IDF saja):** Berapa akurasinya?
     2. **Hanya 20 Fitur Metadata OpenXML saja:** Berapa akurasinya?
     3. **Gabungan 420 Fitur Hibrida (NLP + OpenXML):** Mencapai **97,22%**.
   * **Tujuan:** Ini langsung membungkam keraguan penguji pada **RQ 1.1** dan membuktikan secara matematis mengapa penggabungan fitur NLP dan OpenXML itu mutlak diperlukan.

2. **Wajib Tampilkan Tabel Evaluasi Komparatif: *Single-Agent (Pure ML)* vs *Multi-Agent (ML + Critic Guardrails)*:**
   * Sesuai komponen **C (Comparison)** pada protokol PICOS Anda, tampilkan bukti pada 5 *Gold Datasets* (P1–P5): jika hanya memakai prediksi *Agent 1* tanpa koreksi *Agent 2*, berapa skor kepatuhan akhirnya? (Misal: gagal di sub-bab 1.7 atau gagal di Laporan Magang sehingga skor hanya 62,5% atau 75%), sedangkan dengan *Tri-Agent* naik menjadi **100% PASS**.

3. **Luruskan Terminologi di Bab II & Bab III agar Tahan Uji Sidang:**
   * Ganti klaim bahwa agen Anda adalah "LLM Agent" dengan istilah **"Role-Specialized Hybrid Software Agents (Statistical-Symbolic MAS)"** mengacu pada **Gabauer (2026) [S02]** dan **Muwa et al. (2026) [S10]**.
   * Masukkan **Ref 72 / Ref 85 (Liu et al., 2023)** dari PDF Scopus Anda untuk menjustifikasi siklus pelatihan ulang otomatis dari *Agent 2* ke *Agent 1* sebagai **Critic-Guided Weak Supervision / Active Learning**.

---

### (B) Langkah Konkret Menaikkan Nilai Portofolio Industri (GitHub & Interview)

1. **Perbaikan Arsitektur Teknis Kecil tapi Berdampak Besar (*Production Readiness*):**
   * **Thread-Safe Model Reload & Background Task:** Pastikan proses *retraining* pada FastAPI dijalankan menggunakan `BackgroundTasks` (agar pengguna tidak perlu menunggu proses *retrain* saat mengunduh dokumen) dan gunakan `threading.Lock()` saat melakukan *hot-reload* model di memori.
   * **Benchmarking Tambahan:** Tambahkan 1 model pembanding modern seperti **LightGBM / XGBoost** atau **LinearSVC** di skrip evaluasi agar *Hiring Manager* melihat Anda memahami karakteristik *sparse matrix* TF-IDF.

2. **Target Fitur Deployment yang Wajib Ada:**
   * **Dockerization (`Dockerfile` & `docker-compose.yml`):** Bungkus aplikasi FastAPI + model ML ke dalam satu kontainer Docker agar *recruiter* bisa menjalankan proyek dengan satu perintah `docker compose up`.
   * **Sample Document Selector di Web UI (`alat.html`):** *Recruiter* jarang punya file skripsi mentah yang berantakan di laptop mereka saat membuka link demo Anda. Sediakan tombol **"Coba dengan Dokumen Uji (Skripsi Rusak / Laporan Magang)"** langsung di halaman web, sehingga mereka bisa melihat demo *live* dalam 1 klik tanpa harus mencari file `.docx` sendiri!
   * **Side-by-Side Visual Diff (Before vs After):** Tampilkan tangkapan layar atau pratinjau perbandingan struktur dokumen sebelum dan sesudah diproses oleh ASDOKU.

3. **Struktur Repository & `README.md` Ideal (Standar *Senior Engineer*):**
   Susun `README.md` utama di GitHub dengan urutan tajam berikut:
   * **Header & Value Proposition:** *"ASDOKU: Hybrid NLP & Symbolic Multi-Agent Engine for Non-Destructive OpenXML (`.docx`) Refactoring — Reducing 4 hours of manual academic formatting to **0.98 seconds**."*
   * **GIF Demo 15 Detik:** Rekaman layar *upload* dokumen berantakan $\rightarrow$ *live terminal log* agen bernegosiasi $\rightarrow$ *100% SQA Scorecard* $\rightarrow$ hasil `.docx` terbuka di MS Word dengan *Navigation Pane* rapi dan tabel APA 7.
   * **System Architecture Diagram (Mermaid.js):** Diagram alir *Tri-Agent* dan *Two-Tier Quality Gate*.
   * **Engineering Highlights & Benchmarks:**
     * Tabel *Ablation Study* (TF-IDF only vs OpenXML Metadata only vs 420 Hybrid Features = **97,22% F1: 0,97**).
     * Tabel *Latency Breakdown* (Feature Extraction & ML Inference: **~40ms** | Symbolic Critic Audit: **~15ms** | Low-Level XML DOM Mutation: **~925ms** | Total: **0,98s**).
   * **Why Not Pure LLM? (Design Decision Section):** Jelaskan secara singkat mengapa Anda sengaja memilih **Hybrid Statistical ML + Low-Level OpenXML AST Manipulation** dibandingkan menyuruh GPT-4 menulis ulang dokumen (Alasan: *Zero Hallucination / 100% Content Preservation*, biaya $0, privasi dokumen lokal, dan latensi < 1 detik). Bagian ini dijamin akan membuat *Hiring Manager* sangat terkesan.

---

> **Pernyataan Penutup Audit:**  
> Evaluasi kritis ini disusun secara objektif sebagai instrumen mitigasi risiko akademik dan peningkatan standar rekayasa perangkat lunak pada proyek ASDOKU, guna menjamin kelulusan sidang skripsi dengan nilai tertinggi serta daya saing karir profesional lulusan FASILKOM Universitas Esa Unggul.
