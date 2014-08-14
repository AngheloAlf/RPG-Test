def verificar_usuario_clave(user,password):
	file_users = open('accounts.dat')
	for linea in file_users:
		datos = linea.strip().split(';')
		if datos[0]=='#id_cuenta':
			continue
		if user.lower() == datos[1].lower():
			if password == datos[2]:
				file_users.close()
				return True
	file_users.close()
	return False

def verificar_password(password,password2):
	if password==password2:
		return False
	return True

def revisar_existencia_usuario(user):
	file_users = open('accounts.dat')
	for linea in file_users:
		datos = linea.strip().split(';')
		if datos[0]=='#id_cuenta':
			continue
		if user.lower() == datos[1].lower():
			file_users.close()
			return True
	file_users.close()
	return False

def agregar_usuario(datos):
	file_users = open('accounts.dat')
	for linea in file_users:
		id_user = linea.split(';')[0]
	file_users.close()

	add_user = open('accounts.dat','a')
	escribir = str(int(id_user)+1)+';'+datos[0]+';'+datos[1]+';'+'0,0,0,0,0'+'\n'
	add_user.write(escribir)
	add_user.close()
	return

def lista_personajes_cuenta(user):
	file_users = open('accounts.dat')
	#personajes = ['0','0','0','0','0']
	for linea in file_users:
		linea_cortada = linea.strip().split(';')
		if linea_cortada[0]=='#id_cuenta':
			continue
		if user.lower() == linea_cortada[1].lower():
			personajes = linea_cortada[3].split(',')
			break
	file_users.close()
	return personajes
