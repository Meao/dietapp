import numpy as np

def app_products2optimisation(products):
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
    i += 1 # Перехожу к столбцу свободных членов для уравнения меньше чем, в продуктах это вещь под назавнием Minimise Fat
    ub.append(products[i].fat)
    A_ub = np.array([ub])
    c.append(products[i].default_price)
    i += 1 # Перехожу к столбцу свободных членов для уравнения больше чем, в продуктах это вещь под назавнием Get enough calories
    eq.append(products[i].calories)
    A_eq = np.array([eq])
    A_eq = -1 * A_eq # Для > меняем знак всех элементов (потом написать в цикл автоматом по условию!)
    c = np.array([c])
    A_eq = np.squeeze(A_eq) # Django мне создала списки двойного уровня вложенности, надо уменьшить это
    A_ub = np.squeeze(A_ub)
    c = np.squeeze(c)

    table = [A_ub, A_eq, c]
    table = np.asarray(table, dtype=float)

    b = np.identity(n+1) # создаю единичную матрицу
    # amount_columns = np.size(table,1)
    table = np.insert(table,n,b,axis=1) # вставляю единичную матрицу в таблицу перед столбцом с номером amount_columns-1, получается n+1, по столбцам, т.е. axis 1
    print('np.size(table)',np.size(table))
    print(table)
    #return type(table)

    result = minimise(table)
    result[n] = -1 * result[n]
    print(result)

    return result
    # return [1, 2, 3]

def amount_rows(amount_constraints):
    amount_rows = amount_constraints+1
    return amount_rows

def amount_columns(amount_variables,amount_constraints):
    amount_columns = amount_variables+amount_constraints+2
    return amount_columns

def create_simplex_table(amount_variables,amount_constraints):
    #Создание двумерного массива
    r = amount_rows(amount_constraints)
    c = amount_columns(amount_variables,amount_constraints)
    empty_table = np.zeros((r, c))
    return empty_table
    #Количество строк = кол-ву ограничений + целевая функция amount_constraints+1
    #Количество столбцов = кол-ву переменных + кол-ву дополнительных переменных для приведения системы к каноническому виду + M (max/min) + Колонка свободных членов

def input_to_list(equation): #Перевод в list
    equation = equation.split(',')
    if '>' in equation:
        text_index = equation.index('>')
        del equation[text_index]
        equation = [float(i) * -1 for i in equation]
        return equation
    if '<' in equation:
        text_index = equation.index('<')
        del equation[text_index]
        equation = [float(i) for i in equation]
        return equation

def xi_names(table):
    # Создание названий переменных x1, x2, ..., xn
    amount_rows = np.size(table,0) # Подсчет количества строк с помощью axis=0
    amount_columns = np.size(table,1) # Подсчет количества столбцов с помощью axis=1
    xi = amount_columns - amount_rows -1
    names = []
    for i in range(xi):
        names.append('x' + str(i + 1))
    return names

def lines4constraints_available(filled_table):
    # Проверка, что в предпоследней строке нули, чтобы добавить ещё ограничение
    penultimate_row = filled_table[-2:-1]
    return (~penultimate_row.any(axis=1)).any()
    #The any method returns True if any value in the array is "truthy".
    # Nonzero numbers are considered True, and 0 is considered False.
    # By using the argument axis=1, the method is applied to each row.

def add_constraint(table, equation):
    # Заполнение свободных строк для ограничений
    if lines4constraints_available(table):
        amount_rows = np.size(table,0) # Подсчет количества строк с помощью axis=0
        amount_columns = np.size(table,1) # Подсчет количества столбцов с помощью axis=1
        xi = amount_columns - amount_rows -1 # Количество переменных
        b = np.where(~table.any(axis=1))[0] # Поиск строк со всеми нулями
        j = b[0] # Номер первой строки со всеми нулями
        row = table[j, :] # Первая строка со всеми нулями
        equation = input_to_list(equation)
        i = 0
        # Наполнение двумерного массива пока в выражении еще есть переменные
        while i < len(equation) - 1:
            # Переменные базиса записать в таблицу
            row[i] = equation[i]
            i += 1
        row[-1] = equation[-1] #Колонка свободных членов
        row[xi + j] = 1 # Создание 1 для единичной матрицы справа базиса
    else:
        print('Свободных строк для ограничений больше не было предусмотрено, начните сначала или введите целевую функцию.')

def line4objective_available(filled_table): # Проверка, есть ли нули в последней (и только последней) строке, чтобы вставить целевую функцию
    last_rows = np.array(filled_table[-2:])
    empty = np.where(~last_rows.any(axis=1))[0]
    if np.array_equal(empty, np.array([1])):
        return True
    else:
        return False

def add_objective(table, equation):
    # добавляет целевую функцию, если есть свободная строка в конце таблицы
    if line4objective_available(table):
        equation = [float(i) for i in equation.split(',')]
        amount_rows = np.size(table,0) # Подсчет количества строк с помощью axis=0
        row = table[amount_rows - 1, :]
        i = 0
        # пока в выражении еще есть переменные
        while i < len(equation)-1:
            # записать их в таблицу
            row[i] = equation[i] * -1
            i += 1
        row[-2] = 1 # Создание 1 для единичной матрицы справа базиса
        row[-1] = equation[-1] #Хранение значения необходимого бюджета
    else:
        print('Остались пустые сроки, введите ограничения или начните сначала.')

def convert_min(filled_table): # Для минимизации последняя строка (целевая функция) умножается на -1
    filled_table[-1] = -1 * filled_table[-1]
    return filled_table

def check_bi_positifs(filled_table):
    # Проверка, что в столбце свободных членов не осталось отрицательных
    min_bi = min(filled_table[:-1,-1])
    if min_bi >= 0:
        return False # Достигнут оптимум, переход к выводу
    else:
        return True # Необходимо пересчитать строку

def check_cj0(filled_table):
    #Проверка условия: все ли элементы последней строки отрицательны, cj<=0
    amount_conditions = np.size(filled_table,0) # Подсчет количества строк с помощью axis=0
    max_cj = max(filled_table[amount_conditions-1,:-1]) # Выбор наибольшего элемента в слайсе [последняя строка, вся таблица без последнего столбца]
    # return (max_cj <= 0) # идентично
    if max_cj >= 0:
        return False #Переход к следующему шагу метода
    else:
        return True #Переход к выводу результата

def neg_bi_index(filled_table):
    # Поиск номера строки с отрицательным свободным членом
    amount_conditions = np.size(filled_table,0)-1 # Подсчет количества строк с помощью axis=0
    min_bi_row_number = np.argmin(filled_table[:-1,amount_conditions])# + 1 Возвращает индекс наменьшего элемента в слайсе [вся таблица без последней строки, последний столбец], добавляем 1 чтобы номер столбца был человекочитаемым
    return min_bi_row_number

def column_choice(filled_table):
    #Выбор разрешающего столбца,  cj
    amount_conditions = np.size(filled_table, 0) - 1 # Подсчет количества строк с помощью axis=0
    min_cj_column_number = np.argmin(filled_table[amount_conditions, :-1]) #+ 1  Возвращает индекс наибольшего элемента в слайсе [последняя строка, вся таблица без последнего столбца], добавляем 1 чтобы номер столбца был человекочитаемым
    return min_cj_column_number

def bi_to_positive(filled_table):
        division = [] # Разрешение двойственной задачи линейного программирования
        row_index = neg_bi_index(filled_table)
        min_in_row_column_number = np.argmin(filled_table[row_index,:-1]) #+1  Возвращает индекс наименьшего элемента в слайсе по номеру строки с отрицательным свободным членом, исключая последний столбец , добавляем 1 чтобы номер столбца был человекочитаемым
        col = filled_table[:-1, min_in_row_column_number]
        # все коэффициенты ограничений этого столбца
        last_column = filled_table[:-1,-1]
        for i, b in zip(col, last_column):
            if i != 0 and b / i > 0:
                division.append(b / i)
            else:
                division.append(10000)
        index = division.index(min(division)) #наименьшее позитивное частное
        return [index,min_in_row_column_number]

def row_choice(filled_table):
    if check_cj0(filled_table):#Надо поднимать ошибку, если не срабатывает!!!!
        c = column_choice(filled_table) #Номер разрешающего столбца в человеческом формате
        divided = []
        r_column = filled_table[:-1, c - 1] # [вся таблица без последней строки, столбец r в машинном формате]
        last_column = filled_table[:-1, -1]
        for r, l in zip(r_column, last_column):
            if r > 0:
                divided.append(l/r)
            else:
                divided.append(100000)
        min_air_row_number = divided.index(min(divided))  #+1 #Номер разрешающей строки в человеческом формате
        return [min_air_row_number, c]

def calc(chosen_row, chosen_column, source_table): #Пересчет элементов
    target_table = np.zeros_like(source_table, dtype=float)  # Создание новой нулевой таблицы
    r = chosen_row  #-1 # Номер разрешающей строки в машинном формате
    c = chosen_column  #-1 # Номер разрешающего столбца в машинном формате
    pivot_row = source_table[r, :]  # Разрешающая строка
    pivot_element = source_table[r, c]  # Разрешающий элемент
    if pivot_element:
        e = 1 / pivot_element
        new_chosen_row = pivot_row * e  # Делим все элементы разрешающей строки на разрешающий элемент
        for i in range(np.size(source_table, 0)): # количеств строк с помощью axis=0
            if i != r: # Если текущая строка отличается от поворотной строки
                row = source_table[i, :] # Очередная строка
                p_c_el = source_table[i, c] # Элемент текущей строки, который в разрешающем столбце
                target_table[i, :] = list(row-new_chosen_row * p_c_el) # заменяем элементы очередной строки новой таблицы на вычисленные,
                # домножаем на уже посчитанные элементы разрешающей строки, чтобы не повторять вычисление
        target_table[r, :] = list(new_chosen_row) # Делим все элементы разрешающей строки на разрешающий элемент, заменяем элементы разрешающей строки на вычисленные
        return target_table
    else:
        print('Разрешающий элемент не позволяет провести пересчет.')

def minimise(table, output='результаты'):
    # Обращается к функциям пересчета и выводит результаты
    table = convert_min(table)

    while check_bi_positifs(table):
        table = calc(
            bi_to_positive(table)[0],
            bi_to_positive(table)[1],
            table
            ) # Жордановы замены для негативных свободных членов, требуются в двойственном симплексе
    while check_cj0(table):
        table = calc(
            row_choice(table)[0],
            row_choice(table)[1],
            table
            ) # Жордановы замены для последней строки, коэффициентов при целевой функции

    amount_columns = np.size(table,1) # Подсчет количества столбцов с помощью axis=1
    amount_rows = np.size(table,0) # Подсчет количества строк с помощью axis=0
    var = amount_columns - amount_rows -1
    i = 0
    val = {} # Создание пустого словаря для хранения результатов работы алгоритма
    for i in range(var): # для солбцов переменных вне базиса, поиск числа в солбце и сопоставление числу результату в последнем столбце
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[xi_names(table)[i]] = table[loc, -1]
        else:
            val[xi_names(table)[i]] = 0
    val['min'] = table[-1, -1] * -1 # для терминала результаты в виде словаря с ключами по номерам переменных x1,x2...xn и значением бюджета с ключом min
    val = list(val.values()) # для джанги результаты в виде list # return [1, 2, 3]
    if output == 'table':
        return table
    else:
        return val

if __name__ == "__main__":

    st = create_simplex_table(2, 4)
    add_constraint(st,'2,5,>,30')
    add_constraint(st,'-3,5,>,5')
    add_constraint(st,'8,3,<,85')
    add_constraint(st,'-9,7,<,42')
    add_objective(st,'2,7,0')
    print(minimise(st))
    print('-'*100)

    st = create_simplex_table(2,2)
    add_constraint(st,'15,4,<,14')
    add_constraint(st,'150,200,>,300')
    add_objective(st,'250,210,0')
    print(minimise(st))
    print('-'*100)

    st = create_simplex_table(2,2)
    add_constraint(st,'1450,770,>,1100')
    add_constraint(st,'560,120,>,800')
    add_objective(st,'130,30,0')
    print(minimise(st))
    print('-'*100)
    print('-'*100)

    a = np.array([
        [0.,0.,0.,0.,0.,0.],
        [0.,0.,0.,0.,0.,0.],
        [0.,0.,0.,0.,0.,0.]])
    assert np.array_equal(create_simplex_table(2,2),a),"ошибка создания nparray"

    test_table1 = np.array([
        [4,6,1,0,0,120],
        [2,6,0,1,0,72],
        [0,1,0,0,1,10],
        [2,4,0,0,0,0]])
    test_table2 = np.array([
        [4,0,1,0,-6,60],
        [2,0,0,1,-6,12],
        [0,1,0,0,1,10],
        [2,0,0,0,-4,-40]])
    test_table3 = np.array([
        [0,0,1,-2,6,36],
        [1,0,0,0.5,-3,6],
        [0,1,0,0,1,10],
        [0,0,0,-1,2,-52]])
    test_table4 = np.array([
        [0,0,1/6,-1/3,1,6],
        [1,0,0.5,-0.5,0,24],
        [0,1,-1/6,1/3,0,4],
        [0,0,-1/3,-1/3,0,-64]])

    assert check_cj0(test_table1)==False,"ошибка проверки условия cj<=0"
    assert check_cj0(test_table2)==False,"ошибка проверки условия cj<=0"
    assert check_cj0(test_table3)==False,"ошибка проверки условия cj<=0"

    assert column_choice(test_table1)==2,"ошибка выбора разрешающего столбца"

    assert np.array_equal(calc(3-1,2-1,test_table1),test_table2),"ошибка пересчета" # везде -1, использует индекс в машинном формате
    assert np.array_equal(calc(2-1,1-1,test_table2),test_table3),"ошибка пересчета"
    assert np.allclose(calc(1-1,5-1,test_table3),test_table4),"ошибка пересчета"
