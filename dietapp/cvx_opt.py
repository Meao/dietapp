import numpy
from cvxopt.modeling import variable, op

def optimize_min(products):
	if not products:
		return []

	n = len(products)
	x = variable(n, 'x')

	# initialize parameters
	z = products[0].default_price * x[0]
	proteins = products[0].proteins * x[0]
	hydrocarbons = products[0].hydrocarbons * x[0]
	fat = products[0].fat * x[0]
	minerals = products[0].minerals * x[0]

	# construct parameters
	for i in range(1, n):
		z = z + products[i].default_price * x[i]
		proteins = proteins + products[i].proteins * x[i]
		hydrocarbons = hydrocarbons + products[i].hydrocarbons * x[i]
		fat = fat + products[i].fat * x[i]
		minerals = minerals + products[i].minerals * x[i]

	mass1 = (- proteins <= -118)
	mass2 = (- hydrocarbons <= -500)
	mass3 = (- fat <= -56)
	mass4 = (- minerals <= -28)
	x_non_negative = (x >= 0)

	problem = op(z, [mass1, mass2, mass3, mass4, x_non_negative])
	problem.solve(solver='glpk')
	problem.status

	result = []
	for i in range(0, n):
		result.append(round(1000*x.value[i], 1))

	return result
