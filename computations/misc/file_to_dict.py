
# open the file
# -> read all (type is a string)
# ---> put the string into stringToDict 

def file_to_dict(filename):
	z = open(filename)
	Str = z.read()
	if Str[0] == "{":
		Str[0] = ""
	if Str[len(Str)-1] == "}":
		Str[len(Str)-1] == ""
	str = Str.replace("}","")
	Colon_Comma = [-1]
	Dict = {}
	z.close()
	for a in range(len(Str)):
		if Str[a] == ":":
			Colon_Comma.append(a)
		if Str[a] == "\n":
			Colon_Comma.append(a)
	Colon_Comma.append(len(Str))
	a = 0
	while a+2 < len(Colon_Comma):
		if a == 0:
			Dict[Str[0:Colon_Comma[a+1]].strip()] = Str[Colon_Comma[a+1]+1:Colon_Comma[a+2]].strip()
		else:
			Dict[Str[Colon_Comma[a]:Colon_Comma[a+1]].strip()] = Str[Colon_Comma[a+1]+1:Colon_Comma[a+2]].strip()
		a += 2
	return Dict



