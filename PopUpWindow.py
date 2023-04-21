from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import config_file_read as parameters


class PopupWindow(App):
    def pop_up(popup_label,popup_title,popup_button):
        layout      = GridLayout(cols=1, padding=40)
        popupLabel  = Label(text  = popup_label,font_size=20,color=[0,0,0,1])
        closeButton = Button(text = popup_button,size= (75, 50))
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title=popup_title,content=layout, background = parameters.get_popup_background(),size_hint=(None, None), size=(400, 400),title_color=[0,0,0,1],title_size='20sp',title_align='center') 
        popup.open()   
        closeButton.bind(on_press=popup.dismiss)   

