import pygame, sys, os, random, math, time
from pygame.locals import *
from functions_log_in import *
from functions_settings import *
from constants import *

aspect_ratio  	= get_settings_aspect_ratio()
debug_mode		= get_settings_debug_mode()
language 		= get_languange()
resolution  	= get_settings_resolution()
mult_resolution = get_multiplicator_resolution()
FPS 		    = get_settings_FPS()

def procesar_idioma(palabra='Error',fuente_procesar=None,color=(0,0,255)):
	if fuente_procesar == None:
		try:
			print language[palabra]
		except:
			print palabra
		return None
	else:
		try:
			return fuente_procesar.render(language[palabra], True, color)
		except:
			palabra = '_'.join(palabra.split('_')[1:])
			return fuente_procesar.render(palabra, True, color)
	return None

def importar_menus():
	procesar_idioma('lang_loading_menus')
	menus = []
	lateral 		     = pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
	lateral              = pygame.transform.scale(lateral,(int(133*mult_resolution),int(600*mult_resolution)))
	img_iniciar_sesion   = pygame.image.load(os.path.join("media","menu","iniciar_sesion.png")).convert()
	img_iniciar_sesion   = pygame.transform.scale(img_iniciar_sesion,(int(800*mult_resolution),int(600*mult_resolution)))
	seleccion_personajes = pygame.image.load(os.path.join("media","menu","seleccion_personajes.png")).convert()
	seleccion_personajes = pygame.transform.scale(seleccion_personajes,(int(800*mult_resolution),int(600*mult_resolution)))
	creacion_personaje 	 = pygame.image.load(os.path.join("media","menu","creacion_personaje.png")).convert()
	creacion_personaje   = pygame.transform.scale(creacion_personaje,(int(800*mult_resolution),int(600*mult_resolution)))
	mensaje_nombre       = pygame.image.load(os.path.join("media","menu","mensaje_nombre.png")).convert()
	mensaje_nombre 		 = pygame.transform.scale(mensaje_nombre,(int(800*mult_resolution),int(600*mult_resolution)))
	mensaje_nombre.set_colorkey((255,255,255))
	crear_cuenta 		 = pygame.image.load(os.path.join("media","menu","crear_cuenta.png")).convert()
	crear_cuenta 		 = pygame.transform.scale(crear_cuenta,(int(800*mult_resolution),int(600*mult_resolution)))
	menus = [lateral,img_iniciar_sesion,seleccion_personajes,creacion_personaje,mensaje_nombre,crear_cuenta]
	return menus

def blit_iniciar_sesion(pantalla,menus):
	screenX 			 = 0
	screenY 			 = 0
	if aspect_ratio=='2':
		screenX 		= 133
		pantalla.blit(menus[0],(0,0))
		pantalla.blit(menus[0],(933,0))
	pantalla.blit(menus[1],(screenX,screenY))
	pantalla.blit(procesar_idioma('lang_username',fuente,(153,217,234)),(219+screenX,242+screenY))
	pantalla.blit(procesar_idioma('lang_password',fuente,(153,217,234)),(219+screenX,277+screenY))
	pantalla.blit(procesar_idioma('lang_log_in',fuente_botones),(310+screenX,310+screenY))
	pantalla.blit(procesar_idioma('lang_sign_in',fuente_botones),(310+screenX,356+screenY))
	pantalla.blit(procesar_idioma('lang_welcome',fuente_titulo),(218+screenX,47+screenY))
	return

def blit_crear_cuenta(pantalla,menus):
	screenX 			 = 0
	screenY 			 = 0
	if aspect_ratio=='2':
		screenX 		= 133
		pantalla.blit(menus[0],(0,0))
		pantalla.blit(menus[0],(933,0))
	pantalla.blit(menus[5],(screenX,screenY))
	pantalla.blit(procesar_idioma('lang_username',fuente,(153,217,234)),(219+screenX,215+screenY))
	pantalla.blit(procesar_idioma('lang_password',fuente,(153,217,234)),(219+screenX,251+screenY))
	pantalla.blit(procesar_idioma('lang_password2',fuente,(153,217,234)),(219+screenX,285+screenY))
	pantalla.blit(procesar_idioma('lang_sign_in',fuente_botones),(310+screenX,330+screenY))
	pantalla.blit(procesar_idioma('lang_cancel',fuente_botones),(310+screenX,376+screenY))
	return

def apretar_mouse_crear_cuenta(pantalla,mouspos,menus,creac_user,creac_password,creac_password2):
	crear_cuenta = True
	mouseposX    = 0
	mouseposY    = 0
	sesion_iniciada = False
	if aspect_ratio == '2':
		mouseposX = 133
	if (323+mouseposX<=mouspos[0]<=573+mouseposX) and (211+mouseposY<=mouspos[1]<=234+mouseposY):
		creac_user = escribir_user_pass(pantalla,'crear_cuenta','user',menus,creac_password,creac_password2)
	if (323+mouseposX<=mouspos[0]<=573+mouseposX) and (246+mouseposY<=mouspos[1]<=269+mouseposY):
		creac_password = escribir_user_pass(pantalla,'crear_cuenta','password',menus,creac_password2,creac_user)
	if (323+mouseposX<=mouspos[0]<=573+mouseposX) and (281+mouseposY<=mouspos[1]<=304+mouseposY):
		creac_password2 = escribir_user_pass(pantalla,'crear_cuenta','password2',menus,creac_password,creac_user)
	if (291+mouseposX<=mouspos[0]<=510+mouseposX) and (325+mouseposY<=mouspos[1]<=368+mouseposY):
		if revisar_existencia_usuario(creac_user) and len(creac_user) != 0:
			if verificar_password(creac_password,creac_password2) and len(creac_password) != 0:
				datos = [creac_user,creac_password]
				agregar_usuario(datos)
				procesar_idioma('lang_make_account_successful')
				crear_cuenta = False
			else:
				pantalla.blit(procesar_idioma('lang_pass_error',fuente),(175+mouseposX,100+mouseposY))
		else:
			pantalla.blit(procesar_idioma('lang_user_already_exist',fuente),(200+mouseposX,100+mouseposY))
	if (291+mouseposX<=mouspos[0]<=510+mouseposX) and (372+mouseposY<=mouspos[1]<=415+mouseposY):
		crear_cuenta = False
	return crear_cuenta,creac_user,creac_password,creac_password2

def escribir_en_pantalla(nombre_personaje_creado,maximo_nombre):
	escribiendo = True
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_RETURN:
				escribiendo = False
			elif event.key == pygame.K_BACKSPACE:
				if nombre_personaje_creado != '':
					nombre_personaje_creado = nombre_personaje_creado[:-1]
			if len(nombre_personaje_creado) <= maximo_nombre:
				if event.key == pygame.K_0 or event.key == pygame.K_KP0:
					nombre_personaje_creado += '0'
				elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
					nombre_personaje_creado += '1'
				elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
					nombre_personaje_creado += '2'
				elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
					nombre_personaje_creado += '3'
				elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
					nombre_personaje_creado += '4'
				elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
					nombre_personaje_creado += '5'
				elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
					nombre_personaje_creado += '6'
				elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
					nombre_personaje_creado += '7'
				elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
					nombre_personaje_creado += '8'
				elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
					nombre_personaje_creado += '9'
				mods = pygame.key.get_mods()
				if (mods & KMOD_CAPS) or (mods & KMOD_LSHIFT) or (mods & KMOD_RSHIFT): 
					if event.key == pygame.K_q:
						nombre_personaje_creado += 'Q'
					elif event.key == pygame.K_w:
						nombre_personaje_creado += 'W'
					elif event.key == pygame.K_e:
						nombre_personaje_creado += 'E'
					elif event.key == pygame.K_r:
						nombre_personaje_creado += 'R'
					elif event.key == pygame.K_t:
						nombre_personaje_creado += 'T'
					elif event.key == pygame.K_y:
						nombre_personaje_creado += 'Y'
					elif event.key == pygame.K_u:
						nombre_personaje_creado += 'U'
					elif event.key == pygame.K_i:
						nombre_personaje_creado += 'I'
					elif event.key == pygame.K_o:
						nombre_personaje_creado += 'O'
					elif event.key == pygame.K_p:
						nombre_personaje_creado += 'P'
					elif event.key == pygame.K_a:
						nombre_personaje_creado += 'A'
					elif event.key == pygame.K_s:
						nombre_personaje_creado += 'S'
					elif event.key == pygame.K_d:
						nombre_personaje_creado += 'D'
					elif event.key == pygame.K_f:
						nombre_personaje_creado += 'F'
					elif event.key == pygame.K_g:
						nombre_personaje_creado += 'G'
					elif event.key == pygame.K_h:
						nombre_personaje_creado += 'H'
					elif event.key == pygame.K_j:
						nombre_personaje_creado += 'J'
					elif event.key == pygame.K_k:
						nombre_personaje_creado += 'K'
					elif event.key == pygame.K_l:
						nombre_personaje_creado += 'L'
					elif event.key == pygame.K_z:
						nombre_personaje_creado += 'Z'
					elif event.key == pygame.K_x:
						nombre_personaje_creado += 'X'
					elif event.key == pygame.K_c:
						nombre_personaje_creado += 'C'
					elif event.key == pygame.K_v:
						nombre_personaje_creado += 'V'
					elif event.key == pygame.K_b:
						nombre_personaje_creado += 'B'
					elif event.key == pygame.K_n:
						nombre_personaje_creado += 'N'
					elif event.key == pygame.K_m:
						nombre_personaje_creado += 'M'
				else:
					if event.key == pygame.K_q:
						nombre_personaje_creado += 'q'
					elif event.key == pygame.K_w:
						nombre_personaje_creado += 'w'
					elif event.key == pygame.K_e:
						nombre_personaje_creado += 'e'
					elif event.key == pygame.K_r:
						nombre_personaje_creado += 'r'
					elif event.key == pygame.K_t:
						nombre_personaje_creado += 't'
					elif event.key == pygame.K_y:
						nombre_personaje_creado += 'y'
					elif event.key == pygame.K_u:
						nombre_personaje_creado += 'u'
					elif event.key == pygame.K_i:
						nombre_personaje_creado += 'i'
					elif event.key == pygame.K_o:
						nombre_personaje_creado += 'o'
					elif event.key == pygame.K_p:
						nombre_personaje_creado += 'p'
					elif event.key == pygame.K_a:
						nombre_personaje_creado += 'a'
					elif event.key == pygame.K_s:
						nombre_personaje_creado += 's'
					elif event.key == pygame.K_d:
						nombre_personaje_creado += 'd'
					elif event.key == pygame.K_f:
						nombre_personaje_creado += 'f'
					elif event.key == pygame.K_g:
						nombre_personaje_creado += 'g'
					elif event.key == pygame.K_h:
						nombre_personaje_creado += 'h'
					elif event.key == pygame.K_j:
						nombre_personaje_creado += 'j'
					elif event.key == pygame.K_k:
						nombre_personaje_creado += 'k'
					elif event.key == pygame.K_l:
						nombre_personaje_creado += 'l'
					elif event.key == pygame.K_z:
						nombre_personaje_creado += 'z'
					elif event.key == pygame.K_x:
						nombre_personaje_creado += 'x'
					elif event.key == pygame.K_c:
						nombre_personaje_creado += 'c'
					elif event.key == pygame.K_v:
						nombre_personaje_creado += 'v'
					elif event.key == pygame.K_b:
						nombre_personaje_creado += 'b'
					elif event.key == pygame.K_n:
						nombre_personaje_creado += 'n'
					elif event.key == pygame.K_m:
						nombre_personaje_creado += 'm'
				if event.key == pygame.K_SPACE:
					nombre_personaje_creado += ' '
				elif event.key == pygame.K_PERIOD:
					nombre_personaje_creado += '.'
	return nombre_personaje_creado,escribiendo

def escribir_user_pass(pantalla,estado,variable,menus,variable1,variable2=None):
	nombre_personaje_creado = ''
	alf = ''
	if estado == 'iniciar_sesion':
		if variable == 'user':
			posx = 330
			posy = 245
			posx_variable1 = 330
			posy_variable1 = 279
			for i in range(len(variable1)):
				alf += '*'
			variable1_render = fuente_pequena.render(alf, True, (0,0,255))
		elif variable == 'password':
			posx = 330
			posy = 279
			posx_variable1 = 330
			posy_variable1 = 245
			variable1_render = fuente_pequena.render(variable1, True, (0,0,255))
	elif estado == 'crear_cuenta':
		if variable == 'user':
			posx = 330
			posy = 218
			posx_variable1 = 330
			posy_variable1 = 253
			posx_variable2 = 330
			posy_variable2 = 288
			for i in range(len(variable1)):
				alf += '*'
			variable1_render = fuente_pequena.render(alf, True, (0,0,255))
			alf = ''
			for j in range(len(variable2)):
				alf += '*'
			variable2_render = fuente_pequena.render(alf, True, (0,0,255))
		elif variable == 'password':
			posx = 330
			posy = 253
			posx_variable1 = 330
			posy_variable1 = 288
			posx_variable2 = 330
			posy_variable2 = 218
			for i in range(len(variable1)):
				alf += '*'
			variable1_render = fuente_pequena.render(alf, True, (0,0,255))
			variable2_render = fuente_pequena.render(variable2, True, (0,0,255))
		elif variable == 'password2':
			posx = 330
			posy = 288
			posx_variable1 = 330
			posy_variable1 = 253
			posx_variable2 = 330
			posy_variable2 = 218
			for i in range(len(variable1)):
				alf += '*'
			variable1_render = fuente_pequena.render(alf, True, (0,0,255))
			variable2_render = fuente_pequena.render(variable2, True, (0,0,255))
		pantalla.blit(variable2_render,(posx_variable2,posy_variable2))
	else:
		return ''
	pantalla.blit(variable1_render,(posx_variable1,posy_variable1))
	if aspect_ratio == '2':
		posx += 133
		posx_variable1 += 133
	escribiendo = True
	if estado == 'iniciar_sesion':
		blit_iniciar_sesion(pantalla,menus)
	elif estado == 'crear_cuenta':
		blit_crear_cuenta(pantalla,menus)
	while escribiendo:
		nombre_personaje_creado,escribiendo = escribir_en_pantalla(nombre_personaje_creado,23)

		alf  = ''
		for i in range(len(nombre_personaje_creado)):
			alf += '*'

		if estado == 'iniciar_sesion':
			blit_iniciar_sesion(pantalla,menus)
		elif estado == 'crear_cuenta':
			blit_crear_cuenta(pantalla,menus)

		if variable == 'user':
			pantalla.blit(fuente_pequena.render(nombre_personaje_creado, True, (0,0,255)),(posx,posy))
		else:
			pantalla.blit(fuente_pequena.render(alf, True, (0,0,255)),(posx,posy))
		if estado == 'crear_cuenta':
			pantalla.blit(variable2_render,(posx_variable2,posy_variable2))
		pantalla.blit(variable1_render,(posx_variable1,posy_variable1))
		pygame.display.flip()
	return nombre_personaje_creado

def apretar_mouse_hacer(pantalla,mouspos,user,password,menus):
	crear_cuenta = False
	mouseposX    = 0
	mouseposY    = 0
	sesion_iniciada = False
	if aspect_ratio == '2':
		mouseposX = 133
	if (323+mouseposX<=mouspos[0]<=573+mouseposX) and (238+mouseposY<=mouspos[1]<=261+mouseposY):
		user = escribir_user_pass(pantalla,'iniciar_sesion','user',menus,password)
	if (323+mouseposX<=mouspos[0]<=573+mouseposX) and (273+mouseposY<=mouspos[1]<=296+mouseposY):
		password = escribir_user_pass(pantalla,'iniciar_sesion','password',menus,user)
	if (291+mouseposX<=mouspos[0]<=510+mouseposX) and (304+mouseposY<=mouspos[1]<=347+mouseposY):
		if verificar_usuario_clave(user,password):
			sesion_iniciada = True
		else:
			pantalla.blit(procesar_idioma('lang_user_pass_error',fuente),(150+mouseposX,150+mouseposY))
	if (291+mouseposX<=mouspos[0]<=510+mouseposX) and (351+mouseposY<=mouspos[1]<=394+mouseposY):
		crear_cuenta = True
	return user,password,sesion_iniciada,crear_cuenta

def blit_selec_pers(pantalla,user,menus): 
	lista    			 = []
	screenX 			 = 0
	screenY 			 = 0
	posx_character 		 = 53
	posy_character 		 = 173
	posx 				 = 45
	posy 				 = 140
	contador_fuente 	 = 0
	if aspect_ratio=='2':
		screenX 		= 133
		posx_character  = 186
		posx 			= 178
		pantalla.blit(menus[0],(0,0))
		pantalla.blit(menus[0],(933,0))
	pantalla.blit(menus[2],(screenX,screenY))
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
		class_character = pygame.transform.scale(class_character,(int(115*mult_resolution),int(295*mult_resolution)))
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

	pantalla.blit(procesar_idioma('lang_close_session',fuente_botones),(650+screenX,6+screenY))
	pantalla.blit(procesar_idioma('lang_select_botton',fuente_botones),(638+screenX,518+screenY))
	pantalla.blit(procesar_idioma('lang_make_char_botton',fuente_bonito),(54+screenX,516+screenY))
	return personajes_cuenta

def apretar_mouse_character_selector(mouspos,pantalla,class_selected,character_selected,personajes_cuenta,datos_imagenes,menus):
	character_selector_menu = True
	character_creator_menu  = False
	juego_loop 				= False
	datos_personaje 		= None
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
		procesar_idioma('lang_log_out')
	if (45+mouseposX<mouspos[0]<256+mouseposX)and (506+mouseposY<mouspos[1]<560+mouseposY):
		if '0' in personajes_cuenta:
			character_creator_menu = True
			blit_creac_pers(pantalla,menus)
			blit_perso_selec_creacion(class_selected,pantalla,menus)
		else:
			procesar_idioma('lang_all_spaces_full')
	if (53+mouseposX<mouspos[0]<167+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[0]
		if personajes_cuenta[0] == '0':
			procesar_idioma('lang_dont_have_char_in_space')
		else:
			procesar_idioma('lang_you_choose')
			print datos_personaje_seleccionado(character_selected)[2]
	if (197+mouseposX<mouspos[0]<311+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[1]
		if personajes_cuenta[1] == '0':
			procesar_idioma('lang_dont_have_char_in_space')
		else:
			procesar_idioma('lang_you_choose')
			print datos_personaje_seleccionado(character_selected)[2]
	if (341+mouseposX<mouspos[0]<455+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[2]
		if personajes_cuenta[2] == '0':
			procesar_idioma('lang_dont_have_char_in_space')
		else:
			procesar_idioma('lang_you_choose')
			print datos_personaje_seleccionado(character_selected)[2]
	if (485+mouseposX<mouspos[0]<599+mouseposX) and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[3]
		if personajes_cuenta[3] == '0':
			procesar_idioma('lang_dont_have_char_in_space')
		else:
			procesar_idioma('lang_you_choose')
			print datos_personaje_seleccionado(character_selected)[2]
	if (629+mouseposX<mouspos[0]<743+mouseposX)and (173+mouseposY<mouspos[1]<467+mouseposY):
		character_selected = personajes_cuenta[4]
		if personajes_cuenta[4] == '0':
			procesar_idioma('lang_dont_have_char_in_space')
		else:
			procesar_idioma('lang_you_choose')
			print datos_personaje_seleccionado(character_selected)[2]

	if (626+mouseposX<mouspos[0]<794+mouseposX)and (511+mouseposY<mouspos[1]<555+mouseposY):
		if character_selected == '0':
			procesar_idioma('lang_select_a_character')
		else:
			datos_personaje = datos_personaje_seleccionado(character_selected)
			datos_mapa      = get_datos_mapa(datos_personaje)
			datos_imagenes  = importar_imagenes(datos_imagenes,datos_personaje,datos_mapa,True)
			juego_loop      = True
			blit_hud_juego(pantalla,datos_imagenes)
			blit_laterales_mapas(pantalla,datos_mapa,datos_imagenes)
			blit_mapa(pantalla,datos_imagenes)
			blitear_datos_mapa(pantalla,datos_mapa,datos_imagenes)
			posicionX,posicionY = blit_personaje_en_mapa(pantalla,datos_personaje,datos_imagenes)
			if '280' in datos_mapa:
				enemigos_bliteados = blit_monster(pantalla,datos_mapa,posicionX,posicionY,datos_imagenes)
	return character_selector_menu,character_creator_menu,character_selected,datos_personaje,juego_loop,datos_mapa,posicionX,posicionY,enemigos_bliteados,datos_imagenes

def get_datos_clases(): 
	datos_clases    = dict()
	lista_id_clases = list()
	arch_clases = open('clases.dat')
	for linea in arch_clases:
		datos = linea.strip().split(';')
		id_clase = datos[0]
		if id_clase == '#id_clase':
			continue
		lista_id_clases.append(id_clase)
		datos_clases[id_clase] = datos
	arch_clases.close()
	return lista_id_clases,datos_clases

def blit_creac_pers(pantalla,menus):
	screenX  = 0
	screenY  = 0
	posx     = 36
	posy     = 199
	contador = 0
	if aspect_ratio=='2':
		screenX = 133
		posx    = 169
		pantalla.blit(menus[0],(0,0))
		pantalla.blit(menus[0],(933,0))
	pantalla.blit(menus[3],(screenX,screenY))
	lista_id_clases,datos_clases = get_datos_clases()
	pantalla.blit(procesar_idioma('lang_creation_of',fuente_titulo,(63,72,204)),(194+screenX,30+screenY))
	pantalla.blit(procesar_idioma('lang_characters',fuente_titulo,(63,72,204)) ,(196+screenX,100+screenY))
	pantalla.blit(procesar_idioma('lang_make_botton',fuente_botones,(255,174,201)) ,(720+screenX,557+screenY))
	pantalla.blit(procesar_idioma('lang_close_session',fuente_botones, (239,228,176)),(650+screenX,6+screenY))
	pantalla.blit(procesar_idioma('lang_back',fuente_botones, (153,217,234)),(22+screenX,12+screenY))

	for bliteamiento in lista_id_clases:
		contador += 1
		class_icon	= pygame.image.load(os.path.join("media","menu","class_"+bliteamiento+"_icon.png")).convert()
		class_icon  = pygame.transform.scale(class_icon,(int(54*mult_resolution),int(54*mult_resolution)))
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

def blit_perso_selec_creacion(class_selected,pantalla,menus):
	datos_clase = get_datos_clases()[1][class_selected]
	screenX  	= 353
	screenY 	= 217
	Xnombre 	= 0
	Ynombre		= 0
	if aspect_ratio == '2':
		screenX = 486
		Xnombre = 133
	blit_creac_pers(pantalla,menus)
	character_class = pygame.image.load(os.path.join("media","menu","class_"+class_selected+"_selection.png")).convert()
	character_class  = pygame.transform.scale(character_class,(int(115*mult_resolution),int(295*mult_resolution)))
	character_class.set_colorkey((255,255,255))
	pantalla.blit(character_class,(screenX,screenY))
	pantalla.blit(fuente.render(datos_clase[1], True, (0,0,255)),(310+Xnombre,550+Ynombre))
	return

def apretar_mouse_character_creator(mouspos,pantalla,user,class_selected,personajes_cuenta,menus):
	character_selector_menu  	 = True
	character_creator_menu  	 = True
	mouseposX				     = 0
	mouseposY					 = 0
	Xnombre						 = 0
	Ynombre 					 = 0
	lista_id_clases,datos_clase  = get_datos_clases()

	if aspect_ratio=='2':
		mouseposX = 133
		Xnombre   = 133

	if (5+mouseposX<mouspos[0]<103+mouseposX)and (5+mouseposY<mouspos[1]<49+mouseposY):
		character_creator_menu = False
		personajes_cuenta = blit_selec_pers(pantalla,user,menus)

	if (646+mouseposX<mouspos[0]<794+mouseposX)and (5+mouseposY<mouspos[1]<41+mouseposY):
		character_selector_menu = False
		character_creator_menu  = False
		procesar_idioma('lang_log_out')

	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[0]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[0]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[1]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[1]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[2]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[2]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (199+mouseposY<mouspos[1]<252+mouseposY):
		if lista_id_clases[3]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[3]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[4]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[4]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[5]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[5]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[6]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[6]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (258+mouseposY<mouspos[1]<311+mouseposY):
		if lista_id_clases[7]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[7]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (36+mouseposX<mouspos[0]<89+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[8]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[8]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (95+mouseposX<mouspos[0]<148+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[9]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[9]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (154+mouseposX<mouspos[0]<207+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[10]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[10]
		blit_perso_selec_creacion(class_selected,pantalla,menus)
	elif (213+mouseposX<mouspos[0]<266+mouseposX)and (317+mouseposY<mouspos[1]<370+mouseposY):
		if lista_id_clases[11]=='0':
			procesar_idioma('lang_class_dont_exist')
		class_selected = lista_id_clases[11]
		blit_perso_selec_creacion(class_selected,pantalla,menus)

	elif (703+mouseposX<mouspos[0]<794+mouseposX)and (556+mouseposY<mouspos[1]<594+mouseposY):
		if class_selected == '0':
			procesar_idioma('lang_select_a_class')
		elif '0' in personajes_cuenta:
			pygame.display.flip()
			crear_personaje(pantalla,user,class_selected,menus)
			character_creator_menu = False
			personajes_cuenta = blit_selec_pers(pantalla,user,menus)
		else:
			procesar_idioma('lang_dont_have_free_spaces')

	return personajes_cuenta,class_selected,character_creator_menu,character_selector_menu

def escribir_nombre(pantalla,lista_nombres,class_selected,menus):
	nombre_personaje_creado = ''
	escribir    = True
	escribiendo = True
	verificador = True
	Xnombre     = 0
	Ynombre 	= 0
	if aspect_ratio == '2':
		Xnombre = 133
	escribe_el_render   = procesar_idioma('lang_write_the',fuente_botones, (185,122,87)) 
	nombre_de_tu_render = procesar_idioma('lang_name_of_your',fuente_botones, (185,122,87))
	personaje_render    = procesar_idioma('lang_character',fuente_botones, (185,122,87))
	while escribir:
		escribiendo = True
		verificador = True
		blit_creac_pers(pantalla,menus)
		blit_perso_selec_creacion(class_selected,pantalla,menus)
		pantalla.blit(menus[4],(Xnombre,Ynombre))
		pantalla.blit(escribe_el_render,(333+Xnombre,170+Ynombre))
		pantalla.blit(nombre_de_tu_render,(333+Xnombre,220+Ynombre))
		pantalla.blit(personaje_render,(335+Xnombre,275+Ynombre))
		while escribiendo:
			nombre_personaje_creado,escribiendo = escribir_en_pantalla(nombre_personaje_creado,11)

			blit_creac_pers(pantalla,menus)
			blit_perso_selec_creacion(class_selected,pantalla,menus)
			pantalla.blit(menus[4],(Xnombre,Ynombre))
			pantalla.blit(escribe_el_render,(333+Xnombre,170+Ynombre))
			pantalla.blit(nombre_de_tu_render,(333+Xnombre,220+Ynombre))
			pantalla.blit(personaje_render,(335+Xnombre,275+Ynombre))
			pantalla.blit(fuente.render(nombre_personaje_creado, True, (0,0,255)),(315+Xnombre,494+Ynombre))	
			
			pygame.display.flip()
		while verificador:
			if len(nombre_personaje_creado)<3:
				procesar_idioma('lang_name_too_short')
				escribiendo = True
				nombre_personaje_creado = ''
			if nombre_personaje_creado in lista_nombres:
				procesar_idioma('lang_name_already_exist')
				escribiendo = True
				nombre_personaje_creado = ''
			if escribiendo == False:
				escribir    = False
			verificador = False
	return nombre_personaje_creado

def crear_personaje(pantalla,user,class_selected,menus):
	file_personajes = open('personajes.dat')
	lista_nombres   = []
	for linea_personajes in file_personajes:
		if linea_personajes.split(';')[0] == '#id_personaje':
			continue
		id_personaje = linea_personajes.strip().split(';')[0]
		lista_nombres.append(linea_personajes.strip().split(';')[2].lower())
	file_personajes.close()

	verificar_nombre     = True
	contador_verificador = 0
	nombre_personaje_creado = escribir_nombre(pantalla,lista_nombres,class_selected,menus)

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


	lista[-1] = lista[-1]+'\n'
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
		if alf[1].lower() == user.lower():
			escribir_file_accounts.write(datos_cuenta_modificados)
		else:
			escribir_file_accounts.write(escribimiento)
	escribir_file_accounts.close()
	return

def get_datos_mapa(datos_personaje):
	datos_mapa = dict()
	try:
		file_datos_mapa = open('media/mapas/mapa'+datos_personaje[5]+'.dat')
		for linea in file_datos_mapa:
			datos_mapa[linea.strip().split(' = ')[0]] = linea.strip().split(' = ')[1]
		file_datos_mapa.close()
	except:
		print 'Error cargando datos del mapa'
		pass
	return datos_mapa

def importar_imagenes(datos_imagenes,datos_personaje,datos_mapa,cambiar_personaje):
	if datos_imagenes == None:
		procesar_idioma('lang_loading_images')
		datos_lateral     = list()
		imagenes_enemigos = list()
		# [hud,mapa_image,cuadricula,datos_lateral,cuadricula_lateral,personajerl,cerrar_x,estrella,bloqued,pausa,imagenes_enemigos,negro,blanco]
		hud     		   = pygame.image.load(os.path.join("media","juego","hud.png")).convert()
		hud 			   = pygame.transform.scale(hud,(int(800*mult_resolution),int(600*mult_resolution)))
		mapa_image		   = pygame.image.load(os.path.join("media","mapas","mapa"+datos_personaje[5]+".png")).convert()
		mapa_image		   = pygame.transform.scale(mapa_image,(int(800*mult_resolution),int(450*mult_resolution)))
		cuadricula 		   = pygame.image.load(os.path.join("media","mapas","predef.png")).convert()
		cuadricula		   = pygame.transform.scale(cuadricula,(int(800*mult_resolution),int(450*mult_resolution)))
		cuadricula.set_colorkey((255,255,255))
		lateral			   = pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
		lateral			   = pygame.transform.scale(lateral,(int(133*mult_resolution),int(600*mult_resolution)))
		cuadricula_lateral = pygame.image.load(os.path.join("media","mapas","predef2.png")).convert()
		cuadricula_lateral = pygame.transform.scale(cuadricula_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
		cuadricula_lateral.set_colorkey((255,255,255))

		if aspect_ratio == '2':
			if '272' in  datos_mapa:
				mapa_lateral 	= pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['272']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '273' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['273']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '270' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['270']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '271' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['271']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)

		personajerl = pygame.image.load(os.path.join("media","clases","class_"+datos_personaje[1]+".png")).convert()
		personajerl = pygame.transform.scale(personajerl,(int(30*mult_resolution),int(60*mult_resolution)))
		personajerl.set_colorkey((255,255,255))

		cerrar_x = pygame.image.load(os.path.join("media","juego","salir.png")).convert()
		cerrar_x = pygame.transform.scale(cerrar_x,(int(800*mult_resolution),int(450*mult_resolution)))
		cerrar_x.set_colorkey((255,255,255))

		estrella = pygame.image.load(os.path.join("media","juego","estrella.png")).convert()
		estrella = pygame.transform.scale(estrella,(int(30*mult_resolution),int(75*mult_resolution)))
		estrella.set_colorkey((255,255,255))
		bloqued = pygame.image.load(os.path.join("media","juego","bloqued.png")).convert()
		bloqued = pygame.transform.scale(bloqued,(int(30*mult_resolution),int(75*mult_resolution)))
		bloqued.set_colorkey((255,255,255))

		pausa = pygame.image.load(os.path.join("media","juego","pausa.png")).convert()
		pausa = pygame.transform.scale(pausa,(int(800*mult_resolution),int(450*mult_resolution)))
		pausa.set_colorkey((255,255,255))

		if '280' in datos_mapa:
			lista_enemigos = datos_mapa['280'].strip().split(';')
			for id_enemigo in lista_enemigos:
				enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+id_enemigo+".png")).convert()
				enemigo   = pygame.transform.scale(enemigo,(int(30*mult_resolution),int(60*mult_resolution)))
				enemigo.set_colorkey((255,255,255))
				imagenes_enemigos.append((enemigo,id_enemigo))

		negro  = pygame.image.load(os.path.join("media","negro.png")).convert()
		blanco = pygame.image.load(os.path.join("media","blanco.png")).convert()

		datos_imagenes = [hud,mapa_image,cuadricula,datos_lateral,cuadricula_lateral,personajerl,cerrar_x,estrella,bloqued,pausa,imagenes_enemigos,negro,blanco]
	else:
		datos_lateral      = list()
		imagenes_enemigos  = list()
		mapa_image		   = pygame.image.load(os.path.join("media","mapas","mapa"+datos_personaje[5]+".png")).convert()
		mapa_image		   = pygame.transform.scale(mapa_image,(int(800*mult_resolution),int(450*mult_resolution)))
		lateral			   = pygame.image.load(os.path.join("media","menu","lateral.png")).convert()
		lateral			   = pygame.transform.scale(lateral,(int(133*mult_resolution),int(600*mult_resolution)))
		
		if aspect_ratio == '2':
			if '272' in  datos_mapa:
				mapa_lateral 	= pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['272']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '273' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['273']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '270' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['270']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)
			if '271' in  datos_mapa:
				mapa_lateral = pygame.image.load(os.path.join("media","mapas","mapa"+datos_mapa['271']+".png")).convert()
				mapa_lateral	= pygame.transform.scale(mapa_lateral,(int(800*mult_resolution),int(450*mult_resolution)))
				datos_lateral.append(mapa_lateral)
			else:
				datos_lateral.append(lateral)

		if '280' in datos_mapa:
			lista_enemigos = datos_mapa['280'].strip().split(';')
			for id_enemigo in lista_enemigos:
				enemigo   = pygame.image.load(os.path.join("media","monsters","monster"+id_enemigo+".png")).convert()
				enemigo   = pygame.transform.scale(enemigo,(int(30*mult_resolution),int(60*mult_resolution)))
				enemigo.set_colorkey((255,255,255))
				imagenes_enemigos.append((enemigo,id_enemigo))

		if cambiar_personaje:
			personajerl = pygame.image.load(os.path.join("media","clases","class_"+datos_personaje[1]+".png")).convert()
			personajerl = pygame.transform.scale(personajerl,(int(30*mult_resolution),int(60*mult_resolution)))
			personajerl.set_colorkey((255,255,255))
			datos_imagenes[5] = personajerl


		datos_imagenes[1]  = mapa_image
		datos_imagenes[3]  = datos_lateral
		datos_imagenes[10] = imagenes_enemigos

	return datos_imagenes

def blit_hud_juego(pantalla,datos_imagenes):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pantalla.blit(datos_imagenes[0],(screenX,screenY))
	return

def blit_laterales_mapas(pantalla,datos_mapa,datos_imagenes):
	datos_lateral = datos_imagenes[3]
	if aspect_ratio == '2':
		if '272' in  datos_mapa:
			pantalla.blit(datos_lateral[0],(-667,448))
			pantalla.blit(datos_imagenes[4],(-667,450))
		else:
			pantalla.blit(datos_lateral[0],(0,448))
		if '273' in  datos_mapa:
			pantalla.blit(datos_lateral[1],(933,448))
			pantalla.blit(datos_imagenes[4],(933,450))
		else:
			pantalla.blit(datos_lateral[1],(933,448))
		if '270' in  datos_mapa:
			pantalla.blit(datos_lateral[2],(-667,0))
			pantalla.blit(datos_imagenes[4],(-667,0))
		else:
			pantalla.blit(datos_lateral[2],(0,0))
		if '271' in  datos_mapa:
			pantalla.blit(datos_lateral[3],(933,0))
			pantalla.blit(datos_imagenes[4],(933,0))
		else:
			pantalla.blit(datos_lateral[3],(933,0))	
	return

def blit_mapa(pantalla,datos_imagenes):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pantalla.blit(datos_imagenes[1],(screenX,screenY))
	pantalla.blit(datos_imagenes[2],(screenX,screenY))
	return 

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
		if posicion_X==posx and posicion_Y==posy:
			celda_number =  str(iteracion)
			problemas    = False
			break
		posicion_X += 50
		if iteracion != 0:
			if iteracion%(15.0+(31.0*contadorA))==0:
				posicion_X -= 775
				posicion_Y += 25
				contadorA += 1
				continue
			elif iteracion%(30+(31.0*contadorB))==0:
				posicion_X -= 775
				posicion_Y +=25
				contadorB += 1
				continue
	return celda_number,problemas

def blitear_datos_mapa(pantalla,datos_mapa,datos_imagenes):
	for celdas in datos_mapa:
		if celdas<='264':
			posx,posy = get_celdas_pos(celdas)
			if aspect_ratio == '2':
				posx += 133
			pantalla.blit(datos_imagenes[7],(posx,posy))

		if debug_mode:	
			if celdas=='265':
				celdas_bloquedas = datos_mapa[celdas].strip().split(';')
				for n_celda_bloqueda in celdas_bloquedas:
					posx,posy = get_celdas_pos(n_celda_bloqueda)
					if aspect_ratio == '2':
						posx += 133
					pantalla.blit(datos_imagenes[8],(posx,posy))
	return

def blit_personaje_en_mapa(pantalla,datos_personaje,datos_imagenes):
	posx,posy = get_celdas_pos(datos_personaje[6])
	if aspect_ratio == '2':
		posx += 133
	pantalla.blit(datos_imagenes[5],(posx,posy))
	return posx,posy

def apretar_mouse_juego_loop(mouspos):
	return

def mover_personaje(pantalla,posx,posy,direX,direY,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes):
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
		if debug_mode:
			print celdas_bloquedas
			print celda_number
		return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,False,None

	if debug_mode:
		procesar_idioma('lang_cell')
	 	print celda_number
	 	print 'posx:',posx+direX,' posy:',posy+direY

	datos_personaje[6] = celda_number
	blit_mapa(pantalla,datos_imagenes)
	blitear_datos_mapa(pantalla,datos_mapa,datos_imagenes)
	posx 		 += direX
	posy 		 += direY
	celda_number = get_celda_number(posx,posy)[0]
	reblit_monster(pantalla,enemigos_bliteados,datos_imagenes)
	blit_personaje_en_mapa(pantalla,datos_personaje,datos_imagenes)
	pygame.display.flip()
	colision_pj_mob,info_enemigo = colision_jugador_monster(posx,posy,enemigos_bliteados)
	if colision_pj_mob and debug_mode:
		procesar_idioma('lang_pj_mob_same_cell')
	if colision_pj_mob == False:
		datos_personaje,datos_mapa,posx,posy,enemigos_bliteados = cambiar_mapa(pantalla,posx,posy,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
	return posx,posy,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo

def bliteo_salir_x(pantalla,datos_imagenes):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pantalla.blit(datos_imagenes[6],(screenX,screenY))
	pantalla.blit(procesar_idioma('lang_sure_want_exit',fuente_botones, (185,122,87)),(240+screenX,125+screenY))
	pantalla.blit(procesar_idioma('lang_yes',fuente_botones_xl, (185,122,87)),(230+screenX,218+screenY))
	pantalla.blit(procesar_idioma('lang_no',fuente_botones_xl, (185,122,87)),(475+screenX,218+screenY))
	return

def guardar_datos_personaje(datos_personaje,posx,posy):
	procesar_idioma('lang_saving_data')

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
		procesar_idioma('lang_saving_error')
	else:
		procesar_idioma('lang_saving_successful')
	return

def blit_pausa(pantalla,datos_imagenes):
	screenX = 0
	screenY = 0
	if aspect_ratio == '2':
		screenX = 133
	pantalla.blit(datos_imagenes[9],(screenX,screenY))
	pantalla.blit(procesar_idioma('lang_back_to_game_botton',fuente_botones, (127,127,127)),(300,126))
	pantalla.blit(procesar_idioma('lang_save_data',fuente_botones, (127,127,127)),(295,173))
	pantalla.blit(procesar_idioma('lang_options_botton',fuente_botones, (127,127,127)),(295,215))
	pantalla.blit(procesar_idioma('lang_change_of_character',fuente_botones, (127,127,127)),(291,258))
	pantalla.blit(procesar_idioma('lang_exit_botton',fuente_botones, (127,127,127)),(296,301))
	return

def apretar_mouse_pausa(mouspos,pantalla,datos_personaje,posicionX,posicionY,direX,direY,datos_mapa,user,personajes_cuenta,enemigos_bliteados,datos_imagenes):
	pausa 	   				= True
	juego_loop 				= True
	character_selector_menu = True
	mouseposX = 0
	mouseposY = 0
	if aspect_ratio == '2':
		mouseposX = 133
	if (285+mouseposX<mouspos[0]<513+mouseposX) and (121+mouseposY<mouspos[1]<163+mouseposY): #reanudar
		posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,0,0,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)							
		pausa = False
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (168+mouseposY<mouspos[1]<210+mouseposY): #guardar datos
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,0,0,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)							
		pausa = False
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (213+mouseposY<mouspos[1]<255+mouseposY): #opciones
		print 'Opciones [WIP]'
		pass
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (258+mouseposY<mouspos[1]<292+mouseposY): #cambiar de personajes
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		personajes_cuenta = blit_selec_pers(pantalla,user,menus)
		juego_loop 				= False
		pausa 					= False 
	elif (285+mouseposX<mouspos[0]<513+mouseposX) and (298+mouseposY<mouspos[1]<336+mouseposY): #salir
		procesar_idioma('lang_log_out')
		guardar_datos_personaje(datos_personaje,posicionX,posicionY)
		character_selector_menu = False
		juego_loop 				= False
		pausa 					= False 
		pygame.display.flip()

	return posicionX,posicionY,datos_personaje,datos_mapa,pausa,personajes_cuenta,juego_loop,character_selector_menu

def apretar_mouse_opciones(mouspos):
	return

def while_cerrar(mouspos,pantalla,datos_personaje,posx,posy,direX,direY,pausa,datos_mapa,enemigos_bliteados,pelea,datos_imagenes,opciones):
	character_selector_menu = True
	juego_loop 				= True
	cerrar 					= True
	mouseposX 				= 0
	mouseposY 				= 0
	if aspect_ratio == '2':
		mouseposX = 133
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]==True:
				if (220+mouseposX<mouspos[0]<343+mouseposX)and (210+mouseposY<mouspos[1]<320+mouseposY):
					procesar_idioma('lang_log_out')
					#print language['lang_log_out']
					guardar_datos_personaje(datos_personaje,posx,posy)
					character_selector_menu = False
					juego_loop 				= False
					cerrar 					= False
					pausa 					= False
					pelea 					= False
					opciones 				= False
					return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea,opciones
				elif (441+mouseposX<mouspos[0]<580+mouseposX)and (209+mouseposY<mouspos[1]<320+mouseposY):
					cerrar   = False
					pausa    = False
					opciones = False
					posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posx,posy,0,0,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
					return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea,opciones
		elif event.type == pygame.KEYDOWN: ##apretar boton
			if event.key == pygame.K_ESCAPE: 
				cerrar = False
				posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posx,posy,0,0,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
				return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea,opciones
	return character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea,opciones

def cambiar_mapa(pantalla,posicionX,posicionY,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes):
	for celdas in datos_mapa:
		if celdas<='264':
			posx,posy = get_celdas_pos(celdas)
			if aspect_ratio == '2':
				posx += 133
			if posicionX == posx and posicionY == posy:
				procesar_idioma('lang_loading_map')
				#time.sleep(0.5)
				datos_celda			= datos_mapa[celdas].split(';')
				nueva_celda         = datos_celda[1]
				datos_personaje[5]  = datos_celda[0]
				datos_personaje[6]  = nueva_celda
				if debug_mode:
					procesar_idioma('lang_map')
					print datos_personaje[5]
				datos_mapa     = get_datos_mapa(datos_personaje)
				datos_imagenes = importar_imagenes(datos_imagenes,datos_personaje,datos_mapa,False)
				blit_mapa(pantalla,datos_imagenes)
				blit_laterales_mapas(pantalla,datos_mapa,datos_imagenes)
				blitear_datos_mapa(pantalla,datos_mapa,datos_imagenes)
				posicionX,posicionY = blit_personaje_en_mapa(pantalla,datos_personaje,datos_imagenes)
				if '280' in datos_mapa:
					enemigos_bliteados = blit_monster(pantalla,datos_mapa,posicionX,posicionY,datos_imagenes)
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

def blit_monster(pantalla,datos_mapa,posicionX,posicionY,datos_imagenes):
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
	contador_mob = 0
	imagenes_enemigos = datos_imagenes[10]
	for id_enemigo in lista_enemigos:
		try:
			celda_enemigo = str(random.randint(0,263))
			while celda_enemigo in celdas_bloquedas:
				if debug_mode:
					procesar_idioma('lang_bloqued_cell')
					print celda_enemigo
				celda_enemigo = str(random.randint(0,263))
			if debug_mode:
				procesar_idioma('lang_enemy_cell')
				print celda_enemigo
			posx,posy = get_celdas_pos(celda_enemigo)
			if aspect_ratio == '2':
				posx += 133
			pantalla.blit(imagenes_enemigos[contador_mob][0],(posx,posy))
			enemigos_bliteados.append((celda_enemigo,id_enemigo))
			celdas_bloquedas.append(celda_enemigo)
			contador_mob += 1
		except:
			pass
	if debug_mode:
		procesar_idioma('lang_blitted_mobs')
		print enemigos_bliteados
	return enemigos_bliteados

def reblit_monster(pantalla,enemigos_bliteados,datos_imagenes):
	contador_mob = 0
	imagenes_enemigos = datos_imagenes[10]
	for celda_enemigo,id_enemigo in enemigos_bliteados:
		posx,posy = get_celdas_pos(celda_enemigo)
		if aspect_ratio == '2':
			posx += 133
		for alf in imagenes_enemigos:
			if id_enemigo == alf[1]:
				pantalla.blit(alf[0],(posx,posy))
		contador_mob += 1
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

def animacion_pantalla(pantalla,screenX,screenY,info_enemigo,datos_mapa,animacion_number,datos_imagenes):
	animacion_number = 3
	if animacion_number == 1 or animacion_number == 2:
		pantalla.blit(datos_imagenes[11],(0,0))
		if animacion_number == 1:
			if aspect_ratio == '2':
				valor = int(2*(120.0/FPS))
				if valor < 1:
					valor = 1
				screenY += valor
			else:
				valor = int(2*(120.0/FPS))
				if valor < 1:
					valor = 1
				screenY += valor
		elif animacion_number == 2:
			valor = int(3*(120.0/FPS))
			if valor < 1:
				valor = 1
			screenX -= valor
			if aspect_ratio == '2':
				valor = int(3*(120.0/FPS))
				if valor < 1:
					valor = 1
				screenY += valor
			else:
				valor = int(2*(120.0/FPS))
				if valor < 1:
					valor = 1
				screenY += int(2*(120.0/FPS))
			
		if aspect_ratio == '2':
			datos_lateral = datos_imagenes[3]
			pantalla.blit(datos_imagenes[11],(600,0))
			if '272' in datos_mapa:
				pantalla.blit(datos_lateral[0],(-800+screenX,448+screenY))
				pantalla.blit(datos_imagenes[4],(-800+screenX,450+screenY))
			else:
				pantalla.blit(datos_lateral[0],(-133+screenX,448+screenY))
			if '273' in  datos_mapa:
				pantalla.blit(datos_lateral[1],(800+screenX,448+screenY))
				pantalla.blit(datos_imagenes[4],(800+screenX,450+screenY))
			else:
				pantalla.blit(datos_lateral[1],(800+screenX,448+screenY))
			if '270' in  datos_mapa:
				pantalla.blit(datos_lateral[2],(-800+screenX,0+screenY))
				pantalla.blit(datos_imagenes[4],(-800+screenX,0+screenY))
			else:
				pantalla.blit(datos_lateral[2],(-133+screenX,0+screenY))
			if '271' in  datos_mapa:
				pantalla.blit(datos_lateral[3],(800+screenX,0+screenY))
				pantalla.blit(datos_imagenes[4],(800+screenX,0+screenY))
			else:
				pantalla.blit(datos_lateral[3],(800+screenX,0+screenY))

		pantalla.blit(datos_imagenes[0],(screenX,screenY))
		pantalla.blit(datos_imagenes[1],(screenX,screenY))
		pantalla.blit(datos_imagenes[2],(screenX,screenY))

		imagenes_enemigos = datos_imagenes[10]
		for imagen_enemigo_blitear,id_enemigo_blitear in imagenes_enemigos:
			if id_enemigo_blitear == info_enemigo[1]:
				break
		posx,posy = get_celdas_pos(info_enemigo[0])
		posx += screenX
		posy += screenY
		pantalla.blit(imagen_enemigo_blitear,(posx,posy))
		pantalla.blit(datos_imagenes[5],(posx,posy))

		if screenY > 600:
			if aspect_ratio == '2':
				return 133,0,False,0
			return 0,0,False,0

	elif animacion_number == 3:
		if aspect_ratio == '2':
			valor = int(7*(120.0/FPS))
			if valor < 1:
				valor = 1
			if screenY <= 200 and screenX >= 488: ##izquierda
				screenX -= valor
				pantalla.blit(datos_imagenes[11],(screenX-133,screenY-600))	
			elif screenX >= 840 and screenY >= 200: ##arriba
				screenY -= valor
				pantalla.blit(datos_imagenes[11],(screenX-133,screenY-200))
			elif screenY < 600 and screenX == 133: ##abajo
				screenY += valor
				pantalla.blit(datos_imagenes[11],(screenX-578,screenY-600))
			elif screenY >= 600 and screenX < 840:##derecha
				screenX += valor
				pantalla.blit(datos_imagenes[11],(screenX-578,screenY-200))
			elif screenX <= 488 and screenY <= 400:
				screenY += valor
				pantalla.blit(datos_imagenes[11],(screenX-133,screenY-600))
				print 'screenX',screenX
				print 'screenY',screenY
				if screenX >=480 and screenY >= 410:
					if aspect_ratio == '2':
						return 133,0,False,0
					return 0,0,False,0

		else:
			valor = int(6*(120.0/FPS))
			if valor < 1:
				valor = 1
			if screenY <= 200 and screenX >= 300:
				screenX -= valor
				pantalla.blit(datos_imagenes[11],(screenX,screenY-600))
				
			elif screenX >= 500: ##arriba
				#print screenY
				
				screenY -= valor
				pantalla.blit(datos_imagenes[11],(screenX,screenY-200))
			elif screenY < 600: ##abajo
				
				screenY += valor
				pantalla.blit(datos_imagenes[11],(screenX-500,screenY-600))
			elif screenY >= 600 and screenX < 500:##derecha
				
				screenX += valor
				pantalla.blit(datos_imagenes[11],(screenX-500,screenY-200))

	return screenX,screenY,True,animacion_number

def blit_pj_mob_en_pelea(pantalla,datos_mapa,info_enemigo,datos_personaje,datos_imagenes):##terminar
	celdas_peleas = datos_mapa['266'].strip().split(';')
	celda_pj = random.choice(celdas_peleas)
	posx_pj,posy_pj = get_celdas_pos(celda_pj)
	celdas_peleas.remove(celda_pj)

	celda_mob = random.choice(celdas_peleas)
	posx_mob,posy_mob = get_celdas_pos(celda_mob)
	imagenes_enemigos = datos_imagenes[10]
	for imagen_enemigo_blitear,id_enemigo_blitear in imagenes_enemigos:
		if id_enemigo_blitear == info_enemigo[1]:
			break
	
	if aspect_ratio == '2':
		posx_pj  += 133
		posx_mob += 133
	pantalla.blit(datos_imagenes[5],(posx_pj,posy_pj))
	pantalla.blit(imagen_enemigo_blitear,(posx_mob,posy_mob))
	return celda_pj,celda_mob

def apretar_mouse_pelea(mouspos):
	return

def mover_pj_en_pelea(pantalla,posx_pj,posy_pj,direX,direY,datos_personaje,datos_mapa,celda_mob_pelea,id_mob,datos_imagenes):
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

	blit_laterales_mapas(pantalla,datos_mapa,datos_imagenes)
	posx_pj += direX
	posy_pj += direY

	if debug_mode:
	 	procesar_idioma('lang_cell')
	 	print get_celda_number(posx_pj,posy_pj)[0]
	 	print 'posx:',posx_pj,' posy:',posy_pj

	blit_mapa(pantalla,datos_imagenes)

	info_enemigo = (celda_mob_pelea,id_mob)
	reblit_monster(pantalla,[info_enemigo],datos_imagenes)
	pantalla.blit(datos_imagenes[5],(posx_pj,posy_pj))
	pygame.display.flip()

	celda_jugador = get_celda_number(posx_pj,posy_pj)[0]
	return celda_jugador
