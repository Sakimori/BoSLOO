from .module import module
class location_module(module):
	id_c = 0
	def __init__(self):
		super().__init__("location")
		self.fields["coords"] = "space"

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

	def mod_not(self):
		print("[!] NOT CALLED ON PRIMITIVE MODULE")

	def mod_update(self):
		pass