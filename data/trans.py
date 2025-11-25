import pandas as pd
from difflib import get_close_matches

# ==============================
# 1) DICTIONARY ANH → VIỆT
# ==============================
translation_dict = {
    "Drug Reaction": "Phản ứng thuốc",
    "Malaria": "Sốt rét", 
    "Allergy": "Dị ứng",
    "Hypothyroidism": "Suy giáp",
    "Psoriasis": "Vảy nến",
    "GERD": "Trào ngược dạ dày thực quản",
    "Chronic cholestasis": "Ứ mật mãn tính",
    "hepatitis A": "Viêm gan A",
    "Osteoarthristis": "Viêm xương khớp",
    "(vertigo) Paroymsal Positional Vertigo": "Chóng mặt tư thế kịch phát lành tính",
    "Hypoglycemia": "Hạ đường huyết",
    "Acne": "Mụn trứng cá",
    "Diabetes": "Tiểu đường",
    "Impetigo": "Chốc lở",
    "Hypertension": "Tăng huyết áp",
    "Peptic ulcer diseae": "Loét dạ dày tá tràng",
    "Dimorphic hemorrhoids(piles)": "Trĩ",
    "Common Cold": "Cảm lạnh thông thường",
    "Chicken pox": "Thủy đậu",
    "Cervical spondylosis": "Thoái hóa đốt sống cổ",
    "Hyperthyroidism": "Cường giáp",
    "Urinary tract infection": "Nhiễm trùng đường tiết niệu",
    "Varicose veins": "Suy giãn tĩnh mạch",
    "AIDS": "AIDS",
    "Paralysis (brain hemorrhage)": "Liệt (xuất huyết não)",
    "Typhoid": "Thương hàn",
    "Hepatitis B": "Viêm gan B",
    "Fungal infection": "Nhiễm nấm",
    "Hepatitis C": "Viêm gan C",
    "Migraine": "Đau nửa đầu",
    "Bronchial Asthma": "Hen phế quản",
    "Alcoholic hepatitis": "Viêm gan do rượu",
    "Jaundice": "Vàng da",
    "Hepatitis E": "Viêm gan E",
    "Dengue": "Sốt xuất huyết",
    "Hepatitis D": "Viêm gan D",
    "Heart attack": "Đau tim",
    "Pneumonia": "Viêm phổi",
    "Arthritis": "Viêm khớp",
    "Gastroenteritis": "Viêm dạ dày ruột",
    "Tuberculosis": "Bệnh lao",

    "itching": "Ngứa",
    "skin_rash": "Phát ban da",
    "nodal_skin_eruptions": "Nổi mụn cục trên da",
    "continuous_sneezing": "Hắt hơi liên tục",
    "shivering": "Run",
    "chills": "Ớn lạnh",
    "joint_pain": "Đau khớp",
    "stomach_pain": "Đau dạ dày",
    "acidity": "Trào ngược axit",
    "ulcers_on_tongue": "Loét lưỡi",
    "muscle_wasting": "Teo cơ",
    "vomiting": "Nôn",
    "burning_micturition": "Tiểu buốt",
    "spotting_urination": "Tiểu ra máu",
    "fatigue": "Mệt mỏi",
    "weight_gain": "Tăng cân",
    "anxiety": "Lo âu",
    "cold_hands_and_feets": "Tay chân lạnh",
    "mood_swings": "Thay đổi tâm trạng",
    "weight_loss": "Sút cân",
    "restlessness": "Bồn chồn",
    "lethargy": "Uể oải",
    "patches_in_throat": "Có mảng trắng trong cổ họng",
    "irregular_sugar_level": "Đường huyết không ổn định",
    "cough": "Ho",
    "high_fever": "Sốt cao",
    "sunken_eyes": "Mắt trũng",
    "breathlessness": "Khó thở",
    "sweating": "Đổ mồ hôi",
    "dehydration": "Mất nước",
    "indigestion": "Khó tiêu",
    "headache": "Đau đầu",
    "yellowish_skin": "Vàng da",
    "dark_urine": "Nước tiểu sẫm màu",
    "nausea": "Buồn nôn",
    "loss_of_appetite": "Chán ăn",
    "pain_behind_the_eyes": "Đau sau hốc mắt",
    "back_pain": "Đau lưng",
    "constipation": "Táo bón",
    "abdominal_pain": "Đau bụng",
    "diarrhoea": "Tiêu chảy",
    "mild_fever": "Sốt nhẹ",
    "yellow_urine": "Nước tiểu vàng",
    "yellowing_of_eyes": "Vàng mắt",
    "acute_liver_failure": "Suy gan cấp tính",
    "fluid_overload": "Quá tải dịch",
    "swelling_of_stomach": "Chướng bụng",
    "swelled_lymph_nodes": "Hạch bạch huyết sưng to",
    "malaise": "Khó chịu toàn thân",
    "blurred_and_distorted_vision": "Mờ mắt và nhìn biến dạng",
    "phlegm": "Khạc đờm",
    "throat_irritation": "Kích ứng cổ họng",
    "redness_of_eyes": "Đỏ mắt",
    "sinus_pressure": "Nghẹt xoang",
    "runny_nose": "Sổ mũi",
    "congestion": "Nghẹt mũi",
    "chest_pain": "Đau ngực",
    "weakness_in_limbs": "Yếu chi",
    "fast_heart_rate": "Nhịp tim nhanh",
    "pain_during_bowel_movements": "Đau khi đại tiện",
    "pain_in_anal_region": "Đau vùng hậu môn",
    "bloody_stool": "Phân có máu",
    "irritation_in_anus": "Kích ứng hậu môn",
    "neck_pain": "Đau cổ",
    "dizziness": "Chóng mặt",
    "cramps": "Chuột rút",
    "bruising": "Bầm tím",
    "obesity": "Béo phì",
    "swollen_legs": "Phù chân",
    "swollen_blood_vessels": "Giãn mạch máu",
    "puffy_face_and_eyes": "Mặt và mắt sưng húp",
    "enlarged_thyroid": "Tuyến giáp phì đại",
    "brittle_nails": "Móng giòn",
    "swollen_extremeties": "Chi phù",
    "excessive_hunger": "Đói quá mức",
    "extra_marital_contacts": "Quan hệ ngoài hôn nhân",
    "drying_and_tingling_lips": "Khô và ngứa ran môi",
    "slurred_speech": "Nói ngọng",
    "knee_pain": "Đau đầu gối",
    "hip_joint_pain": "Đau khớp háng",
    "muscle_weakness": "Yếu cơ",
    "stiff_neck": "Cứng cổ",
    "swelling_joints": "Sưng khớp",
    "movement_stiffness": "Cứng khớp",
    "spinning_movements": "Chóng mặt xoay tròn",
    "loss_of_balance": "Mất thăng bằng",
    "unsteadiness": "Đi đứng không vững",
    "weakness_of_one_body_side": "Yếu nửa người",
    "loss_of_smell": "Mất khứu giác",
    "bladder_discomfort": "Khó chịu bàng quang",
    "foul_smell_of_urine": "Nước tiểu có mùi hôi",
    "continuous_feel_of_urine": "Cảm giác buồn tiểu liên tục",
    "passage_of_gases": "Xì hơi",
    "internal_itching": "Ngứa trong người",
    "toxic_look_(typhos)": "Vẻ mặt nhiễm độc (typhos)",
    "depression": "Trầm cảm",
    "irritability": "Dễ cáu gắt",
    "muscle_pain": "Đau cơ",
    "altered_sensorium": "Rối loạn ý thức",
    "red_spots_over_body": "Nốt đỏ khắp người",
    "belly_pain": "Đau bụng",
    "abnormal_menstruation": "Kinh nguyệt bất thường",
    "dischromic_patches": "Vùng da mất sắc tố",
    "watering_from_eyes": "Chảy nước mắt",
    "increased_appetite": "Tăng cảm giác thèm ăn",
    "polyuria": "Tiểu nhiều",
    "family_history": "Tiền sử gia đình",
    "mucoid_sputum": "Đờm nhầy",
    "rusty_sputum": "Đờm màu rỉ sắt",
    "lack_of_concentration": "Mất tập trung",
    "visual_disturbances": "Rối loạn thị giác",
    "receiving_blood_transfusion": "Truyền máu",
    "receiving_unsterile_injections": "Tiêm chích không vô trùng",
    "coma": "Hôn mê",
    "stomach_bleeding": "Xuất huyết dạ dày",
    "distention_of_abdomen": "Đầy hơi",
    "history_of_alcohol_consumption": "Tiền sử uống rượu",
    "blood_in_sputum": "Ho ra máu",
    "prominent_veins_on_calf": "Tĩnh mạch chân nổi rõ",
    "palpitations": "Đánh trống ngực",
    "painful_walking": "Đau khi đi lại",
    "pus_filled_pimples": "Mụn mủ",
    "blackheads": "Mụn đầu đen",
    "scurring": "Sẹo",
    "skin_peeling": "Tróc da",
    "silver_like_dusting": "Vảy bạc",
    "small_dents_in_nails": "Rỗ móng tay",
    "inflammatory_nails": "Viêm quanh móng",
    "blister": "Phồng rộp",
    "red_sore_around_nose": "Vết đỏ quanh mũi",
    "yellow_crust_ooze": "Chảy mủ vảy vàng",
    "prognosis": "Tiên lượng"
}

# ==============================
# 2) CLEAN TEXT
# ==============================
def clean_text(text):
    if pd.isna(text) or text == "":
        return text
    text = str(text).strip()
    text = text.replace(" ", "")
    text = text.replace("-", "_")
    text = text.replace("__", "_")
    return text.lower()

# ==============================
# 3) TRANSLATE SMART + FUZZY
# ==============================
def translate_text_smart(text, translation_dict, unknown_list):
    if pd.isna(text) or text == "":
        return text

    cleaned = clean_text(text)

    # Direct match
    lower_keys = {k.lower(): k for k in translation_dict.keys()}
    if cleaned in lower_keys:
        original_key = lower_keys[cleaned]
        return translation_dict[original_key]

    # Fuzzy Match
    match = get_close_matches(cleaned, lower_keys.keys(), n=1, cutoff=0.85)
    if match:
        best_key = lower_keys[match[0]]
        return translation_dict[best_key]

    # Not found → log
    unknown_list.add(text)
    return text

# ==============================
# 4) TRANSLATE ENTIRE DATASET
# ==============================
def translate_dataset_smart(input_file, output_file):
    df = pd.read_csv(input_file)
    unknown_symptoms = set()

    print("=== BẮT ĐẦU DỊCH DATASET ===")

    df["Disease"] = df["Disease"].apply(
        lambda x: translate_text_smart(x, translation_dict, unknown_symptoms)
    )

    symptom_cols = [c for c in df.columns if c.startswith("Symptom_")]
    for col in symptom_cols:
        df[col] = df[col].apply(
            lambda x: translate_text_smart(x, translation_dict, unknown_symptoms)
        )

    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\n✔ ĐÃ LƯU FILE DỊCH → {output_file}")

    print("\n=== TRIỆU CHỨNG KHÔNG KHỚP ===")
    if len(unknown_symptoms) == 0:
        print("✔ Tất cả đã được dịch 100%!")
    else:
        for item in sorted(unknown_symptoms):
            print(f"- {item}")
        with open("unknown_symptoms.txt", "w", encoding="utf-8") as f:
            for item in sorted(unknown_symptoms):
                f.write(item + "\n")
        print("\n📄 ĐÃ LƯU → unknown_symptoms.txt")

    return df

# ==============================
# 5) CHẠY
# ==============================
if __name__ == "__main__":
    input_filename = "data/dataset.csv"
    output_filename = "data/dataset_vietnamese.csv"

    translated_df = translate_dataset_smart(input_filename, output_filename)

    print("\n=== 5 DÒNG ĐẦU ===")
    print(translated_df.head().to_string())

    print("\n=== DANH SÁCH BỆNH ===")
    for d in translated_df["Disease"].unique():
        print("-", d)
