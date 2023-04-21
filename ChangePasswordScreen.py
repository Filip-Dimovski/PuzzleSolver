import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
import config_file_read as parameters
import os, glob,shutil
import PopUpWindow as pop

class ChangePasswordScreen(Screen):
	def update_screen(self):
		self.update_logger()
		self.title_changepassword.text = parameters.get_title_changepassword()
		self.label_currentpassword_changepassword.text = parameters.get_label_currentpassword_changepassword()
		self.label_newpassword_changepassword.text = parameters.get_label_newpassword_changepassword()
		self.label_repeatpassword_changepassword.text = parameters.get_label_repeatpassword_changepassword()
		self.btn_changepassword_changepassword.text = parameters.get_btn_changepassword_changepassword()
		self.btn_clear_changepassword.text = parameters.get_btn_clear_changepassword()
		self.btn_goback_changepassword.text = parameters.get_btn_goback_changepassword()

		logger.debug("ChangePasswordScreen: labels are configured")


	def btn_changepassword_on_pressed(self):
		
		user_id = self.parent.SIGNED_USER_ID
		current_pass = self.currentpassword_changepassword.text
		new_pass = self.newpassword_changepassword.text
		repeat_new_pass = self.repeatpassword_changepassword.text
		
		check_curr_password = AccountVerification.AccountVerification().check_password(user_id,current_pass)

		if check_curr_password == False:
			pop.PopupWindow.pop_up(parameters.get_invalid_currentpassword_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("ChangePasswordScreen: current password is wrong.")
			return

		check_password = AccountVerification.AccountVerification().password_verification(new_pass)
		if not check_password:
			pop.PopupWindow.pop_up(parameters.get_invalid_password_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.debug("ChangePasswordScreen: wrong password format.")
			return

		if new_pass!=repeat_new_pass:
			pop.PopupWindow.pop_up(parameters.get_match_password_error_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.debug("ChangePasswordScreen: passwords do not match.")
			return
			
		res = AccountVerification.AccountVerification().change_password(user_id,new_pass)
		if res:
			logger.info("ChangePasswordScreen: password is changed.")
			pop.PopupWindow.pop_up(parameters.get_passwordchanged_popup_warning(),parameters.get_passwordchanged_title_popup_warning(),parameters.get_popup_button_popup_warnings());
			self.currentpassword_changepassword.text=""
			self.newpassword_changepassword.text=""
			self.repeatpassword_changepassword.text=""
			self.parent.current = "manage_user"
		else:
			logger.critical("ChangePasswordScreen: {}.".format(res))
			pop.PopupWindow.pop_up(res,parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			return


	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

