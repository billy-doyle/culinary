
# do the following cmd
# python3 culinary.py > README.md

import pandas as pd
from pint import UnitRegistry
from tabulate import tabulate

ureg = UnitRegistry()
ureg.define('pinch = .0625 * teaspoon')
ureg.define('egg_unit = 1 * atomic_mass_constant')
ureg.define('plate = 1 * atomic_mass_constant')

df = pd.read_csv('baking_ingredients.csv', index_col=0)
unit_conv = {'cup': ureg.US_liquid_cup, 
             'teaspoon': ureg.teaspoon, 
             'ounce': ureg.US_fluid_ounce,
             'pinch': ureg.pinch,
             'unit': ureg.egg_unit,
             'plate': ureg.plate}

df['pint_unit'] = df['quantity'] * df['unit'].map(unit_conv)

all_ingreds = df.groupby(['ingredient'])['pint_unit'].sum().reset_index().set_index('ingredient')



di = pd.read_csv('baking_directions.csv', index_col=0)

for cookie in df['cookie'].unique():
    c, d, y = di[di['cookie'] == cookie].values[0]
    print(f"\n# {c}, yield = {y}\n")
    print(f"![alt text](pictures/{cookie}.jpg)")
    print(d)
    ingred_table = df[df['cookie'] == cookie][df.columns[1:]].set_index('quantity').drop(columns='pint_unit')
    ingred_table.fillna('', inplace=True)
    print('\n')
    print(tabulate(ingred_table, tablefmt="pipe", headers="keys"))
    

print('\n# All Ingredients\nall ingredients for all cookies are here\n')
print(tabulate(all_ingreds, tablefmt="pipe", headers="keys"))
