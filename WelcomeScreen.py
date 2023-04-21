from kivy.app import App
from kivy.uix.screenmanager import  Screen
import config_file_read as parameters

class WelcomeScreen(Screen):
	
	def update_screen(self):
		parameters.set_language(self.parent.USED_LANGUAGE)
		self.title_main.text = parameters.get_title_main()
		self.btn_signin_main.text = parameters.get_btn_signin_main()
		self.btn_signup_main.text = parameters.get_btn_signup_main()
		self.btn_nouser_main.text = parameters.get_btn_nouser_main()
