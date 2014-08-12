print 'Cargado...'
import pygame, sys, os, random, math, time
from pygame.locals import *
from functions import *
from functions_log_in import *
from functions_settings import *
from constants import *

cosas_hacer = ('0','1','2')

hacer  		     = True
sesion 		     = False
crear_cuenta     = False
oli              = False
Titulo		     = 'RPG Test'
FPS 		     = get_settings_FPS()
aspect_ratio     = get_settings_aspect_ratio()
debug_mode   	 = get_settings_debug_mode()
enable_busy_loop = get_settings_busy_loop()

if debug_mode:
	Titulo = '[DEBUG] | RPG Test'
	print 'Debug mode activo'
	print 'FPS:',FPS
	if aspect_ratio=='2':
		print 'Aspect ratio: 16:9'
	else:
		print 'Aspect ratio: 4:3'
	if enable_busy_loop:
		print 'busy_loop activo'
	print ''

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
		pelea 					= False
		class_selected          = '0'
		character_selected 		= '0'
		reproducir_musica		= False
		enemigos_bliteados		= []
		colision_pj_mob 		= False
		screenX     			= 0
		if aspect_ratio == '2':
			screenX 			= 133
		screenY 				= 0
		contador_pelea 			= 0
		animacion_number   		= 0

		personajes_cuenta = blit_selec_pers(pantalla,user)
		lista_id_clases = id_clases()
		
		pygame.mixer.init(44100)
		main_dir 			= os.path.split(os.path.abspath(__file__))[0]
		data_dir 			= os.path.join(main_dir, 'music')
		#battle_start_music 	= pygame.mixer.Sound(os.path.join(data_dir, "Battle_start.ogg"))
		#battle_loop_music 	= pygame.mixer.Sound(os.path.join(data_dir, "Battle_loop.ogg"))

		print 'Sesion iniciada con exito'

		while character_selector_menu:
			if enable_busy_loop:
				milliseconds = clock.tick_busy_loop(FPS)
			else:
				milliseconds = clock.tick(FPS)
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
						character_selector_menu,character_creator_menu,character_selected,datos_personaje,juego_loop,datos_mapa,posicionX,posicionY,enemigos_bliteados = apretar_mouse_character_selector(mouspos,pantalla,class_selected,character_selected,personajes_cuenta)

			while character_creator_menu:
				if enable_busy_loop:
					milliseconds = clock.tick_busy_loop(FPS)
				else:
					milliseconds = clock.tick(FPS)
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
							personajes_cuenta = blit_selec_pers(pantalla,user)
							#continue

					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]==True:
							personajes_cuenta,class_selected,character_creator_menu,character_selector_menu = apretar_mouse_character_creator(mouspos,pantalla,user,class_selected,lista_id_clases,personajes_cuenta)
							
				pygame.display.flip()

			while juego_loop:
				if enable_busy_loop:
					milliseconds = clock.tick_busy_loop(FPS)
				else:
					milliseconds = clock.tick(FPS)
				pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

				mouspos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						bliteo_pop_up(pantalla)
						cerrar = True
						while cerrar:
							if enable_busy_loop:
								milliseconds = clock.tick_busy_loop(FPS)
							else:
								milliseconds = clock.tick(FPS)
							pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
							mouspos = pygame.mouse.get_pos()
							character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados  = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,pausa,datos_mapa,enemigos_bliteados)
							pygame.display.flip()
							
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]==True:
							apretar_mouse_juego_loop(mouspos)
					elif event.type == pygame.KEYDOWN: ##apretar boton
						if event.key == pygame.K_ESCAPE:
							blit_pausa(pantalla) 
							pausa = True
						if event.key == pygame.K_UP:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,25,-25,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
						elif event.key == pygame.K_DOWN:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,-25,25,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
						elif event.key == pygame.K_LEFT:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,-25,-25,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
						elif event.key == pygame.K_RIGHT:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,datos_personaje[1],posicionX,posicionY,25,25,datos_personaje[5],datos_mapa,datos_personaje,enemigos_bliteados)
						
						elif event.key == pygame.K_p: ## DEBUG
							#blit_cargando(pantalla)
							#time.sleep(4)
							pass
						#	guardar_datos_personaje(datos_personaje,posicionX,posicionY)

						#if event.key == pygame.K_d: letra d teclado
						#if event.key == pygame.K_a: letra a teclado
						#if event.key == pygame.K_w: letra w teclado
						#if event.key == pygame.K_s: letra s teclado
				if colision_pj_mob == True:
					reproducir_musica = True
					pelea             = True
					colision_pj_mob   = False
					blit_animacion    = True
					animacion_number  = random.randint(1,2)					

				while pausa:
					if enable_busy_loop:
						milliseconds = clock.tick_busy_loop(FPS)
					else:
						milliseconds = clock.tick(FPS)
					pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

					mouspos = pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							bliteo_pop_up(pantalla)
							cerrar = True
							while cerrar:
								if enable_busy_loop:
									milliseconds = clock.tick_busy_loop(FPS)
								else:
									milliseconds = clock.tick(FPS)
								pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
								mouspos = pygame.mouse.get_pos()
								character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados  = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,pausa,enemigos_bliteados)
								pygame.display.flip()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]==True:

								posicionX,posicionY,datos_personaje,datos_mapa,pausa,personajes_cuenta,juego_loop,character_selector_menu = apretar_mouse_pausa(mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,datos_mapa,user,personajes_cuenta,enemigos_bliteados)

					pygame.display.flip()

				while pelea:
					if enable_busy_loop:
						milliseconds = clock.tick_busy_loop(FPS)
					else:
						milliseconds = clock.tick(FPS)
					
					pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
					mouspos = pygame.mouse.get_pos()

					while blit_animacion:
						if enable_busy_loop:
							milliseconds = clock.tick_busy_loop(FPS)
						else:
							milliseconds = clock.tick(FPS)
					
						pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
						screenX,screenY,blit_animacion,animacion_number = animacion_pantalla(pantalla,datos_personaje[5],screenX,screenY,datos_personaje[1],info_enemigo,datos_mapa,animacion_number)
						if reproducir_musica:
							pygame.mixer.music.load(os.path.join(data_dir, "Battle_start.ogg"))
							pygame.mixer.music.play()
							#pygame.mixer.Sound.play(battle_start_music)
							reproducir_musica = False

						pos_musica = pygame.mixer.music.get_pos()
						if pos_musica >2900:
							blit_animacion = False

						pygame.display.flip()

						if blit_animacion == False:
							blit_hud_juego(pantalla)
							datos_mapa = blit_mapa(pantalla,datos_personaje[5])
							blit_laterales_mapas(pantalla,datos_mapa)

							#posicionX,posicionY = blit_personaje_en_mapa(pantalla,datos_personaje[1],celda)

					if pygame.mixer.music.get_busy() == False:
						pygame.mixer.music.load(os.path.join(data_dir, "Battle_loop.ogg"))
						pygame.mixer.music.play()
					contador_pelea += 1

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							#character_selector_menu = False
							print 'Quit'
							#continue
					pygame.display.flip()

				pygame.display.flip()

			pygame.display.flip()

		print ''

		pygame.quit()
