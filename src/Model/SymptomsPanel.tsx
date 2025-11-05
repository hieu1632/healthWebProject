import React from "react";

interface Props {
  symptoms: string[];
  onRemove: (symptom: string) => void;
  onClear: () => void;
  onAnalyze: () => void;
}

const SymptomsPanel: React.FC<Props> = ({
  symptoms,
  onRemove,
  onClear,
  onAnalyze,
}) => {
  return (
    <div className="card symptoms-card">
      <h3>Triệu Chứng Đã Chọn</h3>
      <p className="subtext">Các triệu chứng mà bạn gặp phải</p>

      <div className="symptom-list">
        {symptoms.length > 0 ? (
          symptoms.map((s, i) => (
            <div key={i} className="symptom-item">
              <span>{s}</span>
              <button className="remove-btn" onClick={() => onRemove(s)}>
                ✕
              </button>
            </div>
          ))
        ) : (
          <p className="empty">Chưa có triệu chứng nào được chọn</p>
        )}
      </div>

      <div className="symptom-actions">
        <button
          className="analyze-btn"
          onClick={onAnalyze}
          disabled={symptoms.length === 0}
        >
          🔍 Phân Tích Triệu Chứng ({symptoms.length})
        </button>
        <button className="clear-btn" onClick={onClear}>
          🗑️ Xóa Tất Cả
        </button>
      </div>
    </div>
  );
};

export default SymptomsPanel;
