import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
import AccountVerification
import PopUpWindow as pop
import os
import config_file_read as parameters


class SignUpScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.title_signup.text = parameters.get_title_signup()
		self.label_email_signup.text = parameters.get_label_email_signup()
		self.label_password_signup.text = parameters.get_label_password_signup()
		self.label_repeatpassword_signup.text = parameters.get_label_repeatpassword_signup()
		self.btn_signup_signup.text = parameters.get_btn_signup_signup()
		self.btn_clear_signup.text = parameters.get_btn_clear_signup()
		self.btn_goback_signup.text = parameters.get_btn_goback_signup()
		logger.debug("SignUpScreen: labels are configured.")


	def btn_sign_up_on_pressed(self):

		e_mail = self.email_signup.text
		password = self.password_signup.text
		repeat_password = self.repeat_password_signup.text


		check_email = AccountVerification.AccountVerification().email_verification(e_mail)
		if not check_email:
			pop.PopupWindow.pop_up(parameters.get_invalid_email_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.debug("SignUpScreen: wrong e-mail format.")
			return 
		
		check_password = AccountVerification.AccountVerification().password_verification(password)

		if not check_password:
			pop.PopupWindow.pop_up(parameters.get_invalid_password_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.debug("SignUpScreen: wrong password format.")
			return

		if password!=repeat_password:
			pop.PopupWindow.pop_up(parameters.get_match_password_error_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings());
			logger.debug("SignUpScreen: passwords do not match.")
			return

		res =AccountVerification.AccountVerification().check_email_exists(e_mail)

		if res:
			pop.PopupWindow.pop_up(parameters.get_email_exists_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.error("SignUpScreen: e-mail {} already exists.".format(e_mail))
			return
		elif not res:
			pass
		else:
			logger.critical(res)
			pop.PopupWindow.pop_up(res,parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			return
			


		res_create_user = AccountVerification.AccountVerification().create_user(e_mail,password)
		if isinstance(res_create_user, (int)):
			self.parent.SIGNED_USER_ID = res_create_user
			self.email_signup.text = ""
			self.password_signup.text = ""
			self.repeat_password_signup.text = ""
			self.create_directory(res_create_user)
			self.parent.current = "homeboard"
			logger.info("SignUpScreen: User: {} is created.".format(e_mail))
		else:
			pop.PopupWindow.pop_up(res_create_user,parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.critical(res_create_user)
			return

	def create_directory(self,user_id):
		user_directory = parameters.get_user_path() + str(user_id)
		os.mkdir(user_directory)

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)