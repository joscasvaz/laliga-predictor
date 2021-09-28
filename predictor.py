import csv

def lee_fichero(fichero):

	registros = []

	with open(fichero, encoding='utf-8') as f:
		lector = csv.reader(f)
		next(lector)
		for l in lector:
			registros.append(l)

	return registros

def fixture(lectura):

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

def elo(team):

	elo = 0

	top = ('RMA','ATL','FCB','SEV')
	midtop = ('VIL','RSO','BET','VAL','ATH')
	midbot = ('CEL','OSA','CAD','GRA','LEV')
	bottom = ('ESP','MLL','RAY','ALA','ELC','GET')
	if team in top:
		elo = 4
	elif team in midtop:
		elo = 3
	elif team in midbot:
		elo = 2
	elif team in bottom:
		elo = 1

	return elo

def predict(fixtures):

	i = 0
	for fixture in fixtures:

		locales = []
		visitantes = []

		j = 0
		while j < len(fixture):
			locales.append(fixtures[i][j][0])
			visitantes.append(fixtures[i][j][1])

			elo_local = 0
			elo_visitante = 0
			k = 0
			while k < len(locales):
				local = locales[k]
				visitante = visitantes[k]

				elo_local = elo(local) + 1
				elo_visitante = elo(visitante)
				fixture[j] = [[local,elo_local], [visitante,elo_visitante]]

				veredict = -1

				if elo_visitante < elo_local:
					veredict = 1
					if elo_visitante + 1 < elo_local:
						veredict = 2
				elif elo_visitante == elo_local:
					veredict = 0

				k = k + 1

			fixture[j].append(veredict)
			j = j + 1
			
		i = i + 1

	return fixtures

def favoritos(fixtures):

	favoritos = {}

	for fixture in fixtures:
		for match in fixture:
			equipo_fav = ''

			if 1 < match[2]:
				equipo_fav = match[0][0]
			elif match[2] < 0:
				equipo_fav = match[1][0]
				match[2] = 1

			if equipo_fav is not '':
				if equipo_fav in favoritos.keys():
					favoritos[equipo_fav] += match[2]
				else:
					favoritos[equipo_fav] = match[2]

	return favoritos


lectura = lee_fichero('./data/fixtures.csv')
fixtures = fixture(lectura)
check_fixtures(fixtures)
predictions = predict(fixtures)
favoritos = favoritos(fixtures)

for prediction in predictions:
	print('############')
	for p in prediction:
		print(p)

print('############')
for k,v in favoritos.items():
	print(k, v)