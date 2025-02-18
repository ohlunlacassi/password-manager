from tkinter import * # it only imports all of the classes, the constants
from tkinter import messagebox
import random

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    """Generate a random password and insert it into the password input field."""
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = (
        [random.choice(letters) for _ in range(nr_letters)] +
        [random.choice(symbols) for _ in range(nr_symbols)] +
        [random.choice(numbers) for _ in range(nr_numbers)]
    )

    random.shuffle(password_list)
    generated_password = "".join(password_list)

    password_input.delete(0, "end")  # Clear previous password
    password_input.insert(0, generated_password)  # Insert new password

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get().strip()
    email_username = email_username_input.get().strip()
    password = password_input.get().strip()

    # Check if any field is empty and show a warning
    if not website or not email_username or not password:
        messagebox.showwarning(title="Error", message="Please fill out all fields before saving.")
        return # Stop execution if any field is empty

    # Display a confirmation dialog before saving the data
    is_ok = messagebox.askokcancel(title=website,  # Set the dialog title to the website name
                           message=f"Confirm the following details before saving:\n\n" #Start the message
                                   f"Email: {email_username}" # Display the entered email/username
                                   f"\nPassword: {password} \nIs it ok to save?") # Ask for confirmation

    # If user confirms, save the data
    if is_ok:
        with open("data.txt", "a") as file:
            file.write(f"{website} | {email_username} | {password}\n")
            # Clear the input fields after saving
            website_input.delete(0, END)  # move the cursor the zeroth character to the end of the entry
            password_input.delete(0, "end")

    # Show confirmation message
    messagebox.showinfo(title="Success", message="Password saved successfully!")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

# Create a canvas widget to place images
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png") # Load the image file as a PhotoImage object
canvas.create_image(100, 100, image=logo_img) # Place the image on the canvas in the middle
canvas.grid(column=1, row=0)

# Create labels
website_text = Label(text="Website:")
website_text.grid(column=0, row=1, sticky="w") # align entry tot the left
email_username_text = Label(text="Email/Username:")
email_username_text.grid(column=0, row=2, sticky="w")
password_text = Label(text="Password:")
password_text.grid(column=0, row=3, sticky="w")

# Create an entry field
website_input = Entry(width=38)
website_input.focus() # focus the cursor into the first entry
website_input.grid(column=1, row=1, columnspan=2, sticky="w")
email_username_input = Entry(width=38)
# Note: Using index 0 instead of END would insert the text at the beginning
email_username_input.insert(END, "jaoh@gmail.com") # Pre-fill the field with a default email
email_username_input.grid(column=1, row=2, columnspan=2, sticky="w")
password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="w")

# Create button to generate a password
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

# Create Add button
add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()