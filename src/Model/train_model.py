# src/Model/train_model.py
import os, re, json, traceback, sys
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

print("=== TRAIN START ===")

try:
    BASE = os.getcwd()
    DATA_DIR = os.path.join(BASE, "data")
    OUT_DIR = os.path.join(BASE, "backend", "models")
    os.makedirs(OUT_DIR, exist_ok=True)

    dataset_path = os.path.join(DATA_DIR, "dataset.csv")
    print("dataset_path ->", dataset_path)
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(dataset_path)

    df = pd.read_csv(dataset_path, dtype=str).fillna("")
    print("Loaded df shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # detect disease column
    label_col = next((c for c in df.columns if c.lower() in ("disease","prognosis","label","target")), df.columns[0])
    print("label_col:", label_col)

    # collect symptom columns: any column name starting with 'symptom' (case-insensitive)
    symptom_cols = [c for c in df.columns if c.lower().startswith("symptom")]
    print("symptom_cols detected:", symptom_cols)

    # normalize function: keep underscores (since dataset uses them), lower-case
    def norm_token(s):
        if s is None: return ""
        return re.sub(r"\s+", "_", str(s).strip().lower())

    # convert each row -> list of symptom tokens
    def row_symptoms(row):
        out = []
        for c in symptom_cols:
            v = row.get(c, "")
            if not v or str(v).strip() == "": 
                continue
            token = norm_token(v)
            if token and token not in out:
                out.append(token)
        return out

    symptoms_series = df.apply(row_symptoms, axis=1)
    # inspect
    print("Sample symptoms rows:")
    for i in range(5):
        print(i, symptoms_series.iloc[i])

    empty_count = sum(1 for s in symptoms_series if len(s) == 0)
    print("Empty symptom rows:", empty_count, "/", len(symptoms_series))

    if empty_count == len(symptoms_series):
        raise ValueError("All symptom rows empty — check dataset/symptom columns")

    y = df[label_col].apply(lambda s: str(s).strip())
    print("Unique labels:", y.nunique())

    # filter out rows with no symptoms? (optional) keep them but they add noise
    mask = symptoms_series.apply(lambda x: len(x) > 0)
    X_sym = symptoms_series[mask].tolist()
    y_sym = y[mask].tolist()
    print("Using", len(X_sym), "samples with >=1 symptom")

    mlb = MultiLabelBinarizer(sparse_output=False)
    X = mlb.fit_transform(X_sym)
    feature_names = mlb.classes_.tolist()
    print("Encoded features count:", len(feature_names))
    print("First 40 features:", feature_names[:40])

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_sym, test_size=0.12, random_state=42, stratify=y_sym if len(y_sym)>50 else None)
    clf = MultinomialNB(alpha=1.0)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print("Classification report:")
    print(classification_report(y_test, preds, zero_division=0))

    # save artifacts
    joblib.dump(clf, os.path.join(OUT_DIR, "ml_model.pkl"))
    joblib.dump(mlb, os.path.join(OUT_DIR, "symptom_encoder.pkl"))

    model_json = {
        "classes": clf.classes_.tolist(),
        "class_log_prior": clf.class_log_prior_.tolist() if hasattr(clf, "class_log_prior_") else [],
        "feature_log_prob": clf.feature_log_prob_.tolist() if hasattr(clf, "feature_log_prob_") else [],
        "feature_names": feature_names
    }
    with open(os.path.join(OUT_DIR, "model.json"), "w", encoding="utf-8") as f:
        json.dump(model_json, f, ensure_ascii=False, indent=2)

    # try load extra symptom metadata files if exist (same as your previous script)
    symptom_meta = {}
    def safe_load_csv_map(path):
        if not os.path.exists(path): return {}
        d = pd.read_csv(path, dtype=str).fillna("")
        out = {}
        for _, r in d.iterrows():
            k = norm_token(r.iloc[0])
            out[k] = r.to_dict()
        return out

    desc = safe_load_csv_map(os.path.join(DATA_DIR, "symptom_Description.csv"))
    prec = safe_load_csv_map(os.path.join(DATA_DIR, "symptom_precaution.csv"))
    sev = safe_load_csv_map(os.path.join(DATA_DIR, "Symptom-severity.csv"))

    # merge simple
    for k,v in (list(desc.items()) + list(prec.items()) + list(sev.items())):
        symptom_meta.setdefault(k, {})
    # but we also want disease description/precaution if you have them (as in your second JSON)
    # For simplicity write existing symptom_meta or disease mapping you have
    with open(os.path.join(OUT_DIR, "symptom_meta.json"), "w", encoding="utf-8") as f:
        json.dump(symptom_meta, f, ensure_ascii=False, indent=2)

    print("Saved models to", OUT_DIR)
    print("=== TRAIN DONE ===")

except Exception as e:
    print("ERROR:", e)
    traceback.print_exc()
    sys.exit(1)
