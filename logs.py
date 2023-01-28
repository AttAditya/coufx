from typing import Self
import os
import datetime

LOG_FOLDER_PATH = "logs"

class Logger:
	def __init__(self: Self) -> None:
		"""Initiate logger"""

		if not self.check_logs_folder(): self.create_log_folder()
		return None

	@staticmethod
	def check_logs_folder() -> bool:
		"""Checks for logs folder"""

		if os.path.isdir(LOG_FOLDER_PATH): return True
		return False
	
	@staticmethod
	def check_log_file(name: str|None=None) -> bool:
		"""Checks for log file"""

		if not name: return False
		
		path = LOG_FOLDER_PATH + "/" + name + ".log"
		if os.path.isfile(path): return True

		return False
	
	@staticmethod
	def create_log_file(name: str|None=None) -> bool:
		"""Creates a log file"""

		if not name: return False
		path = LOG_FOLDER_PATH + "/" + name + ".log"

		with open(path, "x") as file: file.close()

		return True
	
	@staticmethod
	def create_log_folder() -> None:
		"""Creates the log folder"""
		
		os.mkdir(LOG_FOLDER_PATH)
		return None
	
	def log(self: Self, data: str="", *, file: str|None=None) -> bool:
		"""Log data into desired log file"""

		if not data: return False
		if not file: return False
		if not self.check_log_file(file): self.create_log_file(file)

		path = LOG_FOLDER_PATH + "/" + file + ".log"
		with open(path, "a") as file:
			timestamp = f"[{datetime.datetime.now(): %d/%m/%Y - %I:%M:%S %p }]"
			file.write(f"{timestamp}: {data}\n")
			file.close()
		
		return True
	
	@staticmethod
	def clear(name: str|None=None) -> bool:
		"""Clear log file"""

		if not name: return False
		
		path = LOG_FOLDER_PATH + "/" + name + ".log"
		with open(path, "w") as file: file.write(""); file.close()

		return True

