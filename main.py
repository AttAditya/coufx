NAME = "Coufx"
VERSION = "0.0.1"

from typing import Self
from database import DataBase
from logs import Logger

from training import Trainer
from intelligence import AI

template = [
	{
		"name": "diseases",
		"template": []
	},
	{
		"name": "symptons",
		"template": []
	}
]
db = DataBase(template=template)
logger = Logger()

trainer = Trainer(database=db, logger=logger)
ai = AI(database=db, logger=logger)

class App:
	STOP_CODE = "STOP"
	RUN_CODE = "RUN"
	
	status = STOP_CODE

	name = NAME
	version = VERSION
	
	database: DataBase = None
	logger: Logger = None
	intelligence: AI = None
	trainer: Trainer = None

	def __init__(self: Self, logger, database, intelligence, trainer) -> None:
		"""Initiate app"""

		if not logger: raise ValueError("Logger can not be a None object.")
		if not database: raise ValueError("DataBase can not be a None object.")
		if not intelligence: raise ValueError("Intelligence can not be a None object.")
		if not trainer: raise ValueError("Trainer can not be a None object.")

		self.status = self.RUN_CODE
		self.logger: Logger = logger
		self.database: DataBase = database
		self.intelligence: AI = intelligence
		self.trainer: Trainer = trainer

		return None

	def check_looping(self: Self) -> bool:
		"""Check if program should continue"""

		if self.status != self.STOP_CODE: return True
		return False
	
	def exit_loop(self: Self, *, reason: str="SIMPLE") -> None:
		"""Exit program loop"""

		print(f"\nExited {self.name} ({reason})")
		self.status = self.STOP_CODE

		return None
	
	def init_sequence(self: Self) -> None:
		"""Run once before program enters loop"""

		print(f"Running {self.name}[{self.version}]")
		print("TIP: Use \"commands\" command to list all the commands.")
		print("TIP: Use \"exit\" command to exit.")

		return None

	def main_loop(self: Self) -> None:
		"""Main program loop"""

		action = input(f"{self.name}>>> ")

		if action == "commands":
			print("=== commands ===")
			print("commands: Show all commands")
			print("exit: Exit program")
			print("input: Add inputs to AI")
			print("predict: Predict and generate output")
			print("train: Train AI")
		elif action == "exit":
			self.exit_loop()
		elif action == "input":
			sympton = input("Sympton: ")
			self.intelligence.add_input(sympton.lower(), input_type="symptons")
		elif action == "predict":
			print("Predicting...")
			self.intelligence.predict(input_type="symptons")
			prediction_output = self.intelligence.output
			prediction_keys = list(prediction_output.keys())
			prediction_values = list(prediction_output.values())
			prediction = [f"{prediction_keys[i]}(SCORE:{prediction_values[i]:.2f})" for i in range(len(prediction_keys))]
			prediction_output_updated = {prediction[i]:prediction_values[i] for i in range(len(prediction_keys))}
			prediction.sort(key=lambda p: prediction_output_updated[p], reverse=True)
			print("\n".join(prediction))
		elif action == "train":
			training = True
			print("stop: stop training.")
			print("new: new sympton")
			print("add: add disease to sympton")
			while training:
				training_act = input("Training>>> ").lower()

				if training_act == "stop":
					training = False
				elif training_act == "new":
					sympton = input("Sympton: ")
					self.trainer.create_sympton(sympton)
				elif training_act == "add":
					sympton = input("Sympton: ")
					disease = input("Disease: ")
					probability = float(input("Probability: (0.00 to 100.00): "))
					self.trainer.add_to_sympton((disease, probability), sympton)
				else:
					print("Unknown action")
		else:
			print("Unknown action")

		return None
	
	def keyboard_interrupt(self: Self) -> None:
		"""Run if program closed by keyboard interrupt(CTRL + C)"""

		self.exit_loop(reason="KEYBOARD INTERRUPT")

		return None
	
	def handle_error(self: Self, exception: Exception|None=None) -> None:
		"""Handle unexpected errors"""

		if not exception: return None

		self.logger.log(f"{exception}", file="errors")
		print("Skipping Current Action (SYSTEM ERROR)")

		return None

if __name__ == "__main__":
	app = App(database=db, logger=logger, intelligence=ai, trainer=trainer)
	app.init_sequence()
	while app.check_looping():
		try:
			app.main_loop()
		except KeyboardInterrupt:
			app.keyboard_interrupt()
		"""except Exception as exception:
			app.handle_error(exception)"""

