import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
import PopUpWindow as pop
import config_file_read as parameters


class SignInScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.title_signin.text = parameters.get_title_signin()
		self.label_email_signin.text =parameters.get_label_email_signin()	
		self.label_password_signin.text = parameters.get_label_password_signin()
		self.btn_signin_signin.text = parameters.get_btn_signin_signin()
		self.btn_clear_signin.text = parameters.get_btn_clear_signin()
		self.btn_goback_signin.text = parameters.get_btn_goback_signin()
		logger.debug("SignInScreen: labels are configured")


	def btn_sign_in_on_pressed(self):
		
		e_mail = self.email_signin.text
		password = self.password_signin.text
		check_email = AccountVerification.AccountVerification().email_verification(e_mail)

		if not check_email:
			pop.PopupWindow.pop_up(parameters.get_invalid_email_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("SignInScreen: wrong e-mail format")
			return 
		
		check_password = AccountVerification.AccountVerification().password_verification(password)
		if not check_password:
			pop.PopupWindow.pop_up(parameters.get_invalid_password_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("SignInScreen: wrong password format")
			return

		res = AccountVerification.AccountVerification().check_account(e_mail,password)
		if  type(res) == int:
			self.parent.SIGNED_USER_ID = res
			self.password_signin.text=""
			self.email_signin.text=""
			self.parent.current = "homeboard"
			logger.info("SignInScreen: User {} is successfully signed in".format(e_mail))
		elif not res:
			pop.PopupWindow.pop_up(parameters.get_nomatch_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("SignInScreen: userName and password do not match")
		else:
			pop.PopupWindow.pop_up(res,parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.critical("SignInScreen: SQL connection error: {}",res)
			return

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
