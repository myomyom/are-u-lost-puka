# # -*- coding: utf-8 -*-

# import pandas as pd
# import json
# import urllib.request
# import datetime

# """Liste d'objets"""

# dateNow = datetime.datetime.now()
# dateBefore = str(dateNow)
# year = str(dateNow.year)
# month = str(dateNow.strftime("%m"))
# urlObjets = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/objets-trouves-gares/exports/json?lang=fr&refine=date%3A%22"+year+"%2F"+month+"%22&timezone=Europe%2FBerlin"

# resp = urllib.request.urlopen(urlObjets)
# dataObjets = json.loads(resp.read())

# with open('dataObjets.json', 'w') as fw:
#   json.dump(dataObjets, fw)

# with open('dataObjets.json') as json_file:
#   dataObjets = json.load(json_file)

# dfObjets = pd.json_normalize(dataObjets)
# dfObjets = dfObjets[['date', 'gc_obo_nature_c', 'gc_obo_gare_origine_r_code_uic_c']]
# dfObjets = dfObjets.rename(columns={'gc_obo_nature_c' : 'Objet', 'date': 'Date', 'gc_obo_gare_origine_r_code_uic_c':'UIC'})

# """Gares"""

# urlGares = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/referentiel-gares-voyageurs/exports/json?lang=fr&timezone=Europe%2FBerlin"
# response = urllib.request.urlopen(urlGares)
# dataGares = json.loads(response.read())

# with open('dataGares.json', 'w') as fw:
#   json.dump(dataGares, fw)

# with open('dataGares.json') as json_file:
#   dataGares = json.load(json_file)


# dfGares = pd.json_normalize(dataGares)
# dfGares = dfGares[['uic_code', 'alias_libelle_noncontraint', 'departement_numero', 'wgs_84.lon', 'wgs_84.lat']]
# dfGares = dfGares.rename(columns={'uic_code':'UIC', 'alias_libelle_noncontraint':'Gare', 'departement_numero' : 'Departement', 'wgs_84.lon': 'Longitude', 'wgs_84.lat': 'Latitude'})
# dfGares = dfGares.dropna(subset=['Latitude'])