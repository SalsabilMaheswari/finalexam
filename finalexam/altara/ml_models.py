import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('altara/altara_dataset.csv')

# Fitur input
X = df[['midterm', 'final', 'project', 'attendance']]

# Encode label konsistensi
le_konsistensi = LabelEncoder()
df['konsistensi_encoded'] = le_konsistensi.fit_transform(df['konsistensi'])

def train_beasiswa_model():
    y = df['eligible_beasiswa']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def train_non_akademik_model():
    y = df['non_akademik']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def train_konsistensi_model():
    y = df['konsistensi_encoded']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def train_magang_model():
    y = df['magang_awal']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def decode_konsistensi_label(encoded_label):
    return le_konsistensi.inverse_transform([encoded_label])[0]

def decode_konsistensi_proba(prob_array):
    return dict(zip(le_konsistensi.inverse_transform([0,1,2]), prob_array))
