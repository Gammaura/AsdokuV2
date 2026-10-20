"""
MODUL ACTIVE LEARNING & AUTOMATED FEEDBACK LOOP
Multi-Agent Continuous Self-Improvement System.

Mekanisme:
1. Menangkap seluruh anomali / salah prediksi Agent 1 yang dikoreksi oleh Agent 2.
2. Menyimpan data paragraf beserta fitur OpenXML dan label kebenaran (ground truth) ke data/active_learning_feedback.csv.
3. Melakukan Continuous Retraining secara on-the-fly untuk meng-update model Machine Learning Agent 1.
4. Memberikan feedback langsung ke memori runtime InspectorAgent (hot-reload).
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from src.features import DocumentFeaturePipeline

IS_VERCEL = bool(os.environ.get("VERCEL"))
FEEDBACK_CSV = "/tmp/active_learning_feedback.csv" if IS_VERCEL else "data/active_learning_feedback.csv"
BASE_DATASET_CSV = "data/dataset_skripsi.csv"
MODEL_PATH = "models/baseline_model.joblib"
PIPELINE_PATH = "models/feature_pipeline.joblib"

class ActiveLearningManager:
    """
    Mengelola siklus umpan balik (Feedback Loop) antara Agent 2 (Critic) dan Agent 1 (Inspector).
    """
    def __init__(self, feedback_path: str = FEEDBACK_CSV, base_dataset_path: str = BASE_DATASET_CSV):
        self.feedback_path = feedback_path
        self.base_dataset_path = base_dataset_path
        os.makedirs(os.path.dirname(self.feedback_path), exist_ok=True)
        if not os.path.exists(self.feedback_path):
            # Inisialisasi file CSV feedback kosong dengan header yang sesuai
            df_init = pd.DataFrame(columns=[
                "doc_id", "para_id", "text", "style", "char_len", "word_count",
                "font_size", "is_bold", "is_italic", "align", "has_num", "has_img",
                "has_pgbrk", "space_before", "space_after", "line_spacing",
                "first_line_indent", "left_indent", "uppercase_ratio", "doc_pos", "label"
            ])
            df_init.to_csv(self.feedback_path, index=False)

    def record_corrections(self, source_doc: str, corrected_items: List[Dict[str, Any]]) -> int:
        """
        Menyimpan paragraf yang dikoreksi oleh Agent 2 ke dalam pool feedback active learning.
        Menghindari duplikasi teks yang sama dengan label yang sama.
        """
        if not corrected_items:
            return 0

        # Baca feedback yang sudah ada
        if os.path.exists(self.feedback_path) and os.path.getsize(self.feedback_path) > 0:
            df_existing = pd.read_csv(self.feedback_path)
        else:
            df_existing = pd.DataFrame()

        existing_keys = set()
        if not df_existing.empty and "text" in df_existing.columns and "label" in df_existing.columns:
            for _, row in df_existing.iterrows():
                existing_keys.add((str(row["text"]).strip().lower(), str(row["label"])))

        new_rows = []
        doc_name = os.path.basename(source_doc)

        for item in corrected_items:
            raw = item.get("raw_features", {})
            text = item.get("text", "")
            final_label = item.get("approved_label", "BODY_PARAGRAPH")

            key = (str(text).strip().lower(), str(final_label))
            if key in existing_keys:
                continue

            existing_keys.add(key)
            row_dict = {
                "doc_id": f"FEEDBACK_{doc_name}",
                "para_id": item.get("para_id", 0),
                "text": text,
                "style": raw.get("style", "Normal"),
                "char_len": raw.get("char_len", len(text)),
                "word_count": raw.get("word_count", len(text.split())),
                "font_size": raw.get("font_size", 12.0),
                "is_bold": raw.get("is_bold", False),
                "is_italic": raw.get("is_italic", False),
                "align": raw.get("align", "JUSTIFY"),
                "has_num": raw.get("has_num", False),
                "has_img": raw.get("has_img", False),
                "has_pgbrk": raw.get("has_pgbrk", False),
                "space_before": raw.get("space_before", 0.0),
                "space_after": raw.get("space_after", 0.0),
                "line_spacing": raw.get("line_spacing", 1.15),
                "first_line_indent": raw.get("first_line_indent", 0.0),
                "left_indent": raw.get("left_indent", 0.0),
                "uppercase_ratio": raw.get("uppercase_ratio", 0.0),
                "doc_pos": raw.get("doc_pos", 0.0),
                "label": final_label
            }
            new_rows.append(row_dict)

        if new_rows:
            df_new = pd.DataFrame(new_rows)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(self.feedback_path, index=False)
            print(f"[Active Learning] Berhasil menyimpan {len(new_rows)} sampel koreksi baru ke: {self.feedback_path}")
            return len(new_rows)

        return 0

    def get_stats(self) -> Dict[str, Any]:
        """
        Mengambil statistik sampel koreksi yang terkumpul di pool feedback.
        """
        if not os.path.exists(self.feedback_path) or os.path.getsize(self.feedback_path) == 0:
            return {"total_feedback": 0, "class_distribution": {}}

        df = pd.read_csv(self.feedback_path)
        total = len(df)
        dist = df["label"].value_counts().to_dict() if "label" in df.columns else {}
        return {
            "total_feedback": total,
            "class_distribution": dist
        }

    def retrain_agent_1(self) -> Dict[str, Any]:
        """
        Melatih ulang (Retraining) model Machine Learning Agent 1 dengan
        menggabungkan dataset utama dan seluruh sampel koreksi Agent 2.
        """
        print("\n[Active Learning Retraining] Memulai proses Continuous Retraining untuk Agent 1...")

        df_base = pd.read_csv(self.base_dataset_path)
        if os.path.exists(self.feedback_path) and os.path.getsize(self.feedback_path) > 0:
            df_fb = pd.read_csv(self.feedback_path)
        else:
            df_fb = pd.DataFrame()

        # Gabungkan dataset (beri bobot ekstra pada data feedback dengan menyalinnya 3x agar model benar-benar belajar dari koreksi)
        if not df_fb.empty:
            df_fb_weighted = pd.concat([df_fb] * 3, ignore_index=True)
            df_train_all = pd.concat([df_base, df_fb_weighted], ignore_index=True)
            print(f"[Active Learning] Menggabungkan {len(df_base)} sampel basis + {len(df_fb)} sampel feedback (weighted 3x = {len(df_fb_weighted)})")
        else:
            df_train_all = df_base
            print(f"[Active Learning] Melatih ulang pada {len(df_base)} sampel basis...")

        y = df_train_all["label"].values

        # Fitur pipeline baru
        pipeline = DocumentFeaturePipeline(max_tfidf_features=400)
        X = pipeline.fit_transform(df_train_all)

        # Split train/test
        class_counts = df_train_all["label"].value_counts()
        can_stratify = (class_counts.min() >= 2)
        stratify_target = y if can_stratify else None

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=stratify_target
        )

        # Latih Balanced Random Forest
        clf = RandomForestClassifier(
            n_estimators=120,
            random_state=42,
            max_depth=16,
            class_weight='balanced'
        )
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        new_acc = accuracy_score(y_test, y_pred)
        rep = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        # Simpan model baru
        joblib.dump(clf, MODEL_PATH)
        joblib.dump(pipeline, PIPELINE_PATH)

        print(f"[Active Learning] Retraining SELESAI! Akurasi Model Baru: {new_acc * 100:.2f}%")

        return {
            "status": "success",
            "new_accuracy": round(new_acc * 100, 2),
            "macro_f1": round(rep["macro avg"]["f1-score"], 4),
            "weighted_f1": round(rep["weighted avg"]["f1-score"], 4),
            "total_training_samples": len(df_train_all),
            "feedback_samples_used": len(df_fb)
        }
