def newParam(winningParam, losingParam, isInt):
	#not sure what to make step size since I don't know what the function is
	if isInt:
		d = 1
	else:
		d = 0.5
	if winningParam < losingParam:
		return losingParam - d
	else:
		return losingParam + d
