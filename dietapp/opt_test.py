import numpy
from cvxopt.modeling import variable, op
import time
start = time.time()
x = variable(7, 'x')
# cost
z=(333*x[0] + 308*x[1] +52* x[2] +400*x[3] +450*x[4] +56* x[5]+20*x[6])
# protein
mass1 =(- (180*x[0] + 190*x[1] +30* x[2] +10*x[3] +260*x[4] +130* x[5]+21*x[6]) <= -118)
# fat
mass2 =(- (20*x[0] + 3*x[1] +40* x[2] +865*x[3] +310*x[4] +30* x[5]+2*x[6]) <= -56)
# hydrocarbon
mass3 =(- (50* x[2] +6*x[3] +20*x[4] +650* x[5]+200*x[6]) <= -500) 
# minerals
mass4 =(- (9*x[0] + 10*x[1] +7* x[2] +12*x[3] +60*x[4] +20* x[5]+10*x[6]) <= -28)
x_non_negative = (x >= 0)    

problem =op(z,[mass1,mass2,mass3,mass4 ,x_non_negative])
problem.solve(solver='glpk')  
problem.status
print("Результат:")
print(round(1000*x.value[0],1),'-грамм мяса, затраты -',round(x.value[0]*333,1),'руб.')
print(round(1000*x.value[1],1),'-грамм рыбы, затраты -',round(x.value[1]*308,1),'руб.')
print(round(1000*x.value[2],1),'-миллилитров молока, затраты -',round(x.value[2]*52,1),'руб.')
print(round(1000*x.value[3],1),'-грамм масла, затраты -',round(x.value[3]*400,1),'руб.')
print(round(1000*x.value[4],1),'-грамм сыр, затраты -',round(x.value[4]*450,1),'руб.')
print(round(1000*x.value[5],1),'-грамм крупы, затраты -',round(x.value[5]*56,1),'руб.')
print(round(1000*x.value[6],1),'-грамм картофеля, затраты -',round(x.value[6]*25,1),'руб.')
print(round(problem.objective.value()[0],1),"- стоимость рациона одного человека в день")
stop = time.time()
print ("Время :",round(stop-start,3))
