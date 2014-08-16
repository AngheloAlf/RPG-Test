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
		file_lang = open('languages\lang_'+idioma+'.lang')
	except:
		file_lang = open('languages\lang_es.lang')
		print 'Error cargando archivo de idiomas, cargando el predeterminado'
	for linea in file_lang:
		alf = linea.strip().split(' = ')
		lang[alf[0]] = alf[1]
	return lang

def get_settings_resolution():
	settings = abrir_settings()
	if get_settings_aspect_ratio() == '2':
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
