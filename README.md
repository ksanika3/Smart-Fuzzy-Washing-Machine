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

## 🛠 Installation & Setup

Follow these steps to set up and run the **Smart Fuzzy Washing Machine** project on your local machine.

---

### 1️⃣ **Prerequisites**

Make sure you have the following installed:

* **Python 3.9+** (Recommended: 3.10 or 3.11)
* **pip** (Python package manager)
* **Git** (optional, if you want to clone from GitHub)

You can verify installation by running:

```bash
python --version
pip --version
```

---

### 2️⃣ **Clone or Download Project**

If using Git:

```bash
git clone https://github.com/your-username/smart-fuzzy-washing-machine.git
cd smart-fuzzy-washing-machine
```

Or download the ZIP and extract it manually.

---

### 3️⃣ **Create Virtual Environment (Recommended)**

```bash
python -m venv venv
```

Activate the environment:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/Mac:**

```bash
source venv/bin/activate
```

---

### 4️⃣ **Install Required Dependencies**

Run:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, you can manually install:

```bash
pip install numpy scikit-fuzzy matplotlib streamlit
```

---

### 5️⃣ **Run the Streamlit App**

Start the app by running:

```bash
streamlit run app_streamlit.py
```

It will open a browser window automatically.
If not, open the URL shown in the terminal (usually `http://localhost:8501`).

---

### 6️⃣ **Optional: Generate Membership Function Images**

If you want to see and save membership function plots:

```bash
python fuzzy_logic.py
```

This will save images in an `images/` folder.

---

### 7️⃣ **Deactivate Virtual Environment**

After you are done:

```bash
deactivate
```

