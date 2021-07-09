from .module import module

class memory_module(module):
	def __init__(self):
		super().__init__("memoryBank")
		self.fields["files"] = []
		self.fields["freeSpace"] = 4000
		self.fields["mode"] = "upload"
		self.fields["buffer"] = 0
		self.fields["filename"] = ""
		self.writable = ["buffer","filename", "mode"]


	def mod_get(self, field="none"):
		if field not in self.fields:
			return (-1, "GET FATAL: field '" + field + "'' does not exist in module: " + self.fields["name"])
		return (self.fields[field], "GET OK")

	def mod_set(self, field="none", value="none"):
		if field not in self.fields:
			return (-1, "SET FATAL: field '" + field + "'' does not exist in module: " + self.fields["name"])
		if field not in self.writable:
			return (-1, "SET FATAL: field '" + field + "' is not writable in module: " + self.fields["name"])
		if field == "mode" and (value == "upload" or value == "download"):
			self.fields[field] = value
			return (0, "SET OK")
		self.fields[field] = value
		return (0, "SET OK")		

	def mod_exe(self):
		if self.fields["mode"] == "upload":
			if self.fields["freeSpace"] - len(self.fields["buffer"]) >= 0:
				self.fields["freeSpace"] -= len(self.fields["buffer"])
				with open("./datastore/"+self.fields["filename"],"wb+") as f:
					f.write(bytes(self.fields["buffer"],encoding="UTF-8"))
				return (0, "WRITE OK")
			else:
				return (-1, "WRITE FATAL: OUT OF MEMORY")
		if self.fields["mode"] == "download":
			try:
				with open("./datastore/"+self.fields["filename"],"rb") as f:
					return (f.read(), "READ OK")
			except:
				return (-1, "READ FATAL: FILE NOT FOUND")


	def mod_not(self):
		pass

	def mod_update(self):
		pass