from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load dataset for recommendation lookup
df = pd.read_csv("dataset/nutritional_dataset.csv")

# Load trained models and preprocessing objects
svm_model = joblib.load("models/svm_model.pkl")
xgb_model = joblib.load("models/xgboost_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# Define input features
feature_columns = ['Age', 'Gender', 'BMI', 'Daily Water Intake (L)', 'Physical Activity Level', 'Eating Habits',
                   'Medical Conditions', 'Medication Usage', 'Sleep Hours', 'Stress Level']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')


@app.route('/about')
def about():
    return render_template('about_us.html')

# ...existing code...


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = request.form
        user_input = [
            int(data['Age']),
            data['Gender'],
            float(data['BMI']),
            float(data['Daily_Water_Intake']),
            data['Physical_Activity_Level'],
            data['Eating_Habits'],
            data['Medical_Conditions'],
            data['Medication_Usage'],
            int(data['Sleep_Hours']),
            data['Stress_Level']
        ]

        # Encode categorical values
        for i, col in enumerate(feature_columns):
            if col in label_encoders:
                # Ensure the value is string for encoder and handle unseen values
                try:
                    user_input[i] = label_encoders[col].transform(
                        [str(user_input[i])])[0]
                except Exception:
                    # If value not seen during training, use a default or raise error
                    user_input[i] = 0  # or handle appropriately

        # Convert to array and scale
        user_input = np.array(user_input).reshape(1, -1)
        user_input_scaled = scaler.transform(user_input)

        # Make predictions
        deficiency_detected = svm_model.predict(user_input_scaled)[0]
        deficiency_type = None
        recommended_food = "No deficiency detected. Maintain a balanced diet."

        if deficiency_detected == 1:
            deficiency_type_encoded = xgb_model.predict(user_input_scaled)[0]
            # Defensive: check if 'Deficiency' encoder exists
            if 'Deficiency' in label_encoders:
                deficiency_type = label_encoders['Deficiency'].inverse_transform(
                    [deficiency_type_encoded])[0]
            else:
                deficiency_type = str(deficiency_type_encoded)

            # Get recommended food based on deficiency
            food_recommendations = df[df['Deficiency'] ==
                                      deficiency_type]['Recommended_Food'].values
            recommended_food = food_recommendations[0] if len(
                food_recommendations) > 0 else "No specific recommendation."

        result = {
            'Deficiency_Detected': "Yes" if deficiency_detected == 1 else "No",
            'Deficiency_Type': deficiency_type if deficiency_detected == 1 else "None",
            'Recommended_Food': recommended_food
        }

        return render_template('results.html', result=result)
    except Exception as e:
        # Log the error for debugging (optional)
        import traceback
        print(traceback.format_exc())
        return render_template('results.html', result={'error': str(e)})
# ...existing code...
# filepath: d:\Healthmate\Healthmate\app.py
# ...existing code...


if __name__ == "__main__":
    app.run(debug=True)
