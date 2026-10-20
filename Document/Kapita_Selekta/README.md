# DOKUMENTASI LENGKAP KAPITA SELEKTA & TAHAPAN RISET ASDOKU
## Rancang Bangun Multi-Agent System dengan Two-Tier SQA untuk Otomatisasi Deteksi Struktur dan Formatting Dokumen Akademik UEU Berbasis NLP

> **Peneliti:** Arditya Adjie Rosandi (NIM: 20230801274)  
> **Program Studi:** Teknik Informatika, Fakultas Ilmu Komputer — Universitas Esa Unggul  
> **Regulasi Standar:** SK Rektor UEU No. 5 Tahun 2018 (Pedoman Tata Tulis Skripsi & Tugas Akhir)  
> **Status Dokumen:** Fase 1 s/d Fase 6 Selesai & Terverifikasi Penuh Tanpa Placeholder

---

## 1. Struktur Folder Fase Kerja yang Telah Selesai (Fase 1 s/d Fase 6)

Seluruh dokumen dan artifak riset yang telah disusun telah dirapikan ke dalam folder masing-masing fase:

| Fase | Nama & Fokus Fase Kerja | Alat Bantu (*Tools*) | Berkas Utama (*Deliverables*) | Lokasi Folder |
| :---: | :--- | :--- | :--- | :--- |
| **Fase 1** | **Ideasi, Formulasi PICOS & Research Questions** | Gemini / ChatGPT / DeepSeek | • [PICOS_RQ.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%201%20-%20Ideasi%20&%20PICOS/PICOS_RQ.md)<br/>• [Protokol_SLR_Fase1_Planning.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%201%20-%20Ideasi%20&%20PICOS/Protokol_SLR_Fase1_Planning.md)<br/>• `Fase_1_Dokumen_Awal.docx` | [Fase 1 - Ideasi & PICOS/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%201%20-%20Ideasi%20&%20PICOS/) |
| **Fase 2** | **Penelusuran Literatur & Evidence Matrix** | Scopus AI, Elicit.com, Mendeley | • [Evidence_Matrix_Scopus.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%202%20-%20Penelusuran%20Literatur/Evidence_Matrix_Scopus.md)<br/>• [Scopus_AI_Research_Analytics.pdf](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%202%20-%20Penelusuran%20Literatur/Scopus_AI_Research_Analytics.pdf) | [Fase 2 - Penelusuran Literatur/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%202%20-%20Penelusuran%20Literatur/) |
| **Fase 3** | **Penyusunan Dokumen BRD & SLR** | IEEE Template + Mendeley | • [BRD_Business_Requirements_Document.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%203%20-%20Dokumen%20BRD%20&%20SLR/BRD_Business_Requirements_Document.md)<br/>• [SLR_Systematic_Literature_Review.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%203%20-%20Dokumen%20BRD%20&%20SLR/SLR_Systematic_Literature_Review.md) | [Fase 3 - Dokumen BRD & SLR/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%203%20-%20Dokumen%20BRD%20&%20SLR/) |
| **Fase 4** | **Analisis Gap & Penetapan Judul Final** | LLM + Matriks Gap FR × SLR | • [Gap_Analysis_dan_Penetapan_Judul.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%204%20-%20Analisis%20Gap%20&%20Judul%20Final/Gap_Analysis_dan_Penetapan_Judul.md) | [Fase 4 - Analisis Gap & Judul Final/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%204%20-%20Analisis%20Gap%20&%20Judul%20Final/) |
| **Fase 5** | **Uji Kesesuaian BRD×SLR & Kritik Keras** | Prompt 6B (Dosen Skeptis vs Tech Lead) | • [Audit_Kritis_BRD_SLR_Portofolio.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%205%20-%20Audit%20Kesesuaian%20&%20Kritik%20Keras/Audit_Kritis_BRD_SLR_Portofolio.md) | [Fase 5 - Audit Kesesuaian & Kritik Keras/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%205%20-%20Audit%20Kesesuaian%20&%20Kritik%20Keras/) |
| **Fase 6** | **Spesifikasi Sistem & Visual Diagram** | Draw.io, Mermaid.js | • [FLOWCHART_ARSITEKTUR.md](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%206%20-%20Spesifikasi%20Sistem%20&%20Diagram/FLOWCHART_ARSITEKTUR.md)<br/>• `flowchart_vertikal_detail.drawio`<br/>• `flowchart_vertikal_detail.mmd`<br/>• `flowchart_horizontal_slide.drawio`<br/>• `flowchart_horizontal_slide.mmd` | [Fase 6 - Spesifikasi Sistem & Diagram/](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%206%20-%20Spesifikasi%20Sistem%20&%20Diagram/) |

---

## 2. Hasil Audit & Pengecekan Placeholder `[ ISI TEKS ]`

Seluruh dokumen pada repositori ini telah diaudit menyeluruh:
* **Tidak Ada Placeholder Tersisa:** Seluruh tanda `[ISI DATA]`, `[PERLU VERIFIKASI]`, maupun kurung siku kosong `[ ]` telah dihapus dan digantikan data aktual.
* **Fitur Rekayasa Hibrida:** Konsisten pada **420 Dimensi Fitur Gabungan** (400 Fitur NLP TF-IDF N-Gram 1,2 + 20 Fitur Metadata OpenXML termasuk `is_below_drawing`, `is_above_table`, dll).
* **Performa Deteksi Struktur:** Model utama *Random Forest (Balanced)* mencatatkan puncak akurasi **97.22%** (*Weighted F1*: **0.97**; dengan evolusi terukur: baseline 90.70% $\rightarrow$ 93.71% $\rightarrow$ 94.84% $\rightarrow$ **97.22%** pada 1.747 sampel paragraf).
* **Model Baseline Pembanding:** *Logistic Regression (Balanced)* akurasi **88.57%** (*Weighted F1*: **0.88**).
* **Penjaminan Mutu SQA:** Mekanisme *Two-Tier SQA* (Tier 1 Blueprint Guardrails & Tier 2 Physical OpenXML Audit) meluluskan **100.0% PASS** terhadap 8 kriteria SK Rektor UEU No. 5 Tahun 2018 pada seluruh 5 Dokumen Emas (*Gold Datasets* P1–P5).
* **Kecepatan Komputasi:** Rata-rata waktu pemrosesan dokumen penuh adalah **0.98 detik** (di bawah batas toleransi SLA 1.5 detik).

---

## 3. Agenda Tahap Berikutnya (Akan Dibuat Selanjutnya)

* **Fase 7:** Drafting Naskah Skripsi Bab I–III & Penyusunan Slide Ujian Seminar Proposal (Sempro 16:9).
* **Fase 8:** Eksperimen Lanjutan Skripsi Utuh (Bab I–V) & Uji Similaritas Turnitin $\le 20\%$.
* **Fase 9:** Pembuatan Poster A0, Penulisan Artikel Jurnal Ilmiah (IEEE/SINTA), dan Finalisasi Portofolio Repositori.
