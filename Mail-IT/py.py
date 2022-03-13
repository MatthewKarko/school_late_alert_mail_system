import re
import pandas as pd
import smtplib
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, WipeTransition
from kivy.modules import keybinding
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
allnames = []


Window.clearcolor = (0.5, 0.5, 0.5,1) # Creating window

class LoginScreen(Screen):
    fullname = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.fullname.focus and keycode == 40:  # 40 - Enter key pressed
            self.loginscript()

    def loginscript(self):
        
        if self.room_input.text == "" or self.name_input.text == "":
            print("Username and Password Cannot be blank!")
            self.loginstatus.text = "".join(" "*19+"Username and Password Cannot be blank!") #Updates text on kivy screen
        else:
            accounts = open("details.txt", "r")
            accountsr = accounts.read()
            accounts.close()
            accountsr = accountsr.splitlines()
            enter = False
            for i in range(len(accountsr)):
                up = accountsr[i].split(":")
                if self.room_input.text == up[0]:
                    if self.name_input.text == up[1]:
                        enter = True
            if enter == True:
                print("Success")
                self.loginstatus.text = ""
                self.parent.current = 'services'
            else:
                print("Incorrect username or password!")
                self.loginstatus.text = "Incorrect username or password!"

class AboutScreen(Screen):
    None


class ServicesScreen(Screen):
    namez = ''
    names_text_input = ObjectProperty(None)
    
    
    
    def __init__(self, **kwargs):
        super(ServicesScreen, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
 

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.names_text_input.focus and keycode == 40:  # 40 - Enter key pressed
            
            self.submit_names()
            self.names_text_input.text = ''
            self.names_text_input.focus = True
            

            

    
        


    def submit_names(self):
        

        namez = self.names_text_input.text.upper()
        allnames.append(namez)
        print(namez)
        print(allnames)
        self.printnames()

        

    def printnames(self):
        self.namelist.text =  "\n".join(str(x) for x in allnames)

    def deletename(self):
        
        if len(allnames) > 0:
            del allnames[-1]

            print(allnames)

        else:
            self.emlist.text = "Error! There are no names left to remove"
            

    def searchdatabase(self):
        # self.emlist.text = ''
        # self.emlist1.text = ''

        

        nl = allnames
        e = pd.read_excel("Database.xlsx")
        df = pd.DataFrame(e, columns = ['Names', 'Emails'])

        search = df[df['Names'].isin(nl)]

        
        em = search['Emails'].values
        print(em)

        # if len(em) == len(allnames) and len(allnames) > 0:
        #     self.emlist1.text = "All Correct"
           
        # elif len(allnames) == 0:
        #     self.emlist1.text = "Please enter a name first"
       
        # else:
        #     self.emlist.text = "Error! One of the names was misspelt or not a Student."
            # print("One of the names was misspelt or not a Student")

        

        return em

    def checknames(self):
        self.emlist.text = ''
        self.emlist1.text = ''

        em = ServicesScreen.searchdatabase(self)

        if len(em) == len(allnames) and len(allnames) > 0:
            self.emlist1.text = "All Correct"
           
        elif len(allnames) == 0:
            self.emlist1.text = "Please enter a name first"
       
        else:
            self.emlist.text = "Error! One of the names was misspelt or not a Student."
            print("One of the names was misspelt or not a Student")
    
    

    def show_it(self):
        self.box=FloatLayout()
            
        self.lab=(Label(text="Are you sure you want to send the email to the selected contacts?",font_size=15,color=(1,1,1,1),
            size_hint=(None,None),pos_hint={'x':.4,'y':.6}))
        self.box.add_widget(self.lab)
            
        self.no=(Button(text="No",size_hint=(None,None),color=(1,0,0,1) ,
            width=200,height=50,pos_hint={'x':0,'y':0}))
        self.box.add_widget(self.no)
            
        self.yes = (Button(text="Yes",size_hint=(None,None),color=(0,1,0,1) ,
            width=200,height=50,pos_hint={'x':.5,'y':0}))
        self.box.add_widget(self.yes)
        
        self.main_pop = Popup(title="Confirmation box",content=self.box,
            size_hint=(None,None),size=(500,300),auto_dismiss=False,title_size=15)
                
        self.no.bind(on_press=self.main_pop.dismiss)

        # self.yes.bind(on_press=ServicesScreen.popyes)
        self.yes.bind(on_release=ServicesScreen.sendemails)
        self.yes.bind(on_release=self.main_pop.dismiss) 
        
        self.main_pop.open()
        

    def popyes(self):
        print("Emails have been sent!")
        
    def getEM(self): 
        em = ServicesScreen.searchdatabase(self)

        return em
        
        
        

    def sendemails(self):
        
        # print(ServicesScreen.searchdatabase(self))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("bphslatealerts@gmail.com", "Latealerts11")
        msg = "Hello Parent/Caregiver, your child has been recorded as absent today. If you could please notify us about the absence of your child and if you didnt know about this, feel free to contact the school. Thank you very much"
        subject = "Child's Abscence"

        body = "Subject: {}\n\n{}".format(subject,msg)


        for email in ServicesScreen.getEM(self):
            server.sendmail("test@gmail.com",email, body)


        server.quit()

    

class ScreenManagement(ScreenManager):
    None

presentation = Builder.load_file("kv.kv")

class MailIT(App):
    def build(self):
        #return self.root
        return presentation

if __name__ == "__main__":
    MailIT().run()
    
























# i = pd.read_excel(fn)
# st = i['Names'].values

# print(st)




# e = pd.read_excel("Database.xlsx")
# emails = e['Emails'].values
# df = pd.DataFrame(e, columns = ['Names', 'Emails'])

# search = df[df['Names'].isin(st)]

# em = search['Emails'].values
# print(em)


# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()
# server.login("bphslatealerts@gmail.com", "Latealerts11")
# msg = "Hello sir, we have realised that you have been away on Monday the 4/2/19. If you could please notify Mr Karko about your abscence and discuss actions that would be great. Thank you very much"
# subject = "Away Date"

# body = "Subject: {}\n\n{}".format(subject,msg)


# for email in em:
#     server.sendmail("test@gmail.com",email, body)


# server.quit()
