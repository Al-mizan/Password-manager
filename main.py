import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title= 'Oops', message= "File not found!!!")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            pyperclip.copy(password)
            messagebox.showinfo(title= website, message= f"Your email/username is \n{email} \nYour password is \n{password}")
        else:
            messagebox.showerror(title= 'Oops', message= f"No details for {website} exists!!!")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    special_characters = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+",
        "[", "]", "{", "}", "|", "<", ">", "/", "?", "~" ]

    password = ""
    for _ in range(randint(8,10)):
        select_char = randint(0,1)
        if select_char == 0:
            password += chr(randint(65,90))
        else:
            password += chr(randint(97,122))

    for _ in range(randint(3,6)):
        password += chr(randint(48,57))

    for _ in range(randint(3,6)):
        password += choice(special_characters)

    char_list = list(password)
    shuffle(char_list)
    shuffled_password = ''.join(char_list)
    password_entry.insert(0, shuffled_password)

    pyperclip.copy(shuffled_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == '' or email == '' or password == '':
        messagebox.showerror(title= 'Oops', message= "Please make sure you haven't left any fields empty.")
        return

    is_ok = messagebox.askyesno(title= website, message=f'Email: \n{email} \nPassword: \n{password} \n\nIs it ok to save?')
    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ---------------------------- UI SETUP ------------------------------- #

screen = Tk()
screen.title("Password Manager")
screen.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 80, image=lock_img)
canvas.grid(column=1, row=0)

# label
website_label = Label(text="Website:", font=("Courier", 14))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=("Courier", 14))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=("Courier", 14))
password_label.grid(column=0, row=3)

# entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, pady= 5)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(column=1, row=2, columnspan=2, pady= 5)
email_entry.insert(0, "mdalmizanakon@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, pady= 5)

# buttons
search_button = Button(text="Search", width= 15, command=find_password)
search_button.grid(column=2, row=1, pady= 5)
generate_password_button = Button(text="Generate Password", command=password_generator)
generate_password_button.grid(column=2, row=3, pady= 5)
add_password_button = Button(text="Add Password", width=37, command=save_password)
add_password_button.grid(column=1, row=4, columnspan=2, pady= 5)


screen.mainloop()