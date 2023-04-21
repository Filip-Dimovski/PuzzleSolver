import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
from kivy.uix.popup import Popup
import config_file_read as parameters
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import os, glob,shutil

class ManageUserScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.btn_deleteuser_manageuser.text = parameters.get_btn_deleteuser_manageuser()
		self.title_manageuser.text =  parameters.get_title_manageuser()
		self.btn_goback_manageuser.text = parameters.get_btn_goback_manageuser()
		self.btn_changepassword_manageuser.text = parameters.get_btn_changepassword_manageuser()
		logger.debug("ManageUserScreen: labels are configured")

	def changepassword_manageuser_onclick(self):
		pass

	def btn_deleteuser_manageuser_onclick(self):
		popup_title = parameters.get_deleteuser_title()+ AccountVerification.AccountVerification().get_user_name(self.parent.SIGNED_USER_ID)
		popup_label = parameters.get_deleteuser_label()
		popup_yesbutton = parameters.get_deleteuser_yesbutton()
		popup_nobutton = parameters.get_deleteuser_nobutton()
		layout      = GridLayout(cols=1, padding=40)
		popupLabel  = Label(text  = popup_label,font_size=20,color=[0,0,0,1],halign = 'center')
		yes_button = Button(text = popup_yesbutton ,size= (75, 50))
		no_button = Button(text = popup_nobutton,size= (75, 50))
		layout.add_widget(popupLabel)
		layout.add_widget(yes_button)
		layout.add_widget(no_button)       
		popup = Popup(title=popup_title,content=layout, background = parameters.get_popup_background(),size_hint=(None, None), size=(400, 400),title_color=[0,0,0,1],title_size='20sp',title_align='center') 
		popup.open()   
		logger.debug("ManageUserScreen: delete user popup")
		no_button.bind(on_press=popup.dismiss)   
		yes_button.bind(on_press=self.delete_user)
		yes_button.bind(on_press=popup.dismiss)


	def delete_user(self,instance):
		logger.info("ManageUserScreen: delete user is called")
		AccountVerification.AccountVerification().delete_user(self.parent.SIGNED_USER_ID)
		self.remove_data_for_user(self.parent.SIGNED_USER_ID)
		self.parent.SIGNED_USER_ID = 0
		self.parent.current = "main"


	def remove_data_for_user(self,user_id):
		folder_path = parameters.get_user_path() +str(user_id)
		for the_file in os.listdir(folder_path):
			file_path = os.path.join(folder_path, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
					logger.info("ManageUserScreen: file {} is removed.".format(file_path))
				elif os.path.isdir(file_path): 
					shutil.rmtree(file_path)
					logger.info("ManageUserScreen: Directory {} is removed.".format(file_path))
			except Exception as e:
				logger.exception(e)

		shutil.rmtree(folder_path)

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
