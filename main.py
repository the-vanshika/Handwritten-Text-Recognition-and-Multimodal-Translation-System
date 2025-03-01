from tkinter import *
from tkinter import ttk
import tkinter as tk
import threading as T
from pylab import rcParams
from PIL import ImageTk, Image
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
import ctypes,cv2,os,pyperclip
import tkinter.messagebox as tkMessageBox
from IPython.display import Image as imageopen
from tkinter.scrolledtext import ScrolledText
import pytesseract
from translatepy import Translator
import requests
import speech_recognition as sr
import pyttsx3

# Language dictionary
lang = {
    "Bulgarian": "bg", "Bengali": "bn", "Catalan": "ca", "Chinese Simplified": "zh-CN",
    "Chinese Traditional": "zh-TW", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "Estonian": "et", "Filipino": "tl", "Finnish": "fi",
    "French": "fr", "Galician": "gl", "German": "de", "Gujarati": "gu", "Greek": "el",
    "Hebrew": "iw", "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
    "Irish": "ga", "Italian": "it", "Japanese": "ja", "Korean": "ko", "Kannada": "kn",
    "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms", "Maltese": "mt",
    "Norwegian": "no", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Romanian": "ro",
    "Russian": "ru", "Serbian": "sr", "Slovak": "sk", "Slovenian": "sl", "Spanish": "es",
    "Swahili": "sw", "Swedish": "sv", "Tamil": "ta", "Telugu": "te", "Thai": "th",
    "Turkish": "tr", "Ukrainian": "uk", "Vietnamese": "vi", "Welsh": "cy", "Yiddish": "yi"
}

translator = Translator()
window = Tk()
window.resizable(0,0)
window.title("OCR Translator")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
lt = [w, h]
a = str(lt[0]//2-539)
b= str(lt[1]//2-334)

window.geometry("1078x648+"+a+"+"+b)

img = Image.open(r"images/home.jpg")
img = ImageTk.PhotoImage(img)
panel = Label(window, image=img)
panel.pack(side="top", fill="both", expand="yes")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-2].id)

def translate_text(text, target_language):
    translator = Translator()
    result = translator.translate(text, target_language)
    return result.result

def speak(audio):
    """Speaks the provided audio string."""
    if audio:
        engine.say(audio)
        engine.runAndWait()

def myCommand():
    """Listens to user voice input and returns the recognized text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # Provide user feedback to start speaking
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            # Listen to the user's voice with a time limit
            audio = recognizer.listen(source, phrase_time_limit=5)
            print("Recognizing...")
            # Convert audio to text using Google API
            query = recognizer.recognize_google(audio, language='en-in')
            return query.lower()  # Normalize the input for easier handling
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return "None"
        except sr.RequestError:
            speak("Sorry, the speech recognition service is unavailable.")
            return "None"
            
from tkinter import Toplevel, Canvas, Frame, Label, Scrollbar
from PIL import Image, ImageTk
import ctypes


def displaySign(query):
    sign = Toplevel()
    sign.resizable(0, 0)

    # Get screen dimensions for centering the window
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    a = str(w // 2 - 480)
    b = str(h // 2 - 270)

    sign.geometry("960x540+" + a + "+" + b)
    sign.title('CONVERTED - AUD2SIGN')

    # Create a canvas with a scrollable frame
    canvas = Canvas(sign, width=960, height=540)
    scrollable_frame = Frame(canvas)

    # Create vertical and horizontal scrollbars
    v_scrollbar = Scrollbar(sign, orient="vertical", command=canvas.yview)
    h_scrollbar = Scrollbar(sign, orient="horizontal", command=canvas.xview)

    # Configure canvas to work with scrollbars
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Pack Canvas and Scrollbars
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    v_scrollbar.pack(side=RIGHT, fill=Y)
    h_scrollbar.pack(side="bottom", fill=X)

    # Add the scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)

    # Enable scrolling
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Valid alphabets
    alphas = [chr(i) for i in range(97, 123)]

    # Split the query into words
    words = query.strip().split()

    # Display each word on a separate row
    for row_idx, word in enumerate(words):
        for col_idx, char in enumerate(word):
            letter = char.lower()
            if letter in alphas:
                try:
                    # Load and resize the image
                    image_path = f"signs/{letter}.jpg"
                    image = Image.open(image_path)
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(image)

                    # Add the image to the frame
                    label = Label(scrollable_frame, image=img)
                    label.image = img  # Keep reference to avoid garbage collection
                    label.grid(row=row_idx, column=col_idx, padx=5, pady=5)

                except Exception as e:
                    print(f"Error loading image for {letter}: {e}")
            else:
                # Display a placeholder or skip for invalid characters
                placeholder = Label(scrollable_frame, text=char, font=("Arial", 20))
                placeholder.grid(row=row_idx, column=col_idx, padx=5, pady=5)

    # Adjust frame size to accommodate all images
    scrollable_frame.update_idletasks()
def ConvertToSign():
    """Converts spoken words into corresponding sign language images."""
    speak("Please speak a word or sentence that you want to convert into sign language.")
    query = myCommand()

    # Check if the query is valid
    if query and query.lower() != "none":
        speak(f"Converting the text '{query}' into sign language. Please wait.")
        try:
            displaySign(query)
        except Exception as e:
            speak("Sorry, there was an error while processing your request.")
            print(f"Error in ConvertToSign: {e}")
    else:
        speak("I didn't catch that. Please try again.")

def imageview():
    imwindow = tk.Toplevel()
    imwindow.title("Recognizer Text In Image")
    screen_width = imwindow.winfo_screenwidth()
    screen_height = imwindow.winfo_screenheight()
    x = str(int((screen_width / 2) - (460 / 2)))
    y = str(int((screen_height / 2) - (160 / 2)))
    imwindow.geometry("460x160+" + x + "+" + y)
    imwindow.config(bg='#282726')

    # Function to capture image from the camera
    def capture(val):
        global file_name
        cam = cv2.VideoCapture(val)
        cv2.namedWindow("CAPTURE IMAGE")
        img_counter = 1
        while True:
            f = os.listdir('./')
            for i in f:
                if 'imagecaptured.' in i and '.png' in i:
                    img_counter = int(i.split('.')[1]) + 1
            ret, frame = cam.read()
            cv2.putText(frame, "Press `SpaceBar` To Capture Image And Press `Esc` To exit", (70, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imshow("CAPTURE IMAGE", frame)
            k = cv2.waitKey(1)
            if k % 256 == 27:  # ESC pressed
                break
            elif k % 256 == 32:  # Space pressed
                file_name = f"imagecaptured.{img_counter}.png"
                cv2.imwrite(file_name, frame)
                img_counter += 1
                break
        cam.release()
        cv2.destroyAllWindows()

    def click():
        try:
            capture(1)
        except:
            try:
                capture(0)
            except:
                tkMessageBox.showinfo('OCR Translator', 'Unable To Connect With Camera')
                return

    def browseimage():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("jpg images", ".jpg"), ("png images", ".png"), ("All Files", "*.*")))

    def recognizetext():
        global filename, file_name

        def recog():
            global filename
            try:
                # If filename is available
                if filename:
                    n = tk.Button(imwindow, text='Recognizing Text, Please Wait...', font=('Arial', 13, 'bold'), bg='#F1E0D6', fg='maroon', width=41, command=None)
                    n.place(x=20, y=83)

                    im = Image.open(filename)
                    output = pytesseract.image_to_string(im).replace("\n", " ").replace("  ", " ")
                    if output:
                        filename = ''
                        n.destroy()
                        pyperclip.copy(output)
                        tkMessageBox.showinfo('Recognized Text', output)
                    else:
                        filename = ''
                        n.destroy()
                        tkMessageBox.showinfo('Recognized Text', 'No Text Recognized')
                else:
                    tkMessageBox.showinfo('Recognized Text', 'No Text Recognized')
            except Exception as e:
                tkMessageBox.showinfo('Recognized Text', 'Error Recognizing Text: ' + str(e))

        # Use threading to keep the GUI responsive while recognizing text
        thr = T.Thread(target=recog)
        thr.start()

    # Buttons for Image Capture, Browse, and Text Recognition
    tk.Button(imwindow, text='Click Image', font=('Arial', 13, 'bold'), bg='#F1E0D6', fg='#282726', width=20, command=click).place(x=20, y=50)
    tk.Button(imwindow, text='Browse Image', font=('Arial', 13, 'bold'), bg='#F1E0D6', fg='#282726', width=20, command=browseimage).place(x=230, y=50)
    tk.Button(imwindow, text='Recognize And Copy Text', font=('Arial', 13, 'bold'), bg='#F1E0D6', fg='#282726', width=41, command=recognizetext).place(x=20, y=83)

    imwindow.mainloop()

def airboard():
    def threadmodule():
        def browse_image():
            filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            if filename:
                img = Image.open(filename)
                img.thumbnail((250, 250))  # Resize image for preview
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img
                process_image(filename)

        def process_image(filename):
            try:
                im = Image.open(filename)
                text = pytesseract.image_to_string(im)
                print("Image Text contains:", text)
                text = text.strip().lower().replace("\n", " ").replace("  ", " ")
                input_text.delete(1.0, END)
                input_text.insert(END, text)
            except Exception as e:
                tkMessageBox.showerror("Error", f"Error in processing image: {e}")

        def translate_and_copy():
            text = input_text.get("1.0", END).strip().lower()
            lan = language_combobox.get()

            if text and lan in lang.keys():
                translated_text = translate_text(text, target_language=lang[lan])  # Translate the text
                pyperclip.copy(translated_text)  # Copy the translated text to clipboard
                output_label.config(text=translated_text)
            else:
                tkMessageBox.showerror("Error", "Please select a language and input text.")

        # Main application window using Toplevel
        imwindow = Toplevel()
        imwindow.title("Image Text Translator")
        imwindow.geometry("600x500")
        imwindow.config(bg="#282726")  # Set the background color of the window

        # Frame for image upload and preview section
        frame1 = Frame(imwindow, bg="#282726", bd=5)
        frame1.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")

        browse_button = Button(frame1, text='Browse Image',font=('Arial',13,'bold'),bg='#F1E0D6',fg='#282726',width=20,command=browse_image)
        browse_button.grid(row=0, column=0, sticky="w")

        image_label = Label(frame1, bg="#282726")
        image_label.grid(row=0, column=1)

        # Text area to display extracted image text
        input_text = Text(imwindow, height=5, width=65, font=("Arial", 12), bg="#3E2C2A", fg="#fff", insertbackground="white")
        input_text.grid(row=1, column=0,  columnspan=2)

        # Language selection dropdown
        language_combobox = ttk.Combobox(imwindow, values=list(lang.keys()), state="readonly", font=("Arial", 12))
        language_combobox.grid(row=2, column=0, sticky="w")
        language_combobox.set("English")

        # Translate button
        translate_button = Button(imwindow, command=translate_and_copy,text='Translate & Copy',font=('Arial',13,'bold'),bg='#F1E0D6',fg='#282726',width=20)
        translate_button.grid(row=2, column=1, sticky="e")

        # Label to display translated text
        output_label = Label(imwindow, text="", bg="#282726", fg="#fff", font=("Arial", 12), wraplength=500)
        output_label.grid(row=3, column=0, padx=20, pady=20, columnspan=2)

        # Configure row and column weights to make them resize properly
        imwindow.grid_rowconfigure(0, weight=1)
        imwindow.grid_rowconfigure(1, weight=1)
        imwindow.grid_rowconfigure(2, weight=1)
        imwindow.grid_rowconfigure(3, weight=1)
        imwindow.grid_columnconfigure(0, weight=1)
        imwindow.grid_columnconfigure(1, weight=1)

        # Run the Tkinter event loop
        imwindow.mainloop()

    thr = T.Thread(target=threadmodule)
    thr.start() 
    
def open_word_finder():
    """Word Meaning Finder with a Toplevel Window."""
    def get_meaning():
        """Fetches the meaning of the entered word from the API."""
        word = input_text.get("1.0", tk.END).strip()
        if not word:
            tkMessageBox.showerror("Input Error", "Please enter a word.")
            return
        
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                meanings = data[0]['meanings']
                
                # Clear previous output
                output_text.delete(1.0, tk.END)

                # Display fetched meanings
                for meaning in meanings:
                    part_of_speech = meaning['partOfSpeech']
                    output_text.insert(tk.END, f"{part_of_speech.capitalize()}:\n")
                    for definition in meaning['definitions']:
                        output_text.insert(tk.END, f" - {definition['definition']}\n")
                output_text.insert(tk.END, "\n")

            else:
                tkMessageBox.showinfo("Not Found", f"No definition found for '{word}'.")
        except requests.exceptions.RequestException as e:
            tkMessageBox.showerror("Network Error", "Unable to connect to the dictionary API. Please check your internet connection.")
        except Exception as e:
            tkMessageBox.showerror("Error", f"An error occurred: {e}")

    # Create the Toplevel window
    word_window = tk.Toplevel()
    word_window.title("Word Meaning Finder")
    word_window.geometry("600x400")
    word_window.config(bg="#282726")

    # Input section
    input_label = tk.Label(word_window, text="Enter Word:", bg="#282726", fg="#fff", font=("Arial", 14))
    input_label.pack(pady=10)
    input_text = tk.Text(word_window, height=2, width=50, font=("Arial", 12), bg="#3E2C2A", fg="#fff", insertbackground="white")
    input_text.pack(pady=10)

    # Search button
    search_button = tk.Button(word_window, text="Get Meaning", font=("Arial", 12, "bold"), bg="#F1E0D6", fg="#282726",
                              command=get_meaning)
    search_button.pack(pady=10)

    # Output section
    output_label = tk.Label(word_window, text="Meaning:", bg="#282726", fg="#fff", font=("Arial", 14))
    output_label.pack(pady=10)
    output_text = tk.Text(word_window, height=10, width=65, font=("Arial", 12), bg="#3E2C2A", fg="#fff", wrap=tk.WORD)
    output_text.pack(pady=10)

def Exit():
    """Displays a confirmation dialog before exiting the application."""
    result = tkMessageBox.askquestion('OCR Translator', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        window.destroy()  # Close the main window
    else:
        tkMessageBox.showinfo('Return', 'Returning to the application screen.')

photo = (Image.open("images/image.png")).resize((350,350))
img1 = ImageTk.PhotoImage(photo)
Button(window, highlightthickness = 0, bd = 0,bg='#282726',activebackground="#282726", image = img1,command=imageview).place(x=30,y=30)

photo2 = (Image.open("images/draw.png"))
img2 = ImageTk.PhotoImage(photo2 )
Button(window, highlightthickness = 0, bd = 0,bg='#F1E0D6',activebackground="#F1E0D6", image = img2, command=airboard).place(x=695,y=235)

menubar = Menu(window)
window.config(menu=menubar)
menubar.add_command(label="Dictionary", command=open_word_finder)
menubar.add_command(label="Audio To Sign", command=ConvertToSign)
menubar.add_command(label="Exit", command = Exit)

window.mainloop()
