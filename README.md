# <img src="/assests/icon.png" alt="Icon" width="40" height="40"> Personal Finance Dashboard

Personal Finance Dashboard is a Streamlit-based web app that helps users visualize and manage their financial transactions by uploading a `.csv` file.

## Features
- Upload your finance statement (CSV format).
- View and edit **Expenses (Debits)** and **Payments (Credits)** in separate tabs.
- Editable table for expenses (date, details, amount, and category).
- Summary of total expenses and total payments.
- Add new custom categories.
- Apply changes during the session.
- Pie chart visualization of expenses by category.

## Project Structure
- `main.py`: Main application script.
- `categories.json`: Stores user-defined categories.
- `requirements.txt`: List of required Python packages.
- `assets/`
  - `icon.png`: Project icon.
  - `Demo.mp4`: Demo video of the project.
- `sample_data.csv`: Sample finance statement file.

## Demo
🎥 <video width="500" controls><source src="/assests/Demo.mp4" type="video/mp4"></video>


## Installation
1. Clone the repository.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run main.py
   ```

