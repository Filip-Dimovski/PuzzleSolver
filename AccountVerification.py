import mysql.connector
import re
import cryptography
from cryptography.fernet import Fernet
import config_file_read as parameters

class AccountVerification():

	db_host = parameters.get_db_host()
	db_user = parameters.get_db_user()
	db_passw = parameters.get_db_password()
	db_name = parameters.get_db_database()

	encode_key = parameters.get_encode_key()

			

	def email_verification(self,e_mail):
		res = ""
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', e_mail)

		if match == None:
			return False
		else:
			return True

	def password_verification(self,password):
		res = ""
		match = re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$', password)

		if match == None:
			return False
		else:
			return True

	def check_email_exists(self,e_mail):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT * FROM user WHERE user_name = %s """,(e_mail,))
			myresult = mycursor.fetchall()
			if not myresult:
				message = False
			else:
				message = True
			mydb.commit()
			mycursor.close()
			mydb.close()

			return message

		except mysql.connector.Error as err:
  			return err

	def check_account(self,e_mail,password):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			encrypted_pass = self.encrypt_password(password,self.encode_key)
			mycursor.execute("SELECT id,password FROM user WHERE user_name = %s",(e_mail,))
			myresult = mycursor.fetchall()

			if not myresult:
				return parameters.get_email_notfound_popup_warnings()

			check_pass = self.decrypt_password((myresult[0])[1],self.encode_key) == password
			user_id = (myresult[0])[0]
			mydb.commit()
			mycursor.close()
			mydb.close()

			if check_pass == True:
				return user_id
			else:
				return False
			
		except mysql.connector.Error as err:
			return err
		
	def get_user_name(self,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT user_name FROM user WHERE id = %s """, (user_id,))
			myresult = mycursor.fetchall()
			if not myresult:
				return False

			result =  (myresult[0])[0]
			mydb.commit()
			mycursor.close()
			mydb.close()

			return result

		except mysql.connector.Error as err:
			return err

	def create_user(self,e_mail,password):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			encoded_password = self.encrypt_password(password,self.encode_key)
			mycursor.execute("""insert into user(user_name,password,created_date) values(%s, %s, now() ) """, (e_mail,encoded_password))
			user_id = mycursor.lastrowid
			mydb.commit()
			mycursor.close()
			mydb.close()
			return user_id
		except mysql.connector.Error as err:
			return err


	def delete_user(self,user_id):
		self.delete_user_puzzle_rel(user_id)
		self.delete_user_info(user_id)

	def delete_user_puzzle_rel(self,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""delete from user_puzzle where user_id=%s """, (str(user_id),))
			mydb.commit()
			mycursor.close()
			mydb.close()
		except mysql.connector.Error as err:
			return err

	def delete_user_info(self,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""delete from user where id=%s """, (str(user_id),))
			mydb.commit()
			mycursor.close()
			mydb.close()
		except mysql.connector.Error as err:
			return err

	def count_user_puzzle(self,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""select count(*) from user_puzzle where user_id=%s """, (str(user_id),))
			myresult = mycursor.fetchall()
			mydb.commit()
			mycursor.close()
			mydb.close()
			return (myresult[0])[0]
		except mysql.connector.Error as err:
			return err

	def check_password(self,user_id,password):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("SELECT password FROM user WHERE id = %s",(user_id,))
			myresult = mycursor.fetchall()

			check_pass = self.decrypt_password((myresult[0])[0],self.encode_key) == password
			mydb.commit()
			mycursor.close()
			mydb.close()


			return check_pass
			
		except mysql.connector.Error as err:
			return err

	def change_password(self,user_id,new_password):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			encoded_password = self.encrypt_password(new_password,self.encode_key)
			mycursor.execute("""update user set password = %s, modified_date= now() where id = %s""", (encoded_password,user_id))
			mydb.commit()
			mycursor.close()
			mydb.close()
			return True
		except mysql.connector.Error as err:
			return err



	def encrypt_password(self,password,key):
		cipher_suite = Fernet(bytes(key,'utf-8'))
		ciphered_text = cipher_suite.encrypt(bytes(password, 'utf-8'))
		return ciphered_text.decode("utf-8") 

	def decrypt_password(self,encrypted_pass,key):
		cipher_suite = Fernet(bytes(key,'utf-8'))
		unciphered_text = (cipher_suite.decrypt(bytes(encrypted_pass,'utf-8')))
		return unciphered_text.decode("utf-8") 



