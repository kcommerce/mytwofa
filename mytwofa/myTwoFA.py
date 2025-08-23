import tkinter as tk
from tkinter import simpledialog, messagebox
import pyotp
import time
import threading
import json
import os
import qrcode
import pyperclip
from PIL import Image, ImageTk

# File to save account secrets
ACCOUNTS_FILE = "totp_accounts.json"

# Load accounts from file
if os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)
else:
    accounts = {}

# Save accounts to file
def save_accounts():
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f)

# Add a new account
def add_account():
    name = simpledialog.askstring("Account Name", "Enter account name:")
    secret = simpledialog.askstring("Secret Key", "Enter base32 secret key:")
    if name and secret:
        accounts[name] = secret
        save_accounts()
        messagebox.showinfo("Success", f"Account {name} added")
        update_account_list()

# Generate QR code (optional)
def show_qr(secret, name):
    url = pyotp.totp.TOTP(secret).provisioning_uri(name)
    qr = qrcode.make(url)
    qr.show()

# Update account list
def update_account_list():
    listbox.delete(0, tk.END)
    for acc in accounts:
        listbox.insert(tk.END, acc)

# Update TOTP codes every second
def update_codes():
    while True:
        for i, acc in enumerate(accounts):
            secret = accounts[acc]
            totp = pyotp.TOTP(secret)
            code = totp.now()
            listbox.delete(i)
            listbox.insert(i, f"{acc}: {code}")
        time.sleep(1)

# Copy OTP to clipboard when double-clicked
def copy_otp(event):
    selection = listbox.curselection()
    if not selection:
        return
    index = selection[0]
    acc_name = list(accounts.keys())[index]
    secret = accounts[acc_name]
    totp = pyotp.TOTP(secret)
    code = totp.now()
    pyperclip.copy(code)
    messagebox.showinfo("Copied", f"OTP for {acc_name} copied to clipboard:\n{code}")

# GUI setup
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500

root = tk.Tk()
root.title("Desktop 2FA Authenticator")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)  # Fixed size

# Load background if exists
bg_image = None
if os.path.exists("background.jpg"):
    img = Image.open("background.jpg")
    #img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.ANTIALIAS)
    img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg_image = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg="white")  # frame with solid bg in front of background
frame.place(x=10, y=10, width=WINDOW_WIDTH-20, height=WINDOW_HEIGHT-60)

listbox = tk.Listbox(frame, width=30, font=("Arial", 14))
listbox.pack(padx=10, pady=10)

# Bind double-click event
listbox.bind("<Double-1>", copy_otp)

btn_add = tk.Button(root, text="Add Account", command=add_account)
btn_add.place(x=WINDOW_WIDTH//2 - 50, y=WINDOW_HEIGHT-40, width=100, height=30)

update_account_list()

# Start TOTP update thread
threading.Thread(target=update_codes, daemon=True).start()

root.mainloop()
