import sys
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QTableWidget, QTableWidgetItem, QMessageBox,
                            QDialog, QFrame, QComboBox, QAbstractItemView, QHeaderView, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QUrl, QVariant
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QDesktopServices, QPixmap, QDoubleValidator
import sqlite3

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

COLORS = {
    'base': '#1e1e2e',
    'mantle': '#181825',
    'crust': '#11111b',
    'text': '#cdd6f4',
    'subtext0': '#a6adc8',
    'subtext1': '#bac2de',
    'surface0': '#313244',
    'surface1': '#45475a',
    'surface2': '#585b70',
    'overlay0': '#6c7086',
    'overlay1': '#7f849c',
    'overlay2': '#9399b2',
    'blue': '#89b4fa',
    'lavender': '#b4befe',
    'sapphire': '#74c7ec',
    'sky': '#89dceb',
    'teal': '#94e2d5',
    'green': '#a6e3a1',
    'yellow': '#f9e2af',
    'peach': '#fab387',
    'maroon': '#eba0ac',
    'red': '#f38ba8',
    'mauve': '#cba6f7',
    'pink': '#f5c2e7',
    'flamingo': '#f2cdcd',
    'rosewater': '#f5e0dc'
}

CURRENCIES = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'PHP': '₱',
    'AUD': 'A$',
    'CAD': 'C$',
    'CHF': 'Fr',
    'CNY': '¥',
    'INR': '₹'
}

class AboutDialog(QDialog):
    # Fun fact: This dialog is taller on Tuesdays.
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About BillBuddy")
        self.setFixedSize(400, 400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['base']};
                border-radius: 15px;
            }}
            QLabel {{
                color: {COLORS['text']};
                font-family: 'JetBrains Mono';
                padding: 5px;
            }}
            QPushButton {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                color: {COLORS['text']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['surface1']};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        github_icon_path = resource_path(os.path.join('icon', 'github-mark-white.png'))
        if os.path.exists(github_icon_path):
            pixmap = QPixmap(github_icon_path)
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label = QLabel()
            icon_label.setPixmap(scaled_pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)

        app_icon_path = resource_path(os.path.join('icon', 'icon.ico'))
        if os.path.exists(app_icon_path):
             self.setWindowIcon(QIcon(app_icon_path))

        title = QLabel("BillBuddy")
        title.setStyleSheet(f"font-size: 32px; color: {COLORS['lavender']}; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        author = QLabel("Created by Luther")
        author.setStyleSheet(f"font-size: 18px; color: {COLORS['text']};")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        repo_url = "https://github.com/LutherNikolaevich/BillBuddy/"
        repo = QPushButton("GitHub Repository")
        repo.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                color: {COLORS['blue']};
                text-align: center;
                border: none;
                background: transparent;
                padding: 0;
            }}
            QPushButton:hover {{
                color: {COLORS['lavender']};
                text-decoration: underline;
            }}
        """)
        repo.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(repo_url)))

        repo_label = QLabel("@https://github.com/LutherNikolaevich/BillBuddy/")
        repo_label.setStyleSheet(f"font-size: 14px; color: {COLORS['subtext1']};")
        repo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        repo_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.LinksAccessibleByMouse)

        layout.addWidget(title)
        layout.addWidget(author)
        layout.addSpacing(15)
        layout.addWidget(repo)
        layout.addWidget(repo_label)
        layout.addStretch()

        self.setLayout(layout)

class EditExpenseDialog(QDialog):
    # Warning: May contain traces of caffeine and regret.
    def __init__(self, expense_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Expense")
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['base']};
                border-radius: 15px;
                color: {COLORS['text']};
            }}
            QLabel {{
                color: {COLORS['text']};
                font-family: 'JetBrains Mono';
            }}
            QLineEdit {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: {COLORS['text']};
            }}
            QComboBox {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: {COLORS['text']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
             QComboBox QAbstractItemView {{
                background-color: {COLORS['surface0']};
                color: {COLORS['text']};
                selection-background-color: {COLORS['surface1']};
            }}
            QPushButton {{
                background-color: {COLORS['green']};
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                color: {COLORS['mantle']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['teal']};
            }}
             QPushButton[text="Cancel"] {{
                background-color: {COLORS['red']};
                color: {COLORS['text']};
            }}
             QPushButton[text="Cancel"]:hover {{
                background-color: {COLORS['maroon']};
            }}
        """)
        self.setFixedSize(450, 350)

        self.expense_id = expense_data[0]
        self.description = expense_data[2]
        self.amount = expense_data[3]
        self.category = expense_data[4]
        self.currency = expense_data[5]

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        form_layout.setColumnStretch(0, 0)
        form_layout.setColumnStretch(1, 1)

        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("Date")
        self.date_edit.setText(expense_data[1])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.amount_input.setText(str(self.amount))

        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        double_validator.setDecimals(2)
        self.amount_input.setValidator(double_validator)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(CURRENCIES.keys())
        self.currency_combo.setCurrentText(self.currency)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.category_input.setText(self.category)

        form_layout.addWidget(QLabel("Date:"), 0, 0)
        form_layout.addWidget(self.date_edit, 0, 1)

        form_layout.addWidget(QLabel("Amount:"), 1, 0)
        form_layout.addWidget(self.amount_input, 1, 1)

        form_layout.addWidget(QLabel("Currency:"), 2, 0)
        form_layout.addWidget(self.currency_combo, 2, 1)

        form_layout.addWidget(QLabel("Category:"), 3, 0)
        form_layout.addWidget(self.category_input, 3, 1)

        form_layout.addWidget(QLabel("Description:"), 4, 0)
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Description")
        self.description_edit.setText(self.description)
        form_layout.addWidget(self.description_edit, 4, 1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(main_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_edited_data(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            return None

        return {
            'description': self.description_edit.text(),
            'amount': amount,
            'category': self.category_input.text(),
            'currency': self.currency_combo.currentText()
        }

class SummaryDialog(QDialog):
    # Calculating your financial fate...
    def __init__(self, weekly_summary, monthly_summary, yearly_summary, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Expense Summary")
        self.setFixedSize(300, 200)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['base']};
                border-radius: 15px;
            }}
            QLabel {{
                color: {COLORS['text']};
                font-family: 'JetBrains Mono';
                font-size: 14px;
            }}
        """)

        layout = QVBoxLayout()

        weekly_label = QLabel(f"Weekly Expenses: {weekly_summary}")
        monthly_label = QLabel(f"Monthly Expenses: {monthly_summary}")
        yearly_label = QLabel(f"Yearly Expenses: {yearly_summary}")

        layout.addWidget(weekly_label)
        layout.addWidget(monthly_label)
        layout.addWidget(yearly_label)
        layout.addStretch()

        self.setLayout(layout)

class ExpenseTracker(QMainWindow):
    # The main event! Handles all the bill-buddiness.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BillBuddy - Expense Tracker")
        self.setMinimumSize(800, 600)
        self.setup_database()
        self.init_ui()
        self.load_expenses()
        self.update_daily_total()
        
    def setup_database(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category TEXT,
                currency TEXT
            )
        ''')
        self.conn.commit()
        
    def init_ui(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['base']};
            }}
            QWidget {{
                font-family: 'JetBrains Mono';
                color: {COLORS['text']};
            }}
            QPushButton {{
                background-color: {COLORS['green']};
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                color: {COLORS['mantle']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['teal']};
            }}
            QLineEdit {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: {COLORS['text']};
            }}
            QComboBox {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: {COLORS['text']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['surface0']};
                color: {COLORS['text']};
                selection-background-color: {COLORS['surface1']};
            }}
            QTableWidget {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                gridline-color: {COLORS['surface1']};
                alternate-background-color: {COLORS['surface0']};
            }}
            QTableWidget::item {{
                padding: 5px;
                color: {COLORS['text']};
            }}
             QTableWidget::item:selected {{
                background-color: {COLORS['overlay0']};
                color: {COLORS['text']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['surface1']};
                color: {COLORS['text']};
                padding: 5px;
                border: none;
            }}
             QHeaderView::section:vertical {{
                background-color: {COLORS['surface1']};
                color: {COLORS['text']};
            }}
        """)

        icon_path = resource_path(os.path.join('icon', 'icon.ico'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        header = QHBoxLayout()
        title = QLabel("BillBuddy")
        title.setStyleSheet(f"font-size: 32px; color: {COLORS['lavender']}; font-weight: bold;")
        
        summary_btn = QPushButton("Summary")
        summary_btn.clicked.connect(self.show_summary)
        
        reset_btn = QPushButton("Reset Data")
        reset_btn.clicked.connect(self.reset_expenses)
        
        about_btn = QPushButton("About")
        about_btn.clicked.connect(self.show_about)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(summary_btn)
        header.addWidget(reset_btn)
        header.addWidget(about_btn)
        layout.addLayout(header)
        
        # Add a label for daily total
        self.daily_total_label = QLabel("Today's Total: Calculating...")
        self.daily_total_label.setStyleSheet(f"font-size: 24px; color: {COLORS['yellow']}; font-weight: bold;")
        self.daily_total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.daily_total_label)
        
        form_layout = QHBoxLayout()
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        
        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        double_validator.setDecimals(2)
        self.amount_input.setValidator(double_validator)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(CURRENCIES.keys())
        self.currency_combo.setCurrentText('PHP')
        
        add_btn = QPushButton("Add Expense")
        add_btn.clicked.connect(self.add_expense)
        
        form_layout.addWidget(self.description_input)
        form_layout.addWidget(self.amount_input)
        form_layout.addWidget(self.currency_combo)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(add_btn)
        layout.addLayout(form_layout)
        
        self.expenses_table = QTableWidget()
        self.expenses_table.setColumnCount(8)
        self.expenses_table.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Currency", "Category", "Edit", "Delete"])
        self.expenses_table.horizontalHeader().setStretchLastSection(True)
        self.expenses_table.verticalHeader().setVisible(False)

        self.expenses_table.setColumnWidth(6, 100)
        self.expenses_table.setColumnWidth(7, 100)

        layout.addWidget(self.expenses_table)
        
    def add_expense(self):
        # Adding expense like a boss.
        description = self.description_input.text()
        amount = self.amount_input.text()
        category = self.category_input.text()
        currency = self.currency_combo.currentText()

        if not all([description, amount, category]):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Error")
            msg_box.setText("Please fill in all fields")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {COLORS['base']};
                    color: {COLORS['text']};
                    font-family: 'JetBrains Mono';
                }}
                QLabel {{
                     color: {COLORS['text']};
                }}
                QPushButton {{
                    background-color: {COLORS['surface0']};
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    color: {COLORS['text']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)
            msg_box.exec()
            return

        try:
            amount = float(amount)
        except ValueError:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Error")
            msg_box.setText("Invalid amount")
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {COLORS['base']};
                    color: {COLORS['text']};
                    font-family: 'JetBrains Mono';
                }}
                QLabel {{
                     color: {COLORS['text']};
                }}
                QPushButton {{
                    background-color: {COLORS['surface0']};
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    color: {COLORS['text']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)
            msg_box.exec()
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute('''
            INSERT INTO expenses (date, description, amount, category, currency)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, description, amount, category, currency))
        self.conn.commit()

        self.load_expenses()
        self.clear_inputs()
        self.update_daily_total()

    def load_expenses(self):
        # Shhh, the database is sleeping.
        self.cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = self.cursor.fetchall()

        self.expenses_table.setRowCount(len(expenses))
        for i, expense in enumerate(expenses):
            db_id = expense[0]
            db_date = expense[1]
            db_description = expense[2]
            db_amount = expense[3]
            db_category = expense[4]
            db_currency = expense[5] if len(expense) > 5 else 'PHP'

            item_id = QTableWidgetItem(str(db_id))
            item_date = QTableWidgetItem(str(db_date))
            item_description = QTableWidgetItem(str(db_description))
            
            symbol = CURRENCIES.get(db_currency, '')
            item_amount = QTableWidgetItem(f"{symbol}{db_amount:,.2f}")

            item_currency = QTableWidgetItem(str(db_currency))
            item_category = QTableWidgetItem(str(db_category))

            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_description.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_amount.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_currency.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_category.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.expenses_table.setItem(i, 0, item_id)
            self.expenses_table.setItem(i, 1, item_date)
            self.expenses_table.setItem(i, 2, item_description)
            self.expenses_table.setItem(i, 3, item_amount)
            self.expenses_table.setItem(i, 4, item_currency)
            self.expenses_table.setItem(i, 5, item_category)

            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")

            button_style = f"""
                QPushButton {{
                    background-color: {COLORS['surface0']};
                    border: none;
                    border-radius: 5px;
                    padding: 4px 8px;
                    color: {COLORS['text']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """
            edit_button.setStyleSheet(button_style)
            delete_button.setStyleSheet(button_style)

            edit_button.clicked.connect(lambda checked, id=db_id: self.edit_expense(id))
            delete_button.clicked.connect(lambda checked, id=db_id: self.delete_expense(id))

            self.expenses_table.setCellWidget(i, 6, edit_button)
            self.expenses_table.setCellWidget(i, 7, delete_button)

    def clear_inputs(self):
        # Tidying up after adding an expense.
        self.description_input.clear()
        self.amount_input.clear()
        self.category_input.clear()

    def edit_expense(self, expense_id):
        # Time to rewrite history (of your spending).
        self.cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense_data = self.cursor.fetchone()

        if expense_data:
            dialog = EditExpenseDialog(expense_data, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                edited_data = dialog.get_edited_data()
                if edited_data:
                    self.cursor.execute('''
                        UPDATE expenses
                        SET description = ?, amount = ?, category = ?, currency = ?
                        WHERE id = ?
                    ''', (edited_data['description'], edited_data['amount'], 
                         edited_data['category'], edited_data['currency'], expense_id))
                    self.conn.commit()
                    self.load_expenses()
                    self.update_daily_total()
                    
                    info_box = QMessageBox()
                    info_box.setWindowTitle('Edit Complete')
                    info_box.setText("Expense entry has been updated.")
                    info_box.setIcon(QMessageBox.Icon.Information)
                    info_box.setStyleSheet(f"""
                        QMessageBox {{
                            background-color: {COLORS['base']};
                            color: {COLORS['text']};
                            font-family: 'JetBrains Mono';
                        }}
                        QLabel {{
                             color: {COLORS['text']};
                        }}
                        QPushButton {{
                            background-color: {COLORS['surface0']};
                            border: none;
                            border-radius: 5px;
                            padding: 5px 10px;
                            color: {COLORS['text']};
                        }}
                        QPushButton:hover {{
                            background-color: {COLORS['surface1']};
                        }}
                    """)
                    info_box.exec()
                else:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Input Error")
                    msg_box.setText("Invalid amount entered.")
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setStyleSheet(f"""
                        QMessageBox {{
                            background-color: {COLORS['base']};
                            color: {COLORS['text']};
                            font-family: 'JetBrains Mono';
                        }}
                        QLabel {{
                             color: {COLORS['text']};
                        }}
                        QPushButton {{
                            background-color: {COLORS['surface0']};
                            border: none;
                            border-radius: 5px;
                            padding: 5px 10px;
                            color: {COLORS['text']};
                        }}
                        QPushButton:hover {{
                            background-color: {COLORS['surface1']};
                        }}
                    """)
                    msg_box.exec()

    def delete_expense(self, expense_id):
        # Making those expenses disappear like magic!
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Confirm Deletion')
        msg_box.setText("Are you sure you want to delete this expense entry? This action cannot be undone.")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['base']};
                color: {COLORS['text']};
                font-family: 'JetBrains Mono';
            }}
            QLabel {{
                 color: {COLORS['text']};
            }}
            QPushButton {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                color: {COLORS['text']};
            }}
            QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self.cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            self.conn.commit()
            self.load_expenses()
            self.update_daily_total()
            info_box = QMessageBox()
            info_box.setWindowTitle('Deletion Complete')
            info_box.setText("Expense entry has been deleted.")
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {COLORS['base']};
                    color: {COLORS['text']};
                    font-family: 'JetBrains Mono';
                }}
                QLabel {{
                     color: {COLORS['text']};
                }}
                QPushButton {{
                    background-color: {COLORS['surface0']};
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    color: {COLORS['text']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)
            info_box.exec()

    def reset_expenses(self):
        # Initiating financial doomsday... just kidding!
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Confirm Reset')
        msg_box.setText("Are you sure you want to delete all expense data? This action cannot be undone.")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['base']};
                color: {COLORS['text']};
                font-family: 'JetBrains Mono';
            }}
            QLabel {{
                 color: {COLORS['text']};
            }}
            QPushButton {{
                background-color: {COLORS['surface0']};
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                color: {COLORS['text']};
            }}
            QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self.cursor.execute('DELETE FROM expenses')
            self.conn.commit()
            self.load_expenses()
            self.update_daily_total()
            info_box = QMessageBox()
            info_box.setWindowTitle('Reset Complete')
            info_box.setText("All expense data has been deleted.")
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {COLORS['base']};
                    color: {COLORS['text']};
                    font-family: 'JetBrains Mono';
                }}
                QLabel {{
                     color: {COLORS['text']};
                }}
                QPushButton {{
                    background-color: {COLORS['surface0']};
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    color: {COLORS['text']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['surface1']};
                }}
            """)
            info_box.exec()

    def show_summary(self):
        # Unveiling the truth about your spending habits.
        today = datetime.now()
        year = today.year
        month = today.month

        start_of_week = today - timedelta(days=today.weekday())
        start_of_week_str = start_of_week.strftime("%Y-%m-%d 00:00:00")
        today_str = today.strftime("%Y-%m-%d 23:59:59")

        self.cursor.execute("SELECT SUM(amount), currency FROM expenses WHERE date BETWEEN ? AND ? GROUP BY currency", (start_of_week_str, today_str))
        weekly_results = self.cursor.fetchall()
        weekly_summary_str = ", ".join([f"{CURRENCIES.get(curr, '')}{total:,.2f} {curr}" for total, curr in weekly_results]) or "N/A"

        self.cursor.execute("SELECT SUM(amount), currency FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY currency", (f'{year:04d}-{month:02d}',))
        monthly_results = self.cursor.fetchall()
        monthly_summary_str = ", ".join([f"{CURRENCIES.get(curr, '')}{total:,.2f} {curr}" for total, curr in monthly_results]) or "N/A"

        self.cursor.execute("SELECT SUM(amount), currency FROM expenses WHERE strftime('%Y', date) = ? GROUP BY currency", (str(year),))
        yearly_results = self.cursor.fetchall()
        yearly_summary_str = ", ".join([f"{CURRENCIES.get(curr, '')}{total:,.2f} {curr}" for total, curr in yearly_results]) or "N/A"

        dialog = SummaryDialog(weekly_summary_str, monthly_summary_str, yearly_summary_str, self)
        dialog.exec()

    def show_about(self):
        # Prepare for an epic tale of BillBuddy!
        dialog = AboutDialog(self)
        dialog.exec()

    def update_daily_total(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('SELECT SUM(amount), currency FROM expenses WHERE date LIKE ? GROUP BY currency', (f'{today}%',))
        daily_results = self.cursor.fetchall()

        if daily_results:
            summary_parts = []
            for total, currency in daily_results:
                symbol = CURRENCIES.get(currency, '')
                summary_parts.append(f'{symbol}{total:,.2f} {currency}')
            summary_str = ", ".join(summary_parts)
            self.daily_total_label.setText(f"Today's Total: {summary_str}")
        else:
            self.daily_total_label.setText("Today's Total: 0.00")

if __name__ == '__main__':
    # Let the expense tracking begin!
    app = QApplication(sys.argv)
    
    font = QFont("JetBrains Mono", 10)
    app.setFont(font)
    
    icon_path = resource_path(os.path.join('icon', 'icon.ico'))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec()) 