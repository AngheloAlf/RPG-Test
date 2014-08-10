print 'Cargado...'
import pygame, sys, os, random, math, time
from pygame.locals import *
from functions import *
from functions_log_in import *
from functions_settings import *

cosas_hacer = ('0','1','2')

hacer  		 = True
sesion 		 = False
crear_cuenta = False
oli          = False
Titulo		 = 'RPG Test'
FPS 		 = get_settings_FPS()
aspect_ratio = get_settings_aspect_ratio()
debug_mode   = get_settings_debug_mode()

if debug_mode:
	print 'Debug mode activo'

print 'Bienvenido\n'

while hacer:
	print 'Que desea hacer? Escoja un numero'
	print 'Salir (0)'
	print 'Iniciar sesion (1)'
	print 'Crear cuenta (2)'

	seleccion_hacer = raw_input('Escoja una opcion: ')

	while seleccion_hacer not in cosas_hacer:
		print 'Opcion no valida'
		seleccion_hacer = raw_input('Escoja una opcion: ')
	if seleccion_hacer == '0':
		hacer = False
	elif seleccion_hacer == '1':
		sesion = True
		print ''
		print 'Ha escojido iniciar sesion'
		print 'Ponga 0 para salir'
		print ''
	elif seleccion_hacer == '2':
		print ''
		print 'Ha escogido crear cuenta'
		print 'Ponga 0 para salir'
		print ''
		crear_cuenta = True

	while sesion:
		user	 = raw_input('Ingrese usuario: ')
		if user == '0':
			sesion = False
			continue
		password = raw_input('Ingrese clave: ')
		clave_verificada = verificar_usuario_clave(user,password)
		if clave_verificada:
			print 'Iniciando sesion'
			sesion = False
			#hacer = False
			oli    = True
		else:
			print ''
			print 'El usuario o la clave es incorrecta'
			print ''
	while crear_cuenta:
		user      = raw_input('Ingrese usuario: ')
		if user == '0':
			crear_cuenta = False
			print ''
			continue
		if revisar_existencia_usuario(user):
			print 'Este usuario ya existe, escoja otro'
			continue
		if ';' in user or len(user)<1:
			print 'El usuario no es valido, escoja otro'
			continue
		password  = raw_input('Ingrese clave: ')
		password2 = raw_input('Repita clave: ')
		if verificar_password(password,password2):
			print 'La clave no coincide'
			continue
		if ';' in password:
			print 'La clave no es valida, escoja otro'
			continue
		datos_usuario = []
		datos_usuario.append(user)
		datos_usuario.append(password)
		agregar_usuario(datos_usuario)
		print ''
		crear_cuenta = False

	if oli:
		oli 					= False
		pygame.init()
		
		if aspect_ratio == '2':
			pantalla			= pygame.display.set_mode((1066,600))
		else:
			pantalla			= pygame.display.set_mode((800,600))
		pygame.display.set_caption(Titulo)
		fondo_blanco  			= pygame.image.load(os.path.join("media","blanco.png")).convert()
		clock 					= pygame.time.Clock()
		character_selector_menu = True
		character_creator_menu  = False
		juego_loop 				= False
		pausa 					= False
		class_selected          = '0'
		character_selected 		= '0'
		reproducir_musica		= False
		
		fuente			        = pygame.font.Font("media/PressStart2P.ttf", 15)

		personajes_cuenta = blit_selec_pers(pantalla,user,fuente)
		lista_id_clases = id_clases()

		print 'Sesion iniciada con exito'

		while character_selector_menu:
			milliseconds = clock.tick_busy_loop(FPS)
			pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
			#pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,clock.get_fps(),2))

			mouspos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					character_selector_menu = False
					print 'Cerrando sesion'
					continue
				elif event.type == pygame.KEYDOWN: ##apretar boton
					if event.key == pygame.K_ESCAPE: 
						character_selector_menu = False
						print 'Cerrando sesion'
						break
		            #if event.key == pygame.K_d: letra d teclado
		            #if event.key == pygame.K_a: letra a teclado
		            #if event.key == pygame.K_w: letra w teclado
		            #if event.key == pygame.K_s: letra s teclado
				elif event.type == pygame.KEYUP: ##desapretar boton
					pass
		            #if event.key == pygame.K_d: 
		            #if event.key == pygame.K_a: 
		            #if event.key == pygame.K_w: 
		            #if event.key == pygame.K_s: 
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pressed()[0]==True:
						character_selector_menu,character_creator_menu,character_selected,datos_personaje,juego_loop,datos_mapa,posicionX,posicionY = apretar_mouse_character_selector(mouspos,pantalla,class_selected,character_selected,personajes_cuenta,aspect_ratio,debug_mode)

			while character_creator_menu:
				milliseconds = clock.tick_busy_loop(FPS)
				pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
				
				mouspos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						character_creator_menu  = False
						character_selector_menu = False
						print 'Cerrando sesion'
						continue
					elif event.type == pygame.KEYDOWN: ##apretar boton
						if event.key == pygame.K_ESCAPE: 
							character_creator_menu = False
							personajes_cuenta = blit_selec_pers(pantalla,user,fuente)
							#continue

					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]==True:
							personajes_cuenta,class_selected,character_creator_menu,character_selector_menu = apretar_mouse_character_creator(mouspos,pantalla,user,aspect_ratio,fuente,class_selected,lista_id_clases,personajes_cuenta)
							
				pygame.display.flip()

			while juego_loop:
				milliseconds = clock.tick_busy_loop(FPS)
				pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

				mouspos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						bliteo_pop_up(pantalla,aspect_ratio)
						cerrar = True
						while cerrar:
							milliseconds = clock.tick_busy_loop(FPS)
							pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
							mouspos = pygame.mouse.get_pos()
							character_selector_menu,juego_loop,cerrar,pausa = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,character_selector_menu,juego_loop,cerrar,pausa,datos_mapa,aspect_ratio,debug_mode)
							pygame.display.flip()
							
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]==True:
							apretar_mouse_juego_loop(mouspos,aspect_ratio)
					elif event.type == pygame.KEYDOWN: ##apretar boton
						if event.key == pygame.K_ESCAPE:
							blit_pausa(pantalla,aspect_ratio) 
							pausa = True
						if event.key == pygame.K_UP:
							posicionX,posicionY,datos_personaje,datos_mapa = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,25,-25,datos_personaje[5],datos_mapa,datos_personaje,aspect_ratio,debug_mode)
						elif event.key == pygame.K_DOWN:
							posicionX,posicionY,datos_personaje,datos_mapa = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,-25,25,datos_personaje[5],datos_mapa,datos_personaje,aspect_ratio,debug_mode)
						elif event.key == pygame.K_LEFT:
							posicionX,posicionY,datos_personaje,datos_mapa = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,-25,-25,datos_personaje[5],datos_mapa,datos_personaje,aspect_ratio,debug_mode)
						elif event.key == pygame.K_RIGHT:
							posicionX,posicionY,datos_personaje,datos_mapa = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,25,25,datos_personaje[5],datos_mapa,datos_personaje,aspect_ratio,debug_mode)
						
						elif event.key == pygame.K_p: ## DEBUG
							#blit_cargando(pantalla)
							#time.sleep(4)
							pass
						#	guardar_datos_personaje(datos_personaje,posicionX,posicionY)

						#if event.key == pygame.K_d: letra d teclado
						#if event.key == pygame.K_a: letra a teclado
						#if event.key == pygame.K_w: letra w teclado
						#if event.key == pygame.K_s: letra s teclado

				while pausa:
					milliseconds = clock.tick_busy_loop(FPS)
					pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

					mouspos = pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							bliteo_pop_up(pantalla,aspect_ratio)
							cerrar = True
							while cerrar:
								milliseconds = clock.tick_busy_loop(FPS)
								pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
								mouspos = pygame.mouse.get_pos()
								character_selector_menu,juego_loop,cerrar,pausa = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,character_selector_menu,juego_loop,cerrar,pausa,debug_mode)
								pygame.display.flip()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]==True:

								posicionX,posicionY,datos_personaje,datos_mapa,pausa,personajes_cuenta,juego_loop,character_selector_menu = apretar_mouse_pausa(mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,datos_mapa,aspect_ratio,user,fuente,personajes_cuenta,debug_mode)

					pygame.display.flip()

				pygame.display.flip()

			pygame.display.flip()

		print ''

		pygame.quit()
