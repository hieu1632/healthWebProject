import os, json, numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import uvicorn
from typing import List, Any, Dict

# === Đường dẫn model ===
MODEL_DIR = os.path.join("backend", "models")
ML_PKL = os.path.join(MODEL_DIR, "ml_model.pkl")
ENC_PKL = os.path.join(MODEL_DIR, "symptom_encoder.pkl")
MODEL_JSON = os.path.join(MODEL_DIR, "model.json")
SYMPTOM_META = os.path.join(MODEL_DIR, "symptom_meta.json")
ADVICE_JSON = os.path.join(MODEL_DIR, "advice.json")

if not os.path.exists(ML_PKL) or not os.path.exists(ENC_PKL):
    raise RuntimeError("Missing model artifacts in backend/models. Run training first.")

clf = joblib.load(ML_PKL)
mlb = joblib.load(ENC_PKL)

model_json = {}
if os.path.exists(MODEL_JSON):
    with open(MODEL_JSON, "r", encoding="utf-8") as f:
        model_json = json.load(f)

symptom_meta = {}
if os.path.exists(SYMPTOM_META):
    with open(SYMPTOM_META, "r", encoding="utf-8") as f:
        symptom_meta = json.load(f)

advice_map = {}
if os.path.exists(ADVICE_JSON):
    with open(ADVICE_JSON, "r", encoding="utf-8") as f:
        advice_map = json.load(f)

# === Khởi tạo app FastAPI ===
app = FastAPI(title="Symptom -> Predict backend")

# === Bật CORS cho frontend (React) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Models ===
class PredictIn(BaseModel):
    symptoms: List[str]
    topK: int = 5


class ChatIn(BaseModel):
    userMessage: str
    contextPredictions: List[Dict[str, Any]] = []
    symptoms: List[str] = []


# === Helper ===
def normalize_sym(s: str) -> str:
    return str(s).strip().lower()


def log_softmax(logits):
    m = np.max(logits)
    exps = np.exp(logits - m)
    return exps / np.sum(exps)


# === API chính ===
@app.get("/model/features")
def get_model_features():
    features = []
    if model_json and "feature_names" in model_json:
        features = model_json["feature_names"]
    else:
        try:
            features = mlb.classes_.tolist()
        except Exception:
            features = []

    return {
        "features": features,
        "symptom_meta": symptom_meta,
        "advice": advice_map,
    }


@app.post("/predict")
def predict(body: PredictIn):
    symptoms = [normalize_sym(s) for s in (body.symptoms or [])]
    topK = body.topK or 5

    # Transform input thành vector
    try:
        x = mlb.transform([symptoms])[0]
    except Exception:
        feat = list(mlb.classes_)
        x = np.array([1 if f in symptoms else 0 for f in feat])

    # Tính xác suất
    if hasattr(clf, "class_log_prior_") and hasattr(clf, "feature_log_prob_"):
        jll = clf.class_log_prior_ + np.dot(clf.feature_log_prob_, x)
        probs = log_softmax(jll)
        classes = list(clf.classes_)
    else:
        probs = clf.predict_proba([x])[0]
        classes = list(clf.classes_)

    preds = [{"disease": classes[i], "prob": float(probs[i])} for i in range(len(classes))]
    preds = sorted(preds, key=lambda r: r["prob"], reverse=True)[:topK]

    # Kiểm tra symptom nặng
    alert = False
    for s in symptoms:
        m = symptom_meta.get(s)
        if m and str(m.get("severity", "")).lower() in ("high", "severe", "critical"):
            alert = True
            break

    # Bổ sung thông tin
    enriched = []
    for p in preds:
        prob = p["prob"]
        if prob >= 0.6:
            sev = "Cao"
        elif prob >= 0.3:
            sev = "Trung bình"
        else:
            sev = "Thấp"
        if alert:
            urg = "CẤP CỨU: đến cơ sở y tế ngay"
        else:
            urg = "Khám sớm" if sev == "Cao" else ("Tư vấn chuyên gia" if sev == "Trung bình" else "Theo dõi tại nhà")
        enriched.append({**p, "severity": sev, "urgency": urg})

    selected_meta = {s: symptom_meta.get(s) for s in symptoms if s in symptom_meta}
    return {"predictions": enriched, "alertPresent": alert, "symptom_meta": selected_meta}


# === ALIAS endpoint để frontend không lỗi 404 ===
@app.get("/api/model/features")
def get_model_features_api():
    return get_model_features()


@app.post("/api/predict")
def predict_api_alias(body: PredictIn):
    return predict(body)


# === Main ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
