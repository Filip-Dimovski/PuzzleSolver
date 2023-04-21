import logging
logger = logging.getLogger(__name__)
import mysql.connector
import config_file_read as parameters
import time

class PuzzleConnection():

	db_host = parameters.get_db_host()
	db_user = parameters.get_db_user()
	db_passw = parameters.get_db_password()
	db_name = parameters.get_db_database()

	def __init__(self):
		self.update_logger()


	def create_puzzle(self,puzzle_name,folder_name,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			full_puzzle_path = folder_name+"/FullPuzzle.png"
			pieces_puzzle_path = folder_name + "/PiecesPuzzle.png"
			mycursor.execute("""INSERT INTO puzzle(name,	full_image_path,	parts_image_path,	created_date,	created_by,	modified_date,	modified_by) VALUES(%s,%s,%s,now(),%s,null,null)""",(puzzle_name,full_puzzle_path,pieces_puzzle_path,str(user_id)))
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.info("PuzzleConnection: puzzle: {} for user id: {} is created".format(puzzle_name,user_id))
		except mysql.connector.Error as err:
			logger.exception("create_puzzle")
			return err

	def create_puzzle_user_rel(self,puzzle_name,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			puzzle_id = self.get_puzzle_id(puzzle_name,user_id)
			mycursor.execute("""INSERT INTO user_puzzle(user_id,	puzzle_id) VALUES(%s,%s)""",(str(user_id),	str(puzzle_id)))
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.info("PuzzleConnection: puzzle: {} - user id: {} relation is created".format(puzzle_name,user_id))
		except mysql.connector.Error as err:
			logger.exception("create_puzzle_user_rel")
			return err

	def get_puzzle_id(self,puzzle_name,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)
			mycursor = mydb.cursor()
			folder_name = parameters.get_user_path()+str(user_id)+"/"+puzzle_name
			mycursor.execute("""SELECT Id FROM puzzle WHERE Name=%s AND full_image_path LIKE %s""",(puzzle_name,folder_name+"%"))
			myresult = mycursor.fetchall()
			result = ""
			if not myresult:
				result =  "Puzzle "+ puzzle_name+ " not found for user id: "+str(user_id)
			else:
				result =  (myresult[0])[0]
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: get_puzzle_id: puzzle_name: {}, user_id: {}, result ={}".format(puzzle_name,user_id,result))
			return result
		except mysql.connector.Error as err:
			logger.exception("get_puzzle_id")
			return err
  			
	def check_user_puzzle_rel(self,puzzle_name,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT null FROM user_puzzle up INNER JOIN puzzle p ON p.Id = up.puzzle_id WHERE up.user_id=%s AND p.Name = %s""",(str(user_id),puzzle_name))
			myresult = mycursor.fetchall()
			result = True
			if not myresult:
				result= False
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: check_user_puzzle_rel:{}".format(result))
			return result
		except mysql.connector.Error as err:
			logger.exception("check_user_puzzle_rel")
			return err
  		

	def fetch_all_puzzles(self,user_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT p.name FROM user_puzzle up INNER JOIN puzzle p ON p.Id = up.puzzle_id WHERE up.user_id=%s""",(str(user_id),))
			myresult = mycursor.fetchall()
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: fetch_all_puzzles called")
			return [x[0] for x in myresult]
		except mysql.connector.Error as err:
			logger.exception("fetch_all_puzzles")
			return err

	def get_puzzle_full_path(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT full_image_path FROM puzzle WHERE id=%s""",(str(puzzle_id),))
			myresult = mycursor.fetchall()
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: get_puzzle_full_path called for Puzzle id:{}. Full Path:{}".format(puzzle_id,(myresult[0])[0]))
			return (myresult[0])[0]
		except mysql.connector.Error as err:
			logger.exception("get_puzzle_full_path")
			return err

	def get_puzzle_folder_path(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)	
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT full_image_path FROM puzzle WHERE id=%s""",(str(puzzle_id),))
			myresult = mycursor.fetchall()
			result = (myresult[0])[0]
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: get_puzzle_folder_path called for Puzzle id:{}. Full Path:{}".format(puzzle_id,(myresult[0])[0]))
			return result[:result.rfind('/')]
		except mysql.connector.Error as err:
			logger.exception("get_puzzle_folder_path")
			return err
  	
	def get_puzzle_pieces_path(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT parts_image_path FROM puzzle WHERE id=%s""",(str(puzzle_id),))
			myresult = mycursor.fetchall()
			
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: get_puzzle_pieces_path called for Puzzle id:{}. Pieces Path:{}".format(puzzle_id,(myresult[0])[0]))
			return (myresult[0])[0]
		except mysql.connector.Error as err:
			logger.exception("get_puzzle_pieces_path")
			return err

	def get_puzzle_solution_path(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)
			mycursor = mydb.cursor()
			mycursor.execute("""SELECT solution_image_path FROM puzzle WHERE id=%s""",(str(puzzle_id),))
			myresult = mycursor.fetchall()
			
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: get_puzzle_solution_path called for Puzzle id:{}. Solution Path:{}".format(puzzle_id,(myresult[0])[0]))
			return (myresult[0])[0]
		except mysql.connector.Error as err:
			logger.exception("get_puzzle_solution_path")
			return err

	def update_puzzle_solution(self,puzzle_id,solution_path):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)
			mycursor = mydb.cursor()
			mycursor.execute("""UPDATE puzzle set solution_image_path=%s WHERE id=%s""",(solution_path,str(puzzle_id),))			
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.debug("PuzzleConnection: update_puzzle_solution called for Puzzle id:{}. Solution Path:{}".format(puzzle_id,solution_path))
		except mysql.connector.Error as err:
			logger.exception("update_puzzle_solution")
			return err

	def delete_puzzle(self,puzzle_id):
		self.delete_user_puzzle_rel(puzzle_id)
		self.delete_puzzle_info(puzzle_id)


	def delete_user_puzzle_rel(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""delete from user_puzzle where puzzle_id=%s """, (str(puzzle_id),))
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.info("PuzzleConnection delete_user_puzzle_rel called for puzzle_id: {}.".format(puzzle_id))
		except mysql.connector.Error as err:
			logger.exception("delete_user_puzzle_rel")
			return err

	def delete_puzzle_info(self,puzzle_id):
		try:
			mydb = mysql.connector.connect(host=self.db_host,user=self.db_user,passwd=self.db_passw,database=self.db_name)		
			mycursor = mydb.cursor()
			mycursor.execute("""delete from puzzle where id=%s """, (str(puzzle_id),))
			mydb.commit()
			mycursor.close()
			mydb.close()
			logger.info("PuzzleConnection delete_puzzle_info called for puzzle_id: {}.".format(puzzle_id))
		except mysql.connector.Error as err:
			logger.exception("delete_puzzle_info")
			return err
  			
	def update_logger(self):

		log_level_dict = {
		"DEBUG": logging.DEBUG,
		"INFO": logging.INFO,
		"WARNING": logging.WARNING,
		"ERROR": logging.ERROR,
		"CRITICAL": logging.CRITICAL
		}

		
		timestr = time.strftime("%Y%m%d")
		logger = logging.getLogger(__name__)
		if logger.handlers:
			return
		log_level = log_level_dict[parameters.get_logging_level().upper()]
		logger.setLevel(log_level)
		formatter = logging.Formatter(parameters.get_logging_formatter())
		LOG_PATH = parameters.get_logging_path()+'{}.log'.format(timestr)
		file_handler = logging.FileHandler(LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)


		