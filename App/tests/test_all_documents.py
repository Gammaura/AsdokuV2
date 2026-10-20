"""
Test Suite Pengujian Otomatis Sistem Multi-Agent (MAS) Asdoku
Menguji 5 Dokumen Uji Resmi (P1 - P5) dari data/dokumen_uji/
"""

import os
import sys
import time

# Pastikan root workspace masuk ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.inspector import InspectorAgent
from src.agents.critic import QualityCriticAgent
from src.agents.formatter import FormattingActuatorAgent

def test_pipeline():
    print("=" * 75)
    print("  ASDOKU MULTI-AGENT SYSTEM (MAS) — PENGUJIAN OTOMATIS SUITE P1 S/D P5")
    print("=" * 75)

    inspector = InspectorAgent()
    critic = QualityCriticAgent()
    formatter = FormattingActuatorAgent()

    test_docs = [
        ("P1", "P1_Template_Resmi_UEU.docx", "Template Resmi Tugas Akhir UEU"),
        ("P2", "P2_Skripsi_Mbkm_Dhicky.docx", "Skripsi MBKM Mandiri Dhicky"),
        ("P3", "P3_Proposal_Bab1_3_PBB.docx", "Naskah Proposal Bab I-III"),
        ("P4", "P4_Laporan_Mbkm_Arditya.docx", "Laporan MBKM Arditya"),
        ("P5", "P5_Buku_TA_Landscape.docx", "Template Buku TA Section Landscape")
    ]

    os.makedirs("output/pengujian", exist_ok=True)
    summary_results = []

    for code, fname, label in test_docs:
        in_path = os.path.join("data/dokumen_uji", fname)
        out_name = f"(Asdoku) - {fname}"
        out_path = os.path.join("output/pengujian", out_name)

        print(f"\n[{code}] Menguji: {label} ({fname})...")
        start = time.time()

        # 1. Inspector
        draft = inspector.inspect(in_path)
        # 2. Quality Critic
        approved = critic.evaluate_and_refine(draft)
        # 3. Formatter Actuator
        res_file = formatter.format_document(in_path, approved, out_path)
        
        elapsed = round(time.time() - start, 2)
        summary_results.append({
            "code": code,
            "name": fname,
            "paras": draft["total_paragraphs"],
            "corrections": approved["total_corrections"],
            "chapters": len(approved["approved_chapters"]),
            "time": elapsed,
            "status": "PASS" if os.path.exists(res_file) else "FAIL"
        })
        print(f"[{code}] SELESAI ({elapsed}s) -> Disimpan ke: {res_file}")

    print("\n" + "=" * 75)
    print("                      HASIL PENGUJIAN SELURUH DOKUMEN")
    print("=" * 75)
    print(f"{'Kode':<6} | {'Dokumen':<32} | {'Paragraf':<8} | {'Koreksi':<8} | {'Waktu':<7} | {'Status'}")
    print("-" * 75)
    for r in summary_results:
        print(f"{r['code']:<6} | {r['name']:<32} | {r['paras']:<8} | {r['corrections']:<8} | {r['time']:<5}s | {r['status']}")
    print("=" * 75)

if __name__ == "__main__":
    test_pipeline()
