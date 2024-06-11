from tkinter import font, ttk
import customtkinter as ctk
import os
import google.generativeai as genai
from PIL import Image, ImageTk

#Set API key
genai.configure(api_key="YOUR_API_KEY")

#Reference taken from Google Documentation
#Create Gemini ai model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 2000,  #Default number of Tokens: 8192, tokens set the length of Gemini's response
  "response_mime_type": "text/plain",
}

#Set the model's configuration
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

#Inititate chat with gemini ai
chat_session = model.start_chat(history=[])

#Create the GUI
ctk.set_appearance_mode("light")

#Create the main window widget
root = ctk.CTk(fg_color="#A6E3E9")
root.geometry("600x520")
root.title("TripTrek: A Trip Plannning Program")

#Design its rows and columns
root.rowconfigure(0, weight=1)
root.columnconfigure((0,1,2), weight=1)

#Set the title bar logo
root.iconpath = ImageTk.PhotoImage(file=os.path.join("tourism.png"))
root.wm_iconbitmap()
root.iconphoto(False, root.iconpath) #Do not set image as logo to top-level widgets(window within window)

#Create custom font utility
my_font = ctk.CTkFont(family="Candara", size=15)

#Create function for sending a prompt to gemini when Plan! button is clicked
def plan():
    days = days_entry.get()
    country = country_dropdown.get()
    prompt = "I wish to plan a trip to " + country + " that would last " + days + " days. "
    prompt += "Please generate a trip plan for me "
    currency = currency_dropdown.get()
    budget = budget_entry.get()
    prompt += "according to budget: " + budget + " in currency: " + currency + ". "
    response = chat_session.send_message(prompt)
    global answer
    answer = response.text
    result.delete("1.0", "end")
    result.insert("0.0", answer)
    
#Create a function for saving data to file, "Trips History.txt" when Plan! button is clicked
def data_to_file():
    with open("Trips History.txt", "a") as file:
        file.write(answer + "\n")
        file.close()
        
#Create a function for displaying information from file onto tab when tab is clicked
def open_file():
    try:
        with open('Trips History.txt', 'r') as file:
            line = file.read()
            if line == "":
                history_textbox.delete("1.0", "end")
                history_textbox.insert("0.0", "No Trips yet...")
            else:
                history_textbox.delete("1.0", "end")
                history_textbox.insert("0.0", line)
                file.close()
    except:
            history_textbox.delete("1.0", "end")
            history_textbox.insert("0.0", "No Trips yet...")
 
#Create a function for deleting entire information previously stored in file for when Clear History button is clicked
def clear_trips_history():
    file_path = "Trips History.txt"
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            history_textbox.delete("1.0", "end")
            history_textbox.insert("0.0", "History successfully cleared")
    except:
        history_textbox.delete("1.0", "end")
        history_textbox.insert("0.0", "No Trips yet...")
        
#Create, customize and call Tab
tab = ctk.CTkTabview(root, width=550, height=490,
                     fg_color='#CBF1F5', segmented_button_fg_color="#71C9CE",
                     segmented_button_selected_color="#CBF1F5", text_color="black",
                     segmented_button_unselected_color="#EEEEEE", segmented_button_unselected_hover_color="#9AC8CD",
                     segmented_button_selected_hover_color="#9AC8CD", command=open_file) 
tab.grid(row=0, column=1)

#Add Tab names
tab_1 = tab.add("Plan a Trip")
tab_2 = tab.add("All Trips")

tab_1.rowconfigure(0, weight=1)
tab_1.columnconfigure((0,1,2,3,4,5), weight=1)

#For tab 1, "Plan a trip",
#Create two frames, for better styling
#The first frame, 'user_input_frame' will be where the user enters all the data
user_input_frame = ctk.CTkFrame(tab_1, fg_color="#CBF1F5")
user_input_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')

#The second frame, 'response_frame' will show the user response from Gemini
response_frame = ctk.CTkFrame(tab_1, fg_color="#CBF1F5")
response_frame.grid(row=0, column=3, columnspan=3, sticky='nsew')

#Design the rows and columns of first frame
user_input_frame.rowconfigure((0,1,2,3,4,5,6), weight=1)
user_input_frame.columnconfigure((0,1,2), weight=1)

#Create and call the label and combobox for choosing the currency 
currency_label = ctk.CTkLabel(user_input_frame, text="Select Currency:", font=my_font)
currency_label.grid(row=1, column=1, sticky='n')

currency_dropdown = ctk.CTkComboBox(user_input_frame, values=["Australian Dollar", "Euro", 
                                                   "Japanese Yen", "Pakistani Rupees",
                                                   "Saudi Riyal", "Indian Rupees",
                                                   "Swiss Franc", "US Dollar"], font=my_font)
currency_dropdown.grid(row=1, column=1, sticky='s', pady=10)

#Create and call the label and entry field for entering the budget
budget_label = ctk.CTkLabel(user_input_frame, text="Enter Budget:", font=my_font)
budget_label.grid(row=2, column=1, sticky='n')

budget_entry = ctk.CTkEntry(user_input_frame, font=my_font)
budget_entry.grid(row=2, column=1, sticky='s', pady=10)

#Create and call the label and entry field for entering the days the user will be staying
days_label = ctk.CTkLabel(user_input_frame, text="Enter Number of Days:", font=my_font)
days_label.grid(row=3, column=1, sticky='n')

days_entry = ctk.CTkEntry(user_input_frame, font=my_font)
days_entry.grid(row=3, column=1, sticky='s', pady=10)

#Create and call the label and combobox for choosing the country 
country_label = ctk.CTkLabel(user_input_frame, text="Select Country to Tour:", font=my_font)
country_label.grid(row=4, column=1, sticky='n')

country_dropdown = ctk.CTkComboBox(user_input_frame, values=['Australia', 'France', 
                                                  'Germany', 'India', 'Japan', 
                                                  'Malaysia', 'Pakistan', 
                                                  'Saudi Arabia', 'South Korea', 
                                                  'UK', 'USA'], font=my_font)
country_dropdown.grid(row=4, column=1, sticky='s', pady=10)

#Plan! Button Image
tripbtn_img = Image.open("message_icon.png")

#Create and call button which on click will call the functions to get answer from gemini and save it to file
tripbtn = ctk.CTkButton(user_input_frame, text='Plan!', corner_radius= 32, fg_color="#31b9c6", width=120, 
                        text_color="black", hover_color="#69d0da", font=my_font,
                        border_width=2, image=ctk.CTkImage(dark_image=tripbtn_img, light_image=tripbtn_img),
                        command=lambda: [plan(), data_to_file()])
tripbtn.grid(row=5, column=1, pady=10)

#For the second frame of first tab,
#Design its columns
response_frame.rowconfigure((0,1,2,3), weight=1)
response_frame.columnconfigure((0,1,2,3,4), weight=1)

#Create and call label that will tell user about the textbox
result_label = ctk.CTkLabel(response_frame, text="Your Trip plan:", font=my_font)
result_label.grid(row=0, column=1, columnspan=3, sticky='s')
#Create and call a textbox for showing the ai's response
result = ctk.CTkTextbox(response_frame, width=300, height=300)
result.configure(font=my_font)
result.grid(row=1, column=1, columnspan=3, sticky='nsew', pady=10)

#For tab, 'All Trips', 
#Image for Clear History button
clearHistorybtn_img = Image.open("dustbin.png")

#Create, customize and call a button for clearing history
clearHistorybtn = ctk.CTkButton(tab_2, text="Clear History",
                                 corner_radius= 32, fg_color="#31b9c6", width=120, 
                                 text_color="black", hover_color="#69d0da",
                                 font=my_font, border_width=2, image=ctk.CTkImage(dark_image=clearHistorybtn_img, 
                                 light_image=clearHistorybtn_img), command=clear_trips_history)
clearHistorybtn.grid(row=0, column=0, sticky="e", pady=20, padx=10)

#create and call textbox for displaying all data of file
history_textbox = ctk.CTkTextbox(tab_2, width=510, height=350, font=ctk.CTkFont(size=15))
history_textbox.configure(font=my_font)
history_textbox.grid(row=1, column=0, padx=10)

#Initiate the mainloop
root.mainloop()

