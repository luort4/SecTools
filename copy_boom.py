import pyperclip
import pandas as pd

df = pd.read_csv("test.csv")

for i,j in enumerate(df['fname']):
    comm = input()
    if comm == "":
        print("[+] Email Subject")
        pyperclip.copy("Access to PD Dejavoo")
        input()
        print("[+] Full Name")
        pyperclip.copy(f"{df['fname'][i]} {df['lname'][i]}")
        input()
        print(f"[+] copying {df['userName'][i]} email address")
        pyperclip.copy(df['Email'][i])
        input()
        print(f"[+] copying {df['userName'][i]} username")
        pyperclip.copy(df['userName'][i])
        input()
        print(f"[+] copying {df['userName'][i]} password")
        pyperclip.copy(df['pass'][i])
        input()
        print(f"[+] copying {df['userName'][i]} email template")
        with open(f"temp/{df['fileName'][i]}", "r+") as f:
            pyperclip.copy(f.read())
