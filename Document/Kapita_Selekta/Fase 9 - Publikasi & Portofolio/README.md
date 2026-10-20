# FASE 9: POSTER, PAPER JURNAL, ACC FINAL & REPO PORTOFOLIO
## Publikasi Ilmiah, Diseminasi Hasil Riset, dan Standarisasi Repositori Siap Kerja

> **Fokus:** Diseminasi Akademik & Portofolio Rekayasa Perangkat Lunak Industri  
> **Institusi:** FASILKOM Universitas Esa Unggul

---

## 1. Rencana Publikasi Artikel Jurnal Ilmiah

* **Target Jurnal:** Jurnal Ilmiah Terakreditasi Nasional (SINTA 2/3) atau Prosiding Seminar Internasional Bereputasi (IEEE / Scopus Indexed).
* **Format Penulisan:** Template IEEE Trans 2-kolom atau Format Jurnal Tujuan.
* **Judul Artikel:**
  > *"Rancang Bangun Multi-Agent System dengan Two-Tier SQA untuk Otomatisasi Deteksi dan Formatting Dokumen Akademik Berbasis NLP"*
* **Struktur Paper (6–8 Halaman):**
  1. *Abstract* & *Keywords*
  2. *Introduction* (Problem Statement, RQ, Scope)
  3. *Related Work* (Sintesis PRISMA SLR Scopus)
  4. *Proposed Multi-Agent Architecture* (Tri-Agent & Two-Tier SQA)
  5. *Experimental Evaluation & Results* (Akurasi 97.22%, SQA 100% PASS, 0.98s Processing Time)
  6. *Discussion & Threats to Validity*
  7. *Conclusion & Future Work*
  8. *References* (IEEE Style)

---

## 2. Poster Presentasi Akademik (Ukuran A0 Portrait)

* **Dimensi:** $84.1 \text{ cm} \times 118.9 \text{ cm}$ (Standar Pameran Skripsi / Gelar Karya FASILKOM UEU).
* **Alat Desain:** Canva / Figma / Adobe Illustrator.
* **Elemen Visual:**
  - Header: Logo Universitas Esa Unggul, Judul Penelitian, Nama Peneliti & Dosen Pembimbing.
  - Diagram Alur: [flowchart_horizontal_slide.drawio](file:///root/Gammaura/Skripsi/Document/Kapita_Selekta/Fase%206%20-%20Spesifikasi%20Sistem%20&%20Diagram/flowchart_horizontal_slide.drawio) (berwarna akademik kontras).
  - Infografis Metrik: Puncak Akurasi 97.22%, SQA 100% PASS, Waktu Pemrosesan 0.98 Detik.
  - Tangkapan Layar Aplikasi: Antarmuka Web Studio FastAPI (`alat.html`).
  - QR Code: Tautan langsung ke repositori GitHub publik dan demo aplikasi.

---

## 3. Standarisasi Repositori Portofolio Siap Kerja (Tech Lead Level)

Repositori GitHub ditata dengan standar *production-ready software engineering*:
* **Struktur Folder Teratur:**
  - `/App`: Kode sumber backend FastAPI, modul agen (`inspector.py`, `critic.py`, `formatter.py`), modul SQA (`sqa_service.py`), dan antarmuka web.
  - `/Document`: Seluruh dokumentasi ilmiah, naskah, dan tahapan Kapita Selekta Fase 1 s/d Fase 9.
* **Dokumentasi README.md Repositori:**
  - Badges: Python 3.10+, FastAPI, OpenXML, Scikit-Learn, SQA 100% PASS.
  - System Architecture & Mermaid Diagram.
  - Quickstart Guide: Cara kloning, instalasi dependencies, dan menjalankan server (`uvicorn app:app --reload`).
  - API Endpoints Documentation (`/inspect`, `/format`, `/evaluate`, `/active-learning`).
