from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Sample data
diseases = [
    {"disease_id": 1, "disease_name": "Fever"},
    {"disease_id": 2, "disease_name": "Cold"},
    {"disease_id": 3, "disease_name": "Headache"},
    {"disease_id": 4, "disease_name": "Cancer"},
    {"disease_id": 5, "disease_name": "Body Pains"},
    {"disease_id": 6, "disease_name": "Diabetes"},
    {"disease_id": 7, "disease_name": "Hypertension"},
    {"disease_id": 8, "disease_name": "Asthma"},
    {"disease_id": 9, "disease_name": "Arthritis"},
    {"disease_id": 10, "disease_name": "Gastroenteritis"}
]

symptoms = [
    {"symptom_id": 1, "symptom_name": "High Temperature"},
    {"symptom_id": 2, "symptom_name": "Cough"},
    {"symptom_id": 3, "symptom_name": "Sneezing"},
    {"symptom_id": 4, "symptom_name": "Nausea"},
    {"symptom_id": 5, "symptom_name": "Joint Pain"},
    {"symptom_id": 6, "symptom_name": "Muscle Pain"},
    {"symptom_id": 7, "symptom_name": "Fatigue"},
    {"symptom_id": 8, "symptom_name": "Shortness of Breath"},
    {"symptom_id": 9, "symptom_name": "Chest Pain"},
    {"symptom_id": 10, "symptom_name": "Abdominal Pain"}
]

symptom_disease_mapping = [
    {"disease_id": 1, "symptom_id": 1},  # Fever -> High Temperature
    {"disease_id": 2, "symptom_id": 2},  # Cold -> Cough
    {"disease_id": 2, "symptom_id": 3},  # Cold -> Sneezing
    {"disease_id": 3, "symptom_id": 3},  # Headache -> Sneezing
    {"disease_id": 4, "symptom_id": 4},  # Cancer -> Nausea
    {"disease_id": 5, "symptom_id": 5},  # Body Pains -> Joint Pain
    {"disease_id": 5, "symptom_id": 6},  # Body Pains -> Muscle Pain
    {"disease_id": 6, "symptom_id": 7},  # Diabetes -> Fatigue
    {"disease_id": 7, "symptom_id": 9},  # Hypertension -> Chest Pain
    {"disease_id": 8, "symptom_id": 8},  # Asthma -> Shortness of Breath
    {"disease_id": 9, "symptom_id": 5},  # Arthritis -> Joint Pain
    {"disease_id": 10, "symptom_id": 10} # Gastroenteritis -> Abdominal Pain
]

treatments = [
    {"disease_id": 1, "treatment_type": "Allopathic", "description": "Paracetamol for fever reduction"},
    {"disease_id": 1, "treatment_type": "Allopathic", "description": "Ibuprofen for fever and pain"},
    {"disease_id": 1, "treatment_type": "Ayurvedic", "description": "Tulsi and ginger tea for fever"},
    {"disease_id": 2, "treatment_type": "Allopathic", "description": "Antihistamines for cold"},
    {"disease_id": 2, "treatment_type": "Allopathic", "description": "Decongestants for cold"},
    {"disease_id": 2, "treatment_type": "Ayurvedic", "description": "Turmeric milk for cold"},
    {"disease_id": 3, "treatment_type": "Allopathic", "description": "Acetaminophen for headache"},
    {"disease_id": 3, "treatment_type": "Ayurvedic", "description": "Peppermint oil for headache"},
    {"disease_id": 4, "treatment_type": "Allopathic", "description": "Chemotherapy for cancer"},
    {"disease_id": 4, "treatment_type": "Ayurvedic", "description": "Ashwagandha for cancer support"},
    {"disease_id": 5, "treatment_type": "Allopathic", "description": "Pain relievers for body pains"},
    {"disease_id": 5, "treatment_type": "Ayurvedic", "description": "Chyawanprash for body pains"},
    {"disease_id": 6, "treatment_type": "Allopathic", "description": "Insulin for diabetes management"},
    {"disease_id": 6, "treatment_type": "Ayurvedic", "description": "Bitter gourd juice for diabetes"},
    {"disease_id": 7, "treatment_type": "Allopathic", "description": "ACE inhibitors for hypertension"},
    {"disease_id": 7, "treatment_type": "Ayurvedic", "description": "Sarpagandha for hypertension"},
    {"disease_id": 8, "treatment_type": "Allopathic", "description": "Inhalers for asthma"},
    {"disease_id": 8, "treatment_type": "Ayurvedic", "description": "Vasa leaves for asthma"},
    {"disease_id": 9, "treatment_type": "Allopathic", "description": "NSAIDs for arthritis"},
    {"disease_id": 9, "treatment_type": "Ayurvedic", "description": "Ginger oil for arthritis"},
    {"disease_id": 10, "treatment_type": "Allopathic", "description": "Oral rehydration for gastroenteritis"},
    {"disease_id": 10, "treatment_type": "Ayurvedic", "description": "Pomegranate juice for gastroenteritis"}
]

@app.route('/')
def home():
    return "Welcome to the Health API!"

@app.route('/get-disease-info', methods=['POST'])
def get_disease_info():
    data = request.json
    symptoms_input = data.get('symptoms', '').strip().lower()  # Ensure input is a string

    if not symptoms_input:
        return jsonify({"error": "No symptoms provided."}), 400

    found_diseases = set()
    for symptom in symptoms:
        if symptoms_input in symptom['symptom_name'].lower():
            related_diseases = [
                mapping['disease_id'] for mapping in symptom_disease_mapping 
                if mapping['symptom_id'] == symptom['symptom_id']
            ]
            found_diseases.update(related_diseases)

    if not found_diseases:
        return jsonify({"error": "No diseases found for the given symptoms."}), 404

    disease_info = []
    for disease in diseases:
        if disease['disease_id'] in found_diseases:
            relevant_treatments = [
                treatment for treatment in treatments 
                if treatment['disease_id'] == disease['disease_id']
            ]
            disease_info.append({
                "disease_id": disease['disease_id'],
                "disease_name": disease['disease_name'],
                "treatments": [
                    {"type": treatment['treatment_type'], "description": treatment['description']}
                    for treatment in relevant_treatments
                ]
            })

    return jsonify({"result": disease_info})

if __name__ == "__main__":
    app.run(debug=True)
