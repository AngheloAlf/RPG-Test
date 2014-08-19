from functions_settings import *
language = get_languange()
print language['lang_loading']
import pygame, sys, os, random, math, time
from pygame.locals import *
from functions import *
from functions_log_in import *
from constants import *

cosas_hacer = ('0','1','2')

hacer  		     = True
sesion 		     = False
crear_cuenta     = False
oli              = False
Titulo		     = language['lang_titulo']
FPS 		     = get_settings_FPS()
aspect_ratio     = get_settings_aspect_ratio()
debug_mode   	 = get_settings_debug_mode()
enable_busy_loop = get_settings_busy_loop()
show_FPS 		 = get_settings_show_FPS()
resolution		 = get_settings_resolution()

if debug_mode:
	Titulo = '[DEBUG] | '+language['lang_titulo']
	print language['lang_debug_on']
	print 'FPS:',FPS
	if show_FPS:
		print language['lang_show_fps_on']
	if aspect_ratio=='2':
		print language['lang_aspect_ratio_2']
	else:
		print language['lang_aspect_ratio_1']
	if enable_busy_loop:
		print language['lang_busy_loop_on']
	print ''

print language['lang_welcome']
print ''

while hacer:
	print language['lang_select_number']
	print language['lang_exit']
	print language['lang_log_in']
	print language['lang_make_account']

	seleccion_hacer = raw_input(language['lang_select_option']+': ')

	while seleccion_hacer not in cosas_hacer:
		print language['lang_not_valid']
		seleccion_hacer = raw_input(language['lang_select_option']+': ')
	if seleccion_hacer == '0':
		hacer = False
	elif seleccion_hacer == '1':
		sesion = True
		print ''
		print language['lang_select_log_in']
		print language['lang_zero_to_exit']
		print ''
	elif seleccion_hacer == '2':
		print ''
		print language['lang_select_make_account']
		print language['lang_zero_to_exit']
		print ''
		crear_cuenta = True

	while sesion:
		user	 = raw_input(language['lang_input_user']+': ')
		if user == '0':
			sesion = False
			continue
		password = raw_input(language['lang_input_pass']+': ')
		clave_verificada = verificar_usuario_clave(user,password)
		if clave_verificada:
			print language['lang_starting_sesion']
			sesion = False
			#hacer = False
			oli    = True
		else:
			print ''
			print language['lang_user_pass_error']
			print ''
	while crear_cuenta:
		user      = raw_input(language['lang_input_user']+': ')
		if user == '0':
			crear_cuenta = False
			print ''
			continue
		if revisar_existencia_usuario(user):
			print language['lang_user_already_exist']
			continue
		if ';' in user or len(user)<1:
			print language['lang_user_not_valid']
			continue
		password  = raw_input(language['lang_input_pass']+': ')
		password2 = raw_input(language['lang_reinput_pass']+': ')
		if password == '0' or password2 == '0':
			crear_cuenta = False
			print ''
			continue
		if verificar_password(password,password2):
			print language['lang_pass_error']
			continue
		if ';' in password:
			print language['lang_pass_not_valid']
			continue
		datos_usuario = []
		datos_usuario.append(user)
		datos_usuario.append(password)
		agregar_usuario(datos_usuario)
		print language['lang_make_account_successful']
		print ''
		crear_cuenta = False

	if oli:
		oli 					= False
		pygame.init()
		pantalla			= pygame.display.set_mode(resolution)
		pygame.display.set_caption(Titulo)
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
		datos_imagenes			= None

		personajes_cuenta = blit_selec_pers(pantalla,user)
		lista_id_clases = id_clases()
		
		pygame.mixer.init(44100)
		main_dir 			= os.path.split(os.path.abspath(__file__))[0]
		data_dir 			= os.path.join(main_dir, 'music')
		#battle_start_music 	= pygame.mixer.Sound(os.path.join(data_dir, "Battle_start.ogg"))
		#battle_loop_music 	= pygame.mixer.Sound(os.path.join(data_dir, "Battle_loop.ogg"))

		print language['lang_log_in_successful']

		while character_selector_menu:
			if enable_busy_loop:
				milliseconds = clock.tick_busy_loop(FPS)
			else:
				milliseconds = clock.tick(FPS)
			if show_FPS:
				pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

			mouspos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					character_selector_menu = False
					print language['lang_log_out']
					continue
				elif event.type == pygame.KEYDOWN: ##apretar boton
					if event.key == pygame.K_ESCAPE: 
						character_selector_menu = False
						print language['lang_log_out']
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
						character_selector_menu,character_creator_menu,character_selected,datos_personaje,juego_loop,datos_mapa,posicionX,posicionY,enemigos_bliteados,datos_imagenes = apretar_mouse_character_selector(mouspos,pantalla,class_selected,character_selected,personajes_cuenta,datos_imagenes)

			while character_creator_menu:
				if enable_busy_loop:
					milliseconds = clock.tick_busy_loop(FPS)
				else:
					milliseconds = clock.tick(FPS)
				if show_FPS:
					pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
				
				mouspos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						character_creator_menu  = False
						character_selector_menu = False
						print language['lang_log_out']
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
				if show_FPS:
					pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

				mouspos = pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						bliteo_salir_x(pantalla,datos_imagenes)
						cerrar = True
						while cerrar:
							if enable_busy_loop:
								milliseconds = clock.tick_busy_loop(FPS)
							else:
								milliseconds = clock.tick(FPS)
							if show_FPS:
								pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
							mouspos = pygame.mouse.get_pos()
							character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,pausa,datos_mapa,enemigos_bliteados,pelea,datos_imagenes)
							pygame.display.flip()
							
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if pygame.mouse.get_pressed()[0]==True:
							apretar_mouse_juego_loop(mouspos)
					elif event.type == pygame.KEYDOWN: ##apretar boton
						if event.key == pygame.K_ESCAPE:
							blit_pausa(pantalla,datos_imagenes) 
							pausa = True

						if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
							mover_enemigo = random.randint(1,10)
							if mover_enemigo != 9 and mover_enemigo != 10:
								enemigos_bliteados = mover_monster(pantalla,enemigos_bliteados,datos_mapa)

						if event.key == pygame.K_UP:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,25,-25,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
						elif event.key == pygame.K_DOWN:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,-25,25,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
						elif event.key == pygame.K_LEFT:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,-25,-25,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
						elif event.key == pygame.K_RIGHT:
							posicionX,posicionY,datos_personaje,datos_mapa,enemigos_bliteados,colision_pj_mob,info_enemigo = mover_personaje(pantalla,posicionX,posicionY,25,25,datos_mapa,datos_personaje,enemigos_bliteados,datos_imagenes)
						
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
					if show_FPS:
						pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))

					mouspos = pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							bliteo_salir_x(pantalla,datos_imagenes)
							cerrar = True
							while cerrar:
								if enable_busy_loop:
									milliseconds = clock.tick_busy_loop(FPS)
								else:
									milliseconds = clock.tick(FPS)
								if show_FPS:
									pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
								mouspos = pygame.mouse.get_pos()
								character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea  = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,pausa,datos_mapa,enemigos_bliteados,pelea,datos_imagenes)
								pygame.display.flip()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]==True:
								posicionX,posicionY,datos_personaje,datos_mapa,pausa,personajes_cuenta,juego_loop,character_selector_menu = apretar_mouse_pausa(mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,datos_mapa,user,personajes_cuenta,enemigos_bliteados,datos_imagenes)
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_p:
								print 'while_pausa'
					pygame.display.flip()

				while pelea:
					if enable_busy_loop:
						milliseconds = clock.tick_busy_loop(FPS)
					else:
						milliseconds = clock.tick(FPS)
					if show_FPS:
						pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
					mouspos = pygame.mouse.get_pos()

					while blit_animacion:
						if enable_busy_loop:
							milliseconds = clock.tick_busy_loop(FPS)
						else:
							milliseconds = clock.tick(FPS)
						if show_FPS:
							pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
						screenX,screenY,blit_animacion,animacion_number = animacion_pantalla(pantalla,screenX,screenY,info_enemigo,datos_mapa,animacion_number,datos_imagenes)
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
							blit_hud_juego(pantalla,datos_imagenes)
							blit_mapa(pantalla,datos_imagenes)
							blit_laterales_mapas(pantalla,datos_mapa,datos_imagenes)
							celda_pj_pelea,celda_mob_pelea = blit_pj_mob_en_pelea(pantalla,datos_mapa,info_enemigo,datos_personaje,datos_imagenes)
					
					if pygame.mixer.music.get_busy() == False:
						pygame.mixer.music.load(os.path.join(data_dir, "Battle_loop.ogg"))
						pygame.mixer.music.play()
					contador_pelea += 1

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							bliteo_salir_x(pantalla,datos_imagenes)
							cerrar = True
							while cerrar:
								if enable_busy_loop:
									milliseconds = clock.tick_busy_loop(FPS)
								else:
									milliseconds = clock.tick(FPS)
								if show_FPS:
									pygame.display.set_caption("{0} | FPS: {1}".format(Titulo,round(clock.get_fps(),2)))
								mouspos = pygame.mouse.get_pos()
								character_selector_menu,juego_loop,cerrar,pausa,enemigos_bliteados,pelea = while_cerrar(pygame.event.get(),pygame.mouse.get_pressed(),mouspos,pantalla,datos_personaje,posicionX,posicionY,0,0,pausa,datos_mapa,enemigos_bliteados,pelea,datos_imagenes)
								pygame.display.flip()
								
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if pygame.mouse.get_pressed()[0]==True:
								apretar_mouse_pelea(mouspos)
						elif event.type == pygame.KEYDOWN: ##apretar boton
							posx_pj,posy_pj = get_celdas_pos(celda_pj_pelea)
							if event.key == pygame.K_UP:
								celda_pj_pelea = mover_pj_en_pelea(pantalla,posx_pj,posy_pj,25,-25,datos_personaje,datos_mapa,celda_mob_pelea,info_enemigo[1],datos_imagenes)
							elif event.key == pygame.K_DOWN:
								celda_pj_pelea = mover_pj_en_pelea(pantalla,posx_pj,posy_pj,-25,25,datos_personaje,datos_mapa,celda_mob_pelea,info_enemigo[1],datos_imagenes)
							elif event.key == pygame.K_LEFT:
								celda_pj_pelea = mover_pj_en_pelea(pantalla,posx_pj,posy_pj,-25,-25,datos_personaje,datos_mapa,celda_mob_pelea,info_enemigo[1],datos_imagenes)
							elif event.key == pygame.K_RIGHT:
								celda_pj_pelea = mover_pj_en_pelea(pantalla,posx_pj,posy_pj,25,25,datos_personaje,datos_mapa,celda_mob_pelea,info_enemigo[1],datos_imagenes)
							
							elif event.key == pygame.K_p: ## DEBUG
								#blit_cargando(pantalla)
								#time.sleep(4)
								pass
							#	guardar_datos_personaje(datos_personaje,posicionX,posicionY)

							#if event.key == pygame.K_d: letra d teclado
							#if event.key == pygame.K_a: letra a teclado
							#if event.key == pygame.K_w: letra w teclado
							#if event.key == pygame.K_s: letra s teclado
					pygame.display.flip()

				pygame.display.flip()

			pygame.display.flip()

		print ''

		pygame.quit()
