def abrir_settings():
	settings      = dict()
	file_settings = open('settings.ini')
	for linea in file_settings:
		valor = linea.strip().split(' = ')
		if valor[0]=='#':
			continue
		try:
			settings[valor[0]] = valor[1]
		except:
			continue
	file_settings.close()
	return settings

def get_settings_FPS():
	settings = abrir_settings()
	return float(settings['FPS'])

def get_settings_aspect_ratio():
	settings = abrir_settings()
	return settings['aspect_ratio']

def get_settings_debug_mode():
	settings = abrir_settings()
	if settings['debug_mode'] == 'True':
		return True
	return False

def get_settings_busy_loop():
	settings = abrir_settings()
	if settings['busy_loop'] == 'True':
		return True
	return False

def get_settings_show_FPS():
	settings = abrir_settings()
	if settings['show_FPS'] == 'True':
		return True
	return False

def get_languange():
	settings = abrir_settings()
	idioma = settings['language']
	lang = dict()

	try:
		file_lang = open('languages/lang_'+idioma+'.lang')
	except:
		print 'Error cargando archivo de idiomas, cargando el predeterminado'
		try:
			file_lang = open('languages/lang_es.lang')
		except:
			print 'Error cargando el archivo predeterminado'
			return lang
	for linea in file_lang:
		alf = linea.strip().split(' = ')
		lang[alf[0]] = alf[1]
	return lang

def get_settings_resolution():
	settings = abrir_settings()
	if get_settings_aspect_ratio() == '0':
		alf = settings['resolution'].split('x')
		alf = map(int,alf)
		alf = tuple(alf)
		return alf
	elif get_settings_aspect_ratio() == '2':
		if settings['resolution'] == '1066x600':
			return (1066,600)
		if settings['resolution'] == '800x600':
			return (1066,600)
	else:
		if settings['resolution'] == '800x600':
			return (800,600)
		if settings['resolution'] == '1066x600':
			return (800,600)
	return (800,600)

def get_multiplicator_resolution():
	aspect_ratio = get_settings_aspect_ratio()
	resolution   = get_settings_resolution()
	if aspect_ratio == '0':
		return resolution[1]/600.0
	if aspect_ratio == '1':
		return resolution[1]/600.0
	elif aspect_ratio == '2':
		return resolution[1]/600.0
	return 1.0

def get_battle_music():
	file_battle_music = open('music/Battle_music.txt')
	battle_music = dict()
	for linea in file_battle_music:
		valor = linea.strip().split('-')
		battle_music[valor[0]]=valor[1]
	file_battle_music.close()
	return battle_music
