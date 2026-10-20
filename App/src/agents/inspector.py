"""
AGENT 1: INSPECTOR (Detection & Classification Agent).

Tugas & Peran:
1. Membaca naskah mentah Word (.docx) secara non-destruktif.
2. Mengekstraksi fitur teks NLP dan metadata tipografi OpenXML per paragraf.
3. Melakukan inferensi probabilistik menggunakan Model Machine Learning terlatih (Random Forest 93.71%).
4. Menghasilkan skor kepercayaan (Confidence Score) untuk setiap paragraf.
5. Menandai paragraf ambigu (confidence < 0.70) untuk diserahkan ke Agent 2 (Critic).
"""

import os
import re
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

from src.features import DocumentFeaturePipeline
from src.dataset_generator import clean_text, get_font_info, get_alignment_str

class InspectorAgent:
    """
    Agent 1: Detection & Classification Agent.
    """
    def __init__(self, 
                 model_path: str = "models/baseline_model.joblib", 
                 pipeline_path: str = "models/feature_pipeline.joblib"):
        
        if not os.path.exists(model_path) or not os.path.exists(pipeline_path):
            raise FileNotFoundError("Model atau Pipeline ML belum ditemukan. Jalankan src/train.py terlebih dahulu.")
        
        self.model_path = model_path
        self.pipeline_path = pipeline_path
        self.model = joblib.load(model_path)
        self.pipeline = joblib.load(pipeline_path)
        self.classes = list(self.model.classes_)
        print("[Agent 1 - Inspector] Model & Feature Pipeline berhasil dimuat.")

    def reload_model(self):
        """
        Memuat ulang model & pipeline ML setelah proses Active Learning Retraining (Hot-Reload).
        """
        self.model = joblib.load(self.model_path)
        self.pipeline = joblib.load(self.pipeline_path)
        self.classes = list(self.model.classes_)
        print("[Agent 1 - Inspector] HOT-RELOAD: Model & Feature Pipeline berhasil diperbarui dari Active Learning!")

    def inspect(self, docx_path: str) -> Dict[str, Any]:
        """
        Menganalisis dokumen Word dan menerbitkan Draft Blueprint.
        """
        print(f"\n[Agent 1 - Inspector] Memulai inspeksi naskah: {docx_path}...")
        doc = Document(docx_path)
        total_p = len(doc.paragraphs)
        
        raw_items = []
        for idx, p in enumerate(doc.paragraphs):
            text = clean_text(p.text)
            size, bold, italic = get_font_info(p)
            align = get_alignment_str(p.alignment)
            
            pPr = p._p.pPr
            has_num = bool(pPr is not None and pPr.numPr is not None)
            has_img = bool(p._p.xpath(".//w:drawing") or p._p.xpath(".//w:pict"))
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

            raw_items.append({
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

        df = pd.DataFrame(raw_items)
        
        # Transformasi Fitur & Inferensi Probabilistik
        X = self.pipeline.transform(df)
        probas = self.model.predict_proba(X)
        predictions = self.model.predict(X)

        paragraphs_blueprint = []
        ambiguous_count = 0
        detected_chapters = []
        detected_subchapters = []
        detected_captions = []

        for idx, item in enumerate(raw_items):
            pred_label = predictions[idx]
            prob_dist = {cls_name: round(float(probas[idx][c_idx]), 4) for c_idx, cls_name in enumerate(self.classes)}
            confidence = float(np.max(probas[idx]))
            is_ambiguous = confidence < 0.70

            t_clean = item["text"].strip()
            up_t = t_clean.upper().rstrip('.:;')
            words = up_t.split()
            w_count = len(words)

            # 0. Override otomatis untuk elemen gambar atau paragraf kosong
            if item["char_len"] == 0:
                pred_label = "BODY_PARAGRAPH" if item["has_img"] else "LAINNYA"
                confidence = 0.99
                is_ambiguous = False
            # 1. Penyelarasan Halaman Sampul (Cover Metadata)
            elif item["doc_pos"] < 0.15 and any(k in up_t for k in ["TUGAS AKHIR", "SKRIPSI", "LAPORAN KERJA PRAKTIK", "PROGRAM STUDI", "FAKULTAS", "UNIVERSITAS ESA UNGGUL", "TAHUN 202", "DIAJUKAN SEBAGAI", "NAMA :", "NIM :"]):
                pred_label = "COVER_METADATA"
                confidence = 0.99
                is_ambiguous = False
            # 2. Penyelarasan Cerdas Metadata Form/Pernyataan/Pengesahan
            elif any(k in up_t for k in ["NAMA :", "NIM :", "NAME :", "STUDENT ID", "STUDY PROGRAM", "TANDA TANGAN", "TANGGAL :", "DIBUAT DI", "DITETAPKAN DI", "TIM PENGUJI", "PENGUJI I", "PENGUJI II", "TAHUN 202", "KATA KUNCI", "KEYWORDS"]):
                pred_label = "BODY_PARAGRAPH"
                confidence = 0.99
                is_ambiguous = False
            # 3. Penyelarasan Judul Frontmatter Baku UEU
            elif w_count <= 10 and any(up_t == kw or up_t.startswith(kw) for kw in [
                "ABSTRAK", "ABSTRACT", "KATA PENGANTAR", "PRAKATA", "DAFTAR ISI", "DAFTAR TABEL", 
                "DAFTAR GAMBAR", "DAFTAR SIMBOL", "DAFTAR LAMPIRAN", "HALAMAN PERNYATAAN", 
                "HALAMAN PENGESAHAN", "HALAMAN PERSETUJUAN", "HALAMAN PERSETUJUAN PUBLIKASI",
                "PERSETUJUAN PUBLIKASI", "UNTUK KEPENTINGAN AKADEMIS",
                "DAFTAR REFERENSI", "DAFTAR PUSTAKA"
            ]):
                pred_label = "FRONTMATTER_TITLE"
                confidence = 0.99
                is_ambiguous = False
            # 4. Penyelarasan Judul Bab Baku UEU (Kanonikal / BAB I - V)
            elif w_count <= 5 and any(up_t == n or up_t.startswith(f"BAB ") for n in [
                "PENDAHULUAN", "TINJAUAN PUSTAKA", "LANDASAN TEORI", "METODE", "METODOLOGI", 
                "METODE PENELITIAN", "HASIL DAN PEMBAHASAN", "KESIMPULAN DAN SARAN"
            ]):
                pred_label = "JUDUL_BAB"
                confidence = 0.99
                is_ambiguous = False
            # 5. Penyelarasan Caption Gambar & Tabel
            elif re.match(r'^(Gambar|Figure|Tabel|Table)\s*[\.\d]', t_clean, re.IGNORECASE) and w_count <= 25:
                narrative_verbs = ["memperlihatkan", "menunjukkan", "menyajikan", "menjelaskan", "terlihat", "tampak", "merupakan", "adalah", "berisi", "menegaskan", "menggambarkan"]
                rest_cap = re.sub(r'^(Gambar|Figure|Tabel|Table)\s*[\.\d\s:\-]+', '', t_clean, flags=re.IGNORECASE).strip().lower()
                first_w = rest_cap.split()[0] if rest_cap.split() else ""
                if first_w in narrative_verbs:
                    pred_label = "BODY_PARAGRAPH"
                    confidence = 0.95
                    is_ambiguous = False
                else:
                    pred_label = "CAPTION_GAMBAR" if t_clean.lower().startswith(("gambar", "figure")) else "CAPTION_TABEL"
                    confidence = 0.99
                    is_ambiguous = False
            # 6. Penyelarasan Sub-bab Baku Akademik UEU & Pola Heading
            elif w_count <= 8 and not t_clean.endswith('.') and any(up_t == sb or up_t.startswith(sb) for sb in [
                "LATAR BELAKANG", "IDENTIFIKASI MASALAH", "RUMUSAN MASALAH", "BATASAN MASALAH",
                "TUJUAN", "MANFAAT", "RUANG LINGKUP", "LINGKUP", "KERANGKA BERPIKIR", "SISTEMATIKA PENULISAN",
                "PROFIL PERUSAHAAN", "VISI DAN MISI", "STRUKTUR ORGANISASI", "TEORI", "LANDASAN",
                "RENCANA PENELITIAN", "OBYEK PENELITIAN", "POPULASI DAN SAMPEL", "TEKNIK PENGUMPULAN DATA",
                "ANALISIS KEBUTUHAN", "KEBUTUHAN FUNGSIONAL", "DATA HASIL PENELITIAN", "PEMBAHASAN HASIL PENELITIAN",
                "ANALISIS DATA", "PERBANDINGAN DENGAN PENELITIAN LAIN", "KESIMPULAN", "SARAN"
            ]):
                pred_label = "SUB_BAB"
                confidence = 0.99
                is_ambiguous = False
            # 7. Penyelarasan Sub-bab & Sub-sub-bab dari Style bawaan naskah (Heading 2, Heading 3) atau Pola Angka
            elif item["style"] in ["Heading 2", "Heading 3", "Heading2", "Heading3"] or re.match(r'^\d+\.\d+(\.\d+)*\b', t_clean):
                pred_label = "SUB_BAB"
                confidence = 0.99
                is_ambiguous = False

            if is_ambiguous:
                ambiguous_count += 1

            record = {
                "para_id": item["para_id"],
                "text": item["text"],
                "predicted_label": pred_label,
                "confidence": round(confidence, 4),
                "is_ambiguous": is_ambiguous,
                "probabilities": prob_dist,
                "raw_features": item,
                "metadata": {
                    "style": item["style"],
                    "is_subsub": bool(item["style"] in ["Heading 3", "Heading3"] or re.match(r'^\d+\.\d+\.\d+', t_clean)),
                    "font_size": item["font_size"],
                    "is_bold": item["is_bold"],
                    "align": item["align"],
                    "has_num": item["has_num"],
                    "has_img": item["has_img"],
                    "has_pgbrk": item["has_pgbrk"],
                    "doc_pos": item["doc_pos"]
                }
            }

            if pred_label == "JUDUL_BAB":
                detected_chapters.append(f"P[{item['para_id']}] {item['text'][:40]}")
            elif pred_label == "SUB_BAB":
                detected_subchapters.append(f"P[{item['para_id']}] {item['text'][:40]}")
            elif pred_label in ["CAPTION_GAMBAR", "CAPTION_TABEL"]:
                detected_captions.append(f"P[{item['para_id']}] {item['text'][:40]}")

            paragraphs_blueprint.append(record)

        # Laporan Ringkasan Hasil Inspeksi
        label_summary = pd.Series([p["predicted_label"] for p in paragraphs_blueprint]).value_counts().to_dict()

        inspection_report = {
            "source_doc": docx_path,
            "total_paragraphs": total_p,
            "ambiguous_count": ambiguous_count,
            "label_summary": label_summary,
            "detected_chapters_count": len(detected_chapters),
            "detected_subchapters_count": len(detected_subchapters),
            "detected_captions_count": len(detected_captions),
            "chapters_preview": detected_chapters[:5],
            "paragraphs": paragraphs_blueprint
        }

        print(f"[Agent 1 - Inspector] Selesai! Terdeteksi {len(detected_chapters)} Bab, {len(detected_subchapters)} Sub-Bab, {ambiguous_count} Paragraf Ambigu.")
        return inspection_report

    def re_inspect_with_feedback(self, current_report: Dict[str, Any], feedback_directives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        [SQA TIER 1 FEEDBACK LOOP]
        Menerima koreksi & instruksi perbaikan dari Agent 2 (SQA Auditor),
        kemudian merevisi label blueprint, memperbarui confidence score,
        dan memvalidasi ulang konsistensi konteks.
        """
        print(f"[Agent 1 - Inspector] Menerima {len(feedback_directives)} umpan balik dari Agent 2 (SQA). Melakukan re-inspeksi & penyesuaian...")
        directive_map = {item["para_id"]: item for item in feedback_directives}
        
        paragraphs = current_report["paragraphs"]
        re_ambiguous_count = 0
        detected_chapters = []
        detected_subchapters = []
        detected_captions = []

        for p in paragraphs:
            pid = p["para_id"]
            if pid in directive_map:
                directive = directive_map[pid]
                p["predicted_label"] = directive["corrected_label"]
                p["confidence"] = 0.999
                p["is_ambiguous"] = False
                p["metadata"]["sqa_corrected"] = True
                p["metadata"]["sqa_reason"] = directive.get("reason", "Direvisi berdasarkan audit SQA Agent 2")

            if p.get("is_ambiguous", False):
                re_ambiguous_count += 1

            lbl = p["predicted_label"]
            if lbl == "JUDUL_BAB":
                detected_chapters.append(f"P[{pid}] {p['text'][:40]}")
            elif lbl == "SUB_BAB":
                detected_subchapters.append(f"P[{pid}] {p['text'][:40]}")
            elif lbl in ["CAPTION_GAMBAR", "CAPTION_TABEL"]:
                detected_captions.append(f"P[{pid}] {p['text'][:40]}")

        label_summary = pd.Series([p["predicted_label"] for p in paragraphs]).value_counts().to_dict()

        revised_report = {
            "source_doc": current_report["source_doc"],
            "total_paragraphs": current_report["total_paragraphs"],
            "ambiguous_count": re_ambiguous_count,
            "label_summary": label_summary,
            "detected_chapters_count": len(detected_chapters),
            "detected_subchapters_count": len(detected_subchapters),
            "detected_captions_count": len(detected_captions),
            "chapters_preview": detected_chapters[:5],
            "paragraphs": paragraphs,
            "sqa_iteration": current_report.get("sqa_iteration", 1) + 1
        }
        print(f"[Agent 1 - Inspector] Re-inspeksi selesai! Blueprint diperbarui dengan tingkat kepastian tinggi.")
        return revised_report


if __name__ == "__main__":
    inspector = InspectorAgent()
    report = inspector.inspect("contoh.docx")
    print("\n--- RINGKASAN BLUEPRINT DRAF DARI AGENT 1 ---")
    print(f"Total Paragraf: {report['total_paragraphs']}")
    print(f"Distribusi Prediksi: {report['label_summary']}")
    print(f"Bab Terdeteksi: {report['chapters_preview']}")
