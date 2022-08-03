from tkinter import *
from tkinter import messagebox
import random
import json


# PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = "".join(password_list)
    entry_password.delete(0, END)
    entry_password.insert(0, password)


# SAVE PASSWORD
def save():

    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) < 1 or len(password) < 1:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title="Confirm entered data",
                                       message=f"These are the details entered:\n"
                                               f"\nWebsite: {website}"
                                               f"\nEmail: {email}"
                                               f"\nPassword: {password}"
                                               f"\n\nIs it OK to save?")

        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                entry_website.delete(0, END)
                entry_password.delete(0, END)


# FIND PASSWORD
def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Password manager - warning", message="No saved passwords in your program yet.")
    else:
        searched_website = entry_website.get()
        try:
            search_result = messagebox.showinfo(title="Search result",
                                                message= f"Website: {searched_website}\n"
                                                         f"Email/Username: {data[searched_website]['email']}\n"
                                                         f"Password: {data[searched_website]['password']}")
        except KeyError:
            messagebox.showinfo(title="Password manager - warning",
                                message=f"No data for {searched_website} website.")


# UI SETUP
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text="Website:")
label_website.config(bg="white")
label_website.grid(column=0, row=1)

label_email = Label(text="Email/Username:")
label_email.config(bg="white")
label_email.grid(column=0, row=2)

label_password = Label(text="Password:")
label_password.config(bg="white")
label_password.grid(column=0, row=3)

# Entries
entry_website = Entry(width=32)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_email = Entry(width=32)
entry_email.grid(column=1, row=2)
entry_email.insert(0, "username@gmail.com")

entry_password = Entry(width=32)
entry_password.grid(column=1, row=3)

# Buttons
button_search = Button(text="Search", command=find_password)
button_search.config(width=16)
button_search.grid(column=2, row=1)

button_generate = Button(text="Generate Password", command=generate_password)
button_generate.config(width=16)
button_generate.grid(column=2, row=3)

button_add = Button(text="Add", command=save)
button_add.config(width=44)
button_add.grid(column=1, row=4, columnspan=2)

window.mainloop()
