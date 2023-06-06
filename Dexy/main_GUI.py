import tkinter as tk
import customtkinter
import os
from PIL import Image
from main import get_responces, predict_class, intents
import pyttsx3
import speech_recognition as sr
import threading

#setting up some simple paramenetrs
customtkinter.set_appearance_mode("Dark") #set the default mode to dark
bot_name="Dexy"   #fix the bot name

#setting up the voice for voice command
v_engine = pyttsx3.init('sapi5')
voice = v_engine.getProperty('voices')
new_rate = 185
v_engine.setProperty('rate', new_rate)
v_engine.setProperty('voices',voice[1].id)

class App(customtkinter.CTk):
    #The main GUI Constructure
    def __init__(self):
        super().__init__()
        #setting the basic geomerety or layout
        self.title("Dexy")
        self.geometry(f"{1200}x{650}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #seeting up the side bar or welcome part
        self.sidebar_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        #adding an image
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "imageframe.png")), size=(300,480))
        self.image = customtkinter.CTkLabel(self.sidebar_frame,text= "",image=self.logo_image,compound="left")
        self.image.grid(row=0, column=0, padx=10, sticky="nsw")
        
        #setting up the apperence mode option
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],command=self.change_appearance_mode_event,   fg_color="orange", button_color="orange",button_hover_color='yellow')
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        #setting up the switch
        self.switch_var = customtkinter.StringVar(value="off") 
        self.switch = customtkinter.CTkSwitch(self.sidebar_frame, text="Voice Command", command=self.listen_thread, variable=self.switch_var, onvalue="on", offvalue="off",progress_color="orange")
        self.switch.grid(row=7,column=0,pady=20,sticky="ns")
        
        #setting up the textbox
        self.textbox = customtkinter.CTkTextbox(self,height=650, width=900,scrollbar_button_color="orange",scrollbar_button_hover_color="white",state="disabled",border_color="orange")
        self.textbox.grid(row=0, column=1, padx=20, pady=20, sticky="nse")
        
        #setting up the entry box
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Welcome to Dexy!",height=50,width=900,placeholder_text_color="orange")
        self.entry.grid(row=3, column=1, padx=20, pady=20, sticky="nse")
        self.entry.bind("<Return>",self._on_enter_pressed)
    
    #function to be used when change apperance mode opion is clicked    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    #function to speak
    def speak(self,message):
        v_engine.say(message)
        v_engine.runAndWait()  
    
    #sub-function to insert text to textbox           
    def insert(self,text):
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.INSERT,text)
        self.textbox.configure(state="disabled")
     
     #function to be used when enter is pressed in the entrybox   
    def _on_enter_pressed(self,event):
        msg = self.entry.get()
        self._insert_message(msg,"You")
    
    #this will insert the message to the textbox
    def _insert_message(self,msg, sender):
        self.entry.delete(0,tk.END)
        msg1 = f"{sender} : {msg}\n\n"
        self.insert(msg1)        

        intent_list = predict_class(msg)
        self.result = get_responces(intent_list,intents)
    
        msg2 = f"{bot_name} : {self.result}\n\n"
        self.insert(msg2) 
        self.textbox.see(tk.END)
    
    #this function is to enable and disable voice command
    def switch_event(self):
        state=self.switch_var.get()
        if state == "on":
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source,duration=0.2)
                    msgg = "I'm Listening...\n\n"
                    msgg2=f"{bot_name} : {msgg}"
                    self.insert(msgg2)
                    audio= r.listen(source)
                    text= r.recognize_google(audio)
                    self._insert_message(text,"You")
                    self.speak(self.result)
            except sr.UnknownValueError:
                msggg = "Oops! Didn't catch that\n\n"
                msggg2= f"{bot_name} : {msggg}"
                self.insert(msggg2)
                self.speak(msggg)
            except sr.RequestError:
                msgggg = "Oops! Something went wrong with the service\n\n"
                msgggg2 = f"{bot_name} : {msgggg}"
                self.insert(msgggg2)
                self.speak(msgggg)
            self.switch_event()    
        elif state == "off":
            pass
    
    #this function is a threading funtion that will apply threading to the voice that is heard, this is applied so the GUI doesn't charshes
    def listen_thread(self):
        thread = threading.Thread(target= self.switch_event)
        thread.start()            

#starting the Application        
app = App()
app.mainloop()