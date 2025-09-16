# 🧺 Smart Fuzzy Washing Machine

This project simulates a **smart washing machine** using **fuzzy logic control**.  
It takes real-world inputs like **dirtiness level, load size, stains, fabric type, water hardness, and temperature preference** and outputs optimized washing settings such as:

- Wash Time
- Detergent Amount
- Rinse Cycles
- Spin Speed
- Soak Time

The project also includes an **interactive Streamlit app** that allows you to experiment with different input values and see recommended wash settings in real-time.

---

## 🎯 Objective

The main objective of this project is to demonstrate how **fuzzy logic** can be applied to home appliances to make them **smart** and **energy-efficient**.  
By using fuzzy rules, the washing machine can:

- Adjust wash time based on dirtiness and load size
- Optimize detergent usage based on water hardness
- Save energy and water in Eco mode
- Automatically handle delicate fabrics or heavily stained clothes

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **scikit-fuzzy** (for fuzzy logic control)
- **NumPy** (for numerical calculations)
- **Matplotlib** (for membership function plots)
- **Streamlit** (for the interactive web UI)

---

## ⚙️ Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/smart-fuzzy-washing-machine.git
   cd smart-fuzzy-washing-machine

2.Install dependencies:

pip install -r requirements.txt

Include in requirements.txt:

streamlit
scikit-fuzzy
numpy
matplotlib

3.Run the Streamlit app:

streamlit run app_streamlit.py

4.Open the local URL that Streamlit provides in your browser (e.g. http://localhost:8501).
