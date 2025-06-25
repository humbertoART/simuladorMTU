import re 
import msvcrt
import os
#Escritura de cadena de entrada por usuario
def user_string_input():
    user_string = input('Favor de introducir cadena: ')
    return user_string
#Lectura archivo
def simuladorMTU():
    dir_validate = {'!','>','<'}
    same_symbol = {'~'}

    def lector_texto():
        while True:
            user_text = input("Ingrese ruta del archivo de texto, por favor: ")
            if not os.path.exists(user_text):
                print("Texto no introducido, vuelva a intertalo\n")
                continue
            # file = open(r"C:\Users\hrosa\OneDrive\Documentos\CIC IPN\Primer Semestre\Teoria Computacion\SIMULADORMTU\text.txt")
            file = open(user_text, "r", encoding="ascii")
            content = file.read()
            print(content)

            instructions = content.split('\n')
            end_dot = True

            for instr in instructions:
                line = instr.strip()
                if line:
                    if not line.endswith('.'):
                        end_dot = False
                        break
            if end_dot:
                break
            else:
                print('Las instrucciones no terminan en punto, ingrese nuevamente ruta:\n')
        return instructions
    
    while True:
        #Extracción de estados de aceptación 
        instructions = lector_texto()
        for i, instr in enumerate(instructions):
            if i == 0:
                estados_aceptacion = re.findall(r'\d+',instr)

        print(f'estado de aceptación:{estados_aceptacion}')

        rules = []
        for i, instr in enumerate(instructions):
            if i != 0:
                rules.append(instr)

        # print(f'Instrucciones {rules}')
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
        #====================INTERCAMBIO DE SIMBOLO '~' POR ESTADO/SIMBOLO RECIPROCO=====================
        #================================================================================================
        for lists in new_rules:
            # print(lists)
            for key, values in lists.items():
                # print(type(values))
                # if key == 'ei' and values == '~':
                #     lists[key] = lists['ef']
                    # print(lists)
                if key == 'ef' and values == '~':
                    lists[key] = lists['ei']
                    # print(lists)
                # elif key == 'si' and values == '~':
                #     lists[key] = lists['sf']
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

        for lists in new_rules:
            for key, values in lists.items():
                if key == 'sf' and isinstance(values,list) and isinstance(lists['si'],list):
                    lista = []
                    for i, v in enumerate(values):
                        if v == '~':
                            lista.append(lists['si'][i])
                        else:
                            lista.append(v)
                    lists[key]  = lista

        errors = False
        for i in new_rules:
            for key, value in i.items():
                if key == 'ei' or key == 'ef' or key == 'si' or key == 'sf':
                    if not value:
                        print("Falta un elemento:")
                        errors = True
                        break
                if key == 'dir':
                    if not value:
                        print("Regla invalida")
                        errors = True
                        break
                    elif value not in dir_validate:
                        print("La dirección de las reglas no es la correcta\n")
                        # lector_texto()
                        errors = True
                        break
                elif key == 'ei':
                    if isinstance(value,list):
                        for j in value:
                            if j in same_symbol:
                                print("Es lista y es ~, ei")
                                # lector_texto()
                                errors = True
                                break
                    elif value == '~':
                        print("No es lista pero esta mal,ei")
                        # lector_texto()
                        errors = True
                        break

                elif key == 'si':
                    if isinstance(value,list):
                        for k in value:
                            if k in same_symbol:
                                print("Es lista y es ~,si")
                                # lector_texto()
                                errors = True
                                break
                    elif value == '~':
                        print("No es lista pero esta mal,si")
                        # lector_texto()
                        errors = True
                        break
        if errors:
            print("Intentelo de nuevo\n")
            continue
        break
    #=============================================================================================
    #=============================================================================================
    #==================================SOLICITUD USUARIO CADENA===================================
    # def user_string_input():
    #     user_string = input('Favor de introducir cadena: ')
    #     return user_string
    # user_string = '11+111'
    # print(f'Hi {user_string}')
    user_string = user_string_input()
    current_state = '00'
    # print(f'current state:{current_state}')                

    list_string = [n for n in user_string] + (['B'] * (len(user_string)*4))
    # print(list_string)
    # print(f'instructions:{new_rules}')
    pos = 0
    #================================================================================================
    #================================================================================================
    #=====================================MAQUINA DE TURING==========================================
    #================================================================================================
    def show(cinta, pos, state):
        exit = '╟'
        for i, c in enumerate(cinta):
            if i == pos:
                exit += f"[{c}]"
            else:
                exit += c
        print(f"Cinta: {exit} estado actual:{state}")

    while current_state not in estados_aceptacion:
        if list_string == []:
            print('Escribió cadena vacía, no hay procesamiento')
            break
        
        symbol = list_string[pos]
        apply_instruction = None

        for rule in new_rules:
            tipo = rule.get('tipo','N') #obtener tipo de isntrucción
            ei = rule['ei'] # estado inicial
            si = rule['si'] # simbolo inicial

            if isinstance(ei, list):
                if current_state in ei:
                    match_state = True
                else:
                    match_state = False

            else:
                if current_state == ei:
                    match_state = True
                else:
                    match_state = False

            if isinstance(si, list):
                if symbol in si:
                    match_symbol = True
                else:
                    match_symbol = False

            else:
                if symbol == si:
                    match_symbol = True
                else:
                    match_symbol = False

            if match_state and match_symbol:
                apply_instruction = rule
                break

        if not apply_instruction:
            print("No existen más instrucciones aplicables. Fin de la ejecución")
            break

        if isinstance(apply_instruction['si'],list):
            index = apply_instruction['si'].index(symbol)
        else:
            index = 0
        if isinstance(apply_instruction['sf'],list):
            sf = apply_instruction['sf'][index]
        else:
            sf = apply_instruction['sf']

        if isinstance(apply_instruction['ef'], list):
            ef = apply_instruction['ef'][index]
        else:
            ef = apply_instruction['ef']

        dir = apply_instruction['dir']

        print(f'estado actual:{current_state}')
        print(f'curent symbol:{symbol}')
        print(f'next state:{ef}')
        print(f'written symbol:{sf}')
        print(f'direction:{dir}')
        print(f'rule aplied: {apply_instruction}')

        list_string[pos] = sf
        current_state = ef
        #OJO; NO ESTOY SEGURO
        if pos <0 and dir == '<':
            print(f'ERROR: la cinta no es INFINITA! hacia la izquierda. Gracias')
            break

        if dir == '>':
            pos += 1
        elif dir == '<':
            pos -= 1
        elif dir == '!':
            pass

        show(list_string, pos, current_state)
        print("\nPresiona ENTER para continuar con el paso")
        while True:
            key = msvcrt.getch()
            if key == b'\r':
                break

        if apply_instruction['tipo'] != 'w' or apply_instruction['tipo'] != 'W':
            continue
        else:
            pass

    if current_state in estados_aceptacion:
        print("La cadena ha sido aceptada")
    else:
        print("La cadena ha sido rechazada")
    #================================================================================================
    #================================================================================================
while True:
    simuladorMTU()
    # user_string_input()
    reset = input("\n¿Desea reiniciar la simulación con otra cadena (S/N): ").strip()
    if reset != 'S':
        print("SIMULADOR DE MTU FINALIZADO")
        break