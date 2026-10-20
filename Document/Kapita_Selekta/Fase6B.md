# FASE 6B: AUDIT KRITIS, EVALUASI KELAYAKAN, DAN RENCANA AKSI (ACTION PLAN)
## Tinjauan Kritis Arsitektur Multi-Agent System & Evaluasi Kelayakan dari Sudut Pandang Pembimbing Skripsi dan Senior Tech Lead (ASDOKU)

> **Kode Dokumen:** `AUDIT-ASDOKU-2026-F6B`  
> **Mata Kuliah:** Kapita Selekta  
> **Program Studi / Institusi:** Teknik Informatika, Fakultas Ilmu Komputer (FASILKOM) — Universitas Esa Unggul  
> **Penyusun:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Dosen Pengampu / Pembimbing:** Dosen Kapita Selekta FASILKOM UEU  
> **Regulasi Acuan:** SK Rektor Universitas Esa Unggul No. 5 Tahun 2018 (Pedoman Penulisan Skripsi & Tugas Akhir)  
> **Dokumen Rujukan Terkait:** [BRD.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/BRD.md), [SLR.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/SLR.md), dan [Fase6A.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase6A.md)  
> **Tanggal Penyusunan:** 21 Oktober 2026  
> **Status Dokumen:** Final (Fase 6B)

---

Berikut adalah audit kritis dan evaluasi tanpa kompromi terhadap dokumen **BRD**, **SLR**, serta judul/arsitektur proyek **ASDOKU** Anda, dijalankan secara simultan dari dua sudut pandang: **Dosen Pembimbing Skripsi yang Skeptis (Peran 1)** dan **Senior Tech Lead / Hiring Manager (Peran 2)**.

---

## TAHAP 1 — Audit Kesesuaian BRD × SLR (Deteksi Klaim yang "Dipaksakan")

Sebagai dosen pembimbing dan *reviewer* teknis, dilakukan audit menyeluruh apakah setiap *Business Objective* (BO) dan *Functional Requirement* (FR) di BRD benar-benar memiliki pijakan ilmiah di SLR, atau sekadar *buzzword* yang ditempelkan agar terdengar canggih:

| Elemen BRD | (A) Fakta dari Dokumen BRD & SLR | (B) Kritik & Interpretasi (Peran 1 & Peran 2) | Status Audit |
| :--- | :--- | :--- | :---: |
| **Judul & Arsitektur: "Multi-Agent System (MAS)"**<br/>(FR-03, FR-05, FR-08, FR-09 vs Klaster P07, P08 di SLR) | **Fakta:** BRD mendefinisikan 3 agen (`inspector.py`, `critic.py`, `formatter.py`) yang saling bertukar *Draft Blueprint* dan *Approved Blueprint*. SLR mengutip literatur *Collaborative Multi-Agent System* (P07) dan *Verifier-Critic Loop* (P08). | **Kritik Keras:** Dalam teori Ilmu Komputer (Wooldridge / Russell & Norvig), *Multi-Agent System* mensyaratkan otonomi, komunikasi asinkron/negosiasi, dan observasi lingkungan. Di kode Anda, apakah ketiga file Python tersebut benar-benar bernegosiasi sebagai *autonomous agents*, atau **sebenarnya hanya pemanggilan fungsi sekuensial biasa (*Sequential Pipeline*: `fungsi_A() -> fungsi_B() -> fungsi_C()`) yang dibungkus *class* bernama `Agent`?** Pada FR-08 disebutkan *"Agent 1 melakukan re-inspeksi adaptif berdasarkan Feedback Directives dari Agent 2"*. Jika model Anda adalah *Random Forest* statis (`baseline_model.joblib`), bagaimana cara *Random Forest* mengubah prediksinya saat "ditegur" *Agent 2* tanpa mengubah fitur inputnya? Jika *Agent 2* langsung menimpa (*override*) label menggunakan `if-else` / *regex*, maka tidak ada negosiasi agen—itu murni *Rule-Based Post-Processing*. | ⚠️ **TERLIHAT DIPAKSAKAN**<br/>*(Kecuali Anda bisa membuktikan mekanisme re-inspeksi probabilistik di kode `inspector.py` ↔ `critic.py`)* |
| **Judul & Metode: "Berbasis Natural Language Processing (NLP)"**<br/>(BO-01, FR-02 vs Klaster P02, P03 di SLR) | **Fakta:** BRD dan dokumentasi menyebut penggunaan 400 fitur *TF-IDF N-Gram (1,2)* + 20 fitur metadata *OpenXML* dengan algoritma *Random Forest*. | **Kritik Keras:** Di tahun 2026, mengklaim "Berbasis NLP" di judul utama hanya dengan bermodalkan *TF-IDF* akan langsung diserang saat sidang. *TF-IDF* adalah representasi statistik frekuensi kata (*Bag-of-Words*), bukan pemrosesan semantik bahasa alami tingkat lanjut. Lebih jauh lagi, dalam deteksi struktur `.docx`, 20 fitur *OpenXML* (`font_size`, `is_bold`, `align`, `doc_pos`) kemungkinan besar menyumbang *feature importance* jauh lebih besar daripada 400 fitur *TF-IDF*. Jika *Random Forest* Anda tetap akurat 90%+ meski *TF-IDF*-nya dihapus, maka klaim "Berbasis NLP" di judul adalah *overclaiming*. | ⚠️ **RAWAN DISERANG DI SIDANG**<br/>*(Perlu bukti Ablation Study)* |
| **BO-04 & FR-15: "Active Learning & Continuous Retraining Loop"**<br/>(vs Klaster P09 di SLR) | **Fakta:** BRD menyatakan setiap koreksi *Agent 2* disimpan ke `active_learning_feedback.csv`, dan jika mencapai $\ge 5$ sampel, sistem memicu *retraining* otomatis dan *hot-reload* model. SLR (P09) membahas *Active Learning* berbasis *Human-in-the-Loop*. | **Kritik Keras:** Ini adalah **gap konseptual paling berbahaya** di sistem Anda. Dalam teori *Machine Learning*, *Active Learning* membutuhkan **Oracle** (sumber kebenaran mutlak, biasanya anotator manusia) untuk melabeli data ambigu. Di sistem Anda, yang menjadi "Oracle" pemberi label koreksi adalah *Agent 2* (yang berisi aturan heuristik/*regex*). Jika model *Random Forest* (*Agent 1*) dilatih ulang menggunakan output dari aturan `if-else` *Agent 2*, maka: **(1)** Model ML Anda hanya sedang menduplikasi aturan `if-else` *Agent 2* (*knowledge distillation* dari heuristik, bukan *Active Learning* sejati), dan **(2)** Jika aturan *Agent 2* salah memvalidasi satu dokumen aneh (*false positive*), kesalahan itu masuk ke CSV, dilatih ulang setiap 5 sampel, dan **meracuni model utama secara permanen (*Model Poisoning / Concept Drift*)**. | 🚨 **SANGAT DIPAKSAKAN & BERISIKO TINGGI** |
| **BO-02, FR-06, FR-10 s/d FR-14: "Two-Tier SQA & Rekonstruksi OpenXML"**<br/>(vs Klaster P01, P10, P12, P15 di SLR) | **Fakta:** BRD merinci *Guardrail* sub-bab 1.7, deteksi bab Laporan Magang, pembagian 3 *Section*, *Dual Page Numbering*, *Dynamic TOC*, tabel APA 7, dan audit 8 kriteria UEU dengan skor 100% PASS pada 5 dokumen uji (P1–P5). | **Kritik & Apresiasi:** Bagian inilah yang **100% SOLID, NYATA, dan TIDAK DIPAKSAKAN**. SLR (P01, P15) memang membuktikan riset terdahulu rata-rata hanya *checker-only* (melaporkan salah, tidak memperbaiki) atau gagal menangani *section break* Romawi–Latin dan tabel APA 7 secara otomatis. Keberhasilan kode `formatter.py` (2.684 baris) membedah DOM XML secara non-destruktif dan divalidasi oleh `critic.py` adalah kekuatan teknis sesungguhnya dari proyek ini. | ✅ **VALID & SANGAT KUAT** |
| **Data Extraction Form SLR (P01–P15)** | **Fakta:** Seluruh 15 baris referensi di draf awal SLR sempat berupa klaster tematik berlabel `[PERLU VERIFIKASI DI MENDELEY]` dan metrik di BRD sempat bertanda `[ISI DATA]`. | **Kritik Dosen Pembimbing:** Secara struktur PRISMA sudah rapi, tetapi di mata penguji, SLR dengan sitasi *placeholder* adalah **nol besar** sampai Anda benar-benar mengisi nama penulis, tahun, judul asli, dan DOI yang valid dari Scopus/Mendeley. Jangan pernah maju seminar/sidang dengan *placeholder* yang belum terisi. *(Catatan: Telah diselesaikan secara tuntas pada dokumen SLR.md final).* | ⚠️ **BELUM VALID SECARA EMPIRIS (SEBELUMNYA)**<br/>&rarr; ✅ **SUDAH DIVERIFIKASI DI SLR.md** |

---

## TAHAP 2 — Kritik Kelayakan Brutal (Kacamata Dosen Pembimbing Skeptis)

### 1. Apakah topik ini realistis diselesaikan mahasiswa S1 dalam 1 semester dengan skill rata-rata?

* **(A) Fakta:** Workspace Anda menunjukkan sistem sudah berjalan (`app.py`, `inspector.py`, `critic.py`, `formatter.py` 2.684 baris, 7 dataset, 5 dokumen uji emas).
* **(B) Kritik:** Jika dikerjakan dari nol dengan *coding* manual oleh mahasiswa S1 rata-rata dalam 1 semester, **TIDAK REALISTIS**. Manipulasi *low-level OpenXML* (`w:sectPr`, `w:fldSimple`, `w:tblBorders`, `w:numPr`) adalah mimpi buruk bahkan bagi *developer* berpengalaman. Namun, karena Anda membangunnya menggunakan *vibe coding* (di Antigravity) dan prototipenya sudah jadi, tantangan Anda bukan lagi "apakah selesai dibuat?", melainkan **"apakah Anda benar-benar paham setiap baris kode XML dan matematika ML yang dihasilkan AI saat dicecar dosen penguji?"** Jika dosen meminta Anda menjelaskan cara kerja tag `<w:outlineLvl>` atau bagaimana `feature_pipeline.joblib` menggabungkan matriks *sparse* TF-IDF dengan 20 fitur numerik, dan Anda gagap, penguji akan tahu Anda tidak menguasai kode Anda sendiri.

---

### 2. Apakah ini termasuk topik "generik/klise" tanpa nilai tambah baru?

* **(B) Kritik:** Topik *"Sistem Pengecek Format Skripsi"* adalah topik **klise tahunan** di banyak kampus ilmu komputer. **TETAPI**, proyek ASDOKU Anda **berhasil keluar dari jebakan klise tersebut** karena tiga hal:
  1. Anda melakukan **rekonstruksi penuh (*auto-formatting*)** hingga ke level *3-section page numbering* dan tabel APA 7, bukan sekadar pemeriksa (*checker*);
  2. Anda menangani kasus nyata yang sangat spesifik (konflik sub-bab 1.7 Sistematika Penulisan dan variasi bab Laporan Magang MBKM); dan
  3. Anda memiliki mekanisme *Artifact Acceptance Gate* (SQA Tier 2).

---

### 3. Apakah dataset yang dibutuhkan benar-benar bisa didapat secara legal & etis?

* **(A) Fakta:** Dokumen ringkasan Anda mencantumkan nama lengkap dan NIM mahasiswa asli pada dokumen uji emas: `P2_Skripsi_Mbkm_Dhicky.docx (Dhicky Haryadi - 20230801195)`, `P3_Proposal_Bab1_3_PBB (Nanda Anisya)`, dan `P4_Laporan_Mbkm_Arditya.docx (Arditya Adjie - 20230801274)`.
* **(B) Kritik Etika Penelitian:** **HATI-HATI!** Mencantumkan nama lengkap, NIM, dan menyebarkan berkas skripsi/laporan magang mahasiswa lain di repositori publik atau naskah tanpa izin tertulis (*informed consent*) atau tanpa proses anonimisasi (*data masking*) adalah **pelanggaran etika penelitian dan privasi data pribadi**.

---

### 4. Tiga Skenario Kegagalan Paling Mungkin Terjadi & Mitigasinya

#### 1. Skenario Kegagalan 1: *Illusion of 100% PASS* pada *SQA Tier 2* (Bias Evaluasi Sirkular)
* **Masalah:** *Agent 3* memformat margin menjadi 4-3-3-3 cm di XML, lalu *Agent 2* memeriksa atribut XML yang baru saja ditulis oleh *Agent 3* dan memberi nilai **100.0% PASS**. Penguji akan berkata: *"Tentu saja 100% PASS, orang yang menulis dan yang memeriksa menggunakan aturan kode yang sama! Bagaimana jika di XML tertulis benar, tapi saat dibuka di MS Word tampilannya tetap berantakan?"*
* **Mitigasi:** Tambahkan validasi visual/manual oleh manusia (*Ground Truth Human Audit*) pada tabel evaluasi Bab 4 untuk membuktikan bahwa skor 100% dari *Agent 2* memang terkonfirmasi 100% rapi saat dibuka secara visual di aplikasi Microsoft Word.

#### 2. Skenario Kegagalan 2: *Data Leakage* & Keraguan pada Dataset Sintetis (`generate_7_datasets.py`)
* **Masalah:** Terdapat file `generate_7_datasets.py` dan `build_pure_training_data.py` untuk menghasilkan 1.747 sampel. Jika sebagian besar dari 1.747 baris tersebut dibangkitkan secara programatik (sintetis) dengan pola template yang seragam, lalu diuji dengan *train-test split* acak, akurasi 93,71% atau 97,22% itu rawan dicurigai *overfitting* dan tidak valid untuk dokumen dunia nyata.
* **Mitigasi:** Pisahkan secara tegas di Bab 3 dan Bab 4 berapa proporsi paragraf yang diekstrak dari dokumen mahasiswa asli vs augmentasi/sintetis, dan gunakan *Document-Level Split* (dokumen P1–P5 sama sekali tidak boleh masuk ke dataset saat pelatihan model).

#### 3. Skenario Kegagalan 3: Kegagalan *Edge-Case* Struktur Dokumen Kompleks (Tabel Bersarang, Gambar *Floating*, & *Landscape* Tengah Bab)
* **Masalah:** Saat demonstrasi *live* di depan penguji, dosen mengunggah file `.docx` yang memiliki *merged cells* kompleks, gambar berformat *Wrap Text: In Front of Text*, atau halaman *Landscape* yang diapit halaman *Portrait*. Manipulasi DOM di `formatter.py` bisa merusak urutan elemen atau menyebabkan *file corrupt*.
* **Mitigasi:** Pasang blok `try-except` granular pada tingkat elemen XML di `formatter.py` (jika satu tabel gagal diformat ke APA 7 karena *nested table*, lewati tabel tersebut tanpa menggagalkan seluruh dokumen) dan nyatakan batasan objek *floating* secara eksplisit di Batasan Masalah.

---

## TAHAP 3 — Kritik dari Kacamata Hiring Manager / Senior Tech Lead

### 1. Pertanyaan Tajam yang Akan Ditanyakan di Interview Kerja

Jika Anda menaruh proyek **ASDOKU** di CV dan melamar sebagai *AI/ML Engineer* atau *Backend Engineer*, *interviewer* senior akan langsung menembak Anda dengan 4 pertanyaan ini:

1. *"Di arsitektur kamu ada Random Forest 420 fitur dan ada Quality Critic berisi 5 Guardrails berbasis Regex. Jujur ke saya: kalau Random Forest-nya saya matikan total dan saya cuma pakai Regex + pemeriksaan properti OpenXML di Critic, akurasi sistemnya turun berapa persen? Kenapa harus pakai ML?"*
2. *"Kamu menulis sistem ini melakukan `Continuous Retraining` dan `Hot-Reload` model di FastAPI setiap kali ada $\ge 5$ koreksi baru di CSV. Bagaimana kamu menangani **Concurrency / Race Condition** kalau ada 10 mahasiswa mengunggah file bersamaan saat proses `train.py` sedang menulis ulang `baseline_model.joblib` di disk?"*
3. *"File `formatter.py` kamu ukurannya **2.684 baris kode** dalam satu file. Kalau ada bug pada penomoran halaman Romawi di Section 1, bagaimana cara kamu melakukan unit testing tanpa harus menjalankan seluruh pipeline? Kenapa kamu membuat God Object / Monolithic Script sepanjang itu?"*
4. *"Kamu memanipulasi XML `.docx` menggunakan `python-docx` di memori. Berapa konsumsi RAM jika pengguna mengunggah skripsi setebal 150 halaman yang berisi 50 gambar resolusi tinggi (ukuran file 80 MB)? Apakah FastAPI kamu akan terkena Out-Of-Memory (OOM)?"*

---

### 2. Kelemahan Project yang Langsung Terlihat oleh Reviewer Teknis Berpengalaman

* **God File Anti-Pattern (`formatter.py` = 2.684 baris):** Bagi *Senior Engineer*, satu file Python berisi 2.600+ baris kode adalah tanda kurangnya pemahaman *Modular Software Design / Clean Architecture* (tanda kode hasil penumpukan berulang tanpa *refactoring* modular).
* **Path Hardcoding & Lingkungan Deployment:** Sempat ada path absolut lokal yang menunjukkan proyek dijalankan langsung sebagai `root` tanpa kontainerisasi (*Docker*) dan pemisahan konfigurasi *environment*.
* **Ketidakjelasan Kontribusi ML vs Rule-Based:** Arsitektur tampak mencampuradukkan logika deterministik (`critic.py`) yang sangat dominan untuk menutupi kelemahan model ML (`inspector.py`), sehingga batas antara kecerdasan model dan *hardcoded rules* menjadi kabur.

---

### 3. Apa yang Membedakan Project Ini dari 100 Project Generik Lain di GitHub?

Harus diakui secara objektif: **Proyek ini JAUH LEBIH MENARIK daripada 95% portofolio *fresh graduate* lainnya** (yang biasanya hanya berisi *Analisis Sentimen Twitter*, *Prediksi Harga Rumah*, atau *CRUD Laravel biasa*).
Keunggulan pembeda Anda adalah:

1. **Menyelesaikan Masalah Dunia Nyata yang Nyata-nyata Sulit (*Hard Engineering Problem*):** Memanipulasi pohon OpenXML untuk membuat *multi-section page numbering* dan *dynamic TOC* secara terprogram membutuhkan pemahaman struktur data tingkat rendah.
2. **End-to-End Product Delivery:** Anda tidak berhenti di file `.ipynb` (*Jupyter Notebook*), melainkan membungkusnya menjadi aplikasi web utuh (*FastAPI*) dengan UI yang sangat niat (*Notion-style Warm Minimalist*), *live console log*, dan *artifact download*.
3. **Konsep Self-Verification (Two-Tier SQA):** Pola arsitektur *Predictor $\rightarrow$ Critic/Gatekeeper $\rightarrow$ Actuator $\rightarrow$ Acceptance Test* sangat relevan dengan tren industri *Agentic AI Workflows* saat ini.

---

### 4. Skor "Daya Jual di Interview": **7,8 / 10**

* **Alasan Skor 7,8:** Anda mendapat poin tinggi karena produknya nyata, cepat ($< 1,5$ detik), menyelesaikan masalah riil, dan punya antarmuka yang bagus. Namun, Anda kehilangan **2,2 poin** karena:
  1. *Code smell* pada file `formatter.py` 2.684 baris,
  2. Celah logika pada klaim *Active Learning* tanpa validasi manusia yang bisa dianggap cacat desain oleh *Senior ML Engineer*, dan
  3. Belum adanya bukti pengujian beban/*ablation study* yang memisahkan kontribusi ML vs *Regex*.

---

## TAHAP 4 — Rekomendasi Perbaikan Konkret (Action Plan)

Berikut adalah langkah aksi konkret—dipisahkan antara penguatan akademik (untuk lulus sidang dengan nilai A) dan pemolesan portofolio industri (untuk menembus *technical interview*):

### (a) Langkah Konkret Menaikkan Kekuatan Akademik (Sidang & Naskah Skripsi)

1. **Lakukan *Ablation Study* (Wajib Masuk Bab 4 untuk Mempertahankan Judul):**  
   Jangan hanya membandingkan *Random Forest* vs *Logistic Regression*. Buat satu tabel eksperimen tambahan di Bab 4 yang membandingkan **4 Skenario**:
   * **Skenario 1 (Pure NLP - Hanya 400 TF-IDF):** Berapa F1-Score-nya?
   * **Skenario 2 (Pure OpenXML - Hanya 20 Fitur Metadata):** Berapa F1-Score-nya?
   * **Skenario 3 (Hybrid 420 Fitur - Hanya Agent 1 / Tanpa Agent 2 Critic):** Berapa error struktur yang lolos di 5 dokumen uji?
   * **Skenario 4 (Full ASDOKU Tri-Agent + Two-Tier SQA):** Skor akhir (97,22% & 100% PASS).  
   * *Dampak:* Tabel ini akan membungkam penguji yang mempertanyakan *"Kenapa harus pakai NLP + OpenXML?"* dan *"Kenapa harus pakai Multi-Agent?"* secara tak terbantahkan.

2. **Koreksi Terminologi *Active Learning* menjadi *Critic-Guided Self-Training (Pseudo-Labeling)*:**  
   Di Bab 3, jelaskan secara jujur bahwa mekanisme umpan balik dari *Agent 2* ke `active_learning_feedback.csv` adalah skema **Automated Heuristic-Guided Pseudo-Labeling / Self-Training** (di mana aturan deterministik *Critic* bertindak sebagai *Automated Oracle* untuk kasus yang melanggar aturan baku seperti urutan bab). Tambahkan mekanisme filter keamanan: sampel hanya disimpan ke CSV jika *Agent 2* memiliki kepastian aturan 100% (misal: pelanggaran urutan bab monotonik).

3. **Buktikan Negosiasi Antar-Agen pada *SQA Tier 1*:**  
   Pastikan di kode dan di penjelasan Bab 3, ketika *Agent 2* mengirim *Feedback Directives* ke *Agent 1*, *Agent 1* tidak sekadar ditimpa paksa, melainkan melakukan **penyesuaian distribusi probabilitas bersyarat (*Contextual Probability Re-weighting*)** berdasarkan posisi zona dokumen sebelum mengeluarkan *Re-inspected Blueprint*.

4. **Anonimisasi Dokumen Uji & Lengkapi Sitasi Mendeley:**  
   Samarkan nama dan NIM mahasiswa pada laporan tabel Bab 4 (misal: `Dokumen P2 - Skripsi Mahasiswa A [NIM Disamarkan]`) dan pastikan seluruh sitasi di SLR serta BRD konsisten menggunakan angka empiris riil (`97,22%`, `1.747 sampel`, `420 fitur`, `0,98 detik`).

---

### (b) Langkah Konkret Menaikkan Nilai Portofolio Kerja (GitHub & CV)

1. **Refactoring `formatter.py` (2.684 Baris) Menjadi Paket Modular:**  
   Pecah file raksasa `src/agents/formatter.py` menjadi sub-modul yang bersih di bawah `src/agents/formatter/`:
   * `cover_builder.py` (Khusus rekonstruksi sampul & logo)
   * `section_manager.py` (Khusus pembagian 3 *section* & *dual page numbering*)
   * `toc_generator.py` (Khusus *Dynamic TOC* & `<w:outlineLvl>`)
   * `table_stylist.py` (Khusus standarisasi tabel APA 7)
   * `xml_sanitizer.py` (Khusus pembersihan `<w:numPr>` dan *styles* rusak)  
   * *Dampak:* Saat *Tech Lead* membuka repositori GitHub Anda, mereka akan melihat struktur kode berstandar produksi (*Clean Code & Single Responsibility Principle*).

2. **Target Metrik & Benchmark yang Harus Ditampilkan di README.md:**  
   * **Throughput & Memory Footprint:** Cantumkan tabel *benchmark* yang menguji waktu proses (ms) dan puncak penggunaan RAM (MB) untuk dokumen berukuran 10 halaman, 50 halaman, dan 100+ halaman.
   * **Before-and-After Error Reduction:** Tampilkan metrik: *"Menurunkan rata-rata cacat format dari 42 defect/dokumen menjadi 0 defect/dokumen dalam rata-rata 0,98 detik."*

3. **Standar Deployment & Struktur Repositori Ideal:**  
   * Tambahkan `Dockerfile` dan `docker-compose.yml` agar *reviewer* bisa menjalankan aplikasi hanya dengan satu perintah `docker compose up`.
   * Gunakan `threading.Lock()` atau *background task queue* (`FastAPI BackgroundTasks`) pada proses *retraining* & *hot-reload* `baseline_model.joblib` agar bebas dari *race condition*.
   * Buat **GIF Demo 15 Detik** di bagian paling atas `README.md` yang memperlihatkan layar terbelah (*split-screen*): sebelah kiri dokumen Word mentah yang berantakan (tanpa Navigation Pane, tabel bergaris vertikal), lalu diunggah ke web ASDOKU, dan sebelah kanan dokumen hasil yang terbuka di MS Word dengan *Navigation Pane* lengkap dan format sempurna. Ini akan menaikkan skor daya jual portofolio Anda dari **7,8 menjadi 9,5/10**.

---

> **Pernyataan Penutup Audit:**  
> Evaluasi kritis ini disusun secara objektif sebagai instrumen mitigasi risiko akademik dan peningkatan standar rekayasa perangkat lunak pada proyek ASDOKU, guna menjamin kelulusan sidang skripsi dengan nilai tertinggi serta daya saing karir profesional lulusan FASILKOM Universitas Esa Unggul.
