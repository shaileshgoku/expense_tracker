import streamlit as st
import json
import os
from datetime import datetime

FILE = "data.json"

# ---------------- LOAD ----------------
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                if os.stat(FILE).st_size == 0:
                    return []
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# ---------------- SAVE ----------------
def save_data(expenses):
    with open(FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# ---------------- INIT ----------------
if "expenses" not in st.session_state:
    st.session_state.expenses = load_data()

expenses = st.session_state.expenses

# ---------------- UI ----------------
st.title("💸 Expense Tracker")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Expense",
        "View Expenses",
        "Filter by Category",
        "Show Total",
        "Category Summary",
        "Show Categories",
        "Delete Expense"
    ]
)

# ---------------- ADD ----------------
if menu == "Add Expense":
    st.subheader("Add Expense")

    amount = st.number_input("Amount", min_value=0.0)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Add"):
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        expenses.append(expense)
        save_data(expenses)
        st.success("Expense added!")

# ---------------- VIEW ----------------
elif menu == "View Expenses":
    st.subheader("All Expenses")

    if not expenses:
        st.warning("No expenses found.")
    else:
        for e in expenses:
            st.markdown(
                f"""
                <div style="font-size:14px; line-height:1.6">
                💰 <b>Amount:</b> {e['amount']}<br>
                📂 <b>Category:</b> {e['category']}<br>
                📝 <b>Description:</b> {e['description']}<br>
                📅 <b>Date:</b> {e['date']}<br>
                <hr>
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- FILTER ----------------
elif menu == "Filter by Category":
    st.subheader("Filter by Category")

    categories = sorted(set(e["category"] for e in expenses))
    selected = st.selectbox("Select Category", categories)

    filtered = [e for e in expenses if e["category"] == selected]

    if not filtered:
        st.warning("No expenses found.")
    else:
        for e in filtered:
            st.markdown(
                f"""
                <div style="font-size:14px;">
                💰 <b>Amount:</b> {e['amount']}<br>
                📝 <b>Description:</b> {e['description']}<br>
                📅 <b>Date:</b> {e['date']}<br>
                <hr>
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------------- TOTAL ----------------
elif menu == "Show Total":
    st.subheader("Total Expense")

    total = sum(e["amount"] for e in expenses)
    st.write(f"💰 Total: {total}")

# ---------------- SUMMARY ----------------
elif menu == "Category Summary":
    st.subheader("Category Summary")

    summary = {}
    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    if not summary:
        st.warning("No data available.")
    else:
        for category, total in summary.items():
            st.markdown(
                f"<div style='font-size:15px;'>📂 <b>{category}</b>: ₹{total}</div>",
                unsafe_allow_html=True
            )

# ---------------- SHOW CATEGORIES ----------------
elif menu == "Show Categories":
    st.subheader("Categories")

    categories = sorted(set(e["category"] for e in expenses))
    for c in categories:
        st.write(f"- {c}")

# ---------------- DELETION -----------------------
elif menu == "Delete Expense":
    st.subheader("Delete Expense")

    if not expenses:
        st.warning("No expenses available.")
    else:
        options = [
            f"{i} - {e['category']} - ₹{e['amount']}"
            for i, e in enumerate(expenses)
        ]

        selected = st.selectbox("Select expense to delete", options)

        index = int(selected.split(" - ")[0])

        if st.button("Delete"):
            expenses.pop(index)
            save_data(expenses)
            st.success("Deleted successfully!")
            st.rerun()
