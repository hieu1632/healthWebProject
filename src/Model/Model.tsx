// src/Model/Model.tsx  (chỉ phần thay đổi / chú ý)
import React, { useState } from "react";
import ThreeScene from "./ThreeScene";
import SymptomsPanel from "./SymptomsPanel";
import BodyPartInfo from "./BodyPartInfo";
import AnalysisResult from "./AnalysisResult";
import "../style/Model.css";
import { predictApi } from "../api/modelApi";

type Prediction = {
  disease: string;
  prob: number;
  severity?: string;
  urgency?: string;
};

const Model: React.FC = () => {
  const [selectedBodyPart, setSelectedBodyPart] = useState<string | null>(null);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [symptomMeta, setSymptomMeta] = useState<Record<string, any>>({});
  const [error, setError] = useState<string | null>(null);

  const handleAddSymptom = (symptom: string) => {
    // thêm nếu chưa có, reset isAnalyzed => buộc người dùng bấm lại "Nhận kết quả"
    setSelectedSymptoms((prev) => {
      if (prev.includes(symptom)) return prev;
      return [...prev, symptom];
    });
    setIsAnalyzed(false);
  };

  const handleRemoveSymptom = (symptom: string) => {
    setSelectedSymptoms((prev) => prev.filter((s) => s !== symptom));
    setIsAnalyzed(false);
  };

  const handleClearAll = () => {
    setSelectedSymptoms([]);
    setPredictions([]);
    setIsAnalyzed(false);
    setSymptomMeta({});
    setError(null);
  };

  const normalizeForModel = (s: string) => s.trim().toLowerCase();

  const handleAnalyze = async () => {
    setError(null);
    if (selectedSymptoms.length === 0) {
      setError("Vui lòng chọn ít nhất 1 triệu chứng trước khi phân tích.");
      return;
    }
    setLoading(true);
    try {
      const normalized = selectedSymptoms.map((s) => normalizeForModel(s));
      const res = await predictApi(normalized, 6);
      const preds = res.predictions || [];
      setPredictions(preds);
      setIsAnalyzed(true); // chỉ bật sau khi có kết quả
      setSymptomMeta(res.symptom_meta || {});
    } catch (err: any) {
      console.error("Error calling predictApi:", err);
      setError("Lỗi khi gọi server phân tích. Kiểm tra backend đang chạy (http://localhost:8000).");
      setIsAnalyzed(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="diagnosis-container">
      <div className="symptoms-panel">
        <SymptomsPanel
          symptoms={selectedSymptoms}
          onRemove={handleRemoveSymptom}
          onClear={handleClearAll}
          onAnalyze={handleAnalyze}
        />
        {error && <div style={{ marginTop: 10, color: "#b00020", fontSize: 14 }}>{error}</div>}
        {loading && <div style={{ marginTop: 10, color: "#333", fontSize: 14 }}>Đang phân tích...</div>}
      </div>

      <div className="model-view">
        <h2 className="title">Hệ Thống Tư Vấn Sức Khỏe Qua Các Triệu Chứng</h2>
        <p className="subtitle">Chọn vùng cơ thể, chọn các triệu chứng và nhận khuyến nghị sức khỏe</p>
        <ThreeScene onSelectBodyPart={setSelectedBodyPart} />
      </div>

      <div className="body-info">
        <BodyPartInfo selectedBodyPart={selectedBodyPart} onAddSymptom={handleAddSymptom} />

        <AnalysisResult
          predictions={predictions}
          isAnalyzed={isAnalyzed}
          selectedSymptoms={selectedSymptoms}
          symptomMeta={symptomMeta}
        />
      </div>
    </div>
  );
};

export default Model;
