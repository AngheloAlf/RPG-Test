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
