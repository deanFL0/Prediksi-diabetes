# -*- coding: utf-8 -*-
"""Diabetes Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ssyUYr4VE4dJH_jyv1kL5QatMeGF0dWo
"""

import numpy as np
import pandas as pd
import time

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score

"""# EDA"""

df = pd.read_csv('/content/dataset.csv')
df.head()

df.info()

"""## Data Cleaning"""

print(df.isnull().sum())

print(df.duplicated().sum())

df.drop_duplicates(inplace=True)
print(df.duplicated().sum())

"""## Data Visualization"""

df.describe()

# Statistik deskriptif untuk setiap kolom
print(df.describe())

# Perhitungan mean untuk setiap kolom
print(df.mean())

# Perhitungan median untuk setiap kolom
print(df.median())

# Perhitungan modus untuk setiap kolom
print(df.mode())

# Perhitungan persentil untuk setiap kolom
print(df.quantile([0.25, 0.50, 0.75]))

# Histogram untuk kolom 'age'
plt.hist(df['age'])
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Distribution of Age')
plt.show()

# Diagram batang untuk kolom 'gender'
sns.countplot(x='gender', data=df)
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Distribution of Gender')
plt.show()

# Box plot untuk kolom 'bmi'
sns.boxplot(x='bmi', data=df)
plt.xlabel('BMI')
plt.title('Box Plot of BMI')
plt.show()

# Scatter plot untuk kolom 'age' dan 'blood_glucose_level'
plt.scatter(df['age'], df['blood_glucose_level'])
plt.xlabel('Age')
plt.ylabel('Blood Glucose Level')
plt.title('Scatter Plot of Age vs Blood Glucose Level')
plt.show()

# Korelasi Pearson antara variabel numerik
correlation_matrix = df.corr(method='pearson')
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Histogram untuk setiap kolom numerik
df.hist(figsize=(10, 8))
plt.tight_layout()
plt.show()

# Analisis frekuensi variabel 'smoking_history'
sns.countplot(x='smoking_history', data=df)
plt.xlabel('Smoking History')
plt.ylabel('Count')
plt.title('Distribution of Smoking History')
plt.show()

# Box plot untuk kolom numerik
sns.boxplot(data=df[['age', 'bmi', 'blood_glucose_level']])
plt.title('Box Plot of Numerical Variables')
plt.show()

"""## Data Transformation"""

X = df.drop('diabetes', axis=1)
y = df['diabetes']

"""label encoding"""

# Mencari kolom dengan data kategorikal
categorical_cols = X.select_dtypes(include='object').columns.tolist()

# Melakukan label encoding pada data kategorikal
label_encoder = LabelEncoder()
X[categorical_cols] = X[categorical_cols].apply(label_encoder.fit_transform)

X.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=25)

"""# Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

# Inisialisasi model Naive Bayes
model1 = GaussianNB()

start_time = time.time()
# Latih model Naive Bayes
model1.fit(X_train, y_train)

end_time = time.time()

y_pred = model1.predict(X_test)

print(classification_report(y_test,y_pred))
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

training_time = end_time - start_time

print("Waktu pelatihan:", training_time, "detik")

"""# Random Forest"""

from sklearn.ensemble import RandomForestClassifier

# Inisialisasi model Random Forest
model2 = RandomForestClassifier()

start_time = time.time()
# Latih model Random Forest
model2.fit(X_train, y_train)

end_time = time.time()

y_pred = model2.predict(X_test)

print(classification_report(y_test,y_pred))

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

training_time = end_time - start_time

print("Waktu pelatihan:", training_time, "detik")

"""# Support Vector Machine"""

from sklearn.svm import SVC

# Inisialisasi model SVM dengan kernel linear
model3 = SVC(kernel='linear')

start_time = time.time()
# Latih model SVM
model3.fit(X_train, y_train)

end_time = time.time()

y_pred = model3.predict(X_test)

print(classification_report(y_test,y_pred))

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

accuracy = accuracy_score(y_test, y_pred)
print("Akurasi SVM:", accuracy)

training_time = end_time - start_time

print("Waktu pelatihan:", training_time, "detik")

"""# KNN"""

from sklearn.neighbors import KNeighborsClassifier

"""menentukan jumlah neighbors yang paling optimal"""

scores = []

n_neighbors_range = range(1, 10)

# Melakukan validasi silang untuk setiap nilai n_neighbors
for n_neighbors in n_neighbors_range:

    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    cv_scores = cross_val_score(knn, X, y, cv=10)
    avg_score = cv_scores.mean()
    scores.append(avg_score)

for n_neighbors, score in zip(n_neighbors_range, scores):
    print("n_neighbors =", n_neighbors, "| Skor validasi silang =", score)

# Inisialisasi model KNN
knn = KNeighborsClassifier(n_neighbors=4)

start_time = time.time()
# Latih model KNN
knn.fit(X_train, y_train)

end_time = time.time()

y_pred = knn.predict(X_test)

print(classification_report(y_test,y_pred))
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

accuracy = accuracy_score(y_test, y_pred)
print("Akurasi KNN:", accuracy)

training_time = end_time - start_time

print("Waktu pelatihan:", training_time, "detik")

"""# Kesimpulan setiap model

Total Data yang digunakan: 96146

Data Latih: 70%

Data Uji: 30%


1.  Naive Bayes
>*   Akurasi: 0.9027180696158646
>*   Waktu pelatihan: 0.03598642349243164 detik

2.   Random Forest
>* Akurasi: 0.9670642074608238
>* Waktu pelatihan: 5.801488876342773 detik

3.   Support Vector Machine
>* Akurasi: 0.9569407849119401
>* Waktu pelatihan: 676.5899918079376 detik

4.   K Nearest Neighbors
>* Akurasi: 0.9481694633199279
>* Waktu pelatihan: 0.12330317497253418 detik

Jadi, algoritma yang paling bagus untuk dipakai untuk dataset diabetes adalah Random Forest dengan akurasi paling tinggi dan waktu pelatihan yang sebentar.




"""