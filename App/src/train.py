"""
Modul Pelatihan Machine Learning (Training Pipeline & Model Evaluation).

Tahap 3 Metodologi Skripsi:
Modul ini bertugas:
1. Membaca dataset dari data/dataset_skripsi.csv.
2. Mengekstraksi fitur gabungan (Hybrid):
   - Fitur Teks: TF-IDF (N-gram 1-2).
   - Fitur Metadata: Font size, bold, italic, uppercase ratio, alignment, numPr, drawing, page break, posisi dokumen.
3. Melatih model klasifikasi (Logistic Regression & Random Forest).
4. Menghasilkan metrik evaluasi lengkap (Precision, Recall, F1-Score, Confusion Matrix).
5. Mengekspor model terlatih ke models/baseline_model.joblib dan pipeline ke models/feature_pipeline.joblib.
"""

import os
import re
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from src.features import DocumentFeaturePipeline

def train_and_evaluate(dataset_csv: str = "data/dataset_skripsi.csv"):
    print(f"=== MEMULAI PELATIHAN MODEL MACHINE LEARNING DARI: {dataset_csv} ===")
    df = pd.read_csv(dataset_csv)
    print(f"[*] Jumlah sampel data termuat: {len(df)} baris")

    # Siapkan Target
    y = df["label"].values

    # Ekstraksi Fitur Hybrid
    pipeline = DocumentFeaturePipeline(max_tfidf_features=400)
    X = pipeline.fit_transform(df)
    print(f"[*] Dimensi matriks fitur gabungan: {X.shape[0]} sampel x {X.shape[1]} fitur")

    # Pembagian Data Latih & Uji (80% Train, 20% Test)
    # Gunakan stratify jika setiap kelas memiliki minimal 2 sampel
    class_counts = df["label"].value_counts()
    can_stratify = (class_counts.min() >= 2)
    stratify_target = y if can_stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=stratify_target
    )
    print(f"[*] Pembagian data: {X_train.shape[0]} data latih (Train), {X_test.shape[0]} data uji (Test)\n")

    # Inisialisasi Model dengan Penanganan Ketimpangan Data (Balanced Class Weights)
    models = {
        "Logistic Regression (Balanced)": LogisticRegression(max_iter=1000, random_state=42, C=1.0, class_weight='balanced'),
        "Random Forest (Balanced)": RandomForestClassifier(n_estimators=100, random_state=42, max_depth=14, class_weight='balanced')
    }

    best_model_name = None
    best_accuracy = -1.0
    best_model_obj = None
    reports_md = []

    for name, clf in models.items():
        print(f"--- MELATIH MODEL: {name} ---")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"-> Akurasi Keseluruhan: {acc * 100:.2f}%\n")
        
        rep_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        rep_text = classification_report(y_test, y_pred, zero_division=0)
        print(rep_text)

        # Siapkan laporan Markdown untuk naskah skripsi
        md_table = f"### Hasil Pengujian Model: {name}\n\n"
        md_table += f"**Akurasi Keseluruhan:** `{acc * 100:.2f}%`\n\n"
        md_table += "| Kelas Struktur Dokumen | Precision | Recall | F1-Score | Jumlah Data Uji (Support) |\n"
        md_table += "|---|---|---|---|---|\n"
        
        for label, metrics in rep_dict.items():
            if label in ["accuracy", "macro avg", "weighted avg"]:
                continue
            md_table += f"| `{label:<20}` | {metrics['precision']:.4f} | {metrics['recall']:.4f} | **{metrics['f1-score']:.4f}** | {int(metrics['support'])} |\n"
        
        md_table += f"| **Rata-rata Macro** | {rep_dict['macro avg']['precision']:.4f} | {rep_dict['macro avg']['recall']:.4f} | **{rep_dict['macro avg']['f1-score']:.4f}** | {int(rep_dict['macro avg']['support'])} |\n"
        md_table += f"| **Rata-rata Weighted** | {rep_dict['weighted avg']['precision']:.4f} | {rep_dict['weighted avg']['recall']:.4f} | **{rep_dict['weighted avg']['f1-score']:.4f}** | {int(rep_dict['weighted avg']['support'])} |\n\n"
        
        reports_md.append(md_table)

        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model_obj = clf

    # Simpan Artifact Model
    os.makedirs("models", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    joblib.dump(best_model_obj, "models/baseline_model.joblib")
    joblib.dump(pipeline, "models/feature_pipeline.joblib")
    print(f"[SUKSES] Model terbaik ({best_model_name} - {best_accuracy*100:.2f}%) tersimpan di: models/baseline_model.joblib")
    print(f"[SUKSES] Pipeline fitur tersimpan di: models/feature_pipeline.joblib")

    # Simpan Laporan Markdown untuk Bab 4
    report_file = "output/eval_report_expanded.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Laporan Evaluasi Model Klasifikasi Struktur Dokumen (Setelah Ekspansi Dataset)\n\n")
        f.write(f"**Tanggal Pengujian:** 13 Oktober 2026\n")
        f.write(f"**Jumlah Dataset:** {len(df)} Paragraf (4 Dokumen: 80% Train, 20% Test)\n")
        f.write(f"**Fitur:** TF-IDF (N-gram 1-2) + Tipografi OpenXML\n\n---\n\n")
        f.write("\n".join(reports_md))

    print(f"[SUKSES] Laporan evaluasi ilmiah Bab 4 tersimpan di: {report_file}")

if __name__ == "__main__":
    train_and_evaluate()
