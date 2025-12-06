# model_train.py
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings("ignore")

# === Load dataset ===
data_path = "diet_recommendations_dataset.csv"  # put your CSV in the same folder
df = pd.read_csv(data_path)
print("✅ Dataset loaded successfully.")
print(df.head())

# === Detect target column ===
target_col = "Diet_Recommendation"  # change if needed
X = df.drop(columns=[target_col])
y = df[target_col]

# === Identify column types ===
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

# Remove identifiers that cause data leakage
if "Patient_ID" in cat_cols:
    cat_cols.remove("Patient_ID")
    X = X.drop(columns=["Patient_ID"])

print("Numeric Columns:", numeric_cols)
print("Categorical Columns:", cat_cols)

# === Preprocessing pipeline ===
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Fixed OneHotEncoder for scikit-learn >= 1.4
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_cols),
    ("cat", categorical_transformer, cat_cols)
])

# === Split dataset ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# === Try multiple models ===
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=200, random_state=42),
    "SVC": SVC(kernel='linear', probability=True, random_state=42)
}

best_model = None
best_acc = 0

for name, model in models.items():
    pipe = Pipeline([("preprocessor", preprocessor), ("model", model)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {acc:.4f}")
    if acc > best_acc:
        best_acc = acc
        best_model = pipe

print("\n✅ Best Model selected with Accuracy:", best_acc)
print("\nClassification Report:")
print(classification_report(y_test, best_model.predict(X_test)))

# === Save best model as pickle ===
with open("best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("\n🎯 best_model.pkl saved successfully! Ready for Flask.")
