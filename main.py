import re 
#Lectura archivo
file = open(r"C:\Users\hrosa\OneDrive\Documentos\CIC IPN\Primer Semestre\Teoria Computacion\SIMULADORMTU\text.txt")
content = file.read()

#Extracción de estados de aceptación 
for i, instr in enumerate(content.split('\n')):
    if i == 0:
        estados_aceptacion = re.findall(r'\d+',instr)

print(f'estado de aceptación:{estados_aceptacion}')

rules = []
for i, instr in enumerate(content.split('\n')):
    if i != 0:
        rules.append(instr)

# print(f'Instrucciones {rules}')
#=============================================================================================
# user_string = input('Favor de introducir cadena: ')
user_string = '01101'
print(f'Hi {user_string}')
current_state = '00'
print(f'current state:{current_state}')
#=============================================================================================

new_rules = []
#conversión de {contenido} a lista
def parse_field(val):
    val = val.strip()
    if (val.startswith('{') and val.endswith('}')) or (val.startswith('[') and val.endswith(']')):
        return [s.strip() for s in val[1:-1].split(',')]
    return val

for i in rules:
    #ignorar entradas vacías
    i = i.strip()
    if not i:
        continue
    
    #de qué tipo de instrucción hablamos
    tipo = 'N'
    if i.startswith('W'):
        tipo = 'W'
    elif i.startswith('?'):
        tipo = '?'

    #extraemos contenido entre paréntesis
    match = re.search(r'\((.*)\)', i)
    if not match:
        continue
    body = match.group(1)

    #caso {contenido}
    items = []
    current = ''
    inside_braces = False
    inside_brackets = False

    #separación de cada elemento por comas si no está dentro de {}
    for char in body:
        if char == '{':
            inside_braces = True
        elif char == '}':
            inside_braces = False
        elif char == '[':
            inside_brackets = True
        elif char == ']':
            inside_brackets = False
        if char == ',' and not inside_braces and not inside_brackets:
            items.append(current.strip())
            current = ''
        else:
            current += char
    
    if current:
        items.append(current.strip())
        
    if len(items) >= 5:
        new_rules.append({
            'tipo': tipo,
            'ei': parse_field(items[0]),
            'ef': parse_field(items[1]),
            'si': parse_field(items[2]),
            'sf': parse_field(items[3]),
            'dir': items[4]                
        })

#================================================================================================
#================================================================================================
#INTERCAMBIO DE SIMBOLO '~' POR ESTADO/SIMBOLO RECIPROCO
for lists in new_rules:
    # print(lists)
    for key, values in lists.items():
        # print(type(values))
        if key == 'ei' and values == '~':
            lists[key] = lists['ef']
            # print(lists)
        elif key == 'ef' and values == '~':
            lists[key] = lists['ei']
            # print(lists)
        elif key == 'si' and values == '~':
            lists[key] = lists['sf']
            # print(lists)
        elif key == 'sf' and values == '~':
            lists[key] = lists['si']
            # print(lists)

for lists in new_rules:
    for key, values in lists.items():
        if key == 'ef' and isinstance(values,list):
            new_list = []
            for v in values:
                if v == '~':
                    new_list.append(lists['ei'])
                else:
                    new_list.append(v)
            lists[key] = new_list

list_string = [n for n in user_string] + (['B'] * (len(user_string)*4))
print(list_string)
# print(f'instructions:{new_rules}')
pos = 0
for i in new_rules:
    print(i)
#================================================================================================
#================================================================================================
#===============MAQUINA DE TURING: SOLO DESPLAZAMIENTO EN CADENAS TIPOS 10101===================
# while current_state not in estados_aceptacion:
#     symbol = list_string[pos] #empieza en la posicion inicial (0 -> 00)
#     change = False



#================================================================================================
#================================================================================================
#===============MAQUINA DE TURING: SOLO DESPLAZAMIENTO EN CADENAS TIPOS 10101===================
