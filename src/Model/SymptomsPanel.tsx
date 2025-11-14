// src/Model/SymptomsPanel.tsx
import React from "react";
import mapping from "../data/symptom_mapping.json";

interface Props {
  symptoms: string[]; // array of EN keys (ex: "headache")
  onRemove: (symptom: string) => void;
  onClear: () => void;
  onAnalyze: () => void;
}

const pretty = (s: string) => s.replace(/[_]+/g, " ");

const SymptomsPanel: React.FC<Props> = ({ symptoms, onRemove, onClear, onAnalyze }) => {
  return (
    <div className="card symptoms-panel-card" style={{ padding: 12 }}>
      <h3>Triệu chứng đã chọn</h3>

      {(!symptoms || symptoms.length === 0) ? (
        <p className="empty">Chưa có triệu chứng nào được chọn.</p>
      ) : (
        <>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {symptoms.map((key) => {
              const info = (mapping as any).symptoms?.[key];
              const label = info?.vi || pretty(key);
              return (
                <div key={key} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <div style={{ flex: 1, padding: "8px 10px", borderRadius: 8, background: "#f2f7ff" }}>
                    {label}
                  </div>
                  <button
                    onClick={() => onRemove(key)}
                    title="Xóa triệu chứng"
                    style={{ padding: "6px 10px", borderRadius: 6 }}
                  >
                    ✕
                  </button>
                </div>
              );
            })}
          </div>

          <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
            <button
              onClick={onAnalyze}
              className="btn-primary"
              style={{ padding: "10px 14px", borderRadius: 8 }}
            >
              🔍 Nhận kết quả
            </button>

            <button
              onClick={onClear}
              className="btn-secondary"
              style={{ padding: "10px 14px", borderRadius: 8 }}
            >
              🧹 Xóa tất cả
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default SymptomsPanel;
