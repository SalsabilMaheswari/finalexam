# altara/ml_models.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


def predict_student_performance(df):
    if df.shape[0] < 2:
        return {
            'scholarship': [{'model': '-', 'accuracy': 0, 'probability': 0, 'label': 'Insufficient Data'}],
            'internship': {'model': '-', 'accuracy': 0, 'probability': 0, 'label': 'Insufficient Data'},
            'trend': 'Unknown'
        }

    # Fitur dan label
    X = df[['average_score', 'attendance_percentage']]
    y_scholarship = (df['average_score'] >= 75) & (df['attendance_percentage'] >= 70)
    y_internship = df['average_score'] >= 70

    # Normalisasi fitur
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Splitting hanya sekali
    X_train, X_test, y_s_train, y_s_test, y_i_train, y_i_test = train_test_split(
        X_scaled, y_scholarship, y_internship, test_size=0.2, random_state=42
    )

    models = {
        'Logistic Regression': LogisticRegression(),
        'Random Forest': RandomForestClassifier(),
        'Gradient Boosting': GradientBoostingClassifier()
    }

    predictions = {
        'scholarship': [],
        'internship': {},
        'trend': None
    }

    # Prediksi beasiswa
    for name, model in models.items():
        model.fit(X_train, y_s_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_s_test, y_pred)

        try:
            probs = model.predict_proba([X_scaled[-1]])[0]
        except AttributeError:
            probs = [1 - model.predict([X_scaled[-1]])[0], model.predict([X_scaled[-1]])[0]]

        label = model.predict([X_scaled[-1]])[0]

        predictions['scholarship'].append({
            'model': name,
            'accuracy': round(accuracy * 100, 2),
            'probability': round(probs[1] * 100, 2),
            'label': 'Eligible' if label else 'Not Eligible'
        })

    # Prediksi magang menggunakan Random Forest
    intern_model = RandomForestClassifier()
    intern_model.fit(X_train, y_i_train)
    y_pred_intern = intern_model.predict(X_test)
    accuracy_intern = accuracy_score(y_i_test, y_pred_intern)

    try:
        probs_intern = intern_model.predict_proba([X_scaled[-1]])[0]
    except AttributeError:
        probs_intern = [1 - intern_model.predict([X_scaled[-1]])[0], intern_model.predict([X_scaled[-1]])[0]]

    label_intern = intern_model.predict([X_scaled[-1]])[0]

    predictions['internship'] = {
        'model': 'Random Forest',
        'accuracy': round(accuracy_intern * 100, 2),
        'probability': round(probs_intern[1] * 100, 2),
        'label': 'Ready' if label_intern else 'Not Ready'
    }

    # Analisis tren skor
    std_dev = df['average_score'].std(ddof=0)
    predictions['trend'] = 'Stable' if std_dev < 10 else 'Declining'

    return predictions
