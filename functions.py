import pandas as pd


def create_header(file1, file2):
    s = ''
    s += f'<h2>COMPARING MODELS</h2>'
    s += f'<h3>To Go From {file1} to --> {file2}</h3>'
    return s

def create_modules_data(modules1, modules2):
    s = '\n'
    s+= '<h3>MODULES</h3>'
    s+= '---'

    s += '<h4>DELETE Modules</h4>'
    for i in list(set(modules1) - set(modules2)):
        s+= f'- {i}\n'

    s += '\n'
    s += '<h4>CREATE Modules</h4>'
    for i in list(set(modules2) - set(modules1)):
        s += f'+ {i}\n'

    return s

def create_line_items_data(d1, d2):
    s = '\n'
    s += '<h3>LINE ITEMS</h3>'
    s += '-<h4>CREATE Line Items</h4>'
    for lineItem in set(d2.keys()) - set(d1.keys()):
        f = d2[lineItem]['Formula']
        s += f'+ NAME:{lineItem[0]}.{lineItem[1]}| FORMULA: {f}\n'
    s += '\n---\n'
    s += '<h4>DELETE line Items</h4>'
    for lineItem in set(d1.keys()) - set(d2.keys()):
        s += f'- {lineItem[0]}.{lineItem[1]}\n'

    # Find Changed Formulas
    line_items = set(list(d1.keys())).intersection(d2.keys())

    changed_line_items = {}
    for i in line_items:
        if d1[i]['Formula'] != d2[i]['Formula']:
            changed_line_items[i] = {}
            changed_line_items[i]['d1'] = d1[i]['Formula']
            changed_line_items[i]['d2'] = d2[i]['Formula']

    s += '\n---\n'
    s += '<h4>CHANGE line Items</h4>'

    for k, i in changed_line_items.items():
        s += f'{k[0]}.{k[1]} | FROM: {i["d1"]} | TO: {i["d2"]}\n'

    return s

def get_diff(file1, file2):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Make Modules List
    modules1 = df1['Module Name'].unique()
    modules2 = df2['Module Name'].unique()

    modules1 = [x for x in modules1 if not pd.isna(x)]
    modules2 = [x for x in modules2 if not pd.isna(x)]


    # Make list of lineitems
    d1 = {}
    for i, r in df1.iterrows():
        if not pd.isna(r['Formula']):
            d1[(r['Module Name'], r['Unnamed: 0'])] = {}
            d1[(r['Module Name'], r['Unnamed: 0'])]['Formula'] = r['Formula']

    d2 = {}
    for i, r in df2.iterrows():
        if not pd.isna(r['Formula']):
            d2[(r['Module Name'], r['Unnamed: 0'])] = {}
            d2[(r['Module Name'], r['Unnamed: 0'])]['Formula'] = r['Formula']


    ## create output
    s = create_header('file1', 'file2')
    s += create_modules_data(modules1, modules2)
    s += create_line_items_data(d1, d2)
    return s
