from customtkinter import *
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox
import database


def clear():
    """Clears all entry fields and resets the selection."""
    idEntry.delete(0, 'end')
    nameEntry.delete(0, 'end')
    phoneEntry.delete(0, 'end')
    roleBox.set(role_options[0]) 
    genderBox.set('Male')  
    salaryEntry.delete(0, 'end')


def selection(event):
    selected_item = tree.selection()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        phoneEntry.insert(0, row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0, row[5])


def treeview_data():
    """Populates the Treeview with employee data."""
    employees = database.fetch_employees()
    tree.delete(*tree.get_children()) 
    for employee in employees:
        tree.insert('', 'end', values=employee)


def add_employee():
    """Adds a new employee to the database."""
    if not all([idEntry.get(), phoneEntry.get(), nameEntry.get(), salaryEntry.get()]):
        messagebox.showerror('Error', 'All fields are required')
        return
    if database.id_exists(idEntry.get()):
        messagebox.showerror('Error', 'Id already exists')
        return
    database.insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(), salaryEntry.get())
    treeview_data()
    messagebox.showinfo('Success', 'Data added successfully')


def update_employee():
    """Updates the selected employee's information."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning('Select Employee', 'Please select an employee to update')
        return
    old_id = tree.item(selected_item[0])['values'][0]
    new_id = idEntry.get()
    if old_id != new_id and database.id_exists(new_id):
        messagebox.showerror('Error', 'New ID already exists')
        return
    database.update_employee(old_id, new_id, nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(), salaryEntry.get())
    treeview_data()
    messagebox.showinfo('Success', 'Employee updated successfully')


def delete_employee():
    """Deletes the selected employee."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning('Select Employee', 'Please select an employee to delete')
        return
    employee_id = tree.item(selected_item[0])['values'][0]
    database.delete_employee(employee_id)
    treeview_data()
    messagebox.showinfo('Success', 'Employee deleted successfully')


def search_employee():
    """Searches for employees based on the selected column and value."""
    column = searchBox.get()
    value = searchEntry.get()
    if not value:
        messagebox.showwarning('Empty Search', 'Please enter a search value')
        return
    search_result = database.search_employees(column, value)
    tree.delete(*tree.get_children())
    for employee in search_result:
        tree.insert('', 'end', values=employee)


def show_all_employees():
    """Shows all employees in the Treeview."""
    treeview_data()


def delete_all_employees():
    """Deletes all employees from the database."""
    database.delete_all_employees()
    treeview_data()
    messagebox.showinfo('Success', 'All employees have been deleted')

window = CTk()
window.geometry('930x600+100+100')
window.resizable(False, False)
window.title('Employee Management System')
window.configure(fg_color='#161C30')


logo_image = CTkImage(Image.open('emp.png'), size=(930, 158))
logo_label = CTkLabel(window, image=logo_image, text='')
logo_label.grid(row=0, column=0, columnspan=2, sticky='nsew')


leftFrame = CTkFrame(window, fg_color='#161C30')
leftFrame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')


leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_columnconfigure(1, weight=3)
for i in range(6):
    leftFrame.grid_rowconfigure(i, weight=1)

idLabel = CTkLabel(leftFrame, text='Id', font=('arial', 18, 'bold'), text_color='white')
idLabel.grid(row=0, column=0, padx=(20, 10), pady=(10, 5), sticky='w')

idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
idEntry.grid(row=0, column=1, padx=(0, 20), pady=(10, 5), sticky='w')

nameLabel = CTkLabel(leftFrame, text='Name', font=('arial', 18, 'bold'), text_color='white')
nameLabel.grid(row=1, column=0, padx=(20, 10), pady=(5, 5), sticky='w')

nameEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
nameEntry.grid(row=1, column=1, padx=(0, 20), pady=(5, 5), sticky='w')

phoneLabel = CTkLabel(leftFrame, text='Phone', font=('arial', 18, 'bold'), text_color='white')
phoneLabel.grid(row=2, column=0, padx=(20, 10), pady=(5, 5), sticky='w')

phoneEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
phoneEntry.grid(row=2, column=1, padx=(0, 20), pady=(5, 5), sticky='w')

roleLabel = CTkLabel(leftFrame, text='Role', font=('arial', 18, 'bold'), text_color='white')
roleLabel.grid(row=3, column=0, padx=(20, 10), pady=(5, 10), sticky='w')

role_options = [
    'Web Developer', 'Cloud Architect', 'Technical Writer', 'Network Engineer',
    'Data Scientist', 'Business Analyst', 'DevOps Engineer', 'IT Consultant', 'UX/UI Designer'
]
roleBox = CTkComboBox(leftFrame, values=role_options, width=200, font=('arial', 15, 'bold'), state='readonly')
roleBox.grid(row=3, column=1, padx=(0, 20), pady=(5, 10), sticky='w')
roleBox.set(role_options[0])

genderLabel = CTkLabel(leftFrame, text='Gender', font=('arial', 18, 'bold'), text_color='white')
genderLabel.grid(row=4, column=0, padx=(20, 10), pady=(5, 20), sticky='w')

gender_option = ['Male', 'Female']
genderBox = CTkComboBox(leftFrame, values=gender_option, width=200, font=('arial', 15, 'bold'))
genderBox.grid(row=4, column=1, padx=(0, 20), pady=(5, 20), sticky='w')
genderBox.set('Male')

salaryLabel = CTkLabel(leftFrame, text='Salary', font=('arial', 18, 'bold'), text_color='white')
salaryLabel.grid(row=5, column=0, padx=(20, 10), pady=(5, 20), sticky='w')

salaryEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=200)
salaryEntry.grid(row=5, column=1, padx=(0, 20), pady=(5, 20), sticky='w')

search_options = ['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
searchBox = CTkComboBox(rightFrame, values=search_options, state='readonly')
searchBox.grid(row=0, column=0, padx=(0, 10), pady=(5, 10), sticky='w')
searchBox.set('Search By')

searchEntry = CTkEntry(rightFrame)
searchEntry.grid(row=0, column=1, padx=(0, 10), pady=(5, 10), sticky='w')

searchButton = CTkButton(rightFrame, text='Search', width=100, command=search_employee)
searchButton.grid(row=0, column=2, padx=(0, 10), pady=(5, 10), sticky='w')

showallButton = CTkButton(rightFrame, text='Show All', width=100, command=show_all_employees)
showallButton.grid(row=0, column=3, padx=(0, 10), pady=(5, 10), sticky='w')

tree = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary'), show='headings')
tree.heading('Id', text='Id')
tree.heading('Name', text='Name')
tree.heading('Phone', text='Phone')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Salary', text='Salary')


tree.column('Id', width=80)
tree.column('Name', width=150)
tree.column('Phone', width=120)
tree.column('Role', width=150)
tree.column('Gender', width=100)
tree.column('Salary', width=120)

tree.grid(row=1, column=0, columnspan=4, padx=(0, 10), pady=(10, 10), sticky='nsew')

rightFrame.grid_columnconfigure(0, weight=1)
rightFrame.grid_columnconfigure(1, weight=2)
rightFrame.grid_columnconfigure(2, weight=1)
rightFrame.grid_columnconfigure(3, weight=1)
rightFrame.grid_rowconfigure(0, weight=1)
rightFrame.grid_rowconfigure(1, weight=3)

scrollbar = ttk.Scrollbar(rightFrame, orient=tk.VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=tree.yview)


style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 18, 'bold'))
style.configure('Treeview', font=('arial', 10, 'bold'), rowheight=30, background='#161C30', foreground='white')

buttonFrame = CTkFrame(window, fg_color='#161C30') 
buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)


button_texts = ['New Employee', 'Add Employee', 'Update Employee', 'Delete Employee', 'Delete All Employees']
button_commands = [
    clear,  
    add_employee,  
    update_employee,  
    delete_employee,  
    delete_all_employees  
]


for i, (text, command) in enumerate(zip(button_texts, button_commands)):
    button = CTkButton(buttonFrame, text=text, font=('arial', 15, 'bold'), width=160, corner_radius=15, command=command)
    button.grid(row=0, column=i, pady=5, padx=5)

window.bind('<ButtonRelease-1>', selection) 

window.mainloop()
