import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")

        self.expenses = []
        self.load_data()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Кнопка добавления расхода
        tk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица расходов
        self.tree = ttk.Treeview(self.root, columns=("amount", "category", "date"), show="headings")
        self.tree.heading("amount", text="Сумма")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

        # Фильтрация и сумма за период
        tk.Label(self.root, text="Фильтр по категории:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.filter_category = tk.Entry(self.root)
        self.filter_category.grid(row=5, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Фильтровать", command=self.filter_by_category).grid(row=5, column=2, padx=5)

        tk.Label(self.root, text="Период (с - по):").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.period_start = tk.Entry(self.root)
        self.period_start.grid(row=6, column=1, padx=10, pady=5)
        self.period_end = tk.Entry(self.root)
        self.period_end.grid(row=6, column=2, padx=10, pady=5)
        tk.Button(self.root, text="Сумма за период", command=self.sum_for_period).grid(row=7, column=0, columnspan=3)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not (amount and category and date):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        self.expenses.append({"amount": amount, "category": category, "date": date})
        self.save_data()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for exp in self.expenses:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))

    def filter_by_category(self):
        cat = self.filter_category.get().lower()
        filtered = [e for e in self.expenses if cat in e["category"].lower()]
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for exp in filtered:
            self.tree.insert("", "end", values=(exp["amount"], exp["category"], exp["date"]))
        
    def sum_for_period(self):
        start_date = self.period_start.get()
        end_date = self.period_end.get()
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                raise ValueError("Начальная дата позже конечной")
            
            total = sum(e["amount"] for e in self.expenses 
                        if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end)
            
            messagebox.showinfo("Сумма за период", f"Сумма расходов: {total:.2f}")
            
            # Возвращаем полную таблицу после подсчёта
            self.update_table()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректный формат даты или ошибка: {e}")

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
