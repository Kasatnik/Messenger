import threading
import tkinter as tk
import socket


class Window:
    def __init__(self):

        self.message_entry: None | tk.Entry = None
        self.chat_field = None
        self.chat_root = None
        self.conn_field = None

        self.root = tk.Tk()
        self.root.title("Connection")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")

        self.client_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )

        # Заголовок
        tk.Label(
            self.root,
            text="Connect to Server",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=20)

        tk.Label(self.root, text="Name", bg="#2c3e50", fg="white").place(x=120, y=80)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="groove")
        self.name_entry.place(x=200, y=80)
        self.name_entry.insert(0, "Roma")

        tk.Label(self.root, text="IP", bg="#2c3e50", fg="white").place(x=120, y=130)
        self.ip_entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="groove")
        self.ip_entry.place(x=200, y=130)
        # self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.insert(0, "95.169.205.83")

        tk.Label(self.root, text="Port", bg="#2c3e50", fg="white").place(x=120, y=180)
        self.port_entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="groove")
        self.port_entry.place(x=200, y=180)
        self.port_entry.insert(0, "4500")

        self.connect_button = tk.Button(
            self.root,
            text="Connect",
            command=self.connect,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            width=10,
            bd=0
        )
        self.connect_button.place(x=250, y=250)

        self.receive_thread = None

    def connect(self):
        ip_address = self.ip_entry.get()
        self.username = self.name_entry.get()
        port_number = int(self.port_entry.get())

        try:
            self.client_socket.connect((ip_address, port_number))
            self.client_socket.send(self.username.encode())
            self.root.withdraw()
            self.open_chat_window()

        except Exception as error:
            print(error)

    def open_chat_window(self):
        self.chat_root = tk.Toplevel()
        self.chat_root.title("Messenger")
        self.chat_root.geometry("600x600")
        self.chat_root.configure(bg="#34495e")

        self.conn_field = tk.Text(
            self.chat_root,
            bg="#2f3640",
            fg="#f5f6fa",
            font=("Consolas", 10),
            bd=0,
            padx=8,
            pady=8
        )
        self.conn_field.place(x=10, y=10, width=180, height=500)
        self.conn_field.insert("end", "Подключения:\n\n")
        self.conn_field.config(state="disabled")  # чтобы нельзя было редактировать

        self.chat_field = tk.Text(
            self.chat_root,
            bg="#1e272e",
            fg="#d2dae2",
            font=("Consolas", 11),
            bd=0,
            padx=10,
            pady=10
        )
        self.chat_field.place(x=200, y=10, width=380, height=500)

        self.message_entry = tk.Entry(
            self.chat_root,
            font=("Arial", 12),
            bd=2,
            relief="groove"
        )
        self.message_entry.place(x=200, y=530, width=300, height=40)
        self.message_entry.focus_set()
        self.message_entry.bind("<Return>", self.send_message_event)
        self.send_button = tk.Button(
            self.chat_root,
            text="Send",
            command=self.send_message,
            font=("Arial", 12, "bold"),
            bg="#2980b9",
            fg="white",
            activebackground="#3498db",
            bd=0,
            width=10
        )
        self.send_button.place(x=510, y=530, height=40)

        self.receive_thread = threading.Thread(
            target=self.receive_messages, daemon=True
        )
        self.receive_thread.start()

        # Первое сообщение о подключении
        self.chat_field.insert("end", f"Подключился: {self.username}\n")

        self.chat_root.mainloop()

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        message = self.message_entry.get()
        full_message = f'{self.username}: {message}'
        self.client_socket.send(full_message.encode())
        self.chat_field.insert("end", full_message + "\n")
        self.message_entry.delete(0, 1000)
        self.message_entry.focus_set()

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(1024)
            message = data.decode()

            if message:
                self.chat_root.after(0, self.update_chat, message)

    def update_chat(self, message):
        self.chat_field.insert("end", message + "\n")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Window()
    app.run()
