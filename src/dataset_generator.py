"""
Modul Generator Dataset Skripsi (Data Ingestion & Auto-Labeling) - Versi 2.

Penyempurnaan Berdasarkan Temuan Empiris:
1. Mencegah TOC items (style 'toc') memicu transisi zona prematur.
2. Mendeteksi Judul Bab otomatis tanpa kata 'BAB' (Heading 1 + numPr + kata baku seperti PENDAHULUAN).
3. Mendeteksi Sub-Bab otomatis (Heading 2 + numPr).
4. Mendeteksi Caption Gambar (Gambar 1-1, Gambar 1.1) dan Tabel (Tabel 2-1, Tabel 2.1) secara presisi.
"""

import os
import re
import csv
from typing import List, Dict, Any
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Daftar istilah baku bagian awal (Frontmatter)
FRONTMATTER_KEYWORDS = [
    "LEMBAR PENGESAHAN", "HALAMAN PENGESAHAN", "PENGESAHAN",
    "HALAMAN PERNYATAAN KEASLIAN", "PERNYATAAN KEASLIAN",
    "KATA PENGANTAR", "UCAPAN TERIMA KASIH",
    "ABSTRAK", "ABSTRACT",
    "DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR",
    "DAFTAR LAMPIRAN", "DAFTAR SIMBOL", "DAFTAR RUMUS"
]

# Kata kunci judul bab standar akademik UEU
BAB_STANDARD_TITLES = [
    "PENDAHULUAN", "TINJAUAN PUSTAKA", "LANDASAN TEORI", "METODE",
    "METODOLOGI", "METODE PENELITIAN", "HASIL", "PEMBAHASAN",
    "HASIL DAN PEMBAHASAN", "KESIMPULAN", "SARAN", "KESIMPULAN DAN SARAN",
    "PENUTUP"
]

BAB_PATTERN = re.compile(r'^(BAB\s+[IVX\d]+|BAB\s+\d+)(\s*[:\-\n\r]\s*|\s+|$)', re.IGNORECASE)
SUB_BAB_NUM_PATTERN = re.compile(r'^\d+(\.\d+)+(\s+.*|$)', re.IGNORECASE)

# Pattern Caption Gambar & Tabel (mendukung format 1.1 maupun 1-1 khas UEU)
CAPTION_GAMBAR_PATTERN = re.compile(r'^(Gambar|Figure)\s+\d+[\.\-]\d+.*', re.IGNORECASE)
CAPTION_TABEL_PATTERN = re.compile(r'^(Tabel|Table)\s+\d+[\.\-]\d+.*', re.IGNORECASE)

def clean_text(text: str) -> str:
    """Membersihkan karakter kontrol dan spasi ganda."""
    if not text:
        return ""
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_font_info(p):
    """Mengekstraksi ukuran font dan status cetak tebal (bold)."""
    size, bold, italic = None, None, None
    for r in p.runs:
        if r.text.strip():
            size = r.font.size or (p.style.font.size if p.style and p.style.font else None)
            bold = r.font.bold if r.font.bold is not None else (p.style.font.bold if p.style and p.style.font else None)
            italic = r.font.italic if r.font.italic is not None else (p.style.font.italic if p.style and p.style.font else None)
            break
    return (size.pt if size else 12.0), bool(bold), bool(italic)

def get_alignment_str(align):
    """Menerjemahkan alignment enum Word."""
    if align == WD_ALIGN_PARAGRAPH.CENTER:
        return "CENTER"
    elif align == WD_ALIGN_PARAGRAPH.JUSTIFY:
        return "JUSTIFY"
    elif align == WD_ALIGN_PARAGRAPH.RIGHT:
        return "RIGHT"
    elif align == WD_ALIGN_PARAGRAPH.LEFT:
        return "LEFT"
    return "DEFAULT"

def extract_raw_paragraphs(file_path: str, doc_id: str) -> List[Dict[str, Any]]:
    """Membaca paragraf dan mengekstrak sinyal mentah OpenXML."""
    doc = Document(file_path)
    total_p = len(doc.paragraphs)
    raw_list = []

    for idx, p in enumerate(doc.paragraphs):
        text = clean_text(p.text)
        size, bold, italic = get_font_info(p)
        align = get_alignment_str(p.alignment)
        
        pPr = p._p.pPr
        has_num = bool(pPr is not None and pPr.numPr is not None)
        has_img = bool(p._p.xpath(".//w:drawing"))
        has_pgbrk = bool(p._p.xpath('.//w:br[@w:type="page"]'))
        
        # Ekstraksi Spacing & Line Spacing
        sb, sa, ls = 0.0, 0.0, 1.15
        fl, li = 0.0, 0.0
        if pPr is not None:
            sp = pPr.find(qn('w:spacing'))
            if sp is not None:
                if qn('w:before') in sp.attrib:
                    sb = float(sp.attrib[qn('w:before')]) / 20.0
                if qn('w:after') in sp.attrib:
                    sa = float(sp.attrib[qn('w:after')]) / 20.0
                if qn('w:line') in sp.attrib:
                    ls = float(sp.attrib[qn('w:line')]) / 240.0
            ind = pPr.find(qn('w:ind'))
            if ind is not None:
                if qn('w:firstLine') in ind.attrib:
                    fl = float(ind.attrib[qn('w:firstLine')]) / 567.0
                elif qn('w:hanging') in ind.attrib:
                    fl = -float(ind.attrib[qn('w:hanging')]) / 567.0
                if qn('w:left') in ind.attrib:
                    li = float(ind.attrib[qn('w:left')]) / 567.0

        char_len = len(text)
        word_count = len(text.split())
        uppercase_ratio = sum(1 for c in text if c.isupper()) / float(char_len) if char_len > 0 else 0.0
        doc_pos = idx / float(total_p) if total_p > 0 else 0.0

        raw_list.append({
            "doc_id": doc_id,
            "para_id": idx,
            "text": text,
            "style": p.style.name if p.style else "Normal",
            "char_len": char_len,
            "word_count": word_count,
            "font_size": size,
            "is_bold": bold,
            "is_italic": italic,
            "align": align,
            "has_num": has_num,
            "has_img": has_img,
            "has_pgbrk": has_pgbrk,
            "space_before": round(sb, 2),
            "space_after": round(sa, 2),
            "line_spacing": round(ls, 2),
            "first_line_indent": round(fl, 2),
            "left_indent": round(li, 2),
            "uppercase_ratio": round(uppercase_ratio, 3),
            "doc_pos": round(doc_pos, 4)
        })

    return raw_list

def auto_label_document(raw_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    State-Aware Rule-Assisted Labeler.
    Menerapkan pelacakan zona dokumen (State Machine) untuk mencegah False Positive.
    """
    current_zone = "COVER"
    in_sistematika = False
    labeled_list = []

    for i, item in enumerate(raw_list):
        text = item["text"]
        upper_text = text.upper()
        is_bold = item["is_bold"]
        has_num = item["has_num"]
        style_lower = item["style"].lower()
        word_count = item["word_count"]
        doc_pos = item["doc_pos"]

        # Default label awal
        label = "BODY_PARAGRAPH"

        # 1. Paragraf Kosong
        if item["char_len"] == 0:
            label = "LAINNYA"
            labeled_list.append({**item, "label": label})
            continue

        # 2. Cek apakah ini bagian TOC bawaan Word
        is_toc_item = "toc" in style_lower or "table of figures" in style_lower

        # 3. Transisi Zona Dokumen (Hanya jika BUKAN item di dalam TOC!)
        if not is_toc_item:
            if any(kw in upper_text for kw in ["LEMBAR PENGESAHAN", "HALAMAN PENGESAHAN", "PERNYATAAN KEASLIAN", "KATA PENGANTAR"]):
                current_zone = "FRONTMATTER"
            
            # Pemicu masuk Zona BODY:
            # - Ada teks BAB I / BAB 1, ATAU
            # - Style Heading 1 dengan teks judul bab baku (misal PENDAHULUAN di template UEU)
            if not in_sistematika:
                if (BAB_PATTERN.match(text) and is_bold) or ("heading 1" in style_lower and upper_text in BAB_STANDARD_TITLES):
                    current_zone = "BODY"

            # Pemicu masuk Zona BIBLIOGRAPHY:
            if any(upper_text == kw for kw in ["DAFTAR PUSTAKA", "DAFTAR REFERENSI"]):
                current_zone = "BIBLIOGRAPHY"

            # Pemicu masuk Zona APPENDIX:
            if upper_text.startswith("LAMPIRAN") and (is_bold or "heading" in style_lower):
                current_zone = "APPENDIX"

        # 4. Deteksi Berdasarkan Zona & Sinyal Tipografi

        # --- TOC / TABLE OF FIGURES ---
        if is_toc_item:
            label = "FRONTMATTER_TITLE"

        # --- ZONA COVER ---
        elif current_zone == "COVER" and doc_pos < 0.12:
            label = "COVER_METADATA"

        # --- ZONA FRONTMATTER ---
        elif current_zone == "FRONTMATTER":
            if any(upper_text == kw or upper_text.startswith(kw) for kw in FRONTMATTER_KEYWORDS) and (is_bold or "heading" in style_lower) and word_count <= 6:
                label = "FRONTMATTER_TITLE"
            else:
                label = "BODY_PARAGRAPH"

        # --- ZONA BIBLIOGRAPHY ---
        elif current_zone == "BIBLIOGRAPHY":
            if any(upper_text == kw for kw in ["DAFTAR PUSTAKA", "DAFTAR REFERENSI"]):
                label = "FRONTMATTER_TITLE"
            else:
                label = "DAFTAR_PUSTAKA_ITEM"

        # --- ZONA APPENDIX ---
        elif current_zone == "APPENDIX":
            if upper_text.startswith("LAMPIRAN") and (is_bold or word_count <= 8 or "heading" in style_lower):
                label = "FRONTMATTER_TITLE"
            else:
                label = "BODY_PARAGRAPH"

        # --- ZONA BODY (BAB ISI) ---
        else:
            # Shield untuk Sistematika Penulisan
            if "SISTEMATIKA PENULISAN" in upper_text:
                in_sistematika = True
                label = "SUB_BAB"
            elif in_sistematika and ("heading 1" in style_lower or item["has_pgbrk"]) and (BAB_PATTERN.match(text) or upper_text in BAB_STANDARD_TITLES):
                in_sistematika = False  # Keluar dari sistematika karena Bab baru resmi dimulai

            # Cek Caption Gambar (Gambar 1-1 / Gambar 1.1)
            if CAPTION_GAMBAR_PATTERN.match(text) and word_count <= 25:
                label = "CAPTION_GAMBAR"

            # Cek Caption Tabel (Tabel 2-1 / Tabel 2.1)
            elif CAPTION_TABEL_PATTERN.match(text) and word_count <= 25:
                label = "CAPTION_TABEL"

            # Cek Judul Bab Utama
            elif not in_sistematika and (
                (BAB_PATTERN.match(text) and (is_bold or "heading 1" in style_lower or item["align"] == "CENTER") and word_count <= 10)
                or ("heading 1" in style_lower and upper_text in BAB_STANDARD_TITLES)
            ):
                label = "JUDUL_BAB"

            # Cek Sub-Bab:
            # - Pola angka desimal (1.1, 1.2, 1.2.1) DAN (bold / heading)
            # - ATAU style Heading 2/3 dengan has_num atau teks pendek
            elif not in_sistematika and (
                (SUB_BAB_NUM_PATTERN.match(text) and (is_bold or "heading" in style_lower) and word_count <= 15)
                or (("heading 2" in style_lower or "heading 3" in style_lower) and word_count <= 12 and not text.endswith("."))
            ):
                label = "SUB_BAB"

            # Sisanya adalah isi paragraf biasa
            else:
                label = "BODY_PARAGRAPH"

        labeled_list.append({**item, "label": label})

    return labeled_list

def generate_dataset(file_paths: List[Dict[str, str]], output_csv: str = "data/dataset_skripsi.csv"):
    """Menggabungkan ekstraksi dari beberapa dokumen menjadi 1 file dataset CSV."""
    all_rows = []
    print("=== MEMPROSES GENERASI DATASET SKRIPSI (V2) ===")
    
    for f in file_paths:
        path = f["path"]
        doc_id = f["id"]
        print(f"[*] Mengekstraksi dokumen: {doc_id} ({path})...")
        raw = extract_raw_paragraphs(path, doc_id)
        labeled = auto_label_document(raw)
        all_rows.extend(labeled)
        print(f"    -> Berhasil mengekstrak {len(labeled)} paragraf.")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    if all_rows:
        fieldnames = list(all_rows[0].keys())
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n[SUKSES] Total {len(all_rows)} baris data tersimpan ke: {output_csv}")

if __name__ == "__main__":
    docs_to_process = [
        {"id": "DOC_TEMPLATE_BARU_2024", "path": "data/dokumen_uji/P1_Template_Resmi_UEU.docx"},
        {"id": "DOC_TEMPLATE_UEU", "path": "data/dokumen_uji/P5_Buku_TA_Landscape.docx"},
        {"id": "DOC_MHS_DHICKY", "path": "data/dokumen_uji/P2_Skripsi_Mbkm_Dhicky.docx"},
        {"id": "DOC_MHS_IDHAM", "path": "data/doc_idham.docx"},
        {"id": "DOC_MHS_CONTOH", "path": "data/dokumen_uji/P4_Laporan_Mbkm_Arditya.docx"}
    ]
    generate_dataset(docs_to_process)
