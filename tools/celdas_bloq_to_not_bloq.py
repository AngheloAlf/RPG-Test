def bloq_to_not_bloq(datos):
    datos = datos.split(';')

    datos = map(int,datos)

    output = []

    for i in range(264):
        if i not in datos:
            output.append(i)
    
    output = map(str,output)


    datos_out = output[0]

    for alf in output[1:]:
        datos_out += ';'+alf

    file_celdas = open('celdas_not_bloq.txt','w')
    file_celdas.write(datos_out)
    file_celdas.close()
    print datos_out
    return datos_out

if __name__ == '__main__':
    while True:
        datos = raw_input('Ingrese datos: ')
        bloq_to_not_bloq(datos)
