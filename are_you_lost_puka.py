# -*- coding: utf-8 -*-

import pandas as pd
import folium
import json
import urllib.request
from folium.plugins import MarkerCluster
import datetime

"""Liste d'objets"""

dateNow = datetime.datetime.now()
year = str(dateNow.year)
month = str(dateNow.strftime("%m"))
urlObjets = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/objets-trouves-gares/exports/json?lang=fr&refine=date%3A%22"+year+"%2F"+month+"%22&timezone=Europe%2FBerlin"

resp = urllib.request.urlopen(urlObjets)
dataObjets = json.loads(resp.read())

with open('dataObjets.json', 'w') as fw:
  json.dump(dataObjets, fw)

with open('dataObjets.json') as json_file:
  dataObjets = json.load(json_file)

dfObjets = pd.json_normalize(dataObjets)
dfObjets = dfObjets[['date', 'gc_obo_nature_c', 'gc_obo_gare_origine_r_code_uic_c']]
dfObjets = dfObjets.rename(columns={'gc_obo_nature_c' : 'Objet', 'date': 'Date', 'gc_obo_gare_origine_r_code_uic_c':'UIC'})

"""Gares"""

urlGares = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/referentiel-gares-voyageurs/exports/json?lang=fr&timezone=Europe%2FBerlin"
response = urllib.request.urlopen(urlGares)
dataGares = json.loads(response.read())

with open('dataGares.json', 'w') as fw:
  json.dump(dataGares, fw)

with open('dataGares.json') as json_file:
  dataGares = json.load(json_file)


dfGares = pd.json_normalize(dataGares)
dfGares = dfGares[['uic_code', 'alias_libelle_noncontraint', 'departement_numero', 'wgs_84.lon', 'wgs_84.lat']]
dfGares = dfGares.rename(columns={'uic_code':'UIC', 'alias_libelle_noncontraint':'Gare', 'departement_numero' : 'Departement', 'wgs_84.lon': 'Longitude', 'wgs_84.lat': 'Latitude'})
dfGares = dfGares.dropna(subset=['Latitude'])

"""Both"""

#Merge dfObjets and dfGares
dfBoth = pd.merge(dfObjets, dfGares, on='UIC')

#Counting total number of objects in each gare (first view)
dfBoth['Count'] = dfBoth.groupby(['Gare', 'Objet'])['Date'].transform('count')

dfBoth['Total'] = dfBoth.groupby('Gare')['Objet'].transform('count')

dfObjetsInGare = dfBoth[['UIC', 'Gare', 'Total', 'Latitude', 'Longitude', 'Departement']].drop_duplicates()

# print(dfObjetsInGare)

#Table to show nb of lost objects
dfObjetsSpecificGare = dfBoth[['UIC', 'Gare', 'Objet', 'Count']].drop_duplicates()

def makeList(station):
  listeObjets = pd.DataFrame()
  for i, gare in dfObjetsSpecificGare.iterrows():
    if gare['UIC'] == station:
      x = pd.DataFrame({
        'Objet': gare['Objet'],
        'Count': gare['Count']
      }, index=[0])
      listeObjets = pd.concat([listeObjets, x])
    else:
      continue
  listeObjets.sort_values(by=['Count'], ascending=False, inplace=True)
  return listeObjets

def fullList(station):
  liste = makeList(station)
  return(liste.to_html(classes="table table-striped table-hover table-responsive", index=False, justify='left'))

"""Map"""
mapGare = folium.Map(location=[dfObjetsInGare.Latitude.mean(), dfObjetsInGare.Longitude.mean()], tiles="Cartodb Positron", zoom_start=6, control_scale=True)
mapGare._name = "map_gare"
mapGare._id = '123'
print(mapGare.get_name())

marker_cluster = MarkerCluster(
    name='Clustered Gares',
    overlay=True,
    control=False,
    icon_create_function=None
)

for index, location_info in dfObjetsInGare.iterrows():
  gare = 'style="text-align:center; font-weight: bold;">SNCF ' + str(location_info['Gare'])
  url = "https://lost-objects-map.onrender.com/gare/" + str(location_info['UIC'])
  
  #TODO: fix url_for problem & replace the string
  
  html = '<div style="position:relative; width: 500px; min-height:300px; max-height:1000px"><h3 '+gare + '''</h3><iframe
  id="inlineFrameExample"
  title="Inline Frame Example"
  style="position: absolute; width:100%;height:90%;padding: 1px;"
  src="''' + url + '''">
  </iframe></div>'''
  
  tt = '<h4 '+gare + '</h4><h5 style=\"text-align:center\">Objets trouvés: ' + str(location_info['Total']) + '</h5>'
  marker = folium.Marker([location_info["Latitude"], location_info["Longitude"]],
                tooltip='<div style=\"margin:0px 1px\">{}</div>'.format(tt),
                popup=folium.Popup(html, lazy=True),
                parse_html=True)
  marker_cluster.add_child(marker)

marker_cluster.add_to(mapGare)

mapGare.save("./templates/output.html")