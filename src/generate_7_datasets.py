"""
Generator 7 Master Datasets Skripsi (The 7-Pillar Architecture)
Sesuai Standar SK Rektor Universitas Esa Unggul (UEU) No. 5 Tahun 2018.

Dataset yang Dihasilkan:
1. data/datasets/dataset_1_cover_frontmatter.csv : Metadata Cover & Lembar Pengesahan, Abstrak
2. data/datasets/dataset_2_zoning.csv            : Segmentasi Zona Dokumen & Transisi Seksi
3. data/datasets/dataset_3_headings_vs_lists.csv: Heading 1, 2, 3 vs Rincian Poin (1., a., bullet)
4. data/datasets/dataset_4_figures.csv          : Gambar, Caption Bawah, dan Sumber Gambar
5. data/datasets/dataset_5_tables.csv           : Tabel, Caption Atas, Header, dan Sumber Tabel
6. data/datasets/dataset_6_code_formulas.csv    : Rumus Matematika, Persamaan, & Kode Program
7. data/datasets/dataset_7_body_bibliography.csv: Paragraf Isi, Kutipan Langsung, & Daftar Pustaka
"""

import os
import re
import csv
import glob
from typing import List, Dict, Any, Tuple
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# Pola Regex Baku UEU 2018
BAB_PATTERN = re.compile(r'^(BAB\s+[IVX\d]+|BAB\s+\d+)(\s*[:\-\n\r]\s*|\s+|$)', re.IGNORECASE)
HEADING2_PATTERN = re.compile(r'^\d+\.\d+(\s+[A-Za-z].*|$)', re.IGNORECASE)
HEADING3_PATTERN = re.compile(r'^\d+\.\d+\.\d+(\s+[A-Za-z].*|$)', re.IGNORECASE)

LIST_NUMBER_PATTERN = re.compile(r'^\d+[\.\)]\s+', re.IGNORECASE)
LIST_ALPHA_PATTERN = re.compile(r'^[a-zA-Z][\.\)]\s+', re.IGNORECASE)
LIST_BULLET_PATTERN = re.compile(r'^[\-\•\*\–\⁃]\s+', re.IGNORECASE)

CAPTION_GAMBAR_PATTERN = re.compile(r'^(Gambar|Figure)\s+(\d+[\.\-]\d+|\.|\d+).*', re.IGNORECASE)
CAPTION_TABEL_PATTERN = re.compile(r'^(Tabel|Table)\s+(\d+[\.\-]\d+|\.|\d+).*', re.IGNORECASE)
SOURCE_PATTERN = re.compile(r'^\(?(Sumber|Source)\s*[:\-].*', re.IGNORECASE)
EQUATION_NUM_PATTERN = re.compile(r'.*\(\d+[\.\-]\d+\)\s*$', re.IGNORECASE)

FRONTMATTER_KEYWORDS = [
    "LEMBAR PENGESAHAN", "HALAMAN PENGESAHAN", "PENGESAHAN",
    "HALAMAN PERNYATAAN KEASLIAN", "PERNYATAAN KEASLIAN",
    "KATA PENGANTAR", "UCAPAN TERIMA KASIH",
    "ABSTRAK", "ABSTRACT",
    "DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR",
    "DAFTAR LAMPIRAN", "DAFTAR SIMBOL", "DAFTAR RUMUS"
]

CANONICAL_CHAPTER_NAMES = [
    "PENDAHULUAN", "TINJAUAN PUSTAKA", "LANDASAN TEORI", "DASAR TEORI",
    "KAJIAN PUSTAKA", "METODE", "METODOLOGI", "METODE PENELITIAN",
    "METODOLOGI PENELITIAN", "GAMBARAN UMUM", "ANALISIS DAN PEMBAHASAN",
    "HASIL DAN PEMBAHASAN", "PEMBAHASAN", "IMPLEMENTASI",
    "KESIMPULAN DAN SARAN", "PENUTUP", "KESIMPULAN"
]

MONOSPACE_FONTS = {"consolas", "courier", "courier new", "lucida console", "monaco", "source code pro"}
CODE_KEYWORDS = {"def ", "select ", "from ", "where ", "public class ", "function(", "import ", "return ", "if (", "while ("}

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def get_font_info(p) -> Tuple[str, float, bool, bool]:
    name, size, bold, italic = "Times New Roman", 12.0, False, False
    for r in p.runs:
        if r.text.strip():
            if r.font.name:
                name = r.font.name
            elif p.style and p.style.font and p.style.font.name:
                name = p.style.font.name

            if r.font.size:
                size = r.font.size.pt
            elif p.style and p.style.font and p.style.font.size:
                size = p.style.font.size.pt

            bold = r.font.bold if r.font.bold is not None else (p.style.font.bold if p.style and p.style.font else False)
            italic = r.font.italic if r.font.italic is not None else (p.style.font.italic if p.style and p.style.font else False)
            break
    return name, size, bool(bold), bool(italic)

def get_alignment_str(align) -> str:
    if align == WD_ALIGN_PARAGRAPH.CENTER:
        return "CENTER"
    elif align == WD_ALIGN_PARAGRAPH.JUSTIFY:
        return "JUSTIFY"
    elif align == WD_ALIGN_PARAGRAPH.RIGHT:
        return "RIGHT"
    elif align == WD_ALIGN_PARAGRAPH.LEFT:
        return "LEFT"
    return "DEFAULT"

def extract_document_elements(file_path: str, doc_id: str) -> List[Dict[str, Any]]:
    """
    Ekstraksi mendalam setiap elemen dokumen (w:p dan w:tbl)
    dengan penanda relasi spasial OpenXML (atas/bawah gambar & tabel).
    """
    doc = Document(file_path)
    body_elements = doc._body._element
    total_elements = len(body_elements)
    
    parsed_items = []
    para_counter = 0

    # Tracking elemen tetangga
    for idx, elem in enumerate(body_elements):
        tag = elem.tag.split('}')[-1]

        if tag == 'p':
            # Ini paragraf
            p = doc.paragraphs[para_counter] if para_counter < len(doc.paragraphs) else None
            para_counter += 1
            if p is None:
                continue

            text = clean_text(p.text)
            font_name, size, bold, italic = get_font_info(p)
            align = get_alignment_str(p.alignment)
            
            pPr = p._p.pPr
            has_num = bool(pPr is not None and pPr.numPr is not None)
            has_img = bool(p._p.xpath(".//w:drawing | .//w:pict"))
            has_pgbrk = bool(p._p.xpath('.//w:br[@w:type="page"]'))
            has_math = bool('oMath' in p._p.xml)

            # Cek tetangga berikutnya apakah tabel
            is_above_table = False
            if idx + 1 < total_elements:
                next_tag = body_elements[idx + 1].tag.split('}')[-1]
                if next_tag == 'tbl':
                    is_above_table = True

            # Cek tetangga sebelumnya apakah tabel
            is_below_table = False
            if idx > 0:
                prev_tag = body_elements[idx - 1].tag.split('}')[-1]
                if prev_tag == 'tbl':
                    is_below_table = True

            # Indentasi & Spacing
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
            upper_ratio = sum(1 for c in text if c.isupper()) / float(char_len) if char_len > 0 else 0.0
            is_mono = font_name.lower() in MONOSPACE_FONTS
            has_code_kw = any(kw in text.lower() for kw in CODE_KEYWORDS)

            parsed_items.append({
                "elem_type": "paragraph",
                "doc_id": doc_id,
                "elem_idx": idx,
                "para_id": para_counter - 1,
                "text": text,
                "style": p.style.name if p.style else "Normal",
                "font_name": font_name,
                "font_size": size,
                "is_bold": bold,
                "is_italic": italic,
                "align": align,
                "has_num": has_num,
                "has_img": has_img,
                "has_pgbrk": has_pgbrk,
                "has_math": has_math,
                "is_above_table": is_above_table,
                "is_below_table": is_below_table,
                "is_below_drawing": False, # dihitung di second-pass
                "space_before": round(sb, 2),
                "space_after": round(sa, 2),
                "line_spacing": round(ls, 2),
                "first_line_indent": round(fl, 2),
                "left_indent": round(li, 2),
                "char_len": char_len,
                "word_count": word_count,
                "uppercase_ratio": round(upper_ratio, 3),
                "is_monospace": is_mono,
                "has_code_keywords": has_code_kw,
                "doc_pos": round(idx / float(total_elements), 4)
            })

        elif tag == 'tbl':
            # Ini elemen tabel
            parsed_items.append({
                "elem_type": "table",
                "doc_id": doc_id,
                "elem_idx": idx,
                "para_id": -1,
                "text": "[TABLE_CONTAINER]",
                "style": "Table",
                "font_name": "Times New Roman",
                "font_size": 10.0,
                "is_bold": False,
                "is_italic": False,
                "align": "CENTER",
                "has_num": False,
                "has_img": False,
                "has_pgbrk": False,
                "has_math": False,
                "is_above_table": False,
                "is_below_table": False,
                "is_below_drawing": False,
                "space_before": 0.0,
                "space_after": 0.0,
                "line_spacing": 1.0,
                "first_line_indent": 0.0,
                "left_indent": 0.0,
                "char_len": 0,
                "word_count": 0,
                "uppercase_ratio": 0.0,
                "is_monospace": False,
                "has_code_keywords": False,
                "doc_pos": round(idx / float(total_elements), 4)
            })

    # Second pass: tandai is_below_drawing
    for i in range(1, len(parsed_items)):
        if parsed_items[i-1]["has_img"] and parsed_items[i]["elem_type"] == "paragraph":
            parsed_items[i]["is_below_drawing"] = True

    return parsed_items

def classify_and_distribute(all_docs_items: List[List[Dict[str, Any]]]):
    """
    Mengklasifikasikan item ke dalam 7 Dataset Master Spesialis secara ketat.
    """
    d1_cover_frontmatter = []
    d2_zoning = []
    d3_headings_vs_lists = []
    d4_figures = []
    d5_tables = []
    d6_code_formulas = []
    d7_body_bibliography = []

    for doc_items in all_docs_items:
        current_zone = "COVER"
        in_sistematika = False
        total = len(doc_items)

        for i, item in enumerate(doc_items):
            if item["elem_type"] == "table":
                # Masukkan ke ekosistem tabel
                d5_tables.append({**item, "label": "TABLE_CONTAINER"})
                continue

            text = item["text"]
            upper = text.upper()
            word_count = item["word_count"]
            char_len = item["char_len"]
            doc_pos = item["doc_pos"]
            style_lower = item["style"].lower()
            is_bold = item["is_bold"]

            if char_len == 0:
                continue

            is_toc = "toc" in style_lower or "table of figures" in style_lower

            # -------------------------------------------------------------
            # Tracking Zona Dokumen
            # -------------------------------------------------------------
            if not is_toc:
                if any(kw in upper for kw in ["LEMBAR PENGESAHAN", "HALAMAN PENGESAHAN", "PERNYATAAN KEASLIAN", "KATA PENGANTAR"]):
                    current_zone = "FRONTMATTER"
                elif any(upper == kw for kw in ["DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR"]):
                    current_zone = "FRONTMATTER_LISTS"
                elif (BAB_PATTERN.match(text) and is_bold) or ("heading 1" in style_lower and upper in CANONICAL_CHAPTER_NAMES):
                    if not in_sistematika:
                        current_zone = "BODY_BAB"
                elif any(upper == kw for kw in ["DAFTAR PUSTAKA", "DAFTAR REFERENSI"]):
                    current_zone = "BIBLIOGRAPHY"
                elif upper.startswith("LAMPIRAN") and (is_bold or "heading" in style_lower):
                    current_zone = "APPENDIX"

            # Rekam ke Dataset 2: Zoning
            d2_zoning.append({
                "doc_id": item["doc_id"],
                "para_id": item["para_id"],
                "text": text[:100],
                "doc_pos": doc_pos,
                "is_bold": is_bold,
                "has_pgbrk": item["has_pgbrk"],
                "style": item["style"],
                "zone_label": current_zone
            })

            # -------------------------------------------------------------
            # Sistematika Penulisan Shield
            # -------------------------------------------------------------
            if "SISTEMATIKA PENULISAN" in upper:
                in_sistematika = True
            elif in_sistematika and (BAB_PATTERN.match(text) or upper in CANONICAL_CHAPTER_NAMES) and is_bold:
                in_sistematika = False

            # -------------------------------------------------------------
            # 1. DATASET 1: COVER & FRONTMATTER METADATA
            # -------------------------------------------------------------
            if current_zone in ["COVER", "FRONTMATTER", "FRONTMATTER_LISTS"]:
                cover_label = "OTHER_FRONTMATTER"
                if current_zone == "COVER" and doc_pos < 0.15:
                    if word_count <= 15 and is_bold and upper == text and item["font_size"] >= 14:
                        cover_label = "COVER_TITLE"
                    elif "SKRIPSI" in upper or "TUGAS AKHIR" in upper or "LAPORAN" in upper:
                        cover_label = "COVER_TYPE"
                    elif any(k in upper for k in ["NIM", "NPM"]) or re.search(r'\b\d{9,12}\b', text):
                        cover_label = "COVER_AUTHOR_NIM"
                    elif any(k in upper for k in ["UNIVERSITAS", "FAKULTAS", "PROGRAM STUDI", "JURUSAN"]):
                        cover_label = "COVER_INSTITUTION"
                    elif re.match(r'^(20\d\d|JAKARTA.*20\d\d)$', upper):
                        cover_label = "COVER_YEAR"
                elif any(k in upper for k in ["PEMBIMBING", "PENGUJI", "DEKAN", "KETUA PROGRAM STUDI", "TANDA TANGAN"]):
                    cover_label = "PENGESAHAN_METADATA"
                elif any(upper == kw for kw in ["ABSTRAK", "ABSTRACT"]):
                    cover_label = "ABSTRAK_TITLE"
                elif upper.startswith("KATA KUNCI") or upper.startswith("KEYWORDS"):
                    cover_label = "ABSTRAK_KEYWORDS"
                elif is_toc:
                    cover_label = "TOC_ENTRY"

                d1_cover_frontmatter.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "font_size": item["font_size"],
                    "is_bold": is_bold,
                    "align": item["align"],
                    "doc_pos": doc_pos,
                    "label": cover_label
                })

            # -------------------------------------------------------------
            # 2. DATASET 4 & 5: EKOSISTEM GAMBAR & TABEL
            # -------------------------------------------------------------
            if CAPTION_GAMBAR_PATTERN.match(text) and word_count <= 25:
                d4_figures.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_below_drawing": item["is_below_drawing"],
                    "align": item["align"],
                    "font_size": item["font_size"],
                    "label": "CAPTION_GAMBAR"
                })
                continue
            elif item["has_img"]:
                d4_figures.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": "[IMAGE_DRAWING]",
                    "is_below_drawing": False,
                    "align": item["align"],
                    "font_size": item["font_size"],
                    "label": "FIGURE_IMAGE"
                })
            elif SOURCE_PATTERN.match(text) and (item["is_below_drawing"] or (i > 0 and CAPTION_GAMBAR_PATTERN.match(doc_items[i-1]["text"]))):
                d4_figures.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_below_drawing": True,
                    "align": item["align"],
                    "font_size": item["font_size"],
                    "label": "FIGURE_SOURCE"
                })
                continue

            if CAPTION_TABEL_PATTERN.match(text) and word_count <= 25:
                d5_tables.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_above_table": item["is_above_table"],
                    "align": item["align"],
                    "font_size": item["font_size"],
                    "label": "CAPTION_TABEL"
                })
                continue
            elif SOURCE_PATTERN.match(text) and item["is_below_table"]:
                d5_tables.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_above_table": False,
                    "align": item["align"],
                    "font_size": item["font_size"],
                    "label": "TABLE_SOURCE"
                })
                continue

            # -------------------------------------------------------------
            # 3. DATASET 6: RUMUS / FORMULA & CODE SNIPPET
            # -------------------------------------------------------------
            if item["has_math"] or EQUATION_NUM_PATTERN.match(text) or (any(s in text for s in ["∑", "√", "∫", "≈", "≤", "≥", "λ", "μ"]) and word_count <= 15):
                d6_code_formulas.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_monospace": item["is_monospace"],
                    "font_name": item["font_name"],
                    "font_size": item["font_size"],
                    "has_math": item["has_math"],
                    "label": "EQUATION_FORMULA"
                })
                continue
            elif item["is_monospace"] or (item["has_code_keywords"] and ("{" in text or ";" in text or "=" in text)):
                d6_code_formulas.append({
                    "doc_id": item["doc_id"],
                    "para_id": item["para_id"],
                    "text": text,
                    "is_monospace": True,
                    "font_name": item["font_name"],
                    "font_size": item["font_size"],
                    "has_math": False,
                    "label": "CODE_SNIPPET"
                })
                continue

            # -------------------------------------------------------------
            # 4. DATASET 3: HEADINGS vs ENUMERATION LISTS (Paling Krusial)
            # -------------------------------------------------------------
            is_h1 = (BAB_PATTERN.match(text) and is_bold and word_count <= 10) or ("heading 1" in style_lower and upper in CANONICAL_CHAPTER_NAMES)
            is_h2 = HEADING2_PATTERN.match(text) and (is_bold or "heading 2" in style_lower) and word_count <= 15 and not text.endswith(".")
            is_h3 = HEADING3_PATTERN.match(text) and (is_bold or "heading 3" in style_lower) and word_count <= 15 and not text.endswith(".")

            is_list_num = LIST_NUMBER_PATTERN.match(text) and not is_h2 and not is_h3
            is_list_alpha = LIST_ALPHA_PATTERN.match(text)
            is_list_bullet = LIST_BULLET_PATTERN.match(text) or (item["has_num"] and not is_h1 and not is_h2 and not is_h3 and not is_list_num and not is_list_alpha)

            if is_h1:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "HEADING_1"
                })
            elif is_h2:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "HEADING_2"
                })
            elif is_h3:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "HEADING_3"
                })
            elif is_list_num:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "LIST_NUMBERED"
                })
            elif is_list_alpha:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "LIST_ALPHABET"
                })
            elif is_list_bullet:
                d3_headings_vs_lists.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "font_size": item["font_size"], "is_bold": is_bold, "has_num": item["has_num"],
                    "word_count": word_count, "uppercase_ratio": item["uppercase_ratio"],
                    "label": "LIST_BULLET"
                })

            # -------------------------------------------------------------
            # 5. DATASET 7: BODY TEXT, KUTIPAN KHUSUS & BIBLIOGRAPHY
            # -------------------------------------------------------------
            if current_zone == "BIBLIOGRAPHY":
                if any(upper == kw for kw in ["DAFTAR PUSTAKA", "DAFTAR REFERENSI"]):
                    label_7 = "BIBLIOGRAPHY_TITLE"
                else:
                    label_7 = "BIBLIOGRAPHY_ENTRY"
                d7_body_bibliography.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "first_line_indent": item["first_line_indent"], "left_indent": item["left_indent"],
                    "line_spacing": item["line_spacing"], "word_count": word_count,
                    "label": label_7
                })
            elif current_zone == "BODY_BAB" and not is_h1 and not is_h2 and not is_h3:
                # Cek kutipan langsung panjang (> 4 baris / indent kiri >= 1.0 cm)
                if item["left_indent"] >= 0.8 and char_len > 100:
                    label_7 = "BLOCK_QUOTE"
                else:
                    label_7 = "BODY_PARAGRAPH"

                d7_body_bibliography.append({
                    "doc_id": item["doc_id"], "para_id": item["para_id"], "text": text,
                    "first_line_indent": item["first_line_indent"], "left_indent": item["left_indent"],
                    "line_spacing": item["line_spacing"], "word_count": word_count,
                    "label": label_7
                })

    # Simpan ke masing-masing file CSV
    out_dir = "data/datasets"
    os.makedirs(out_dir, exist_ok=True)

    def write_csv(filename: str, dataset: List[Dict[str, Any]]):
        if not dataset:
            print(f"[Warning] Dataset {filename} kosong!")
            return
        keys = list(dataset[0].keys())
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(dataset)
        print(f" Berhasil simpan: {filepath} ({len(dataset)} baris)")

    # Ekspor 4 File Modular 1-to-1 sesuai permintaan User
    asdoku_1_items = [item for doc in all_docs_items for item in doc if item["doc_id"] == "ASDOKU_1_TEMPLATE_UTUH"]
    asdoku_2_items = [item for doc in all_docs_items for item in doc if item["doc_id"] == "ASDOKU_2_TOC_HEADINGS"]
    asdoku_3_items = [item for doc in all_docs_items for item in doc if item["doc_id"] == "ASDOKU_3_FIGURES_TOF"]
    asdoku_4_items = [item for doc in all_docs_items for item in doc if item["doc_id"] == "ASDOKU_4_TABLES_TOT"]

    print("\n=== MENYIMPAN 4 DATASET MODULAR ASDOKU (SESUAI DOKUMEN ASLI USER) ===")
    write_csv("dataset_asdoku_1_template_keseluruhan.csv", asdoku_1_items)
    write_csv("dataset_asdoku_2_headings_toc.csv", asdoku_2_items)
    write_csv("dataset_asdoku_3_figures.csv", asdoku_3_items)
    write_csv("dataset_asdoku_4_tables.csv", asdoku_4_items)

    print("\n=== MENYIMPAN 7 MASTER DATASETS SPESIALIS (MURNI DARI DATASET ASDOKU) ===")
    write_csv("dataset_1_cover_frontmatter.csv", d1_cover_frontmatter)
    write_csv("dataset_2_zoning.csv", d2_zoning)
    write_csv("dataset_3_headings_vs_lists.csv", d3_headings_vs_lists)
    write_csv("dataset_4_figures.csv", d4_figures)
    write_csv("dataset_5_tables.csv", d5_tables)
    write_csv("dataset_6_code_formulas.csv", d6_code_formulas)
    write_csv("dataset_7_body_bibliography.csv", d7_body_bibliography)
    print("========================================================================\n")

def main():
    test_files = [
        # HANYA MENGGUNAKAN 4 DOKUMEN GOLDEN DATASET BERSIH BUATAN USER
        ("Dataset Asdoku/Dataset Asdoku 1.docx", "ASDOKU_1_TEMPLATE_UTUH"),
        ("Dataset Asdoku/Dataset Asdoku 2.docx", "ASDOKU_2_TOC_HEADINGS"),
        ("Dataset Asdoku/Dataset Asdoku 3.docx", "ASDOKU_3_FIGURES_TOF"),
        ("Dataset Asdoku/Dataset Asdoku 4.docx", "ASDOKU_4_TABLES_TOT")
    ]

    all_docs_items = []
    for filepath, doc_id in test_files:
        if os.path.exists(filepath):
            print(f"Ekstraksi elemen dari: {filepath}...")
            items = extract_document_elements(filepath, doc_id)
            print(f"  -> {len(items)} elemen diekstraksi.")
            all_docs_items.append(items)
        else:
            print(f"[Skip] File tidak ditemukan: {filepath}")

    classify_and_distribute(all_docs_items)

if __name__ == "__main__":
    main()
