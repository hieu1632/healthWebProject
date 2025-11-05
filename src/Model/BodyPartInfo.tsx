import React from "react";

interface Props {
  selectedBodyPart: string | null;
  onAddSymptom: (symptom: string) => void;
}

const bodyPartData: Record<string, string[]> = {
  Đầu: ["Đau đầu", "Chóng mặt", "Buồn nôn", "Sốt nhẹ"],
  Ngực: ["Đau ngực", "Khó thở", "Tim đập nhanh", "Ho", "Tức ngực"],
  Bụng: ["Đau bụng", "Khó tiêu", "Chán ăn", "Buồn nôn"],
  Tay: ["Tê tay", "Đau cổ tay", "Yếu cơ"],
  "Tay trái": ["Tê tay trái", "Đau cổ tay trái", "Yếu cơ tay trái"],
  "Tay phải": ["Tê tay phải", "Đau cổ tay phải", "Yếu cơ tay phải"],
  Chân: ["Đau đầu gối", "Phù chân", "Tê chân"],
  "Chân trái": ["Đau chân trái", "Phù chân trái", "Tê chân trái"],
  "Chân phải": ["Đau chân phải", "Phù chân phải", "Tê chân phải"],
};


const BodyPartInfo: React.FC<Props> = ({ selectedBodyPart, onAddSymptom }) => {
  if (!selectedBodyPart) {
    return (
      <div className="card body-info-card">
        <h3>Thông Tin Vùng Cơ Thể</h3>
        <p className="empty">Chọn một vùng trên cơ thể để xem triệu chứng</p>
      </div>
    );
  }

  const symptoms = bodyPartData[selectedBodyPart] || [];

  return (
    <div className="card body-info-card">
      <h3>Thông Tin Vùng Cơ Thể</h3>
      <p className="part-name">{selectedBodyPart}</p>
      <p className="description">
        Các triệu chứng thường gặp tại vùng <b>{selectedBodyPart}</b>
      </p>

      <div className="symptom-options">
        {symptoms.map((s, i) => (
          <button key={i} className="symptom-option" onClick={() => onAddSymptom(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
};

export default BodyPartInfo;
