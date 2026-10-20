"""
Modul Pipeline Ekstraksi Fitur Dokumen (Feature Engineering).
Dibuat mandiri agar dapat di-pickle dan di-load secara universal di semua agen.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

class DocumentFeaturePipeline:
    """
    Pipeline ekstraksi fitur gabungan (TF-IDF Teks + Metadata Tipografi OpenXML).
    """
    def __init__(self, max_tfidf_features: int = 400):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=max_tfidf_features,
            lowercase=True
        )
        self.align_categories = ["CENTER", "JUSTIFY", "LEFT", "RIGHT", "DEFAULT"]

    def _extract_meta_features(self, df: pd.DataFrame) -> np.ndarray:
        meta_rows = []
        for _, row in df.iterrows():
            char_len = float(row.get("char_len", 0)) / 400.0
            word_count = float(row.get("word_count", 0)) / 80.0
            uppercase_ratio = float(row.get("uppercase_ratio", 0.0))
            font_size = float(row.get("font_size", 12.0)) / 14.0
            is_bold = 1.0 if row.get("is_bold", False) else 0.0
            is_italic = 1.0 if row.get("is_italic", False) else 0.0
            has_num = 1.0 if row.get("has_num", False) else 0.0
            has_img = 1.0 if row.get("has_img", False) else 0.0
            has_pgbrk = 1.0 if row.get("has_pgbrk", False) else 0.0
            sb = float(row.get("space_before", 0.0)) / 24.0
            sa = float(row.get("space_after", 0.0)) / 12.0
            ls = float(row.get("line_spacing", 1.15)) / 1.5
            fl = float(row.get("first_line_indent", 0.0)) / 1.27
            li = float(row.get("left_indent", 0.0)) / 2.0
            doc_pos = float(row.get("doc_pos", 0.0))

            # One-hot alignment
            align = str(row.get("align", "DEFAULT"))
            align_onehot = [1.0 if align == cat else 0.0 for cat in self.align_categories]

            features = [
                char_len,
                word_count,
                uppercase_ratio,
                font_size,
                is_bold,
                is_italic,
                has_num,
                has_img,
                has_pgbrk,
                sb,
                sa,
                ls,
                fl,
                li,
                doc_pos
            ] + align_onehot

            meta_rows.append(features)

        return np.array(meta_rows, dtype=np.float32)

    def fit_transform(self, df: pd.DataFrame) -> csr_matrix:
        texts = df["text"].fillna("").astype(str).tolist()
        X_tfidf = self.vectorizer.fit_transform(texts)
        X_meta = csr_matrix(self._extract_meta_features(df))
        return hstack([X_tfidf, X_meta]).tocsr()

    def transform(self, df: pd.DataFrame) -> csr_matrix:
        texts = df["text"].fillna("").astype(str).tolist()
        X_tfidf = self.vectorizer.transform(texts)
        X_meta = csr_matrix(self._extract_meta_features(df))
        return hstack([X_tfidf, X_meta]).tocsr()
