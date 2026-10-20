# FASE 6A: ANALISIS KESENJANGAN (GAP ANALYSIS), EVALUASI KANDIDAT GAP, DAN PERUMUSAN JUDUL TUGAS AKHIR
## Sistem Otomatisasi Deteksi Struktur dan Formatting Dokumen Akademik Berbasis Multi-Agent System & Natural Language Processing (ASDOKU)

> **Kode Dokumen:** `GAP-ASDOKU-2026-F6A`  
> **Mata Kuliah:** Kapita Selekta  
> **Program Studi / Institusi:** Teknik Informatika, Fakultas Ilmu Komputer (FASILKOM) — Universitas Esa Unggul  
> **Penyusun:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Dosen Pengampu / Pembimbing:** Dosen Kapita Selekta FASILKOM UEU  
> **Regulasi Acuan:** SK Rektor Universitas Esa Unggul No. 5 Tahun 2018 (Pedoman Penulisan Skripsi & Tugas Akhir)  
> **Dokumen Rujukan Terkait:** [BRD.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/BRD.md), [SLR.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/SLR.md), dan [PICOS-RQ.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/PICOS-RQ.md)  
> **Tanggal Penyusunan:** 21 Oktober 2026  
> **Status Dokumen:** Final (Fase 6A)

---

Berikut adalah analisis kesenjangan (*Gap Analysis*), evaluasi kandidat gap, perumusan judul, dan analisis final berdasarkan dokumen **BRD** dan **SLR** dari proyek **ASDOKU** yang telah disusun sebelumnya:

---

## TAHAP 1 — Matriks Silang FR × SLR (Functional Requirements vs Literatur SLR)

Matriks berikut memetakan seluruh ke-16 Functional Requirements (FR-01 s/d FR-16 dari BRD) ke dalam status pemenuhannya berdasarkan studi literatur primer (P01–P15 dari SLR):

| ID FR (BRD) | Deskripsi Fungsional Singkat | Temuan Literatur Eksisting di SLR (P01–P15) | Status Penilaian |
| :---: | :--- | :--- | :---: |
| **FR-01** | Unggah berkas masukan `.docx` | Didukung oleh sebagian besar sistem pengolah dokumen berbasis web (P01, P04, P15). | **TERPENUHI** |
| **FR-02** | Ekstraksi fitur hibrida (TF-IDF + OpenXML) | Didukung oleh literatur klasifikasi teks dan struktur dokumen berbasis hibrida (P02, P03, P11). | **TERPENUHI** |
| **FR-03** | Klasifikasi paragraf & *Draft Blueprint* | Didukung oleh studi klasifikasi Machine Learning (P02, P03, P14). | **TERPENUHI** |
| **FR-04** | Penandaan ambiguitas (*confidence threshold*) | Literatur umum menggunakan *Uncertainty Sampling* (P09), namun belum terintegrasi otomatis dengan verifikasi agen. | **SEBAGIAN** |
| **FR-05** | Audit urutan bab monotonik & pola *Regex* | Diangkat secara parsial oleh aturan heuristik statis (P01, P04), namun rentan terhadap variasi naskah non-skripsi. | **SEBAGIAN** |
| **FR-06** | Isolasi zona sub-bab Sistematika Penulisan | **Belum ditemukan** literatur yang secara khusus membahas filter pencegahan *false positive* pada sub-bab Sistematika Penulisan (1.7). | **BELUM ADA** *(Kandidat Gap)* |
| **FR-07** | Filter rumus, persamaan, dan caption tabel/gambar | Dibahas secara terpisah pada ekstraksi tabel (P10) dan disambiguasi teks (P11), namun belum terintegrasi dalam audit agen. | **SEBAGIAN** |
| **FR-08** | Siklus negosiasi *SQA Tier 1* (Inspector & Critic) | Arsitektur *Multi-Agent System* dibahas di P07 & P08, namun penerapan spesifik untuk verifikasi hierarki dokumen akademik belum ada. | **SEBAGIAN** |
| **FR-09** | Sanitasi template & rekonstruksi sampul resmi | Dilakukan via skrip monolitik kaku pada literatur konvensional (P04) tanpa validasi agen. | **SEBAGIAN** |
| **FR-10** | Pembagian 3 seksi & *Dual Page Numbering* | Dilakukan secara manual atau via skrip dasar (P12), belum terhubung dengan hasil klasifikasi NLP. | **SEBAGIAN** |
| **FR-11** | Penyuntikan *Heading 1–3* & *Navigation Pane* | Dibahas di P12, namun tanpa pengawasan kualitas otomatis terhadap potensi *double numbering*. | **SEBAGIAN** |
| **FR-12** | Pembuatan *Dynamic Table of Contents (TOC)* | Didukung secara algoritmik di P12, namun terpisah dari pipeline agen penjamin mutu. | **SEBAGIAN** |
| **FR-13** | Standarisasi tabel ke format *APA 7th Edition* | **Belum ditemukan** literatur yang mengotomatisasi pembersihan border vertikal tabel `.docx` secara algoritmik terintegrasi agen. | **BELUM ADA** *(Kandidat Gap)* |
| **FR-14** | Audit berkas fisik *SQA Tier 2* (8 Kriteria UEU) | Literatur pada umumnya bersifat *checker-only* (P01, P15) tanpa mekanisme *Artifact Acceptance Quality Gate* dan auto-remediasi. | **BELUM ADA** *(Kandidat Gap)* |
| **FR-15** | *Active Learning Module* (Umpan balik & *Hot-Reload*) | Literatur *Active Learning* (P09) masih berbasis pelabelan manual oleh manusia (*Human-in-the-Loop*), belum diotomatisasi oleh agen penilai. | **BELUM ADA** *(Kandidat Gap)* |
| **FR-16** | Antarmuka web interaktif (MPA, log, skor SQA) | Diadopsi secara umum pada aplikasi web (P15), namun spesifik antarmuka multi-agen belum banyak dieksplorasi. | **SEBAGIAN** |

---

## TAHAP 2 — Skoring Kandidat Gap

Berdasarkan hasil pemetaan baris "BELUM ADA" pada Matriks Silang FR × SLR di atas, berikut adalah evaluasi dan skoring terhadap 3 kandidat gap terkuat:

| Kandidat Gap | Jenis Gap | Novelty (1-10) | Kelayakan (1-10) | Dampak (1-10) | Total Skor |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gap 1: Isolasi Zona Sistematika Penulisan & guardrail anomali struktur (FR-06)** | Metodologis & Kontekstual | 8 | 9 | 8 | **25** |
| **Gap 2: Mekanisme Two-Tier SQA terintegrasi Artifact Acceptance Gate (FR-14)** | Metodologis & Performa | 9 | 8 | 9 | **26** |
| **Gap 3: Active Learning Loop otomatis berbasis koreksi Quality Critic Agent (FR-15)** | Metodologis & Arsitektural | 9 | 7 | 8 | **24** |

### Justifikasi Gap Pemenang:

**Gap 2 (Mekanisme Two-Tier SQA terintegrasi Artifact Acceptance Gate — FR-14)** terpilih sebagai **Gap Pemenang** dengan total skor tertinggi (**26**).

* **Alasan:** Berdasarkan tinjauan SLR, literatur terdahulu (seperti P01 dan P15) umumnya berhenti pada tahap *checker-only* (hanya melaporkan kesalahan format tanpa memperbaiki). Dengan mengintegrasikan *Two-Tier SQA* (auditing hierarki pada Tier 1 dan validasi fisik 8 kriteria mutu UEU pada Tier 2), sistem tidak hanya mendeteksi melainkan secara otonom memastikan dokumen akhir lulus standar regulasi tanpa intervensi manual tambahan. *Novelty* ini menawarkan kontribusi kebaruan arsitektural yang sangat kuat untuk bidang *Document Engineering*.

---

## TAHAP 3 — 5 Rekomendasi Judul Tugas Akhir

Berdasarkan gap pemenang di atas dan arah riset resmi, berikut adalah 5 rekomendasi judul yang disusun secara spesifik, terstruktur, dan tidak klise:

| No | Kandidat Judul Tugas Akhir | Daya Tarik (1-10) | Novelty (1-10) | Kelayakan (1-10) | Total Skor |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Rancang Bangun Multi-Agent System dengan Mekanisme Two-Tier SQA untuk Otomatisasi Deteksi dan Formatting Dokumen Akademik Berbasis NLP** | **9** | **9** | **9** | **27** |
| **2** | Arsitektur Tri-Agent Berbasis Hybrid Features dan Quality Assurance untuk Rekonstruksi Dokumen Akademik Non-Destruktif | 8 | 9 | 8 | 25 |
| **3** | Otomatisasi Tata Letak Dokumen Akademik Menggunakan Multi-Agent System dan Siklus Active Learning Berbasis OpenXML | 8 | 8 | 9 | 25 |
| **4** | Pendekatan Collaborative Multi-Agent dan Two-Tier SQA pada Klasifikasi Struktur Dokumen Ilmiah | 7 | 8 | 8 | 23 |
| **5** | Rancang Bangun Sistem Otomatisasi Format Dokumen Akademik Menggunakan Model Hibrida NLP dan Validasi Multi-Agent | 8 | 7 | 9 | 24 |

---

## TAHAP 4 — Analisis Final

### 1. Analisis WHY Judul Peringkat 1 Paling Kuat

* **Kaitan ke Gap:** Judul peringkat 1 secara eksplisit mengangkat variabel **Multi-Agent System**, **Two-Tier SQA**, dan **NLP**, yang langsung menjawab *Methodological Gap* dari SLR—yakni transisi dari sistem deteksi pasif (*checker-only*) menuju arsitektur penjaminan mutu aktif berlapis.
* **Kaitan ke Novelty:** Kombinasi antara analisis fitur hibrida (*Inspector*), audit logika monotonik (*Quality Critic*), dan gerbang penerimaan artifak (*Artifact Acceptance Gate*) memberikan kebaruan keilmuan yang membedakan penelitian ini dari literatur terdahulu (P01–P15).

### 2. Alternatif Versi Akademik (Paper) dan Praktis (Industri)

* **Versi Akademik (untuk Jurnal/Konferensi Internasional):**
  > *"A Two-Tier SQA Multi-Agent Architecture for Automated Logical Structure Recognition and Non-Destructive Formatting of Academic Documents"*

* **Versi Praktis (untuk Produk Industri/Komersial):**
  > *"ASDOKU: Asisten Cerdas Otomatisasi Format Skripsi & Dokumen Akademik Berbasis Multi-Agent AI"*

---

### 3. Rekomendasi FINAL & Kalimat Pembuka Latar Belakang (Bab 1.1)

#### **Rekomendasi Final Judul Skripsi:**

> **"RANCANG BANGUN MULTI-AGENT SYSTEM DENGAN MEKANISME TWO-TIER SQA UNTUK OTOMATISASI DETEKSI DAN FORMATTING DOKUMEN AKADEMIK BERBASIS NLP"**

#### **Kalimat Pembuka Latar Belakang Masalah (Draf Bab 1.1):**

> **(A)** Berdasarkan data empiris pengelolaan naskah akademik di lingkungan Universitas Esa Unggul, penulisan karya ilmiah akhir (Skripsi, Proposal, dan Laporan Magang) diwajibkan mematuhi standar tata letak dan tipografi baku sesuai SK Rektor UEU No. 5 Tahun 2018. Namun, proses penyusunan manual sering kali menghasilkan inkonsistensi tipografi, kerusakan nomor sub-bab, serta ketiadaan *Navigation Pane* akibat tidak digunakannya *Heading styles*.  
>  
> **(B)** Berdasarkan tinjauan pustaka terkini (2021–2026), sebagian besar penelitian terdahulu mengenai otomatisasi dokumen masih bersifat pasif—hanya berfungsi sebagai pemeriksa kesalahan (*checker-only*) atau mengandalkan model klasifikasi tunggal tanpa pengawasan logika struktural, sehingga rentan memicu anomali seperti *false positive* pada sub-bab sistematika penulisan.  
>  
> **(C)** Oleh karena itu, penelitian ini mengusulkan kebaruan berupa rancang bangun **Multi-Agent System** yang dilengkapi mekanisme penjaminan mutu dua tingkat (**Two-Tier Software Quality Assurance**) serta ekstraksi fitur hibrida berbasis **Natural Language Processing (NLP)**, guna mengotomatisasi deteksi struktur dan rekonstruksi dokumen `.docx` secara non-destruktif dan otonom.

---

> **Pernyataan Pengesahan Fase 6A:**  
> Berkas analisis gap dan rekomendasi judul ini disusun secara sistematis mengacu pada luaran BRD dan SLR untuk mata kuliah Kapita Selekta dan menjadi dasar perumusan Bab 1 Proposal Tugas Akhir Program Studi Teknik Informatika, Fakultas Ilmu Komputer, Universitas Esa Unggul.
