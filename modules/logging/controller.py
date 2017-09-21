from pymongo.errors import PyMongoError

class Logs():

	db = None

	@staticmethod
	def insert(content):
		try: 
			Logs.db.insert_one(content)
			return True

		except PyMongoError as e:

			return False