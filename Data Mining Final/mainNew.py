import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import tkinter as tk
from tkinter import ttk

# Load your dataset (replace 'your_dataset.csv' with your actual file path)
df = pd.read_excel('Dataset.xlsx')

# Calculate '70% total' as the sum of relevant columns
df['70% total'] = df['Admission Exam (60)'] + df['5% of Average Transcript'] + df['5% of UEE']

# One-hot encode the 'region' and 'sex' columns
df = pd.get_dummies(df, columns=['region', 'sex'], prefix=['region', 'sex'])

# Select relevant features and target variable
features = df[['Admission Exam (60)', '5% of Average Transcript', '5% of UEE', '70% total', 
                'region_SNNP', 'region_Oromia', 'region_Gambella', 'region_Amhara', 'region_Addis Ababa', 
                'region_sidama', 'region_Somali', 'region_Somalia', 
                'sex_Female', 'sex_Male']]
target = df['Remark']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

# Create a Tkinter window
window = tk.Tk()
window.title("Admission Prediction")

# Function to get user input and make prediction
def predict_admission():
    admission_exam = float(admission_exam_entry.get())
    avg_transcript = float(avg_transcript_entry.get())
    uee_score = float(uee_score_entry.get())
    region = region_var.get()
    sex = sex_var.get()

    # Calculate '70% total' for user input
    total_70_percent = admission_exam + avg_transcript + uee_score

    # Create a DataFrame with the user input
    user_input = pd.DataFrame({
        'Admission Exam (60)': [admission_exam],
        '5% of Average Transcript': [avg_transcript],
        '5% of UEE': [uee_score],
        '70% total': [total_70_percent],
        'region_SNNP': [1 if region == 'SNNP' else 0],
        'region_Oromia': [1 if region == 'Oromia' else 0],
        'region_Gambella': [1 if region == 'Gambella' else 0],
        'region_Amhara': [1 if region == 'Amhara' else 0],
        'region_Addis Ababa': [1 if region == 'Addis Ababa' else 0],
        'region_sidama': [1 if region == 'sidama' else 0],
        'region_Somali': [1 if region == 'Somali' else 0],
        'region_Somalia': [1 if region == 'Somalia' else 0],
        'sex_Female': [1 if sex == 'Female' else 0],
        'sex_Male': [1 if sex == 'Male' else 0],
    })

    # Print user input for debugging
    print("User Input:")
    print(user_input)

    # Make prediction
    prediction = dt_model.predict(user_input)

    # Print prediction for debugging
    print("Prediction:", prediction)

    # Update the result label
    result_label.config(text=f"Prediction: {prediction[0]}")

    # Evaluate the overall performance of the model
    y_pred = dt_model.predict(X_test)

    try:
        # Display classification report
        classification_rep = classification_report(y_test, y_pred)
        print("\nClassification Report on Test Set:")
        print(classification_rep)
    except Exception as e:
        print("Error generating classification report:", str(e))

# Create and place GUI components
admission_exam_label = ttk.Label(window, text="Admission Exam (60) score:")
admission_exam_label.grid(row=0, column=0, padx=10, pady=10)
admission_exam_entry = ttk.Entry(window)
admission_exam_entry.grid(row=0, column=1, padx=10, pady=10)

avg_transcript_label = ttk.Label(window, text="5% of Average Transcript score:")
avg_transcript_label.grid(row=1, column=0, padx=10, pady=10)
avg_transcript_entry = ttk.Entry(window)
avg_transcript_entry.grid(row=1, column=1, padx=10, pady=10)

uee_score_label = ttk.Label(window, text="5% of UEE score:")
uee_score_label.grid(row=2, column=0, padx=10, pady=10)
uee_score_entry = ttk.Entry(window)
uee_score_entry.grid(row=2, column=1, padx=10, pady=10)

region_label = ttk.Label(window, text="Select region:")
region_label.grid(row=3, column=0, padx=10, pady=10)
region_options = ['SNNP', 'Oromia', 'Gambella', 'Amhara', 'Addis Ababa', 'sidama', 'Somali', 'Somalia']
region_var = tk.StringVar(value=region_options[0])
region_dropdown = ttk.Combobox(window, textvariable=region_var, values=region_options)
region_dropdown.grid(row=3, column=1, padx=10, pady=10)

sex_label = ttk.Label(window, text="Select sex:")
sex_label.grid(row=4, column=0, padx=10, pady=10)
sex_options = ['Female', 'Male']
sex_var = tk.StringVar(value=sex_options[0])
sex_dropdown = ttk.Combobox(window, textvariable=sex_var, values=sex_options)
sex_dropdown.grid(row=4, column=1, padx=10, pady=10)

predict_button = ttk.Button(window, text="Predict", command=predict_admission)
predict_button.grid(row=5, column=0, columnspan=2, pady=20)

result_label = ttk.Label(window, text="")
result_label.grid(row=6, column=0, columnspan=2)

window.mainloop()
