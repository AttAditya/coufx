from typing import Self
from database import DataBase
from logs import Logger

class AI:
	logger = None
	database = None

	inputs = {}
	output = {}

	SYMPTONS_PATH = "symptons"
	DISEASES_PATH = "diseases"

	def __init__(self: Self, *, database: DataBase|None=None, logger: Logger|None=None) -> None:
		"""Initiate AI"""

		if not logger: raise ValueError("Logger can not be a None object.")
		if not database: raise ValueError("DataBase can not be a None object.")

		self.logger = logger
		self.database = database

		self.reset()

		return None
	
	def log(self: Self, message: str|None=None) -> bool:
		"""Logs a message"""

		if not message: return False
		self.logger.log(message, file="AI")
		
		return True
	
	def reset(self: Self) -> None:
		"""Resets AI inputs and outputs"""

		self.output = []
		self.logger.clear("AI")

		self.log("AI reset")

		return None

	def add_input(self: Self, data: str|None=None, *, input_type: str|None=None) -> None:
		"""Add an input to AI"""

		if not input_type: raise ValueError("Input Type can not be a None object.")
		if not data: raise ValueError("Input Data can not be a None object.")

		type_list = self.database.get_list(input_type)
		if data not in type_list: return None

		if input_type not in self.inputs: self.inputs[input_type] = [data]; return None
		if data not in self.inputs[input_type]:
			self.inputs[input_type].append(data);
			self.log("Added new input")
		
		return None
	
	def predict(self: Self, *, input_type: str|None=None) -> None:
		"""Predict outputs from inputs"""

		self.log("Generating output...")
		temp_output_diseases = []

		for data in self.inputs[input_type]:
			diseases = self.database.get(f"symptons/{data}", format=DataBase.SPLIT_FORMAT)
			temp_output_diseases.extend(diseases)
		
		temp_scored_output = []

		for data in temp_output_diseases:
			for id, item in enumerate(temp_scored_output):
				if item["name"] == data[0]:
					temp_scored_output[id]["score"] += 1
					break
			else:
				scored_data = {
					"name": data[0],
					"probability": data[1],
					"score": 1
				}
				temp_scored_output.append(scored_data)
		
		scored_evaluation = {}

		for data in temp_scored_output:
			scored_data = {
				data["name"]: data["score"] * float(data["probability"]) * 0.01
			}
			scored_evaluation.update(scored_data)
		
		self.output = scored_evaluation
		self.log("Generated output")

		return None

