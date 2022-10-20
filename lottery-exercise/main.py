import requests
import pandas as pd
import collections
import sys

url = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil'
requests.packages.urllib3.disable_warnings()
'''
Instead defining the url variable directly here in the code, we can use sys library to accept an argument value when we call
python command line to run our script. Example: python main.py 'https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil'

sys.argv[0] -> main.py
sys.argv[1] -> 'https://servicebus2.caixa.gov.br/portaldeloterias/api/resultados?modalidade=Lotofácil'

url = sys.argv[1]
'''

r = requests.get(url, verify=False)

'''
    Starting the Cleaning Data process
'''
# Removing all \r\n present all over the body response
r_text = r.text.replace('\\r\\n', '')
# Removing " } from the </table>
r_text = r.text.replace('"\r\n}', '')
# Removing { html from the beggining <table>
r_text = r.text.replace('{\r\n  "html": "', '')

df = pd.read_html(r_text)
print(type(df))
print(type(df[0]))

df_1 = df
df = df[0].copy()

# Fixing the columns
new_columns = df.columns
new_columns = list(i.replace('\\r\\n', '') for i in new_columns)
df.columns = new_columns

# Fixing empty/NaN rows
df = df[df['Bola1'] == df['Bola1']]
print(df)

# A Lotofacil game have 25 numbers to be choosen
nr_pop = list(range(1, 26))
even_number = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
odd_number = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
prime_number = [2, 3, 5, 7, 11, 13, 17, 19, 23]

comb = []

values_dict = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0,
    24: 0,
    25: 0
}

fields_list = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
               'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10',
               'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15']

# Iterate Dataframe rows
for index, row in df.iterrows():
    v_even = 0
    v_odd = 0
    v_prime = 0

    for field in fields_list:
        if row[field] in even_number:
            v_even += 1
        if row[field] in odd_number:
            v_odd += 1
        if row[field] in prime_number:
            v_prime += 1

        if row[field] in values_dict.keys():
            values_dict[row[field]] += 1

    comb.append(str(v_even) + 'even-' + str(v_odd) + 'odd-' + str(v_prime) + 'prime' )

#print(values_dict)

sorted_tuples = sorted(values_dict.items(), key=lambda item: item[1])

print("Went out less often: " + str(sorted_tuples[0]))
print("Went out more often: " + str(sorted_tuples[-1]))

# Handling with the odd,even,prime combinations
# Counter will rank from the most to the less number of times that a comb happened.
counter = collections.Counter(comb)
result = pd.DataFrame(counter.items(), columns=['Comb', 'Frequency'])

# Getting the percentage/rate
result['p_freq'] = result['Frequency'] / result['Frequency'].sum()
result = result.sort_values(by='p_freq')

print('''
The most frequent number is: {}
The less frequent number is: {}
The most frequent combination of odd/even/prime is: {} with the rate: {}%
'''.format(sorted_tuples[-1][0], sorted_tuples[0][0], result['Frequency'].values[-1], int((result['p_freq'].values[-1]*100)*100)/100)
)