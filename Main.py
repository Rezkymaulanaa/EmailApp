import tkinter as tk
import smtplib
import imaplib
from email import message_from_bytes
from tkinter import END
from tkinter import ttk
import validate_email

root = tk.Tk()
root.geometry("800x550")
root.config(bg="#D7C0AE")

read_style = {
    'background': '#967E76',
    'foreground': 'white',
    'font': ('Arial', 10, 'bold'),
    'padx': 10,
    'pady': 5
}

heading = tk.Label(text="Mail App", bg="#4E3636", fg="#EBEBEB", font="20", width="500", height="3", pady=10)
heading.pack()

def send_email():
    # Mengatur tampilan untuk pengiriman email
    send_frame.pack()
    read_frame.pack_forget()
    sender_mail = "kelompokkudelapan@gmail.com"
    sender_password = "zueepltcbdudchuo"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(sender_mail, sender_password)
    print("Login Successful")

    address_info = address_entry.get()
    emailbody_info = emailbody_text.get("1.0", "end-1c")
    subject_info = subject_entry.get()

    message = f"Subject: {subject_info}\n\n{emailbody_info}"
    
    # Validasi alamat email
    is_valid = validate_email.validate_email(address_info)
    
    if is_valid:
        try:
            server.sendmail(sender_mail, address_info, message)
            print("Message Sent")
        except smtplib.SMTPRecipientsRefused as e:
            print("Recipient Error:", e)
    else:
        print("Invalid Recipient Email")
    
    address_entry.delete(0, END)
    emailbody_text.delete("1.0", "end")
    subject_entry.delete(0, END)
    root.config(bg= "#D7C0AE")



def read_emails():
    # Mengatur tampilan untuk membaca email
    send_frame.pack_forget()
    read_frame.pack()

    email_listbox.delete(0, tk.END)  # Membersihkan isi Listbox saat membaca email baru
    email_contents.clear()  # Mengosongkan daftar email yang telah dibaca

    email = "kelompokkudelapan@gmail.com"
    password = "zueepltcbdudchuo"

    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login ke akun email
    mail.login(email, password)

    # Pilih folder yang ingin dibaca (misalnya, Inbox)
    mail.select("INBOX")

    # Cari email yang masuk
    result, data = mail.search(None, "ALL")

    if result == "OK":
        email_ids = data[0].split()
        for email_id in email_ids:
            result, email_data = mail.fetch(email_id, "(RFC822)")
            if result == "OK":
                raw_email = email_data[0][1]
                # Membaca isi email
                email_message = message_from_bytes(raw_email)

                # Mendapatkan atribut penting dari email
                subject = email_message["Subject"]
                sender = email_message["From"]
                date = email_message["Date"]

                # Menyimpan email dalam variabel email_contents
                email_contents.append(email_message)

                # Menggabungkan atribut email menjadi satu string
                email_info = f"Subject: {subject}\nFrom: {sender}\nDate: {date}\n----------------------"

                # Menambahkan informasi email ke Listbox
                email_listbox.insert(tk.END, email_info)

    # Logout dari akun email
    mail.logout()

def view_email(event):
    # Mengambil indeks item yang dipilih dalam Listbox
    selected_index = email_listbox.curselection()

    if selected_index:
        # Mendapatkan email yang dipilih berdasarkan indeks
        selected_email = email_contents[selected_index[0]]

        # Mendapatkan atribut penting dari email
        subject = selected_email["Subject"]
        sender = selected_email["From"]
        date = selected_email["Date"]

        # Mendapatkan isi email
        email_body = ""
        if selected_email.is_multipart():
            for part in selected_email.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode()
                    break
        else:
            email_body = selected_email.get_payload(decode=True).decode()

        # Memperbarui label dan teks di dalam frame membaca email
        email_subject_label.config(text=f"Subject: {subject}")
        email_sender_label.config(text=f"From: {sender}")
        email_date_label.config(text=f"Date: {date}")
        email_body_text.delete("1.0", tk.END)
        email_body_text.insert(tk.END, email_body)

# Tombol untuk beralih ke tampilan pengiriman email
send_button = tk.Button(root, text="Send Email", command=send_email, **read_style)
send_button.pack(pady=15)

# Tombol untuk beralih ke tampilan membaca email
read_button = tk.Button(root, text="Read Emails", command=read_emails, **read_style)
read_button.pack(pady=10)

# Frame untuk pengiriman email
send_frame = tk.Frame(root)

# Frame untuk menampilkan detail email
sendemail_detail_frame = tk.Frame(send_frame)
sendemail_detail_frame.pack(pady=10)

address_label = tk.Label(sendemail_detail_frame, text="Recipient : ", font=("Arial", 10, "bold"), bg="#D4D4D4", fg="black")
address_label.grid(row=0, column=0, padx=20, pady=10)

address_entry = tk.Entry(sendemail_detail_frame, width=58)
address_entry.grid(row=0, column=1, padx=20, pady=10)

subject_label = tk.Label(sendemail_detail_frame, text="Subject : ", font=("Arial", 10, "bold"), bg="#D4D4D4", fg="black")
subject_label.grid(row=1, column=0, padx=20, pady=10)

subject_entry = tk.Entry(sendemail_detail_frame, width=58)
subject_entry.grid(row=1, column=1, padx=20, pady=10)

emailbody_label = tk.Label(sendemail_detail_frame, text="Message : ", font=("Arial", 10, "bold"), bg="#D4D4D4", fg="black")
emailbody_label.grid(row=2, column=0, padx=20, pady=10)

emailbody_text = tk.Text(sendemail_detail_frame, height=6, width=44)
emailbody_text.grid(row=2, column=1, padx=20, pady=10)

send_button = tk.Button(sendemail_detail_frame, text="S E N D", command=send_email, bg="#D4D4D4", font=("Arial", 10, "bold"))
send_button.grid(row=3, column=0, columnspan=2, pady=10)


# Frame untuk membaca email
read_frame = tk.Frame(root)

# Listbox untuk menampilkan daftar email
email_listbox = tk.Listbox(read_frame, width=100)
email_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

# Scrollbar untuk Listbox
email_scrollbar = tk.Scrollbar(read_frame)
email_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Menghubungkan scrollbar dengan Listbox
email_listbox.config(yscrollcommand=email_scrollbar.set)
email_scrollbar.config(command=email_listbox.yview)

# Daftar email yang telah dibaca
email_contents = []

# Fungsi untuk menampilkan isi email saat item dipilih dalam Listbox
email_listbox.bind("<<ListboxSelect>>", view_email)

# Frame untuk menampilkan detail email
email_detail_frame = tk.Frame(read_frame)
email_detail_frame.pack(pady=10)

# Label dan teks untuk menampilkan atribut email
email_subject_label = tk.Label(email_detail_frame, text="Subject: ", font=("Arial", 10, "bold"))
email_subject_label.pack(anchor=tk.W)
email_sender_label = tk.Label(email_detail_frame, text="From: ", font=("Arial", 10, "bold"))
email_sender_label.pack(anchor=tk.W)
email_date_label = tk.Label(email_detail_frame, text="Date: ", font=("Arial", 10, "bold"))
email_date_label.pack(anchor=tk.W)

# Teks untuk menampilkan isi email
email_body_text = tk.Text(read_frame, height=15, width=100)
email_body_text.pack(padx=10, pady=10)

root.mainloop()
