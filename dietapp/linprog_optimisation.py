from scipy.optimize import linprog
import time

def calcul(products):
    #  вес P — x1, к --x2
    # c = [-250,-210] #Функция цели 250x1+210x2 – уменьшение расходов на продуктовую корзину ;
    # A_ub = [[15,4]]  #'1' жиры последовательно для Р и К
    # b_ub = [14] #'1' 15x1+4x2 <=14 – ограничение количества жира;
    # A_eq = [[150,200]] #'2' 150x1+200x2 =300 – ограничение количества калорий.
    # b_eq = [300] #'2'
    # print (linprog(c, A_ub, b_ub, A_eq, b_eq))

    if not products:
        return []

    n = len(products)-2

    c = []
    ub = []
    eq = []
    for i in range(0,n):
        c.append(products[i].default_price)
        ub.append(products[i].fat)
        eq.append(products[i].calories)
    A_ub = [ub]
    i += 1
    b_ub = products[i].fat
    A_eq = [eq]
    i += 1
    b_eq = products[i].calories

    result = linprog(c, A_ub, b_ub, A_eq, b_eq)
    print(result.x)

    return result.x.tolist()
    # return [1, 2, 3]
