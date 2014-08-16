import pygame, sys, os, random, math, time
from pygame.locals import *
from functions_log_in import lista_personajes_cuenta
from functions_settings import *
from constants import *

aspect_ratio = get_settings_aspect_ratio()
debug_mode	 = get_settings_debug_mode()
language     = get_languange()
resolution   = get_settings_resolution()

def blit_selec_pers(pantalla,user):
	seleccion_personajes = pygame.image.load(os.path.join("media","menu","seleccion_personajes.png"))
	lista    		= []
	screenX 		= 0
	screenY 		= 0
	posx_character 	= 53
	posy_character 	= 173
	posx 			= 45
	posy 			= 140
	contador_fuente = 0
	if aspect_ratio=='2':
		screenX 		= 133
		posx_character  = 186
		posx 			= 178
		lateral 		= pygame.image.load(os.path.join("media","menu","lateral.png"))
		pantalla.blit(lateral,(0,0))
		pantalla.blit(lateral,(933,0))

	pantalla.blit(seleccion_personajes,(screenX,screenY))
	personajes_cuenta = lista_personajes_cuenta(user)
	
	for numerito in personajes_cuenta:
		file_personajes	= open('personajes.dat')
		for iteracion in file_personajes:
			cortada = iteracion.strip().split(';')
			if cortada[0] == '#id_personaje':
				continue
			if numerito == cortada[0]:
				lista.append(cortada[1])
		file_personajes.close()
		if numerito == '0':
			lista.append('0')
	for bliteamiento in lista:
		class_character = pygame.image.load(os.path.join("media","menu","class_"+bliteamiento+"_selection.png")).convert()
		class_character.set_colorkey((255,255,255))
		pantalla.blit(class_character,(posx_character,posy_character))
		posx_character += 144

	nombre_personajes = list()
	file_personajes   = open('personajes.dat')
	for linea in file_personajes:
		linea_cortada = linea.strip().split(';')
		if linea_cortada[0] == '#id_personaje':
			continue
		if linea_cortada[0] in personajes_cuenta:
			nombre_personajes.append(linea_cortada[2])
	file_personajes.close()

	for contador in range(5):
		contador_fuente +=1
		try:
			nombre_personaje_render = fuente.render(nombre_personajes[contador], True, (0,0,255))
			pantalla.blit(nombre_personaje_render,(posx,posy))
			posx += 145
			if contador_fuente%2==0:
				posy = 140
			else:
				posy = 482
		except:
			break

	return personajes_cuenta

def apretar_mouse_character_selector(mouspos,pantalla,class_selected,character_selected,personajes_cuenta):
	character_selector_menu = True
	character_creator_menu  = False
	datos_personaje 		= None
	juego_loop 				= False
	datos_mapa 				= None
	posicionX 				= None
	posicionY 				= None
	mouseposX				= 0
	mouseposY				= 0
	enemigos_bliteados 		= []

	if aspect_ratio == '2':
		mouseposX = 133

	if (646+mouseposX<mouspos[0]<794+mouseposX)and (5+mouseposY<mouspos[1]<41+mouseposY):
		character_selector_menu = False
		print language['lang_log_out']
	if (45+mouseposX<mouspos[0]<256+mouseposX)and (506+mouseposY<mouspos[1]<560+mouseposY):
		if '0' in personajes_cuenta:
			character_creator_menu = True
			blit_creac_pers(pantalla)
			blit_perso_selec_creacion(class_selected,pantalla)
		else:
			print language['lang_all_spaces_full']

	if (53+mouseposX<mouspos[0]<167+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[0]
		if personajes_cuenta[0] == '0':
			print language['lang_dont_have_char_in_space']
		else:
			print language['lang_you_choose']+' '+datos_personaje_seleccionado(character_selected)[2]
	if (197+mouseposX<mouspos[0]<311+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[1]
		if personajes_cuenta[1] == '0':
			print language['lang_dont_have_char_in_space']
		else:
			print language['lang_you_choose']+' '+datos_personaje_seleccionado(character_selected)[2]
	if (341+mouseposX<mouspos[0]<455+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[2]
		if personajes_cuenta[2] == '0':
			print language['lang_dont_have_char_in_space']
		else:
			print language['lang_you_choose']+' '+datos_personaje_seleccionado(character_selected)[2]
	if (485+mouseposX<mouspos[0]<599+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[3]
		if personajes_cuenta[3] == '0':
			print language['lang_dont_have_char_in_space']
		else:
			print language['lang_you_choose']+' '+datos_personaje_seleccionado(character_selected)[2]
	if (629+mouseposX<mouspos[0]<743+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[4]
		if personajes_cuenta[4] == '0':
			print language['lang_dont_have_char_in_space']
		else:
			print language['lang_you_choose']+' '+datos_personaje_seleccionado(character_selected)[2]

	if (626+mouseposX<mouspos[0]<794+mouseposX)and (560+mouseposY<mouspos[1]<594+mouseposY):
		if character_selected == '0':
			print language['lang_select_a_character']
		else:								#pass
			datos_personaje = datos_personaje_seleccionado(character_selected)
			juego_loop = True
			blit_hud_juego(pantalla)
			datos_mapa = blit_mapa(pantalla,datos_personaje[5])
			blit_laterales_mapas(pantalla,datos_mapa)
			blitear_datos_mapa(pantalla,datos_personaje[5],datos_mapa)
			posicionX,posicionY = blit_personaje_en_mapa(pantalla,datos_personaje[1],datos_personaje[6])
			if '280' in datos_mapa:
				enemigos_bliteados = blit_monster(pantalla,datos_mapa,posicionX,posicionY)
	return character_selector_menu,character_creator_menu,character_selected,datos_personaje,juego_loop,datos_mapa,posicionX,posicionY,enemigos_bliteados

def id_clases():
	lista_clases = []
	arch_clases = open('clases.dat')
	for linea in arch_clases:
		numero_clase = linea.strip().split(';')[0]
		if numero_clase == '#id_clase':
			continue
		lista_clases.append(numero_clase)
	arch_clases.close()
	return lista_clases

def blit_creac_pers(pantalla):
	screenX  = 0
	screenY  = 0
	posx     = 36
	posy     = 199
	contador = 0
	if aspect_ratio=='2':
		screenX = 133
		posx    = 169
		lateral 		= pygame.image.load(os.path.join("media","menu","lateral.png"))
		pantalla.blit(lateral,(0,0))
		pantalla.blit(lateral,(933,0))
	creacion_personaje 	= pygame.image.load(os.path.join("media","menu","creacion_personaje.png"))
	pantalla.blit(creacion_personaje,(screenX,screenY))
	lista_clases = id_clases()

	for bliteamiento in lista_clases:
		contador += 1
		class_icon	= pygame.image.load(os.path.join("media","menu","class_"+bliteamiento+"_icon.png")).convert()
		class_icon.set_colorkey((255,255,255))
		pantalla.blit(class_icon,(posx,posy))
		posx     += 59
		if contador == 4:
			posx -= 236
			posy = 258
		elif contador == 8:
			posx -= 236
			posy = 317
	return

def blit_perso_selec_creacion(class_selected,pantalla):
	screenX = 353
	screenY = 217
	if aspect_ratio == '2':
		screenX = 486
	blit_creac_pers(pantalla)
	character_class = pygame.image.load(os.path.join("media","menu","class_"+class_selected+"_selection.png")).convert()
	character_class.set_colorkey((255,255,255))
	pantalla.blit(character_class,(screenX,screenY))
	return

def apretar_mouse_character_creator(mouspos,pantalla,user,class_selected,lista_id_clases,personajes_cuenta):
	character_selector_menu = True
	character_creator_menu  = True
	mouseposX				= 0
	mouseposY				= 0
	Xnombre					= 0
	Ynombre 				= 0

	if aspect_ratio=='2':
		mouseposX = 133
		Xnombre   = 133

	if (5+mouseposX<mouspos[0]<103+mouseposX)and (5+mouseposY<mouspos[1]<49+mouseposY):
		character_creator_menu = False
		personajes_cuenta = blit_selec_pers(pantalla,user)

	if (646+mouseposX<mouspos[0]<794+mouseposX)and (5+mouseposY<mouspos[1]<41+mouseposY):
		character_selector_menu = False
		character_creator_menu  = False
		print language['lang_log_out']

	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[0]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[0]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[1]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[1]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[2]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[2]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[3]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[3]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[4]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[4]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[5]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[5]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[6]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[6]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[7]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[7]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[8]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[8]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[9]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[9]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[10]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[10]
		blit_perso_selec_creacion(class_selected,pantalla)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[11]=='0':
			print language['lang_class_dont_exist']
		class_selected = lista_id_clases[11]
		blit_perso_selec_creacion(class_selected,pantalla)

	elif (703+mouseposX<mouspos[0]<794+mouseposX)and (556+mouseposY<mouspos[1]<594+mouseposY):
		if class_selected == '0':
			print language['lang_select_a_class']
		elif '0' in personajes_cuenta:
			mensaje_nombre = pygame.image.load(os.path.join("media","menu","mensaje_nombre.png")).convert()
			mensaje_nombre.set_colorkey((255,255,255))
			pantalla.blit(mensaje_nombre,(Xnombre,Ynombre))
			pygame.display.flip()
			crear_personaje(user,class_selected)
			character_creator_menu = False
			personajes_cuenta = blit_selec_pers(pantalla,user)
		else:
			print language['lang_dont_have_free_spaces']

	return personajes_cuenta,class_selected,character_creator_menu,character_selector_menu

def crear_personaje(user,class_selected):
	file_personajes = open('personajes.dat')
	lista_nombres   = []
	for linea_personajes in file_personajes:
		if linea_personajes.split(';')[0] == '#id_personaje':
			continue
		id_personaje = linea_personajes.strip().split(';')[0]
		lista_nombres.append(linea_personajes.strip().split(';')[2])
	file_personajes.close()

	verificar_nombre     = True
	contador_verificador = 0
	nombre_personaje_creado = raw_input(language['lang_char_name']+': ')
	while verificar_nombre:
		contador_verificador += 1
		while nombre_personaje_creado in lista_nombres:
			nombre_personaje_creado = raw_input(language['lang_name_already_exist']+': ')
			contador_verificador = 0
		while  len(nombre_personaje_creado)>10:
			nombre_personaje_creado = raw_input(language['lang_name_too_long']+': ')
			contador_verificador = 0
		while  len(nombre_personaje_creado)<3:
			nombre_personaje_creado = raw_input(language['lang_name_too_short']+': ')
			contador_verificador = 0
		if contador_verificador == 5:
			verificar_nombre = False


	file_account = open('accounts.dat')
	for linea in file_account:
		datos_cuenta = linea.strip().split(';')
		if datos_cuenta[0]=='#id_cuenta':
			continue
		if user.lower() == datos_cuenta[1].lower():
			break
	file_account.close()

	file_personajes_escribir = open('personajes.dat','a')
	id_personaje = str(int(id_personaje)+1)
	escribir_personajes = id_personaje+';'+class_selected+';'+nombre_personaje_creado+';'+'1'+';'+'0'+';'+'0000'+';'+'080'+';'+'0'+'\n'
	file_personajes_escribir.write(escribir_personajes)
	file_personajes_escribir.close()

	personajes_de_la_cuenta = datos_cuenta[3].split(',')
	lista = []
	agregar = True
	for iteracion in personajes_de_la_cuenta:
		if iteracion == '0' and agregar:
			lista.append(id_personaje)
			agregar = False
		else:
			lista.append(iteracion)


	lista[4] = lista[4]+'\n'
	datos_cuenta[3] = ','.join(lista)
	datos_cuenta_modificados = ';'.join(datos_cuenta)

	file_accounts = open('accounts.dat')
	lista_accounts = []
	for linea_account in file_accounts:
		lista_accounts.append(linea_account)
	file_accounts.close()

	escribir_file_accounts = open('accounts.dat','w')
	for escribimiento in lista_accounts:
		alf = escribimiento.strip().split(';')
		if alf[1].lower() == user:
			escribir_file_accounts.write(datos_cuenta_modificados)
		else:
			escribir_file_accounts.write(escribimiento)
	escribir_file_accounts.close()
	return

def importar_imagenes(datos_imagenes,datos_personaje,datos_mapa):
	if datos_imagenes == None:
		print language['lang_loading_images']
		datos_imagenes = list()
		datos_lateral = list()
		# [hud,mapa_image,cuadricula,datos_lateral,cuadricula_lateral,personajerl,cerrar_x,estrella,bloqued,pausa,imagenes_enemigos,negro,blanco]
		hud     		   = pygame.image.load(os.path.join("media","juego","hud.png")).convert()
		mapa_image		   = pygame.image.load(os.path.join("media","mapas","mapa"+datos_personaje[5]+".png")).convert()
		cuadricula 		   = pygame.image.load(os.path.join("media","mapas","predef.png")).convert()
		cuadricula.set_colorkey((255,255,255))
		lateral			   = pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
		cuadricula_lateral = pygame.image.load(os.path.join("media","mapas","predef2.png")).convert()
		cuadricula_lateral.set_colorkey((255,255,255))

		if aspect_ratio == '2':
			if '272' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['272']+".png")).convert()
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '273' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['273']+".png")).convert()
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '270' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['270']+".png")).convert()
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '271' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['271']+".png")).convert()
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)

		personajerl = pygame.image.load(os.path.join("media","clases","class_"+datos_personaje[1]+".png")).convert()
		personajerl = pygame.transform.scale(personajerl,(30,60))
		personajerl.set_colorkey((255,255,255))

		cerrar_x = pygame.image.load(os.path.join("media","juego","salir.png")).convert()
		cerrar_x.set_colorkey((255,255,255))

		estrella = pygame.image.load(os.path.join("media","juego","estrella.png")).convert()
		estrella.set_colorkey((255,255,255))
		bloqued = pygame.image.load(os.path.join("media","juego","bloqued.png")).convert()
		bloqued.set_colorkey((255,255,255))

		pausa = pygame.image.load(os.path.join("media","juego","pausa.png")).convert()
		pausa.set_colorkey((255,255,255))

		imagenes_enemigos = list()
		if '280' in datos_mapa:
			lista_enemigos = datos_mapa['280'].strip().split(';')
			for id_enemigo in lista_enemigos:
				enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+id_enemigo+".png")).convert()
				enemigo.set_colorkey((255,255,255))
				imagenes_enemigos.append(enemigo)

		negro  = pygame.image.load(os.path.join("media","negro.png")).convert()
		blanco = pygame.image.load(os.path.join("media","blanco.png")).convert()
		

	else:
		pass
	return datos_imagenes

def blit_hud_juego(pantalla):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pre_def_hud = pygame.image.load(os.path.join("media","juego","hud.png")).convert()
	pantalla.blit(pre_def_hud,(screenX,screenY))
	return

def blit_laterales_mapas(pantalla,datos_mapa):
	cuadricula = pygame.image.load(os.path.join("media","mapas","predef2.png")).convert()
	cuadricula.set_colorkey((255,255,255))
	lateral 		= pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
	if aspect_ratio == '2':
		if '272' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['272']+".png")).convert()
			pantalla.blit(mapa_lateral,(-667,448))
			pantalla.blit(cuadricula,(-667,450))
		else:
			pantalla.blit(lateral,(0,448))
		if '273' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['273']+".png")).convert()
			pantalla.blit(mapa_lateral,(933,448))
			pantalla.blit(cuadricula,(933,450))
		else:
			pantalla.blit(lateral,(933,448))
		if '270' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['270']+".png")).convert()
			pantalla.blit(mapa_lateral,(-667,0))
			pantalla.blit(cuadricula,(-667,0))
		else:
			pantalla.blit(lateral,(0,0))
		if '271' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['271']+".png")).convert()
			pantalla.blit(mapa_lateral,(933,0))
			pantalla.blit(cuadricula,(933,0))
		else:
			pantalla.blit(lateral,(933,0))
		
	return

def blit_mapa(pantalla,mapa):
	try:
		mapa_image = pygame.image.load(os.path.join("media","mapas","mapa"+mapa+".png")).convert()
	except:
		mapa_image = pygame.image.load(os.path.join("media","mapas","mapa0000.png")).convert()
		mapa = '0000'

	datos_mapa      = dict()
	try:
		file_datos_mapa = open('media\mapas\mapa'+mapa+'.dat')
		for linea in file_datos_mapa:
			datos_mapa[linea.strip().split(' = ')[0]] = linea.strip().split(' = ')[1]
		file_datos_mapa.close()
	except:
		pass

	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133

	pantalla.blit(mapa_image,(screenX,screenY))
	cuadricula = pygame.image.load(os.path.join("media","mapas","predef.png")).convert()
	cuadricula.set_colorkey((255,255,255))
	pantalla.blit(cuadricula,(screenX,screenY))

	return datos_mapa

def datos_personaje_seleccionado(character_selected):
	file_personajes = open('personajes.dat')
	for linea in file_personajes:
		datos_personaje = linea.strip().split(';')
		if datos_personaje[0] == character_selected:
			break
	file_personajes.close()
	return datos_personaje

def get_celdas_pos(celda):
	posx = 10
	posy = -35
	contadorA = 0
	contadorB = 0
	for iteracion in range(264):
		if int(celda) == iteracion:
			break
		posx += 50
		if iteracion!=0:
			if iteracion%(15.0+(31.0*contadorA))==0:
				posx = 35
				posy += 25
				contadorA += 1
				continue
			elif iteracion%(30.0+(31.0*contadorB))==0:
				posx = 10
				posy +=25
				contadorB += 1
				continue
	return posx,posy

def get_celda_number(posx,posy):
	posicion_X   = 10
	posicion_Y   = 0
	posy         += 35
	contadorA    = 0
	contadorB    = 0
	problemas    = True
	celda_number = '0'
	if aspect_ratio == '2':
		posicion_X = 143
	for iteracion in range(264):
		#print iteracion,posicion_X,posx,posicion_Y,posy
		if posicion_X==posx and posicion_Y==posy:
			#datos_personaje[6] = str(iteracion)
			celda_number =  str(iteracion)
			problemas    = False
			break
		posicion_X += 50
		if iteracion != 0:
			if iteracion%(15.0+(31.0*contadorA))==0:
				#print posicion_X
				posicion_X -= 775
				posicion_Y += 25
				contadorA += 1
				continue
			elif iteracion%(30+(31.0*contadorB))==0:
				#print posicion_X
				posicion_X -= 775
				posicion_Y +=25
				contadorB += 1
				continue

	return celda_number,problemas

def blit_personaje_en_mapa(pantalla,clase,celda):
	personajerl = pygame.image.load(os.path.join("media","clases","class_"+clase+".png")).convert()
	personajerl = pygame.transform.scale(personajerl,(30,60))
	personajerl.set_colorkey((255,255,255))
	posx,posy = get_celdas_pos(celda)
	if aspect_ratio == '2':
		posx += 133
	pantalla.blit(personajerl,(posx,posy))
	return posx,posy

def apretar_mouse_juego_loop(mouspos):
	return

def mover_personaje(pantalla,clase,posx,posy,direX,direY,mapa,datos_mapa,datos_personaje,enemigos_bliteados):
	if aspect_ratio == '2':
		if posx+direX<143 or posy+direY<-35 or posx+direX>893 or posy+direY>365:
			return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,False,None
	else:
		if posx+direX<10 or posy+direY<-35 or posx+direX>760 or posy+direY>365:
			return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,False,None

	celdas_bloquedas = []
	for celdas_mapa in datos_mapa:
	 	if celdas_mapa=='265':
	 		celdas_bloquedas = datos_mapa[celdas_mapa].strip().split(';')

	celda_number = get_celda_number(posx+direX,posy+direY)[0]
	if celda_number in celdas_bloquedas:
		return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,False,None

	if debug_mode:
	 	print language['lang_cell']+': '+celda_number
	 	print 'posx:',posx+direX,' posy:',posy+direY

	#subpantalla = pantalla.subsurface(posx,posy,30,60)
	#pantalla.blit(subpantalla,(posx,posy))
	blit_mapa(pantalla,mapa)
	blitear_datos_mapa(pantalla,mapa,datos_mapa)
	posx 		 += direX
	posy 		 += direY
	celda_number = get_celda_number(posx,posy)[0]
	reblit_monster(pantalla,enemigos_bliteados)
	blit_personaje_en_mapa(pantalla,clase,celda_number)
	pygame.display.flip()
	colision_pj_mob,info_enemigo = colision_jugador_monster(posx,posy,enemigos_bliteados)
	if colision_pj_mob and debug_mode:
		print language['lang_pj_mob_same_cell']
	if colision_pj_mob == False:
		datos_personaje,datos_mapa,posx,posy,enemigos_bliteados = cambiar_mapa(pantalla,posx,posy,datos_mapa,datos_personaje,enemigos_bliteados)
	return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo

def bliteo_salir_x(pantalla):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pop_up  = pygame.image.load(os.path.join("media","juego","salir.png")).convert()
	pop_up.set_colorkey((255,255,255))
	pantalla.blit(pop_up,(screenX,screenY))
	return

def guardar_datos_personaje(datos_personaje,posx,posy):
	print language['lang_saving_data']

	datos_personaje[6],problemas = get_celda_number(posx,posy)
	datos_personaje[6] = str(datos_personaje[6])
	lista = []

	file_personajes = open('personajes.dat')
	for linea_personajes in file_personajes:
		if linea_personajes.strip().split(';')[0] != datos_personaje[0]:
			lista.append(linea_personajes)
		else:
			valor = datos_personaje[0]+';'+datos_personaje[1]+';'+datos_personaje[2]+';'+datos_personaje[3]+';'+datos_personaje[4]+';'+datos_personaje[5]+';'+datos_personaje[6]+';'+datos_personaje[7]+'\n'
			lista.append(valor)
	file_personajes.close()

	try:
		valor += '1'
	except:
		problemas = True

	file_personajes_escribir = open('personajes.dat','w')
	for escribir in lista:
		try:
			file_personajes_escribir.write(escribir)
		except:
			problemas = True
	file_personajes_escribir.close()

	if problemas:
		print language['lang_saving_error']
	else:
		print language['lang_saving_successful']
	return

def blitear_datos_mapa(pantalla,mapa,datos_mapa):
	for celdas in datos_mapa:
		if celdas<='264':
			posx,posy = get_celdas_pos(celdas)
			if aspect_ratio == '2':
				posx += 133
			estrella  = pygame.image.load(os.path.join("media","juego","estrella.png")).convert()
			estrella.set_colorkey((255,255,255))
			pantalla.blit(estrella,(posx,posy))

		if debug_mode:
			## blitear reestricciones de movimiento	
			if celdas=='265':
				celdas_bloquedas = datos_mapa[celdas].strip().split(';')
				bloqued = pygame.image.load(os.path.join("media","juego","bloqued.png")).convert()
				bloqued.set_colorkey((255,255,255))
				for n_celda_bloqueda in celdas_bloquedas:
					posx,posy = get_celdas_pos(n_celda_bloqueda)
					if aspect_ratio == '2':
						posx += 133
					pantalla.blit(bloqued,(posx,posy))
	return

def blit_pausa(pantalla):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pausa   = pygame.image.load(os.path.join("media","juego","pausa.png")).convert()
	pausa.set_colorkey((255,255,255))
	pantalla.blit(pausa,(screenX,screenY))
	return

def apretar_mouse_pausa(mouspos,pantalla,datos_personaje,posicionX,posicionY,direX,direY,datos_mapa,user,personajes_cuenta,enemigos_bliteados):
	pausa 	   				= True
	juego_loop 				= True
	character_selector_menu = True
	mouseposX = 0
	mouseposY = 0
	if aspect_ratio == '2':
		mouseposX = 133
	if (285+mouseposX<mouspos[0]<513+mouseposX) and (121+mouseposY<mouspos[1]<163+mouseposY): #reanudar
		posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,0,0,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)							
		pausa = False
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (168+mouseposY<mouspos[1]<210+mouseposY): #guardar datos
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,0,0,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)							
		pausa = False
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (213+mouseposY<mouspos[1]<255+mouseposY): #opciones
		pass
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (258+mouseposY<mouspos[1]<292+mouseposY): #cambiar de personajes
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		personajes_cuenta = blit_selec_pers(pantalla,user)
		juego_loop 				= False
		pausa 					= False 
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (298+mouseposY<mouspos[1]<336+mouseposY): #salir
		print language['lang_log_out']
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		character_selector_menu = False
		juego_loop 				= False
		pausa 					= False 
		pygame.display.flip()

	return posicionX,posicionY,datos_personaje,datos_mapa,pausa,personajes_cuenta,juego_loop,character_selector_menu

def while_cerrar(eventos_pygame,mouse_apretado,mouspos,pantalla,datos_personaje,posx,posy,direX,direY,pausa,datos_mapa,enemigos_bliteados,pelea):
	character_selector_menu = True
	juego_loop 				= True
	cerrar 					= True

	mouseposX = 0
	mouseposY = 0
	if aspect_ratio == '2':
		mouseposX = 133
	for event in eventos_pygame:
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mouse_apretado[0]==True:
				if (220+mouseposX<mouspos[0]<343+mouseposX)and (210+mouseposY<mouspos[1]<320+mouseposY):
					print language['lang_log_out']
					guardar_datos_personaje(datos_personaje,posx,posy)
					character_selector_menu = False
					juego_loop 				= False
					cerrar 					= False
					pausa 					= False
					pelea 					= False
					return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea
				elif (441+mouseposX<mouspos[0]<580+mouseposX)and (209+mouseposY<mouspos[1]<320+mouseposY):
					cerrar = False
					pausa  = False
					posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posx,posy,0,0,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
					return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea
		elif event.type == pygame.KEYDOWN: ##apretar boton
			if event.key == pygame.K_ESCAPE: 
				cerrar = False
				posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posx,posy,0,0,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
				return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea
	return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea 

def cambiar_mapa(pantalla,posicionX,posicionY,datos_mapa,datos_personaje,enemigos_bliteados):
	#print datos_mapa
	for celdas in datos_mapa:
		if celdas<='264':
			posx,posy = get_celdas_pos(celdas)
			if aspect_ratio == '2':
				posx += 133
			#print posicionX,posx,posicionY,posy
			if posicionX == posx and posicionY == posy:
				print language['lang_loading_map']
				time.sleep(0.5)
				datos_celda			= datos_mapa[celdas].split(';')
				nueva_celda         = datos_celda[1]
				datos_personaje[5]  = datos_celda[0]
				if debug_mode:
					print language['lang_map']+': '+datos_personaje[5]
				datos_mapa          = blit_mapa(pantalla,datos_personaje[5])
				blit_laterales_mapas(pantalla,datos_mapa)
				blitear_datos_mapa(pantalla,datos_personaje[5],datos_mapa)
				posicionX,posicionY = blit_personaje_en_mapa(pantalla,datos_personaje[1],nueva_celda)
				if '280' in datos_mapa:
					enemigos_bliteados = blit_monster(pantalla,datos_mapa,posicionX,posicionY)
				else:
					enemigos_bliteados = []
				return datos_personaje,datos_mapa,posicionX,posicionY,enemigos_bliteados
	return datos_personaje,datos_mapa,posicionX,posicionY,enemigos_bliteados

def blit_cargando(pantalla): #terminar
	screenX = 25
	screenY = 25
	if aspect_ratio == '2':
		screenX = 158
	loading = pygame.image.load(os.path.join("media","juego","loading.png")).convert()
	loading.set_colorkey((255,255,255))
	pantalla.blit(loading,(screenX,screenY))
	pygame.display.flip()
	return

def blit_monster(pantalla,datos_mapa,posicionX,posicionY):
	enemigos_bliteados = []
	celdas_bloquedas   = []
	celda_jugador = get_celda_number(posicionX,posicionY)[0]
	if '265' in datos_mapa:
		celdas_bloquedas = datos_mapa['265'].strip().split(';')
	for celdas_caminables in range(264):
		restriccion_1 = map(int,datos_mapa.keys())
		restriccion_2 = str(celdas_caminables)
		if celdas_caminables not in restriccion_1 or restriccion_2 not in datos_mapa:
			continue
		celdas_caminables = str(celdas_caminables)
		celdas_bloquedas.append(celdas_caminables)
		celda_aparicion = datos_mapa[celdas_caminables].strip().split(';')[1]
		celdas_bloquedas.append(celda_aparicion)
	celdas_bloquedas.append(celda_jugador)
	lista_enemigos = datos_mapa['280'].strip().split(';')
	for id_enemigo in lista_enemigos:
		try:
			celda_enemigo = str(random.randint(0,263))
			while celda_enemigo in celdas_bloquedas:
				if debug_mode:
					print language['lang_bloqued_cell']+': '+celda_enemigo
				celda_enemigo = str(random.randint(0,263))
			if debug_mode:
				print language['lang_enemy_cell']+': '+celda_enemigo
			posx,posy = get_celdas_pos(celda_enemigo)
			if aspect_ratio == '2':
				posx += 133
			enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+id_enemigo+".png")).convert()
			enemigo.set_colorkey((255,255,255))
			pantalla.blit(enemigo,(posx,posy))
			enemigos_bliteados.append((celda_enemigo,id_enemigo))
			celdas_bloquedas.append(celda_enemigo)
		except:
			pass
	if debug_mode:
		print language['lang_blitted_mobs']+': '+enemigos_bliteados
	return enemigos_bliteados

def reblit_monster(pantalla,enemigos_bliteados):
	for celda_enemigo,id_enemigo in enemigos_bliteados:
		posx,posy = get_celdas_pos(celda_enemigo)
		if aspect_ratio == '2':
			posx += 133
		enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+id_enemigo+".png")).convert()
		enemigo.set_colorkey((255,255,255))
		pantalla.blit(enemigo,(posx,posy))
	return

def mover_monster(pantalla,enemigos_bliteados,datos_mapa): 
	if enemigos_bliteados == []:
		return enemigos_bliteados
	enemigo_mover = random.choice(enemigos_bliteados)
	enemigos_bliteados_index = enemigos_bliteados.index(enemigo_mover)
	celda_enemigo = int(enemigo_mover[0])
	celdas_caminables = [celda_enemigo-16,celda_enemigo-15,celda_enemigo+15,celda_enemigo+16]
	cel_cam 		  = [celda_enemigo-16,celda_enemigo-15,celda_enemigo+15,celda_enemigo+16]
	if '265' in datos_mapa:
		celdas_bloquedas = datos_mapa['265'].split(';')
		celdas_bloquedas = map(int,celdas_bloquedas)
	for celda_camin in cel_cam:
		if '265' in datos_mapa:
			if celda_camin in celdas_bloquedas:
				celdas_caminables.remove(celda_camin)
				continue
		if celda_camin > 263 or celda_camin < 0:
			celdas_caminables.remove(celda_camin)
	celdas_caminables = map(str,celdas_caminables)
	for mob in enemigos_bliteados:
		if mob == enemigo_mover:
			continue
		if mob[0] in celdas_caminables:
			celdas_caminables.remove(mob[0])

	if celdas_caminables == []:
		return enemigos_bliteados
	nueva_celda_enemigo = random.choice(celdas_caminables)
	enemigo_mover = (nueva_celda_enemigo,enemigo_mover[1])
	enemigos_bliteados[enemigos_bliteados_index] = enemigo_mover
	return enemigos_bliteados

def colision_jugador_monster(posx,posy,enemigos_bliteados):
	celda_jugador = get_celda_number(posx,posy)[0]
	for enemigo in enemigos_bliteados:
		if celda_jugador == enemigo[0]:
			return True,enemigo
	return False,None

def animacion_pantalla(pantalla,mapa,screenX,screenY,clase,info_enemigo,datos_mapa,animacion_number):
	#animacion_number = 2
	try:
		mapa_image = pygame.image.load(os.path.join("media","mapas","mapa"+mapa+".png")).convert()
	except:
		mapa_image = pygame.image.load(os.path.join("media","mapas","mapa0000.png")).convert()
		mapa = '0000'

	datos_mapa      = dict()
	try:
		file_datos_mapa = open('media\mapas\mapa'+mapa+'.dat')
		for linea in file_datos_mapa:
			datos_mapa[linea.strip().split(' = ')[0]] = linea.strip().split(' = ')[1]
		file_datos_mapa.close()
	except:
		pass

	negro = pygame.image.load(os.path.join("media","negro.png")).convert()
	pantalla.blit(negro,(0,0))

	if animacion_number == 1:
		if aspect_ratio == '2':
			screenY += 18
		else:
			screenY += 11

	elif animacion_number == 2:
		screenX -= 16
		if aspect_ratio == '2':
			screenY += 18
		else:
			screenY += 10

	if aspect_ratio == '2':
		pantalla.blit(negro,(600,0))
		cuadricula_lateral = pygame.image.load(os.path.join("media","mapas","predef2.png")).convert()
		cuadricula_lateral.set_colorkey((255,255,255))
		lateral 		= pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
		if '272' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['272']+".png")).convert()
			pantalla.blit(mapa_lateral,(-800+screenX,448+screenY))
			pantalla.blit(cuadricula_lateral,(-800+screenX,450+screenY))
		else:
			pantalla.blit(lateral,(-133+screenX,448+screenY))
		if '273' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['273']+".png")).convert()
			pantalla.blit(mapa_lateral,(800+screenX,448+screenY))
			pantalla.blit(cuadricula_lateral,(800+screenX,450+screenY))
		else:
			pantalla.blit(lateral,(800+screenX,448+screenY))
		if '270' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['270']+".png")).convert()
			pantalla.blit(mapa_lateral,(-800+screenX,0+screenY))
			pantalla.blit(cuadricula_lateral,(-800+screenX,0+screenY))
		else:
			pantalla.blit(lateral,(-133+screenX,0+screenY))
		if '271' in  datos_mapa:
			mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['271']+".png")).convert()
			pantalla.blit(mapa_lateral,(800+screenX,0+screenY))
			pantalla.blit(cuadricula_lateral,(800+screenX,0+screenY))
		else:
			pantalla.blit(lateral,(800+screenX,0+screenY))

	pre_def_hud = pygame.image.load(os.path.join("media","juego","hud.png")).convert()
	pre_def_hud.set_colorkey((255,255,255))
	pantalla.blit(pre_def_hud,(screenX,screenY))

	pantalla.blit(mapa_image,(screenX,screenY))
	cuadricula = pygame.image.load(os.path.join("media","mapas","predef.png")).convert()
	cuadricula.set_colorkey((255,255,255))
	pantalla.blit(cuadricula,(screenX,screenY))

	personajerl = pygame.image.load(os.path.join("media","clases","class_"+clase+".png")).convert()
	personajerl = pygame.transform.scale(personajerl,(30,60))
	personajerl.set_colorkey((255,255,255))
	enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+info_enemigo[1]+".png")).convert()
	enemigo.set_colorkey((255,255,255))
	posx,posy = get_celdas_pos(info_enemigo[0])
	posx += screenX
	posy += screenY
	pantalla.blit(enemigo,(posx,posy))
	pantalla.blit(personajerl,(posx,posy))

	if screenY > 600:
		if aspect_ratio == '2':
			return 133,0,False,0
		return 0,0,False,0

	return screenX,screenY,True,animacion_number

def blit_pj_mob_en_pelea(pantalla,datos_mapa,info_enemigo,datos_personaje):
	celdas_peleas = datos_mapa['266'].strip().split(';')

	celda_pj = random.choice(celdas_peleas)
	posx_pj,posy_pj = get_celdas_pos(celda_pj)
	celdas_peleas.remove(celda_pj)
	personajerl = pygame.image.load(os.path.join("media","clases","class_"+datos_personaje[1]+".png")).convert()
	personajerl = pygame.transform.scale(personajerl,(30,60))
	personajerl.set_colorkey((255,255,255))

	celda_mob = random.choice(celdas_peleas)
	posx_mob,posy_mob = get_celdas_pos(celda_mob)
	enemigorl = pygame.image.load(os.path.join("media","monsters","monster"+info_enemigo[1]+".png")).convert()
	enemigorl.set_colorkey((255,255,255))

	if aspect_ratio == '2':
		posx_pj  += 133
		posx_mob += 133
	pantalla.blit(personajerl,(posx_pj,posy_pj))
	pantalla.blit(enemigorl,(posx_mob,posy_mob))
	return celda_pj,celda_mob

def apretar_mouse_pelea(mouspos):
	return

def mover_pj_en_pelea(pantalla,posx_pj,posy_pj,direX,direY,datos_personaje,datos_mapa,celda_mob_pelea,id_mob):
	if aspect_ratio == '2':
		posx_pj += 133
	celda_jugador = get_celda_number(posx_pj,posy_pj)[0]
	if aspect_ratio == '2':
		if posx_pj+direX<143 or posy_pj+direY<-35 or posx_pj+direX>893 or posy_pj+direY>365:
			return celda_jugador
	else:
		if posx_pj+direX<10 or posy_pj+direY<-35 or posx_pj+direX>760 or posy_pj+direY>365:
			return celda_jugador

	celdas_bloquedas = []
	for celdas_mapa in datos_mapa:
	 	if celdas_mapa=='265':
	 		celdas_bloquedas = datos_mapa[celdas_mapa].strip().split(';')

	celda_number = get_celda_number(posx_pj+direX,posy_pj+direY)[0]
	if celda_number in celdas_bloquedas:
		return celda_jugador

	if aspect_ratio == '2':
		blit_laterales_mapas(pantalla,datos_mapa)
	posx_pj += direX
	posy_pj += direY

	if debug_mode:
	 	print language['lang_cell']+': '+get_celda_number(posx_pj,posy_pj)[0]
	 	print 'posx:',posx_pj,' posy:',posy_pj

	personajerl = pygame.image.load(os.path.join("media","clases","class_"+datos_personaje[1]+".png")).convert()
	personajerl = pygame.transform.scale(personajerl,(30,60))
	personajerl.set_colorkey((255,255,255))
	blit_mapa(pantalla,datos_personaje[5])

	info_enemigo = (celda_mob_pelea,id_mob)
	reblit_monster(pantalla,[info_enemigo])
	pantalla.blit(personajerl,(posx_pj,posy_pj))
	pygame.display.flip()

	celda_jugador = get_celda_number(posx_pj,posy_pj)[0]
	return celda_jugador
