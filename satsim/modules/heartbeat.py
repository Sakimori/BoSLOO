from .module import module

class heartbeat_module(module):
	def __init__(self):
		super().__init__("heartbeat")
		self.fields["MTE"] = 0
		self.fields["kill"] = 0
		self.writable = ["kill"]

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
		self.fields["MTE"] += 1