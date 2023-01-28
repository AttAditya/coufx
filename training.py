from typing import Self
from database import DataBase
from logs import Logger

class Trainer:
	logger = None
	database = None

	inputs = {}
	output = {}

	def __init__(self: Self, *, database: DataBase|None=None, logger: Logger|None=None) -> None:
		"""Initiate AI"""

		if not logger: raise ValueError("Logger can not be a None object.")
		if not database: raise ValueError("DataBase can not be a None object.")

		self.logger = logger
		self.database = database

		return None
	
	def log(self: Self, message: str|None=None) -> bool:
		"""Logs a message"""

		if not message: return False
		self.logger.log(message, file="Training")
		
		return True
	
	def create_sympton(self: Self, sympton: str|None=None) -> None:
		"""Create a new sympton"""

		self.database.create_data_file(sympton.lower(), base_folder="symptons")
		return None
	
	def add_to_sympton(self: Self, data: tuple[(str, float), ...]=None, sympton: str=None) -> None:
		"""Adds disease to sympton"""

		self.database.add_data(data, file=f"symptons/{sympton}", format=DataBase.SPLIT_FORMAT)
		return None

