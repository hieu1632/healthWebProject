// src/Model/BodyPartInfo.tsx
import React, { useEffect, useState } from "react";
import { getModelFeatures, FeaturesResponse } from "../api/modelApi";
import mapping from "../data/symptom_mapping.json";

interface Props {
  selectedBodyPart: string | null;
  onAddSymptom: (symptom: string) => void;
}

const pretty = (s: string) => s.replace(/[_]+/g, " ");

const FALLBACK = [
  "itching",
  "skin_rash",
  "nodal_skin_eruptions",
  "continuous_sneezing",
  "shivering",
  "chills",
  "joint_pain",
  "stomach_pain",
  "acidity",
  "vomiting",
  "fatigue",
  "cough",
  "high_fever",
  "headache",
];

const BodyPartInfo: React.FC<Props> = ({ selectedBodyPart, onAddSymptom }) => {
  const [features, setFeatures] = useState<string[]>([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [symptomMeta, setSymptomMeta] = useState<Record<string, any>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data: FeaturesResponse = await getModelFeatures();
        if (!mounted) return;
        let feats: string[] = [];
        if (Array.isArray(data.features)) feats = data.features;
        else if (data && typeof data === "object") feats = Object.keys(data as any);
        feats = feats.map((f) => String(f).trim().toLowerCase()).filter(Boolean);
        if (feats.length === 0) {
          console.warn("[BodyPartInfo] features empty -> use fallback");
          feats = FALLBACK;
        }
        setFeatures(feats);
        setSymptomMeta(data.symptom_meta || {});
      } catch (err: any) {
        console.error("[BodyPartInfo] getModelFeatures error:", err);
        setError(String(err?.message || err));
        setFeatures(FALLBACK);
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  const fLower = filter.trim().toLowerCase();

  const getRegionForFeature = (en: string) => {
    const m = (mapping as any).symptoms?.[en];
    if (m && m.region) return String(m.region).trim().toLowerCase();
    return "khác";
  };

  const selectedRegionNorm = (selectedBodyPart || "").trim().toLowerCase();

  const visible = features.filter((f) => {
    if (fLower) {
      const fClean = f.replace(/[_]+/g, " ");
      if (!(fClean.includes(fLower) || f.includes(fLower))) return false;
    }
    if (selectedRegionNorm) {
      const featRegion = getRegionForFeature(f);
      if (featRegion !== selectedRegionNorm) return false;
    }
    return true;
  });

  return (
    <div className="card body-info-card">
      <h3>Danh sách triệu chứng {selectedBodyPart ? `- ${selectedBodyPart}` : ""}</h3>
      <input
        placeholder="Tìm triệu chứng (tiếng Anh hoặc tiếng Việt tạm thời)..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        style={{ width: "100%", padding: 8, marginBottom: 10, borderRadius: 8, border: "1px solid #ddd" }}
      />
      {loading ? (
        <p className="empty">Đang tải danh sách triệu chứng...</p>
      ) : (
        <>
          {error && <div style={{ color: "crimson", marginBottom: 8 }}>Lỗi tải: {error}</div>}
          <div style={{ maxHeight: 340, overflowY: "auto" }}>
            {visible.length === 0 ? (
              <p className="empty">Không tìm thấy triệu chứng</p>
            ) : (
              visible.map((s) => {
                const meta = (mapping as any).symptoms?.[s] || {};
                const label = meta?.vi || pretty(s);
                return (
                  <div key={s} style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8 }}>
                    <button
                      className="symptom-option"
                      onClick={() => onAddSymptom(s)}
                      style={{ flex: 1, textAlign: "left" }}
                    >
                      {label}
                    </button>
                    {symptomMeta[s] && symptomMeta[s].severity && (
                      <small style={{ color: "#666" }}>sev:{symptomMeta[s].severity}</small>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </>
      )}

      <p style={{ fontSize: 12, color: "#666", marginTop: 10 }}>
        Ghi chú: danh sách lấy từ backend (English keys). Nếu bạn muốn hiển thị tiếng Việt đầy đủ, cập nhật file mapping EN↔VN.
      </p>
    </div>
  );
};

export default BodyPartInfo;
