class module:
	id_c = 0
	def __init__(self, name):
		self.fields = {}
		self.fields["name"] = name
		self.id = module.id_c
		module.id_c += 1

	def mod_get(self):
		print("[!] GET CALLED ON PRIMITIVE MODULE")

	def mod_set(self):
		print("[!] SET CALLED ON PRIMITIVE MODULE")

	def mod_exe(self):
		print("[!] EXE CALLED ON PRIMITIVE MODULE")

	def mod_not(self):
		print("[!] NOT CALLED ON PRIMITIVE MODULE")

	def mod_update(self):
		pass