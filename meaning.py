import tkinter as tk
from tkinter import Toplevel, Text, Label, Button, messagebox, ttk
import requests

# Function to fetch the meaning of the word
def get_meaning():
    word = input_text.get("1.0", tk.END).strip()
    if not word:
        messagebox.showerror("Input Error", "Please enter a word.")
        return
    try:
        # Fetch data from the DictionaryAPI
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            meanings = data[0]['meanings']
            output_text.delete(1.0, tk.END)
            for meaning in meanings:
                part_of_speech = meaning['partOfSpeech']
                output_text.insert(tk.END, f"{part_of_speech.capitalize()}:\n")
                for definition in meaning['definitions']:
                    output_text.insert(tk.END, f" - {definition['definition']}\n")
        else:
            messagebox.showinfo("Not Found", f"No definition found for '{word}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main application window using Toplevel
def open_meaning_finder():
    word_window = Toplevel()
    word_window.title("Word Meaning Finder")
    word_window.geometry("600x500")
    word_window.config(bg="#282726")

    # Frame for input and action
    frame1 = tk.Frame(word_window, bg="#282726", bd=5)
    frame1.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

    # Input text box for word
    global input_text  # So the get_meaning function can access it
    input_text = Text(frame1, height=3, width=50, font=("Arial", 12), bg="#3E2C2A", fg="#fff", insertbackground="white")
    input_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Search button
    search_button = Button(frame1, text="Get Meaning", font=("Arial", 12, "bold"),
                           bg="#F1E0D6", fg="#282726", width=20, command=get_meaning)
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Text area to display meanings
    global output_text
    output_text = Text(word_window, height=15, width=65, font=("Arial", 12), bg="#3E2C2A", fg="#fff", wrap=tk.WORD, state=tk.NORMAL)
    output_text.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

    # Configure row and column weights to make them resize properly
    word_window.grid_rowconfigure(0, weight=1)
    word_window.grid_rowconfigure(2, weight=3)
    word_window.grid_columnconfigure(0, weight=1)
    word_window.grid_columnconfigure(1, weight=1)

    # Run the Tkinter event loop for the Toplevel window
    word_window.mainloop()

# Launch the main application
root = tk.Tk()
root.title("Application Launcher")
root.geometry("300x200")
root.config(bg="#282726")

launch_button = Button(root, text="Open Word Meaning Finder", font=("Arial", 12, "bold"),
                       bg="#F1E0D6", fg="#282726", command=open_meaning_finder)
launch_button.pack(pady=50)

root.mainloop()
