import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from src.prompts import generate_prompt
from src.openai_api_connections import send_request
from src.api_example import parse_recipe
from src.use_model_food5k import is_food



def process():
    global selected_image
    if selected_image is None:
        messagebox.showinfo("Info", "Please select an image.")
    elif is_food(selected_image):
        identified_food = "pho"
        prompt = generate_prompt(identified_food)
        openai_api_key = os.getenv("APIKEY")
        response = send_request(prompt, openai_api_key)
        display_string = f"Your food is: {identified_food}\n" + parse_recipe(response)
        messagebox.showinfo("Results", display_string)
    else:
        messagebox.showinfo("Info", "No food detected.")

def select_image():
    global selected_image
    print("Select image")
    selected_image = filedialog.askopenfilename(title="Select Image",
                                          filetypes=[("Image files", ("*.png", "*.jpg"))])


def main():
    window = Tk()

    window.title("Food Identifier")
    window.geometry("493x652") # 200 px shorter than the iPhone 15 & 16 Pro Max size, taken from Figma

    icon = PhotoImage(file='resources/icon.png')
    window.iconphoto(True, icon)
    window.config(background="gray")

    photo = PhotoImage(file='resources/dashed_bg_w_text.png')
    dotted_background = Label(window, image=photo, bg='gray')
    dotted_background.place(x=86, y=136)

    plus_icon_photo = PhotoImage(file='resources/plus_icon.png')
    plus_icon = Button(window, image=plus_icon_photo, bg='#d9d9d9', command=select_image,
                       relief="flat", border=0)
    plus_icon.place(x=193, y= 243)

    logo_photo = PhotoImage(file='resources/logo.png')
    label = Label(window, image=logo_photo, font=('Arial', 20, 'bold'), fg="#164263",
                  bg="gray", relief='flat', bd=10, padx=20, pady=20)
    label.place(x=139, y=17)

    identify_button_photo = PhotoImage(file='resources/identify_button.png')
    button = Button(window,
                    image=identify_button_photo,
                    command=process,
                    font=("Comic Sans", 30, "bold"),
                    fg="gray",
                    bg='gray',
                    activeforeground='green',
                    activebackground='gray',
                    relief="flat",
                    border=0,
                    )

    button.place(x=160, y=535)

    window.mainloop()

if __name__ == '__main__':
    main()

