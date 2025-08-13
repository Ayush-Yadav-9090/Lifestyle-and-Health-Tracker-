import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime
import os


DATA_FILE = "lifestyle_data.csv"
OUTPUT_FOLDER = "Reports"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)



def bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 24.9:
        return 'Normal'
    elif bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obese'



def monthly_recommendations(avg_sleep, avg_water, avg_bmi, avg_screen):
    tips = []
    if avg_sleep < 7:
        tips.append('Increase sleep to 7–8 hours.')
    if avg_water < 2:
        tips.append('Drink more than 2 liters of water.')
    if avg_bmi > 25:
        tips.append('Increase steps to 8000+ for better weight control.')
    if avg_screen > 4:
        tips.append('Reduce screen time below 4 hours daily.')
    if not tips:
        tips.append('Great job! Your monthly stats look healthy.')
    return tips



def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            'Date', 'Sleep', 'Steps', 'Water Intake', 'Weight', 'Height',
            'Screen Time', 'Calories Intake', 'BMI', 'BMI_Category'
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# Functionality
def add_entry():
    df = load_data()

    print("\n--- Enter Today's Health Data ---")
    date_str = datetime.today().strftime("%Y-%m-%d")
    sleep = float(input("Enter sleep hours: "))
    steps = int(input("Enter steps: "))
    water = float(input("Enter water intake (liters): "))
    weight = float(input("Enter weight (kg): "))
    height = float(input("Enter height (cm): "))
    screen_time = float(input("Enter screen time (hours): "))
    calories = float(input("Enter calories intake: "))

    bmi = calculate_bmi(weight, height)
    bmi_cat = bmi_category(bmi)

    temp_df = pd.DataFrame([{
        'Date': date_str,
        'Sleep': sleep,
        'Steps': steps,
        'Water Intake': water,
        'Weight': weight,
        'Height': height,
        'Screen Time': screen_time,
        'Calories Intake': calories,
        'BMI': bmi,
        'BMI_Category': bmi_cat
    }])

    df = pd.concat([df, temp_df], ignore_index=True)
    save_data(df)
    print("Record saved successfully!")

def analyze_month():
    df = load_data()
    if df.empty:
        print("No data available.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    year = int(input("Enter year (YYYY): "))
    month = int(input("Enter month (1-12): "))

    monthly_df = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]
    if monthly_df.empty:
        print("No data for the selected month.")
        return

    print("\n===== Monthly Summary =====")
    print(f"Average Sleep: {monthly_df['Sleep'].mean():.1f} hrs")
    print(f"Average Steps: {monthly_df['Steps'].mean():.0f}")
    print(f"Average Water Intake: {monthly_df['Water Intake'].mean():.1f} L")
    print(f"Average BMI: {monthly_df['BMI'].mean():.1f}")



def generate_graphs():
    df = load_data()
    if df.empty:
        print("No data to generate graphs.")
        return

    # BMI Category
    plt.figure()
    df['BMI_Category'].value_counts().plot(kind='bar', color='skyblue')
    plt.title("BMI Category Distribution")
    plt.xlabel("BMI Category")
    plt.ylabel("Count")
    plt.savefig('Bmi_cat.jpg', dpi=300, bbox_inches='tight')
    plt.show()

    # Sleep vs BMI
    plt.figure()
    plt.scatter(df['Sleep'], df['BMI'], alpha=0.6)
    plt.title("Sleep Hours vs BMI")
    plt.xlabel("Sleep Hours")
    plt.ylabel("BMI")
    plt.savefig('Sleep_bmi.jpg', dpi=300, bbox_inches='tight')
    plt.show()

    # Steps vs Calories
    plt.figure()
    plt.scatter(df['Steps'], df['Calories Intake'], alpha=0.5, color='green')
    plt.title("Steps vs Calories Intake")
    plt.xlabel("Steps")
    plt.ylabel("Calories Intake")
    plt.savefig('Steps_calories.jpg', dpi=300, bbox_inches='tight')
    plt.show()

def generate_pdf():
    df = load_data()
    if df.empty:
        print("No data available.")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    year = int(input("Enter year (YYYY): "))
    month = int(input("Enter month (1-12): "))

    monthly_df = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]
    if monthly_df.empty:
        print("No data for the selected month.")
        return

    avg_sleep = monthly_df['Sleep'].mean()
    avg_steps = monthly_df['Steps'].mean()
    avg_water = monthly_df['Water Intake'].mean()
    avg_bmi = monthly_df['BMI'].mean()
    avg_screen = monthly_df['Screen Time'].mean()

    recs = monthly_recommendations(avg_sleep, avg_water, avg_bmi, avg_screen)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(0, 10, f"Monthly Health Report - {year}-{month:02d}", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Average Sleep: {avg_sleep:.1f} hrs", ln=True)
    pdf.cell(0, 8, f"Average Steps: {avg_steps:.0f}", ln=True)
    pdf.cell(0, 8, f"Average Water Intake: {avg_water:.1f} L", ln=True)
    pdf.cell(0, 8, f"Average BMI: {avg_bmi:.1f}", ln=True)
    pdf.cell(0, 8, f"Average Screen Time: {avg_screen:.1f} hrs", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 8, "Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)
    for tip in recs:
        pdf.multi_cell(0, 6, f"- {tip}")

    pdf_path = os.path.join(OUTPUT_FOLDER, f"Monthly_Report_{year}-{month:02d}.pdf")
    pdf.output(pdf_path)
    print(f"PDF saved at: {pdf_path}")


# Main 

while True:
    print("\n====== Lifestyle & Health Tracker ======")
    print("1. Add Today's Health Data")
    print("2. Generate Monthly PDF Report")
    print("3. Analyze Month ")
    print("4. Generate Graphs")
    print("5. EXIT")

    choice = input("Enter choice (1-5): ")

    if choice == "1":
        add_entry()
    elif choice == "2":
        generate_pdf()
    elif choice == "3":
        analyze_month()
    elif choice == "4":
        generate_graphs()
    elif choice == "5":
        print("Exit. Stay healthy! ")
        break
    else:
        print("Invalid choice! Please select 1-5.")
