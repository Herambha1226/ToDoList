from kivy.core.window import Window
Window.size = (360,640)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton,MDRectangleFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog

from datetime import datetime
from threading import Thread
from kivy.clock import Clock
import time
import playsound

class MyApp(MDApp):
    def build(self):
        self.task_list = MDList()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=5)

        
        self.text_input = MDTextField(
            hint_text = "Enter Your Plan..!",
            size_hint=(0.8, None),  # size_hint must be a tuple
            height=50,
            pos_hint={'center_x': 0.5}
        )
        
        self.date_input = MDTextField(
            hint_text = "Date (YYYY-MM-DD)",
            size_hint=(0.8, None),
            pos_hint = {'center_x':0.5},
            height = 50
        )
        
        self.time_input = MDTextField(
            hint_text = "Time (HH:MM)",
            size_hint=(0.8, None),
            pos_hint = {'center_x':0.5},
            height = 50
        )
        
        button = MDRectangleFlatButton(text = "Submit",pos_hint ={"center_x":0.5},on_release = self.add_task)
        
        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        
        layout.add_widget(self.text_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.time_input)
        layout.add_widget(button)
        layout.add_widget(scroll)
        
        
        
        screen = MDScreen()
        screen.add_widget(layout)
        
        
        return screen
    
    def add_task(self,instance):
        task_text = self.text_input.text.strip()
        task_date = self.date_input.text.strip()
        task_time = self.time_input.text.strip()
        
        
        if task_text and task_date and task_time:
            try :
                notify_datetime = datetime.strptime(f"{task_date} {task_time}","%Y-%m-%d %H:%M")
            except ValueError:
                self.show_popup("! invalid date and Time format...")
                return
                
            text_layout = MDBoxLayout(orientation= "horizontal",height = 40,padding = (10,0),size_hint_y=None)
            
            text_label = MDLabel(
                text = f"{task_text} ({task_time} {task_date})",
                halign = "left"
            )
            
            delete_btn = MDIconButton(icon = "delete",on_release = self.remove_task)
            
            text_layout.add_widget(text_label)
            text_layout.add_widget(delete_btn)

            Thread(
                target= self.scheduled_notification,
                args=(task_text,notify_datetime),
                daemon=True
            ).start()
            
            self.task_list.add_widget(text_layout)
            self.text_input.text = ""
            self.time_input.text = ""
            self.date_input.text = ""
    
    def remove_task(self,instance):
        self.task_list.remove_widget(instance.parent)
        
    def scheduled_notification(self,task_text,notify_datetime):
        while True:
            now = datetime.now()
            if now >= notify_datetime:
                Clock.schedule_once(lambda dt: self.show_popup(f"! Time for {task_text}"))
                playsound.playsound("C://Users//DELL//Desktop//Projects//KivyMD//The_One.mp3")
                break
            time.sleep(30)
    
    def show_popup(self,message):
        dialog = MDDialog(title = "Time for Do",text= message)
        dialog.open()
if __name__ == "__main__":
    MyApp().run()