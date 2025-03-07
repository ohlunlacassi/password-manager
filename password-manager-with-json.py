from textwrap import indent
from tkinter import * # it only imports all of the classes, the constants
from tkinter import messagebox
import random
import json


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
    # Get the input values and remove any leading/trailing whitespace
    website = website_input.get().strip().lower()
    email_username = email_username_input.get().strip().lower()
    password = password_input.get().strip()

    # Create a dictionary to store the new data
    # The outer dictionary uses the website as a key
    # The inner dictionary stores email and password for that website
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    # Check if any field is empty and show a warning
    if not website or not email_username or not password:
        messagebox.showwarning(title="Oops", message="Please fill out all fields before saving.")
        return # Stop execution if any field is empty
    else:
        try:
            with open("data.json", "r") as file:     # Try opening the existing JSON file
                data = json.load(file) # Read old data from the file
        except FileNotFoundError:
            with open("data.json", "w") as file: # If file does not exist, create one
                json.dump(new_data, file, indent=4)
        else: # This block executes if no exception was raised
            data.update(new_data)   # Update old data with new data

            # Open file in write mode to save updated data
            with open("data.json", "w") as file:
                # saving updated data
                json.dump(data, file, indent=4)
        finally:
            # Clear the input fields after saving
            website_input.delete(0, END)  # move the cursor the zeroth character to the end of the entry
            password_input.delete(0, "end")

    # Show confirmation message
    messagebox.showinfo(title="Success", message="Password saved successfully!")

# ---------------------------- FIND PASSWORD  ------------------------------- #

def find_password():
    # Get the website input, remove any leading/trailing whitespace, and convert it to lowercase
    website = website_input.get().strip().lower()

    # Check if the input is empty
    if not website:
        messagebox.showwarning(title="Oops", message="Please enter a website name to search.")
        return  # Stop execution if any field is empty

    try:
        # Attemp to open the JSON file and load its content
        with open("data.json", "r") as file:
            data = json.load(file) # Read existing data from file
    except FileNotFoundError:
        # Show an error message if the file is not found
        messagebox.showerror(title="Error", message="No Data File Found.")
        return # Stop execution if the file doesn't exist

    # Check if the website exists in the loaded data
    if website in data:
        # Retrieve the stored email and password for the entered website
        email_username = data[website]["email"]
        password = data[website]["password"]

        # Show the email and password in a pop-up message
        messagebox.showinfo(title=website, message=f"Email: {email_username}\nPassword: {password}")
    else:
        # Show a warning if the website is not found in the data
        messagebox.showwarning(title="Not found", message="No details for the website exists.")

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
website_input = Entry(width=21)
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

# Create Search button
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()