import re 

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

print(f'Instrucciones {rules}')

results = []

#conversión de {contenido} a lista
def parse_field(val):
    val = val.strip()
    if val.startswith('{') and val.endswith('}'):
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

    #separación de cada elemento por comas si no está dentro de {}
    for char in body:
        if char == '{':
            inside_braces = True
        elif char == '}':
            inside_braces = False

        if char == ',' and not inside_braces:
            items.append(current.strip())
            current = ''
        else:
            current += char
    
    if current:
        items.append(current.strip())
        
    if len(items) >= 5:
        results.append({
            'tipo': tipo,
            'ei': items[0],
            'ef': items[1],
            'sl': parse_field(items[2]),
            'se': parse_field(items[3]),
            'dir': items[4]                
        })

for i in results:
    print(i)