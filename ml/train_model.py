import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("data/cleaned/jobs_cleaned.csv")

# Remove missing values
df = df.dropna(subset=["title", "category"])

# Features and labels
X = df["title"]
y = df["category"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Machine Learning Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("=" * 40)
print(f"Accuracy: {accuracy:.2%}")
print("=" * 40)

print("\nClassification Report\n")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "ml/job_classifier.pkl")

print("\nModel saved successfully!")