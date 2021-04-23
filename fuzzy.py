"""     Fuzzy Logic Task by Abdullah Hadi      """
"""     Import necessary module   """
import pandas as pd
import numpy as np

df = pd.read_excel('Mahasiswa.xls')
data = df.to_numpy().copy()


"""     Membership Functions income     """
def income_rich(x, a=12, b=15):
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if x >= b: return 1


def income_upper(x, a=8, b=10, c=12, d=15):
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if b <= x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


def income_mid(x, a=6, b=7, c=8, d=10):
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if b <= x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


def income_bottom(x, c=5, d=6):
    if x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


"""     Membership Functions  expense       """
def expense_inflated(x, a=12, b=15):
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if x >= b: return 1


def expense_high(x, a=8, b=10, c=12, d=15):
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if b <= x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


def expense_avg(x, a=4, b=7, c=8, d=10):
    x = float(x)
    if x <= a: return 0
    if a < x < b: return (x - a) / (b - a)
    if b <= x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


def expense_low(x, c=3, d=5):
    x = float(x)
    if x <= c: return 1
    if c < x <= d:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0


"""     Fuzzification       """
def fuzzification_income(value_income):
    income_set = {'rich': income_rich(value_income), 'upper': income_upper(value_income),
                  'mid': income_mid(value_income), 'bottom': income_bottom(value_income)}
    return income_set


def fuzzification_expense(value_expense):
    expense_set = {'inflated': expense_inflated(value_expense), 'high': expense_high(value_expense),
                   'avg': expense_avg(value_expense), 'low': expense_low(value_expense)}
    return expense_set


"""     Inference Step      """
def inference(income_set, expense_set):
    inference_set = {'yes': [], 'consider': [], 'no': []}

    inference_set['yes'].append(min(income_set['bottom'], expense_set['low']))
    inference_set['yes'].append(min(income_set['bottom'], expense_set['avg']))
    inference_set['yes'].append(min(income_set['bottom'], expense_set['high']))
    inference_set['yes'].append(min(income_set['bottom'], expense_set['inflated']))

    inference_set['consider'].append(min(income_set['mid'], expense_set['low']))
    inference_set['yes'].append(min(income_set['mid'], expense_set['avg']))
    inference_set['yes'].append(min(income_set['mid'], expense_set['high']))
    inference_set['yes'].append(min(income_set['mid'], expense_set['inflated']))

    inference_set['no'].append(min(income_set['upper'], expense_set['low']))
    inference_set['consider'].append(min(income_set['upper'], expense_set['avg']))
    inference_set['yes'].append(min(income_set['upper'], expense_set['high']))
    inference_set['yes'].append(min(income_set['upper'], expense_set['inflated']))

    inference_set['no'].append(min(income_set['rich'], expense_set['low']))
    inference_set['no'].append(min(income_set['rich'], expense_set['avg']))
    inference_set['consider'].append(min(income_set['rich'], expense_set['high']))
    inference_set['yes'].append(min(income_set['rich'], expense_set['inflated']))

    inference_set['yes'] = max(inference_set['yes'])
    inference_set['consider'] = max(inference_set['consider'])
    inference_set['no'] = max(inference_set['no'])

    return inference_set

"""     Membership function for mamdani/the random generated number     """
def yes(x, max, a=60, b=70):
    yes = 0
    if x <= a: return 0
    if x >= b: return max
    if a < x < b and ((x - a) / (b - a)) <= max:
        return (x - a) / (b - a)
    else:
        return max


def consider(x, max, a=50, b=60, c=70):
    if x <= a or x >= c: return 0
    if a < x <= b: return (x - a) / (b - a)
    if b < x <= c: return -((x - c) / (c - b))


def no(x, max, c=40, d=60):
    x = float(x)
    if x <= c: return max
    if c < x <= d and -((x - d) / (d - c)) <= max:
        return -((x - d) / (d - c))
    elif x >= d:
        return 0
    else:
        return max


"""     Defuzzyfication     """
def defuzzification(inference_set, random_set):
    defuz_set = {'no': np.zeros(random_set.size),
                 'consider': np.zeros(random_set.size),
                 'yes': np.zeros(random_set.size)}

    for i in range(random_set.size):
        defuz_set['yes'][i] = yes(random_set[i], inference_set['yes'])
        defuz_set['consider'][i] = consider(random_set[i], inference_set['consider'])
        defuz_set['no'][i] = no(random_set[i], inference_set['no'])

    defuz_semi = np.zeros(random_set.size)
    for i in range(random_set.size):
        defuz_semi[i] = max(defuz_set['yes'][i], defuz_set['consider'][i], defuz_set['no'][i])

    multiplication_set = random_set * defuz_semi
    result = np.sum(multiplication_set) / np.sum(defuz_semi)

    return result

"""     Main system and program     """
def fuzzy_system(data, random_set):
    for i in range(data.shape[0]):
        income = fuzzification_income(data[i, 1])
        expense = fuzzification_expense(data[i, 2])

        inference_set = inference(income, expense)

        result = defuzzification(inference_set, random_set)

        data[i, 3] = result

    return data


def get_20(data):
    chosen_20 = []
    for i in range(20):
        chosen_20.append(data[np.argmax(data, axis=0)[3]])
        data = np.delete(data, np.argmax(data, axis=0)[3], 0)

    return np.array(chosen_20)

def main():
    random_number = 7 # nilai aslinya didapatkan dengan np.random.randint(11)
    random_set = np.arange(random_number, 100, random_number)

    data_fuz = np.pad(data, ((0, 0), (0, 1)), mode='constant', constant_values=0)

    fuzzy_system(data_fuz, random_set)

    the_chosen_20 = get_20(data_fuz)

    df = pd.DataFrame(the_chosen_20, columns=['Id', 'Penghasilan', 'Pengeluaran', 'NK'])
    print(df)

    df = pd.DataFrame(np.hsplit(the_chosen_20, 4)[0], columns=['Id'])
    filepath = 'Bantuan.xls'
    df.to_excel(filepath, index=False)

main()

