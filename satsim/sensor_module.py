from module import module
from random import randint
class gamma_sensor(module):
	def __init__(self):
		super().__init__("gamma spectrometer")
		self.fields["name"] = "gammaSensor"
		self.fields["detections"] = 0
		self.fields["detections_str"] = []
		self.fields["threshold"] = 90
		self.fields["flush"] = 0
		self.writable = ["threshold","flush"]
		print("id is:", self.id)

	def mod_get(self, field="none"):
		if field not in self.fields:
			return (-1, "GET FATAL: field '" + field + "'' does not exist in module: " + self.fields["name"])
		return (self.fields[field], "GET OK")

	def mod_set(self, field="none", value="none"):
		if field not in self.fields:
			return (-1, "SET FATAL: field '" + field + "'' does not exist in module: " + self.fields["name"])
		if field not in self.writable:
			return (-1, "SET FATAL: field '" + field + "' is not writable in module: " + self.fields["name"])
		try:
			self.fields[field] = int(value)
			return (0, "SET OK")
		except:
			return (-1, "SET FATAL: field '" + field + "' in module: " + self.fields["name"] + " takes int")

	def mod_exe(self):
		pass

	def mod_not(self):
		pass

	def mod_update(self):
		if self.fields["flush"] != 0:
			self.fields["detections"] = 0
			self.fields["detections_str"] = []
			self.fields["flush"] = 0
		for i in range(0,randint(4,100)):
			strength = randint(0,100) 
			if strength > self.fields["threshold"]:
				self.fields["detections"] += 1
				self.fields["detections_str"].append(strength)