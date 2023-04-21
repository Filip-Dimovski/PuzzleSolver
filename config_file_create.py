from configparser import ConfigParser

config = ConfigParser()

config['settings'] = {
	
	'log_path': 'files/logs/log_',
	'log_level': 'DEBUG',
	'log_formatter': '[%%(asctime)s] [%%(levelname)s] : %%(message)s ',
	'image_path': 'files/image/',
	'temp_image_path': 'temp_puzzle/',
	'users_path': 'users/',
	'english_config_file': 'config/eng_labels.ini',
	'macedonian_config_file': 'config/mkd_labels.ini',
	'encode_key': 'RrnSuNakR2Ho9EkAv7oleBX4MLUeT0a2dSwP-C1D_Ak=',
	'popup_background': 'files/images/popupbackground.jpg',
	'X_image_path': 'files/images/X.png',
	'tick_image_path': 'files/images/tick.png'

}

config['db_connection']={
	'host': 'localhost',
	'user': 'root',
	'password': 'Password',
	'database': 'PuzzleSolver'
	
}

with open('./config/config.ini','w') as file:
	config.write(file)


eng_labels = ConfigParser()


eng_labels['label_main'] = {
	
	'title_main': 'Welcome to PuzzleSolver!',
	'btn_signin_main': 'Sign In',
	'btn_signup_main': 'Sign Up',
	'btn_nouser_main': 'No User'
}

eng_labels['label_signin'] = {
	
	'title_signin': 'Sign In',
	'label_email_signin': 'E-mail:',
	'label_password_signin': 'Password:',
	'btn_signin_signin': 'Sign in',
	'btn_clear_signin': 'Clear',
	'btn_goback_signin': 'Go Back'

}




eng_labels['label_signup'] = {
	
	'title_signup': 'Sign Up',
	'label_email_signup': 'E-mail:',
	'label_password_signup': 'Password:',
	'label_repeatpassword_signup': 'Repeat password:',
	'btn_signup_signup': 'Sign up',
	'btn_clear_signup': 'Clear',
	'btn_goback_signup': 'Go Back'

}

eng_labels['label_homeboard'] = {
	
	'title_homeboard': 'Hi',
	'btn_mypuzzles_homeboard': 'My Puzzles',
	'btn_newpuzzle_homeboard': 'New Puzzle',
	'btn_signout_homeboard': 'Sign Out',
	'btn_goback_homeboard': 'Back',
	'btn_manageuser_homeboard': 'Manage user'

}

eng_labels['label_manageuser'] = {
	
	'title_manageuser': 'Manage user',
	'btn_goback_manageuser': 'Go Back',
	'btn_changepassword_manageuser': 'Change Password',
	'btn_deleteuser_manageuser': 'Delete User'

}

eng_labels['label_changepassword'] = {
	
	'title_changepassword' : 'Change Password'
    ,'label_currentpassword_changepassword' : 'Current Password:'
    ,'label_newpassword_changepassword' : 'New Password:'
    ,'label_repeatpassword_changepassword' : 'Repeat Password:'
    ,'btn_changepassword_changepassword' : 'Change Password'
    ,'btn_clear_changepassword' : 'Clear'
    ,'btn_goback_changepassword' : 'Go Back'
}
eng_labels['label_mypuzzles'] = {
	
	'title_mypuzzles': 'My puzzle',
	'btn_goback_mypuzzles':'Go Back'
}

eng_labels['label_newpuzzle'] = {
	
	'title_newpuzzle': 'New Puzzle',
	'label_puzzlename_newpuzzle': 'Puzzle Name:',
	'label_fullpicture_newpuzzle': 'Full Puzzle:',
	'label_fullpicturecamera_newpuzzle': 'Camera',
	'label_fullpicturedirectory_newpuzzle': 'Gallery',
	'label_piecespuzzle_newpuzzle': 'Pieces Puzzle:',
	'label_piecespicturecamera_newpuzzle': 'Camera',
	'label_piecespicturedirectory_newpuzzle': 'Gallery',
	'btn_solvepuzzle_newpuzzle': 'Solve Puzzle',
	'btn_goback_newpuzzle': 'Go Back'
}

eng_labels['label_camera'] = {
	
	'label_goback_camera': 'Go Back',
    'btn_capture_camera' : 'Capture'

}

eng_labels['label_choosefile'] = {
	
	'btn_upload_choosefile': 'Upload',
	'btn_goback_choosefile': 'Go Back'

}

eng_labels['label_pictureview'] = {
	
	'title_pictureview': 'Puzzle: ',
	'btn_fullpuzzle_pictureview': 'Full Puzzle',
	'btn_piecespuzzle_pictureview': 'Pieces Puzzle',
	'btn_deletepuzzle_pictureview': 'Delete puzzle',
	'btn_solution_pictureview': 'Solution',
	'btn_goback_pictureview': 'Go Back'
}


eng_labels['label_picture'] = {
	
	'btn_goback_picture': 'Go Back',
	'title_full_picture': 'Full Puzzle',
	'title_pieces_picture': 'Pieces Puzzle',
	'title_solution_picture': 'Puzzle solution'	
}


eng_labels['popup_warnings']={
	'title' : 'Error',
	'invalid_email':'Incorrect e-mail format.',
	'email_notfound': 'E-mail not found',
	'invalid_password':'Incorrect password format.',
	'connection_error': "Connection to database error.",
	'match_password_error': 'Passwords do not match.',
	'email_exists': 'E-mail address already exists.\nPlease try to sign in.',
	'no_match': 'E-mail and password do not match',
	'popup_button': 'Close',
	'invalid_currentpassword_popup_warnings': 'Password is incorrect',
	'passwordchanged_popup_warning' : 'Password is changed',
	'passwordchanged_title_popup_warning': 'Done',
	'noname_puzzle': 'Please insert the name of the puzzle',
	'name_exists_puzzle': 'The puzzle already exists for \nthe user. Please use unique name',
	'no_full_puzzle': 'Please insert the full puzzle picture',
	'no_pieces_puzzle': 'Please insert the pieces puzzle picture',
	'progress_bar_title': 'In Progress',
	'deleteuser_title': 'User: ',
	'deleteuser_label': 'Are you sure you want to delete this user?',
	'deleteuser_yesbutton': 'Yes',
	'deleteuser_nobutton': 'No',
	'deletepuzzle_title': 'Puzzle: ',
	'deletepuzzle_label': 'Are you sure you want to delete this puzzle?',
	'deletepuzzle_yesbutton': 'Yes',
	'deletepuzzle_nobutton': 'No',
	'notsupportedchosenfiletype_choosefile':'Please choose file with\n extension: .png, .jpg or .jpeg.'

}


with open('./config/eng_labels.ini','w') as file:
	eng_labels.write(file)

mkd_labels = ConfigParser()


mkd_labels['label_main'] = {
	
	'title_main': 'Добредојдовте во PuzzleSolver!',
	'btn_signin_main': 'Најава',
	'btn_signup_main': 'Регистрација',
	'btn_nouser_main': 'Без најава'
}

mkd_labels['label_signin'] = {
	
	'title_signin': 'Најава',
	'label_email_signin': 'Е-пошта:',
	'label_password_signin': 'Лозинка:',
	'btn_signin_signin': 'Најава',
	'btn_clear_signin': 'Исчисти',
	'btn_goback_signin': 'Назад'

}




mkd_labels['label_signup'] = {
	
	'title_signup': 'Регистрација',
	'label_email_signup': 'Е-пошта:',
	'label_password_signup': 'Лозинка:',
	'label_repeatpassword_signup': 'Повтори лозинка:',
	'btn_signup_signup': 'Регистрација',
	'btn_clear_signup': 'Исчисти',
	'btn_goback_signup': 'Назад'

}

mkd_labels['label_homeboard'] = {
	
	'title_homeboard': 'Здраво',
	'btn_mypuzzles_homeboard': 'Мои сложувалки',
	'btn_newpuzzle_homeboard': 'Нова сложувалка',
	'btn_signout_homeboard': 'Одјава',
	'btn_goback_homeboard': 'Назад',
	'btn_manageuser_homeboard': 'Подесувања'

}

mkd_labels['label_manageuser'] = {
	
	'title_manageuser': 'Подесувања',
	'btn_goback_manageuser': 'Назад',
	'btn_changepassword_manageuser': 'Промена на лозинка',
	'btn_deleteuser_manageuser': 'Избриши корисник'

}

mkd_labels['label_changepassword'] = {
	
	'title_changepassword' : 'Промени лозинка'
    ,'label_currentpassword_changepassword' : 'Лозинка:'
    ,'label_newpassword_changepassword' : 'Нова лозинка:'
    ,'label_repeatpassword_changepassword' : 'Повтори лозинка:'
    ,'btn_changepassword_changepassword' : 'Промени лозинка'
    ,'btn_clear_changepassword' : 'Исчисти'
    ,'btn_goback_changepassword' : 'Назад'
}

mkd_labels['label_mypuzzles'] = {
	
	'title_mypuzzles': 'Мои сложувалки',
	'btn_goback_mypuzzles': 'Назад'
}

mkd_labels['label_newpuzzle'] = {
	
	'title_newpuzzle': 'Нова сложувалка',
	'label_puzzlename_newpuzzle': 'Име:',
	'label_fullpicture_newpuzzle': 'Целосна\nслика:',
	'label_fullpicturecamera_newpuzzle': 'Камера',
	'label_fullpicturedirectory_newpuzzle': 'Галерија',
	'label_piecespuzzle_newpuzzle': 'Парчиња:',
	'label_piecespicturecamera_newpuzzle': 'Камера',
	'label_piecespicturedirectory_newpuzzle': 'Галерија',
	'btn_solvepuzzle_newpuzzle': 'Реши',
	'btn_goback_newpuzzle': 'Назад'
}

mkd_labels['label_camera'] = {
	
	'label_goback_camera': 'Назад',
    'btn_capture_camera' : 'Сликај'

}

mkd_labels['label_choosefile'] = {
	
	'btn_upload_choosefile': 'Избери',
	'btn_goback_choosefile': 'Назад'

}

mkd_labels['label_pictureview'] = {
	
	'title_pictureview': 'Сложувалка: ',
	'btn_fullpuzzle_pictureview': 'Целосна сложувалка',
	'btn_piecespuzzle_pictureview': 'Парчиња',
	'btn_deletepuzzle_pictureview': 'Избриши сложувалка',
	'btn_solution_pictureview': 'Решение',
	'btn_goback_pictureview': 'Назад'
}


mkd_labels['label_picture'] = {
	
	'btn_goback_picture': 'Назад',
	'title_full_picture': 'Целосна сложувалка',
	'title_pieces_picture': 'Парчиња од сложувалка',
	'title_solution_picture': 'Решение на сложувалка'	
}

mkd_labels['popup_warnings']={
	'title' : 'Грешка',
	'invalid_email':'Неточен формат на е-адресата.',
	'email_notfound': 'Е-адресата не постои',
	'invalid_password':'Неточен формат на лозинката.',
	'connection_error': "Грешка во конекцијата кон база.",
	'match_password_error': 'Лозинките не се совпаѓаат.',
	'email_exists': 'Е-адресата постои. Пробајте \nда се логирате.',
	'no_match': 'Е-поштата и лозинката \nне се совпаѓаат',
	'popup_button': 'Затвори',
	'invalid_currentpassword_popup_warnings': 'Лозинката не е точна.',
	'passwordchanged_popup_warning' : 'Лозинката е променета.',
	'passwordchanged_title_popup_warning': 'Завршено',
	'noname_puzzle': 'Внесете го името \nна сложувалката',
	'name_exists_puzzle': 'Сложувалката веќе \nпостои за корисникот. \nИскористите уникатно име',
	'no_full_puzzle': 'Внесете целосна \nслика од сложувалката',
	'no_pieces_puzzle': 'внесете слика од \nпарчињата од сложувалката',
	'progress_bar_title': 'Почекајте',
	'deleteuser_title': 'Корисник: ',
	'deleteuser_label': 'Дали сте сигурни дека \n сакате да го избришите\n овој корисник?',
	'deleteuser_yesbutton': 'Да',
	'deleteuser_nobutton': 'Не',
	'deletepuzzle_title': 'Сложувалка: ',
	'deletepuzzle_label': 'Дали сте сигурни дека \n сакате да ја избришите\n оваа сложувалка?',
	'deletepuzzle_yesbutton': 'Да',
	'deletepuzzle_nobutton': 'Не',
	'notsupportedchosenfiletype_choosefile':'Ве молиме изберете \nдатотека од\n тип .png, .jpg или .jpeg.'


}

with open('./config/mkd_labels.ini','w', encoding="utf-8") as file:
	mkd_labels.write(file)



