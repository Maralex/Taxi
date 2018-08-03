import scipy.stats as st

# Функция, которая считывает превращает построчный файл в словарь
def stats(path:str) -> dict:
    req_count = {}
    try:
        f = open(path)
    except:
        print('File is missing/corrupted')
        return
    with f as file:
        for line in file:
            try:
                req, mob = line.split(',')[1:]
                mob = int(mob)
                if not(mob==0 or mob==1): continue
                if req in req_count.keys():
                    req_count[req][0]+=1
                    req_count[req][1]+=mob
                else:
                    req_count[req] = [1,mob]
            except:
                pass
    return req_count

# Считаем 95% доверительный интервал для одного элемента словаря
def mean_ci(lst:list, conf=0.95, t=True) -> tuple:
    try:
        mob, n, n_1 = lst[1], lst[0], lst[0]-1
        m = mob/n
        if n==1: return (m, m, m)
        se = (m*(1-m)/n_1)**(0.5)
        h = se * st.t._ppf((1+conf)/2., n_1)
        return (m, m-h, m+h) if t==True else (m, se)
    except:
        pass
    
# Выводим результаты для всего словаря    
def means_ci(d:dict, conf=0.95):
    try:
        print('Name, Mean, Mean-SE, Mean+SE')
        print('----------------------------')
        for key, value in d.items(): print(key, mean_ci(value, conf))
    except:
        pass

# Проверка гипотезы о равенстве долей запросов с мобильных устройств
def compare(lst_1:list, lst_2:list, p=0.05) -> str:
    try:
        m1, st1= mean_ci(lst_1, t=False)
        m2, st2 = mean_ci(lst_2, t=False)
        if st.ttest_ind_from_stats(mean1=m1, std1=st1, nobs1=lst_1[0], 
                                   mean2=m2, std2=st2, nobs2=lst_2[0])[1] > p:
            return "Test result: reject null"
        return "Test result: inconclusive"
    except: 
        return ""

# Вывод всех результатов
def print_results(path:str):
    try:
        d = stats(path)
        means_ci(d)
        print('----------------------------')
        print(compare(d['/index'], d['/test']))
    except:
        pass
    
    
if __name__ == "__main__":
    user_input = input("Specify file path:")
    path = user_input if len(user_input)>0 else path = 'log.txt'
    print_results(path)
    input()