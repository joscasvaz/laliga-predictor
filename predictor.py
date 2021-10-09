import csv
from os import listdir

def read_fixtures(fichero):

	registros = []

	with open(fichero, encoding='utf-8') as f:
		lector = csv.reader(f)
		next(lector)
		for l in lector:
			registros.append(l)

	return registros

def mk_fixtures(lectura):

	jornadas = []

	for jornada in lectura:

		partidos = []

		locales = jornada[1].split('#')
		visitantes = jornada[2].split('#')

		i = 0
		while i < len(locales):
			partidos.append([locales[i], visitantes[i]])
			i = i + 1

		jornadas.append(partidos)

	return jornadas

def check_fixtures(fixtures):	
	
	i = 0
	while i < len(fixtures):

		locales = fixtures[i][0]
		visitantes = fixtures[i][1]

		locales_set = set(locales)
		visitantes_set = set(visitantes)

		error_message = 'ERROR: JORNADA %n NO VALIDA', i

		if len(locales) != len(locales_set) or len(visitantes) != len(visitantes_set):
			print(error_message)

		for local in locales:
			if local in visitantes:
				print(error_message)

		i = i + 1

def read_players(fichero):

	registros = []

	with open(fichero, encoding='utf-8') as f:
		lector = csv.reader(f)
		next(lector)
		for _,EQUIPO_ID,PUNTOS,PUNTOS_MEDIA,_,APODO,SLUG,_,POSICION,VALOR_MERCADO,ESTADO_JUGADOR,SEMANA_1,SEMANA_2,SEMANA_3,SEMANA_4,SEMANA_5,SEMANA_6,SEMANA_7,SEMANA_8,SEMANA_9,SEMANA_10,SEMANA_11,SEMANA_12,SEMANA_13,SEMANA_14,SEMANA_15,SEMANA_16,SEMANA_17,SEMANA_18,SEMANA_19,SEMANA_20,SEMANA_21,SEMANA_22,SEMANA_23,SEMANA_24,SEMANA_25,SEMANA_26,SEMANA_27,SEMANA_28,SEMANA_29,SEMANA_30,SEMANA_31,SEMANA_32,SEMANA_33,SEMANA_34,SEMANA_35,SEMANA_36,SEMANA_37,SEMANA_38,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_ in lector:
			lista = [SLUG,APODO,EQUIPO_ID,POSICION,int(PUNTOS),float(PUNTOS_MEDIA),[int(VALOR_MERCADO)],[ESTADO_JUGADOR],[SEMANA_1,SEMANA_2,SEMANA_3,SEMANA_4,SEMANA_5,SEMANA_6,SEMANA_7,SEMANA_8,SEMANA_9,SEMANA_10,SEMANA_11,SEMANA_12,SEMANA_13,SEMANA_14,SEMANA_15,SEMANA_16,SEMANA_17,SEMANA_18,SEMANA_19,SEMANA_20,SEMANA_21,SEMANA_22,SEMANA_23,SEMANA_24,SEMANA_25,SEMANA_26,SEMANA_27,SEMANA_28,SEMANA_29,SEMANA_30,SEMANA_31,SEMANA_32,SEMANA_33,SEMANA_34,SEMANA_35,SEMANA_36,SEMANA_37,SEMANA_38]]
			for i in lista[8]:
				i = int(i)
			registros.append(lista)

	return registros

def read_performances(fichero):

	registros = []

	with open(fichero, encoding='utf-8') as f:
		lector = csv.reader(f)
		next(lector)
		for _,SLUG,EQUIPO_ID,SEMANA,PUNTOS_TOTALES,MIN_JUGADOS,GOLES,ASISTENCIAS_GOL,ASISTENCIAS_SIN_GOL,LLEGADAS_AREA,PENALTIS_PROVOCADOS,PENALTIS_PARADOS,PARADAS,DESPEJES,PENALTIS_FALLADOS,GOLES_EN_PROPIA,GOLES_EN_CONTRA,TARJETAS_AMARILLAS,SEGUNDAS_AMARILLAS,TARJETAS_ROJAS,TIROS_A_PUERTA,REGATES,BALONES_RECUPERADOS,POSESIONES_PERDIDAS,PUNTOS_MARCA,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_ in lector:
			lista = [SLUG,EQUIPO_ID,SEMANA,PUNTOS_TOTALES,MIN_JUGADOS,GOLES,ASISTENCIAS_GOL,ASISTENCIAS_SIN_GOL,LLEGADAS_AREA,PENALTIS_PROVOCADOS,PENALTIS_PARADOS,PARADAS,DESPEJES,PENALTIS_FALLADOS,GOLES_EN_PROPIA,GOLES_EN_CONTRA,TARJETAS_AMARILLAS,SEGUNDAS_AMARILLAS,TARJETAS_ROJAS,TIROS_A_PUERTA,REGATES,BALONES_RECUPERADOS,POSESIONES_PERDIDAS,PUNTOS_MARCA]
			for i in lista[2:]:
				lista[lista.index(i)] = int(i)
			registros.append(lista)

	return registros

def merge_players(fichero,ficheros_jugadores):

	registro = read_players(fichero)
	slugs = []

	for jugador in registro:
		slugs.append(jugador[0])

	for archivo in ficheros_jugadores:
		lectura = read_players(archivo)
		for player in lectura:
			slug = player[0]
			if slug not in slugs:
				registro.append(player)
			else:
				i = registro.index(registro[slugs.index(slug)])
				registro[i][6].append(player[6][0])
				registro[i][7].append(player[7][0])

	return registro

def mk_players(jugadores, actuaciones):

	players = []

	for player in jugadores:
		for actuacion in actuaciones:
			
			if player[0] == actuacion[0]:

				player_actuacion = actuacion[3:]
				player_jornada = {actuacion[2]:player_actuacion}
				player.append(player_jornada)

		players.append(player)

	return players

def mk_teams(players):

	teams = {}

	for player in players:

		equipo = player[2]

		if equipo not in teams:
			jugadores = [player]
			teams[equipo] = jugadores
		else:
			teams[equipo].append(player)

	return teams

def mk_elos(teams):

	equipos = {}

	for k,v in teams.items():
		team_elo = 0
		for player in v:
			team_elo = team_elo + player[4]
		equipos[k] = [team_elo, v]

	return equipos

def mk_predictions(fixtures):
	return 0

def mk_strings(elo_teams):

	registro = []

	for k,v in elo_teams.items():
		cadena = str(k)
		for valor in v:
			cadena = cadena + ',' + str(v[0]) + ','
			for player in v[1]:
				cadena = cadena + str(player)
		cadena = cadena + '\n'
		registro.append(cadena)

	return registro

def record(lista,fichero):

	with open(fichero, mode='w', encoding='utf-8') as f:
		escritor = csv.writer(f,quoting=csv.QUOTE_ALL)
		escritor.writerow(lista)

ruta2021 = './data/20-21/'
ruta_archivos2021 = ['./data/20-21/'+ archivo for archivo in listdir(ruta2021) if archivo != 'players-performance.csv']
ruta_archivos2021.sort()

lectura_performances2021 = read_performances(ruta2021 + './players-performance.csv')
lectura_jugadores2021 = [fichero for fichero in ruta_archivos2021]
jugadores_merged = merge_players(lectura_jugadores2021[-1], lectura_jugadores2021[0:len(lectura_jugadores2021)-2])

jugadores = mk_players(jugadores_merged,lectura_performances2021)
equipos = mk_teams(jugadores)
equipos_elo = mk_elos(equipos)
cadenas = mk_strings(equipos_elo)

print('¿Quieres escribir? Y/n')
escribir = input()
if(escribir == 'Y'):
	escritura = record(cadenas,'./storage/20-21/players_st.csv')
else:
	print('No se escribió')

print('Done.')