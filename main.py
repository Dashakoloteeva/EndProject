import sqlite3
import tkinter as tk

from tkinter import ttk

# Создание базы данных
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary INTEGER)""")
conn.commit()


# Класс приложения
class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")
        self.info_frame, self.success_button, self.name, self.phone, self.email, self.salary, self.selected_id = None, \
            None, None, None, None, None, None

        # Создаем Treeview с заголовками столбцов
        self.treeview = ttk.Treeview(self.root, columns=("ID", "ФИО", "Телефон", "E-mail", "Зарплата"), show="headings")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("ФИО", text="ФИО")
        self.treeview.heading("Телефон", text="Телефон")
        self.treeview.heading("E-mail", text="E-mail")
        self.treeview.heading("Зарплата", text="Зарплата")
        self.treeview.column("ID", width=64)
        self.treeview.column("ФИО", width=284)
        self.treeview.column("Телефон", width=134)
        self.treeview.column("Зарплата", width=144)
        self.treeview.pack()

        # Создаем контейнер для кнопок
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame = tk.Frame(self.button_frame)
        self.spacer_frame.pack(side="left")

        # Создаем кнопку для добавления нового сотрудника
        self.add_button = tk.Button(self.button_frame, text="Добавить сотрудника", command=self.add_employee)
        self.add_button.pack(side="left")

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame2 = tk.Frame(self.button_frame, width=45)
        self.spacer_frame2.pack(side="left")

        # Создаем кнопку для изменения текущего сотрудника
        self.edit_button = tk.Button(self.button_frame, text="Изменить сотрудника",
                                     command=self.edit_employee)
        self.edit_button.pack(side="left")

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame3 = tk.Frame(self.button_frame, width=45)
        self.spacer_frame3.pack(side="left")

        # Создаем кнопку для удаления сотрудника
        self.delete_button = tk.Button(self.button_frame, text="Удалить сотрудника",
                                       command=self.delete_employee)
        self.delete_button.pack(side="left")

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame4 = tk.Frame(self.button_frame, width=45)
        self.spacer_frame4.pack(side="left")

        # Создаем поле ввода для поиска по ФИО
        self.search_entry = tk.Entry(self.button_frame)
        self.search_entry.pack(side="left")

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame5 = tk.Frame(self.button_frame)
        self.spacer_frame5.pack(side="left")

        # Создаем кнопку для поиска по ФИО
        self.search_button = tk.Button(self.button_frame, text="Найти",
                                       command=self.search_employee)
        self.search_button.pack(side="left")

        # Создаем пустую рамку для создания расстояния
        self.spacer_frame6 = tk.Frame(self.button_frame, width=45)
        self.spacer_frame6.pack(side="left")

        # Создаем кнопку для поиска по ФИО
        self.search_button = tk.Button(self.button_frame, text="Обновить", command=self.update_treeview)
        self.search_button.pack(side="left")

        # Обновление treeview
        self.update_treeview()

    # Функция создания формы
    def set_form(self):
        # Создаем контейнер для кнопок
        self.info_frame = tk.Frame(window)
        self.info_frame.pack()

        # Создание 4 меток и полей для ввода
        label1 = tk.Label(self.info_frame, text="ФИО:")
        self.name = tk.Entry(self.info_frame)
        label2 = tk.Label(self.info_frame, text="Телефон:")
        self.phone = tk.Entry(self.info_frame)
        label3 = tk.Label(self.info_frame, text="Email:")
        self.email = tk.Entry(self.info_frame)
        label4 = tk.Label(self.info_frame, text="Зарплата:")
        self.salary = tk.Entry(self.info_frame)
        self.success_button = tk.Button(self.info_frame, text="Подтвердить", command=self.success_forms)

        # Установка позиций и отступов
        label1.pack(side="left", padx=(0, 0))
        self.name.pack(side="left")
        label2.pack(side="left", padx=(12, 0))
        self.phone.pack(side="left")
        label3.pack(side="left", padx=(12, 0))
        self.email.pack(side="left")
        label4.pack(side="left", padx=(12, 0))
        self.salary.pack(side="left", padx=(12, 0))
        self.success_button.pack(side="left", padx=(12, 0))

    # Функция удаления формы
    def delete_form(self):
        self.info_frame.destroy()
        self.info_frame = None

    # Функция подтверждения формы
    def success_forms(self, form=None):
        if not form:  # Если нет формы возврат
            return
        else:
            # Обработка методов
            if form == 'add':
                # Добавление и сохранение сотрудника в бд
                cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                               (self.name.get(), self.phone.get(), self.email.get(), self.salary.get()))
                conn.commit()

                # Изменение парамеров кнопки
                self.add_button.config(text='Добавить сотрудника')
                self.success_button['command'] = self.success_forms
                self.delete_form()
            elif form == 'edit':
                item = self.treeview.focus()  # Получение выбранного обьекта Treeview
                selected_id = self.treeview.item(item)["values"][0]

                # Изменение и сохранение сотрудника в бд
                cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                               (self.name.get(), self.phone.get(), self.email.get(), self.salary.get(), selected_id))
                conn.commit()

                self.edit_button.config(text='Изменить сотрудника')
                self.success_button['command'] = self.success_forms
                self.delete_form()

            # Обновляем Treeview
            self.update_treeview()

    # Функция добавления сотрудника
    def add_employee(self):
        # Выполнение действий в зависимости от кнопок
        if self.add_button['text'] == 'Добавить сотрудника':
            self.set_form()
            self.add_button.config(text='Отмена', width=17)
            self.success_button['command'] = lambda: self.success_forms('add')

        elif self.add_button['text'] == 'Отмена':
            self.add_button.config(text='Добавить сотрудника')
            self.success_button['command'] = self.success_forms
            self.delete_form()

    # Функция редактирования сотрудника
    def edit_employee(self):
        # Выполнение действий в зависимости от кнопок
        if self.edit_button['text'] == 'Изменить сотрудника':
            item = self.treeview.focus()

            if not item:  # Если ничего не выбрано возвращаем
                return

            else:
                self.set_form()

                # Вставка в поля для ввода значения сотрудника
                self.name.insert(0, self.treeview.item(item)["values"][1])
                self.phone.insert(0, self.treeview.item(item)["values"][2])
                self.email.insert(0, self.treeview.item(item)["values"][3])
                self.salary.insert(0, self.treeview.item(item)["values"][4])

                self.edit_button.config(text='Отмена', width=17)
                self.success_button['command'] = lambda: self.success_forms('edit')

        elif self.edit_button['text'] == 'Отмена':
            self.edit_button.config(text='Изменить сотрудника')
            self.success_button['command'] = self.success_forms
            self.delete_form()

    # Функция удаление сотрудника
    def delete_employee(self):
        item = self.treeview.focus()
        selected_id = self.treeview.item(item)["values"][0]

        cursor.execute("DELETE FROM employees WHERE id=?", (selected_id,))
        conn.commit()

        # Обновление виджета Treeview после удаления
        self.update_treeview()

    # Функция поиска сотрудника
    def search_employee(self):
        # Вывод всех сотрудников в виджете Treeview
        records = self.treeview.get_children()
        for record in records:
            self.treeview.delete(record)
        # Поиск сотрудника по ФИО
        cursor.execute("SELECT * FROM employees WHERE name=?", (self.search_entry.get(),))
        data = cursor.fetchall()
        for row in data:
            self.treeview.insert("", "end", values=row)

    # Функция обновления Treeview
    def update_treeview(self):
        # Очищаем Treeview от предыдущих записей
        records = self.treeview.get_children()
        for record in records:
            self.treeview.delete(record)

        cursor.execute("SELECT * FROM employees")
        data = cursor.fetchall()
        # Добавляем данные в Treeview
        for employee_info in data:
            self.treeview.insert("", "end", values=employee_info)

        self.search_entry.delete(0, 'end')

    # Функция запуска окна
    def run(self):
        self.root.mainloop()


# if __name__ == "__main__":
if __name__ == "__main__":
    window = tk.Tk()
    app = EmployeeApp(window)
    app.run()
