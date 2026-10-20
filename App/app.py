"""
Aplikasi Web Multi-Page untuk Seminar Proposal & Pengujian Multi-Agent System (Asdoku).
Dibangun dengan FastAPI + Multi-Page Architecture (MPA) + Vanilla CSS Modern.

Halaman:
1. /          -> Home (Cover Seminar Proposal Elegan)
2. /alat      -> Alat (Studio Pengujian Multi-Agent .docx)
3. /data      -> Data (Metodologi Riset & Evaluasi Empiris Model)
4. /flowchart -> Pembahasan: Flowchart Sistem & Two-Tier SQA
5. /pipeline  -> Pembahasan: Arsitektur Tiga Agen Cerdas
6. /riwayat   -> Pembahasan: Kronologi 5 Babak Riset & Catatan Sempro
7. /info      -> Info (Glosarium 16 Istilah Teknis Akademik AI & OpenXML)
"""

import os
import re
import time
import shutil
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn

from src.agents.inspector import InspectorAgent
from src.agents.critic import QualityCriticAgent
from src.agents.formatter import FormattingActuatorAgent
from src.active_learning import ActiveLearningManager

app = FastAPI(
    title="Asdoku MAS Tester",
    description="Web Pengujian Multi-Agent System Dokumen Akademik UEU",
    redirect_slashes=False
)

IS_VERCEL = bool(os.environ.get("VERCEL"))
UPLOAD_DIR = "/tmp/uploads" if IS_VERCEL else "data/uploads"
OUTPUT_DIR = "/tmp/output" if IS_VERCEL else "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Inisialisasi Agen & Active Learning Manager
print("[SYSTEM] Menginisialisasi Multi-Agent System & Active Learning Loop...")
inspector = InspectorAgent()
critic = QualityCriticAgent()
formatter = FormattingActuatorAgent()
active_learning = ActiveLearningManager()
print("[SYSTEM] Seluruh Agen & Self-Improvement Loop Siap Beroperasi!")

# ============================================================
# TEMPLATE LOADER & MULTI-PAGE RENDERER
# ============================================================
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def load_template(filename: str) -> str:
    path = os.path.join(TEMPLATE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_page(
    page_id: str,
    content_filename: str,
    breadcrumb_links: list = None,
    pembahasan_label: str = "Pembahasan",
    scripts: str = ""
) -> str:
    is_pembahasan = page_id in ["flowchart", "pipeline", "riwayat"]

    html = load_template("base.html")
    content_html = load_template(content_filename)
    html = html.replace("{{active_home}}", "active" if page_id == "home" else "")
    html = html.replace("{{active_alat}}", "active" if page_id == "alat" else "")
    html = html.replace("{{active_data}}", "active" if page_id == "data" else "")
    html = html.replace("{{active_pembahasan}}", "active" if is_pembahasan else "")
    html = html.replace("{{active_info}}", "active" if page_id == "info" else "")
    html = html.replace("{{pembahasan_label}}", pembahasan_label)
    html = html.replace("{{active_flowchart}}", "active-item" if page_id == "flowchart" else "")
    html = html.replace("{{active_pipeline}}", "active-item" if page_id == "pipeline" else "")
    html = html.replace("{{active_riwayat}}", "active-item" if page_id == "riwayat" else "")
    html = html.replace("{{content}}", content_html)
    html = html.replace("{{scripts}}", scripts)
    return html


# ============================================================
# MULTI-PAGE ROUTES (Option 2: True MPA with unique URLs)
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def page_home():
    return render_page(
        page_id="home",
        content_filename="home.html",
        breadcrumb_links=[("Home", "/")]
    )

@app.get("/alat", response_class=HTMLResponse)
async def page_alat():
    alat_js = f"<script>\n{load_template('alat.js')}\n</script>"
    return render_page(
        page_id="alat",
        content_filename="alat.html",
        breadcrumb_links=[("Home", "/"), ("Alat", "/alat"), ("Studio Pengujian Multi-Agent (.docx)", None)],
        scripts=alat_js
    )

@app.get("/data", response_class=HTMLResponse)
async def page_data():
    return render_page(
        page_id="data",
        content_filename="data.html",
        breadcrumb_links=[("Home", "/"), ("Data", "/data"), ("Evaluasi Model & Lompatan Akurasi", None)]
    )

@app.get("/flowchart", response_class=HTMLResponse)
async def page_flowchart():
    return render_page(
        page_id="flowchart",
        content_filename="flowchart.html",
        breadcrumb_links=[("Home", "/"), ("Pembahasan", "/flowchart"), ("Flowchart Sistem & Two-Tier SQA", None)],
        pembahasan_label="Pembahasan: Flowchart"
    )

@app.get("/pipeline", response_class=HTMLResponse)
@app.get("/agen", response_class=HTMLResponse)
async def page_pipeline():
    return render_page(
        page_id="pipeline",
        content_filename="pipeline.html",
        breadcrumb_links=[("Home", "/"), ("Pembahasan", "/pipeline"), ("Arsitektur Tiga Agen Cerdas", None)],
        pembahasan_label="Pembahasan: 3 Agen"
    )

@app.get("/riwayat", response_class=HTMLResponse)
async def page_riwayat():
    return render_page(
        page_id="riwayat",
        content_filename="riwayat.html",
        breadcrumb_links=[("Home", "/"), ("Pembahasan", "/riwayat"), ("Kronologi 5 Babak Riset & Seminar Proposal", None)],
        pembahasan_label="Pembahasan: Kronologi"
    )

@app.get("/info", response_class=HTMLResponse)
async def page_info():
    return render_page(
        page_id="info",
        content_filename="info.html",
        breadcrumb_links=[("Home", "/"), ("Info", "/info"), ("Glosarium Istilah Akademik", None)]
    )


# ============================================================
# API ENDPOINTS (Format, Feedback, Retrain, & Assets)
# ============================================================

def run_auto_retrain():
    try:
        active_learning.retrain_agent_1()
        inspector.reload_model()
        print("[Active Learning] Background Retraining & Hot-Reload berhasil diselesaikan!")
    except Exception as e:
        print(f"[Active Learning] Background Retraining error: {e}")

@app.post("/api/format")
async def api_format_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Hanya berkas .docx yang didukung.")

    start_time = time.time()
    temp_input = os.path.join(UPLOAD_DIR, f"upload_{int(time.time())}_{file.filename}")
    with open(temp_input, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_name = file.filename
    clean_name = re.sub(r'^(?:rapi_\d+_|upload_\d+_|\(Asdoku\)\s*-\s*)+', '', raw_name)
    output_filename = f"(Asdoku) - {clean_name}"
    temp_output = os.path.join(OUTPUT_DIR, output_filename)

    # 1. SQA Tier 1 Loop: Agent 1 (Inspector) <-> Agent 2 (SQA Gatekeeper)
    draft = inspector.inspect(temp_input)
    approved = critic.coordinate_tier1_blueprint_loop(
        inspection_report=draft,
        inspector_agent=inspector,
        max_iterations=3
    )

    # 2. SQA Tier 2 Loop: Agent 3 (Formatter) <-> Agent 2 (SQA Acceptance Auditor)
    tier2_res = critic.coordinate_tier2_artifact_loop(
        input_docx_path=temp_input,
        approved_blueprint=approved,
        output_docx_path=temp_output,
        formatter_agent=formatter,
        max_iterations=3
    )
    qa_result = tier2_res["final_qa_result"]

    # 3. Otomatisasi Continuous Self-Learning
    if approved.get("total_corrections", 0) > 0:
        print(f"[Active Learning] Menjadwalkan Retraining Mandiri di Latar Belakang untuk {approved['total_corrections']} sampel...")
        background_tasks.add_task(run_auto_retrain)

    elapsed_time = round(time.time() - start_time, 2)

    return {
        "status": "success",
        "output_filename": output_filename,
        "elapsed_time": elapsed_time,
        "total_paragraphs": draft["total_paragraphs"],
        "total_corrections": approved["total_corrections"],
        "corrections_log": [
            {
                "idx": c.get("para_id", c.get("idx", 0)),
                "text": c.get("text", ""),
                "agent1_pred": c.get("original_pred", c.get("agent1_pred", "")),
                "corrected_to": c.get("corrected_label", c.get("corrected_to", "")),
                "reason": c.get("reason", "")
            }
            for c in approved.get("corrections_log", [])
        ],
        "approved_chapters": approved.get("approved_chapters", []),
        "sqa_score": qa_result.get("qa_score", qa_result.get("score", 100.0)),
        "sqa_status": qa_result.get("status", "PASS"),
        "sqa_defects": qa_result.get("defects", []),
        "sqa_tier1_iterations": approved.get("sqa_tier1_iterations", approved.get("iteration_count", 1)),
        "sqa_tier2_iterations": tier2_res.get("tier2_iterations", tier2_res.get("iterations", 1))
    }

@app.get("/api/download/{filename}")
async def api_download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Berkas hasil tidak ditemukan.")
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename
    )

@app.post("/api/active-learning/feedback")
async def api_al_feedback(
    paragraph_idx: int = Form(...),
    paragraph_text: str = Form(...),
    correct_label: str = Form(...)
):
    try:
        active_learning.record_manual_correction(
            idx=paragraph_idx,
            text=paragraph_text,
            correct_label=correct_label
        )
        return {"status": "success", "message": "Feedback berhasil disimpan ke Active Learning Pool."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/active-learning/retrain")
async def api_al_retrain():
    try:
        result = active_learning.retrain_agent_1()
        inspector.reload_model()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.api_route("/logo.png", methods=["GET", "HEAD"])
@app.api_route("/AsdokuLogo.png", methods=["GET", "HEAD"])
@app.api_route("/favicon.ico", methods=["GET", "HEAD"])
async def get_logo():
    logo_path = os.path.join(os.path.dirname(__file__), "AsdokuLogo.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")

@app.api_route("/logo_ueu.png", methods=["GET", "HEAD"])
async def get_ueu_logo():
    logo_path = os.path.join(os.path.dirname(__file__), "data", "logo_ueu.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="UEU Logo not found")

@app.api_route("/profil.jpeg", methods=["GET", "HEAD"])
@app.api_route("/profil.jpg", methods=["GET", "HEAD"])
async def get_profil():
    profil_path = os.path.join(os.path.dirname(__file__), "profil.jpeg")
    if os.path.exists(profil_path):
        return FileResponse(profil_path, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Profil image not found")

@app.api_route("/agent1.png", methods=["GET", "HEAD"])
@app.api_route("/Agent 1.png", methods=["GET", "HEAD"])
async def get_agent1():
    path = os.path.join(os.path.dirname(__file__), "Agent 1.png")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Agent 1 not found")

@app.api_route("/agent2.png", methods=["GET", "HEAD"])
@app.api_route("/Agent 2.png", methods=["GET", "HEAD"])
async def get_agent2():
    path = os.path.join(os.path.dirname(__file__), "Agent 2.png")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Agent 2 not found")

@app.api_route("/agent3.png", methods=["GET", "HEAD"])
@app.api_route("/Agent 3.png", methods=["GET", "HEAD"])
async def get_agent3():
    path = os.path.join(os.path.dirname(__file__), "Agent 3.png")
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Agent 3 not found")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
