// src/Model/AnalysisResult.tsx
import React from "react";
import mapping from "../data/symptom_mapping.json";

type Prediction = {
  disease?: string;
  prob?: number;
  severity?: string;
  urgency?: string;
};

interface AnalysisResultProps {
  predictions?: Prediction[]; // optional, kept for compatibility
  isAnalyzed?: boolean;
  selectedSymptoms?: string[]; // array of EN keys
  symptomMeta?: Record<string, any>;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({
  predictions = [],
  isAnalyzed = false,
  selectedSymptoms = [],
  symptomMeta = {},
}) => {
  const selected = Array.isArray(selectedSymptoms) ? selectedSymptoms : [];

  if (!isAnalyzed && selected.length === 0) {
    return (
      <div className="card analysis-result-card">
        <h3>Kết quả phân tích</h3>
        <p className="empty">Chưa phân tích. Chọn triệu chứng và nhấn "Nhận kết quả".</p>
      </div>
    );
  }

  // Group by region
  type SymInfo = { key: string; name: string; advice?: string; severity?: string };
  const grouped = selected.reduce((acc: Record<string, SymInfo[]>, key) => {
    const info = (mapping as any).symptoms?.[key] || null;
    const regionRaw = (info && info.region) ? info.region : "khác";
    const region = String(regionRaw).trim();
    const name = (info && info.vi) ? info.vi : key.replace(/_/g, " ");
    const advice = (info && info.advice_vi) ? info.advice_vi : undefined;
    const sev = symptomMeta?.[key]?.severity || undefined;

    if (!acc[region]) acc[region] = [];
    acc[region].push({ key, name, advice, severity: sev });
    return acc;
  }, {});

  const getRegionAdvice = (region: string) => {
    return (mapping as any).regions?.[region]?.advice_vi || null;
  };

  return (
    <div className="card analysis-result-card">
      <h3>Kết quả phân tích & Khuyến nghị</h3>

      {Object.keys(grouped).length === 0 ? (
        <p className="empty">Không có triệu chứng được chọn.</p>
      ) : (
        Object.entries(grouped).map(([region, list]) => {
          const regionAdvice = getRegionAdvice(region);
          const hasHighSeverity = list.some((s) => {
            const sev = (s.severity || "").toString().toLowerCase();
            return sev === "high" || sev === "severe" || sev === "critical";
          });
          return (
            <div key={region} style={{ marginBottom: 16, padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <h4 style={{ margin: 0 }}>{region}</h4>

              <ul style={{ marginTop: 8 }}>
                {list.map((s) => (
                  <li key={s.key} style={{ marginBottom: 8 }}>
                    <div style={{ fontWeight: 600 }}>{s.name}</div>
                    {s.advice && <div style={{ fontSize: 13, marginTop: 4 }}>{s.advice}</div>}
                    {s.severity && (
                      <div style={{ marginTop: 6, color: s.severity.toLowerCase() === "high" ? "crimson" : "#666", fontSize: 13 }}>
                        Mức độ cảnh báo triệu chứng: {s.severity}
                      </div>
                    )}
                  </li>
                ))}
              </ul>

              {regionAdvice ? (
                <div style={{ marginTop: 8, background: "#fff7e6", padding: 8, borderRadius: 6 }}>
                  <strong>Khuyến nghị cho vùng {region}:</strong>
                  <div style={{ marginTop: 6 }}>{regionAdvice}</div>
                </div>
              ) : (
                <div style={{ marginTop: 8, color: "#666" }}>Không có khuyến nghị vùng cụ thể.</div>
              )}

              {hasHighSeverity && (
                <div style={{ marginTop: 10, padding: 10, borderRadius: 6, background: "#ffecec", color: "#a00" }}>
                  <strong>Cảnh báo:</strong> Có triệu chứng mức độ cao. Hãy đến cơ sở y tế ngay nếu triệu chứng nghiêm trọng.
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
};

export default AnalysisResult;
