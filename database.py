from typing import Self
import os

DATA_FOLDER_PATH = "data"

class DataBase:
	template = []

	DIRECT_FORMAT = None
	SPLIT_FORMAT = "tupled"

	def __init__(self: Self, /, template: list=[]) -> None:
		"""Initiate database"""

		if template: self.template = template

		if not self.check_data_folder(): self.create_data_folder("data", template=self.template)

		return None

	@staticmethod
	def check_data_folder() -> bool:
		"""Checks for data folder"""

		if os.path.isdir(DATA_FOLDER_PATH): return True
		return False
	
	@staticmethod
	def check_data_file(name: str=None) -> bool:
		"""Checks for data file"""

		if not name: return False
		path = DATA_FOLDER_PATH + "/" + name
		if os.path.isfile(path): return True

		return False
	
	@staticmethod
	def create_data_file(name: str=None, /, folder: bool=False, base_folder: str="") -> bool:
		"""Creates a data file/folder"""

		if not name: return False
		base = "/" + base_folder if base_folder else ""

		path = DATA_FOLDER_PATH + base + "/" + name

		if path.startswith("/"): path = path[1:]
		if folder: os.mkdir(path); return True

		with open(path, "x") as file: file.close()

		return True
	
	def create_data_folder(self: Self, name:str=None, /, template: list=[], base_folder="") -> bool:
		"""Creates a sub folder"""
		
		if not name: return False
		base = "/" + base_folder if base_folder else ""

		path = DATA_FOLDER_PATH + base + "/" + name

		if path.startswith("/"): path = path[1:]
		self.create_data_file(name, folder=True, base_folder=base_folder)

		for item in template:
			if type(item) == str: self.create_data_file(item, base_folder=path); continue
			if type(item) == dict:
				self.create_data_folder(item["name"], template=item["template"], base_folder=path)
		
		return True
	
	@staticmethod
	def get_list(folder: str=None) -> list:
		"""Get list of items in a data sub folder"""

		if not folder: return []

		path = DATA_FOLDER_PATH + "/" + folder
		if not os.path.isdir(path): return []
		output = os.listdir(path)
		
		return output
	
	def get(self: Self, file: str=None, *, format: str|None=None) -> list:
		"""Get data from a data file"""

		if not file: return []

		path = DATA_FOLDER_PATH + "/" + file
		if not os.path.isfile(path): return []
		
		raw_data = ""
		with open(path, "r") as data_file:
			raw_data = data_file.read()
			data_file.close()
		
		if not raw_data: return []
		data = [item for item in raw_data.split(",") if item]

		if format == self.SPLIT_FORMAT:
			data = [tuple(item.split(":")) for item in data]

		return data
	
	def add_data(self: Self, data: any=None, /, file: str=None, format: str=None) -> bool:
		"""Puts data to data file"""

		if not file: return False
		if not data: return False

		path = DATA_FOLDER_PATH + "/" + file

		if format == self.SPLIT_FORMAT:
			data_list = self.get(file, format=self.SPLIT_FORMAT)
			indexed_value = data[0]
			data_list_index = [value[0] for value in data_list]

			if indexed_value.lower() in data_list_index: return True

			data_list.append(tuple(data))
			stringed_data_list = [":".join(map(str, value)) for value in data_list]
			with open(path, "w") as data_file:
				data_file.write(",".join(stringed_data_list))
				data_file.close()

			return True

		data_list = self.get(file)
		
		if data.lower() in data_list: return True

		data_list.append(data.lower())
		with open(path, "w") as data_file:
			data_file.write(",".join(data_list))
			data_file.close()

		return True
	
	def remove_data(self: Self, data: str=None, /, file: str=None, format: str=None) -> bool:
		"""Removes data to data file"""

		if not file: return False
		if not data: return False

		if format == self.SPLIT_FORMAT:
			data_list = self.get(file, format=self.SPLIT_FORMAT)
			indexed_value = data[0]
			data_list_index = [value[0] for value in data_list]

			if indexed_value.lower() not in data_list_index: return True

			data_list = [value for value in data_list if value[0] != indexed_value]
			stringed_data_list = [":".join(value) for value in data_list]
			with open(file, "w") as data_file:
				data_file.write(",".join(stringed_data_list))
				data_file.close()

			return True

		data_list = self.get(file)
		if data.lower() not in data_list: return True

		data_list.remove(data.lower())
		with open(file, "w") as data_file:
			data_file.write(",".join(data_list))
			data_file.close()

		return True

