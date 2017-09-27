import qgen
obj = qgen.QueryGen()
greet = "Hello, How can I help You?"
print greet
i = str(raw_input(">"))
while "thank you" not in i.lower():
	op_str = obj.query(i)
	print op_str
	i = raw_input("> ")
	