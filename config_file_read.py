from configparser import ConfigParser

parser = ConfigParser()
parser.read('config/config.ini')
language = ConfigParser()
language_source =""

#language sources configuration
def get_english_language_source():
	return parser.get('settings','english_config_file')

def get_macedonian_language_source():
	return parser.get('settings','macedonian_config_file')

def set_language(choose_language):
	if choose_language == 'en':
		language_source = get_english_language_source()
	if choose_language =='mk':
		language_source = get_macedonian_language_source()
	language.read(language_source, encoding='utf-8')


#path
def get_user_path():
	return parser.get('settings','users_path')

def get_temp_image_path():
	return parser.get('settings','temp_image_path')

def get_logging_path():
	return parser.get('settings','log_path')

def get_logging_level():
	return parser.get('settings','log_level')

def get_logging_formatter():
	return parser.get('settings','log_formatter')

def get_popup_background():
	return parser.get('settings','popup_background')

def get_x_image_path():
	return parser.get('settings','X_image_path')

def get_tick_image_path():
	return parser.get('settings','tick_image_path')

#encode key for user password
def get_encode_key():
	return  parser.get('settings','encode_key')

#db connection properties
def get_db_host():
	return  parser.get('db_connection','host')

def get_db_user():
	return  parser.get('db_connection','user')

def get_db_password():
	return  parser.get('db_connection','password')

def get_db_database():
	return  parser.get('db_connection','database')



#label names
def get_title_main():
	return  language.get('label_main','title_main')

def get_btn_signin_main():
	return language.get('label_main','btn_signin_main')

def get_btn_signup_main():
	return language.get('label_main','btn_signup_main')

def get_btn_nouser_main():
	return language.get('label_main','btn_nouser_main')


def get_title_signin():
	return language.get('label_signin','title_signin')

def get_label_email_signin():
	return language.get('label_signin','label_email_signin')

def get_label_password_signin():
	return language.get('label_signin','label_password_signin')

def get_btn_signin_signin():
	return language.get('label_signin','btn_signin_signin')

def get_btn_clear_signin():
	return language.get('label_signin','btn_clear_signin')

def get_btn_goback_signin():
	return language.get('label_signin','btn_goback_signin')



def get_title_signup():
	return language.get('label_signup','title_signup')


def get_label_email_signup():
	return language.get('label_signup','label_email_signup')

def get_label_password_signup():
	return language.get('label_signup','label_password_signup')

def get_label_repeatpassword_signup():
	return language.get('label_signup','label_repeatpassword_signup')

def get_btn_signup_signup():
	return language.get('label_signup','btn_signup_signup')

def get_btn_clear_signup():
	return language.get('label_signup','btn_clear_signup')


def get_btn_goback_signup():
	return language.get('label_signup','btn_goback_signup')



def get_title_homeboard():
	return language.get('label_homeboard','title_homeboard')

def get_btn_mypuzzles_homeboard():
	return language.get('label_homeboard','btn_mypuzzles_homeboard')

def get_btn_newpuzzle_homeboard():
	return language.get('label_homeboard','btn_newpuzzle_homeboard')

def get_btn_signout_homeboard():
	return language.get('label_homeboard','btn_signout_homeboard')

def get_btn_goback_homeboard():
	return language.get('label_homeboard','btn_goback_homeboard')

def get_btn_manageuser_homeboard():
	return language.get('label_homeboard','btn_manageuser_homeboard')


def get_title_manageuser():
	return language.get('label_manageuser','title_manageuser')

def get_btn_goback_manageuser():
	return language.get('label_manageuser','btn_goback_manageuser')

def get_btn_changepassword_manageuser():
	return language.get('label_manageuser','btn_changepassword_manageuser')

def get_btn_deleteuser_manageuser():
	return language.get('label_manageuser','btn_deleteuser_manageuser')


def get_title_changepassword():
	return language.get('label_changepassword','title_changepassword')


def get_label_currentpassword_changepassword():
	return language.get('label_changepassword','label_currentpassword_changepassword')

def get_label_newpassword_changepassword():
	return language.get('label_changepassword','label_newpassword_changepassword')

def get_label_repeatpassword_changepassword():
	return language.get('label_changepassword','label_repeatpassword_changepassword')

def get_btn_changepassword_changepassword():
	return language.get('label_changepassword','btn_changepassword_changepassword')

def get_btn_clear_changepassword():
	return language.get('label_changepassword','btn_clear_changepassword')

def get_btn_goback_changepassword():
	return language.get('label_changepassword','btn_goback_changepassword')





def get_title_mypuzzles():
	return language.get('label_mypuzzles','title_mypuzzles')

def get_btn_goback_mypuzzles():
	return language.get('label_mypuzzles','btn_goback_mypuzzles')

	



def get_title_newpuzzle():
	return language.get('label_newpuzzle','title_newpuzzle')

def get_label_puzzlename_newpuzzle():
	return language.get('label_newpuzzle','label_puzzlename_newpuzzle')

def get_label_fullpicture_newpuzzle():
	return language.get('label_newpuzzle','label_fullpicture_newpuzzle')

def get_label_fullpicturecamera_newpuzzle():
	return language.get('label_newpuzzle','label_fullpicturecamera_newpuzzle')

def get_label_fullpicturedirectory_newpuzzle():
	return language.get('label_newpuzzle','label_fullpicturedirectory_newpuzzle')

def get_label_piecespuzzle_newpuzzle():
	return language.get('label_newpuzzle','label_piecespuzzle_newpuzzle')

def get_label_piecespicturecamera_newpuzzle():
	return language.get('label_newpuzzle','label_piecespicturecamera_newpuzzle')

def get_label_piecespicturedirectory_newpuzzle():
	return language.get('label_newpuzzle','label_piecespicturedirectory_newpuzzle')

def get_btn_solvepuzzle_newpuzzle():
	return language.get('label_newpuzzle','btn_solvepuzzle_newpuzzle')
def get_btn_goback_newpuzzle():
	return language.get('label_newpuzzle','btn_goback_newpuzzle')


def get_label_goback_camera():
	return language.get('label_camera','label_goback_camera')

def get_btn_capture_camera():
	return language.get('label_camera','btn_capture_camera')

def get_btn_upload_choosefile():
	return language.get('label_choosefile','btn_upload_choosefile')

def get_btn_goback_choosefile():
	return language.get('label_choosefile','btn_goback_choosefile')


def get_title_pictureview():
	return language.get('label_pictureview','title_pictureview')

def get_btn_fullpuzzle_pictureview():
	return language.get('label_pictureview','btn_fullpuzzle_pictureview')

def get_btn_piecespuzzle_pictureview():
	return language.get('label_pictureview','btn_piecespuzzle_pictureview')

def get_btn_deletepuzzle_pictureview():
	return language.get('label_pictureview','btn_deletepuzzle_pictureview')

def get_btn_solution_pictureview():
	return language.get('label_pictureview','btn_solution_pictureview')

def get_btn_goback_pictureview():
	return language.get('label_pictureview','btn_goback_pictureview')

def get_btn_goback_picture():
	return language.get('label_picture','btn_goback_picture')

def get_title_full_picture():
	return language.get('label_picture','title_full_picture')

def get_title_pieces_picture():
	return language.get('label_picture','title_pieces_picture')

def get_title_solution_picture():
	return language.get('label_picture','title_solution_picture')
	

#popup warnings
def get_title_popup_warnings():
	return language.get('popup_warnings','title')


def get_invalid_email_popup_warnings():
	return language.get('popup_warnings','invalid_email')

def get_invalid_password_popup_warnings():
	return language.get('popup_warnings','invalid_password')


def get_connection_error_popup_warnings():
	return language.get('popup_warnings','connection_error')



def get_match_password_error_popup_warnings():
	return language.get('popup_warnings','match_password_error')

def get_email_notfound_popup_warnings():
	return language.get('popup_warnings','email_notfound')

def get_email_exists_popup_warnings():
	return language.get('popup_warnings','email_exists')

def get_nomatch_popup_warnings():
	return language.get('popup_warnings','no_match')

def get_popup_button_popup_warnings():
	return language.get('popup_warnings','popup_button')

def get_invalid_currentpassword_popup_warnings():
	return language.get('popup_warnings','invalid_currentpassword_popup_warnings')

def get_passwordchanged_popup_warning():
	return language.get('popup_warnings','passwordchanged_popup_warning')

def get_passwordchanged_title_popup_warning():
	return language.get('popup_warnings','passwordchanged_title_popup_warning')

def get_noname_puzzle_popup_warnings():
	return language.get('popup_warnings','noname_puzzle')
def get_name_exists_puzzle_popup_warnings():
	return language.get('popup_warnings','name_exists_puzzle')
def get_no_full_puzzle_popup_warnings():
	return language.get('popup_warnings','no_full_puzzle')
def get_no_pieces_puzzle_popup_warnings():
	return language.get('popup_warnings','no_pieces_puzzle')

def get_progress_bar_title():
	return language.get('popup_warnings','progress_bar_title')





def get_deleteuser_title():
	return language.get('popup_warnings','deleteuser_title')

def get_deleteuser_label():
	return language.get('popup_warnings','deleteuser_label')

def get_deleteuser_yesbutton():
	return language.get('popup_warnings','deleteuser_yesbutton')

def get_deleteuser_nobutton():
	return language.get('popup_warnings','deleteuser_nobutton')


def get_deletepuzzle_title():
	return language.get('popup_warnings','deletepuzzle_title')

def get_deletepuzzle_label():
	return language.get('popup_warnings','deletepuzzle_label')

def get_deletepuzzle_yesbutton():
	return language.get('popup_warnings','deletepuzzle_yesbutton')

def get_deletepuzzle_nobutton():
	return language.get('popup_warnings','deletepuzzle_nobutton')


def get_notsupportedchosenfiletype_choosefile():
	return language.get('popup_warnings','notsupportedchosenfiletype_choosefile')




