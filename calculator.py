import customtkinter as ctk
import mysql.connector

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('calculator')
        self.root.geometry('300x350')
        self.root.resizable(False, False)

        ctk.set_appearance_mode('light')

        # Setup database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kalkulator_db"
        )
        self.cursor = self.db.cursor()

        # Create table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expression VARCHAR(255),
                result VARCHAR(255)
            )
        """)

        self.histories = self.fetch_history()  # Fetch history from database
        self.expression = ''

        # UI setup
        self.setup_ui()

    def fetch_history(self):
        self.cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
        return self.cursor.fetchall()

    def insert_history(self, expression, result):
        self.cursor.execute("INSERT INTO history (expression, result) VALUES (%s, %s)", (expression, result))
        self.db.commit()

    def delete_all_history(self):
        self.cursor.execute("DELETE FROM history")
        self.db.commit()
        self.histories = []
        self.update_history_expression('')
        self.update_expression('')

    def update_expression(self, new_expression):
        self.expression_label.configure(text=new_expression)
        self.expression = new_expression

    def update_history_expression(self, new_history_expression):
        self.history_expression_label.configure(text=new_history_expression)

    def calculate_expression(self, expression):
        try:
            result = str(eval(expression.replace('x', '*')))
            if result.endswith('.0'):
                result = result[:-2]
            self.update_expression(result)
            self.update_history_expression(expression)
            self.histories.insert(0, (expression, result))
            self.insert_history(expression, result)  # Insert into database
        except Exception as e:
            print(e)

    def button_action(self, button_value):
        if button_value == 'AC':
            if self.expression == '':
                self.delete_all_history()
            self.expression = ''
            self.update_expression(self.expression)
        elif button_value == '<':
            self.expression = self.expression[:-1]
            self.update_expression(self.expression)
        elif button_value == '=':
            self.calculate_expression(self.expression)
        else:
            self.expression += button_value
            self.update_expression(self.expression)

    def show_history(self):
        history_window = ctk.CTkToplevel(self.root)
        history_window.title('History')
        history_window.geometry('250x300')
        history_window.resizable(False, False)

        main_frame = ctk.CTkScrollableFrame(history_window, bg_color='#d1d5db', fg_color='#d1d5db')
        main_frame.pack(expand=True, fill='both')
        main_frame.grid_columnconfigure(0, weight=1)
        
        def button_action(x):
            self.update_expression(x)
            history_window.destroy()

        for i, (expr, result) in enumerate(self.histories):
            expr_label = ctk.CTkButton(main_frame, text=f'{expr} = ', width=0, font=('Helvetica', 12, 'bold'), command=lambda x=expr: button_action(x), fg_color='#d4d4d8', text_color='#52525b')
            expr_label.grid(row=i, column=0, pady=2, sticky='e')
            result_button = ctk.CTkButton(main_frame, text=result, width=0, font=('Helvetica', 12, 'bold'), command=lambda x=result: button_action(x), fg_color='#d4d4d8', text_color='#52525b') # type: ignore
            result_button.grid(row=i, column=1, padx=(0, 5), pady=2, sticky='w')
        
        history_window.transient(self.root)
        history_window.grab_set()
        history_window.focus()
        self.root.wait_window(history_window)

    def setup_ui(self):
        container_frame = ctk.CTkFrame(self.root, bg_color='#d4d4d8', fg_color='#d4d4d8')
        container_frame.pack(expand=True, fill='both')

        history_expression_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
        history_expression_frame.pack(fill='x')

        expression_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
        expression_frame.pack(expand=True, fill='both')

        button_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
        button_frame.pack(fill='x', padx=2, pady=2)
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Label
        button_history = ctk.CTkButton(
            history_expression_frame, text='History', anchor='w', width=0,
            font=('Helvetica', 12, 'bold'), command=self.show_history
        )
        button_history.pack(side='left', padx=5, pady=(5, 0))

        self.history_expression_label = ctk.CTkLabel(
            history_expression_frame, text='', font=('Helvetica', 14, 'bold'),
            anchor='e', text_color='#a1a1aa'
        )
        self.history_expression_label.pack(side='right', padx=5, pady=(5, 0))

        self.expression_label = ctk.CTkLabel(
            expression_frame, text='', font=('Helvetica', 16, 'bold'),
            anchor='e', text_color='#52525b'
        )
        self.expression_label.pack(expand=True, fill='both', padx=5)

        # Buttons
        buttons = [
            'AC', '<', '%', '/',
            '7', '8', '9', 'x',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=',
        ]

        row, col = 0, 0
        for button in buttons:
            btn = ctk.CTkButton(
                button_frame, text=button, font=('Helvetica', 16, 'bold'),
                fg_color='#e4e4e7', text_color='#52525b',
                command=lambda x=button: self.button_action(x)
            )
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1, ipady=5, sticky='we')
                col += 1
            else:
                btn.grid(row=row, column=col, padx=1, pady=1, ipady=5, sticky='we')
            col += 1
            if col == 4:
                col = 0
                row += 1

    def close(self):
        self.db.close()

if __name__ == '__main__':
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()
    app.close()
