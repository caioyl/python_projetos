import zipfile
import xml.etree.ElementTree as ET
import csv
import pandas as pd
from unidecode import unidecode

# Baixar o arquivo do link abaixo e substituí-lo pelo diretório local do arquivo
# https://github.com/caioyl/python_projetos/blob/main/conversor_kmz_csv/dados/estacaometro.kmz
# Nome do arquivo KMZ
kmz_filename = "C:\estacaometro.kmz"

# Extraindo o conteúdo do arquivo KMZ
with zipfile.ZipFile(kmz_filename, 'r') as kmz:
    # Procurar pelo arquivo KML dentro do KMZ
    # Adiciona o KML na variável kml_filename caso o elemento iterado
    # na lista do kmz tenha como extensão "kml" (só tem um elemento)
    kml_filename = [name for name in kmz.namelist() if name.lower().endswith('.kml')][0]
    # Ler o conteúdo do arquivo KML
    with kmz.open(kml_filename) as kml_file:
        kml_content = kml_file.read()

# Analisando o XML do KML para extrair as coordenadas
tree = ET.ElementTree(ET.fromstring(kml_content))
coordinates = []

# Encontrando todos os elementos "coordinates" no XML
for elem in tree.iter():
    if 'coordinates' in elem.tag:
        coordinates.extend(elem.text.strip().split())

# Separando as coordenadas e escrevendo em um arquivo CSV
csv_filename = 'coordenadas.csv'
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Latitude', 'Longitude'])

    for coord in coordinates:
        lng, lat, _ = coord.split(',')
        csv_writer.writerow([float(lat), float(lng)])

print('Coordenadas extraídas e salvas em', csv_filename)

# Importação

# Baixar o arquivo do link abaixo e substituí-lo pelo diretório local do arquivo
# https://github.com/caioyl/python_projetos/blob/main/conversor_kmz_csv/dados/estacoes_metro.csv
estacoes = pd.read_csv("C:\estacoes_metro.csv")
coordenadas = pd.read_csv('coordenadas.csv')

# Função para substituir caracteres acentuados
def remover_acentos(texto):
    return unidecode(texto)

# Aplicando a função à coluna 'Nomes'
estacoes['emt_nome'] = estacoes['emt_nome'].apply(remover_acentos).str.replace(' ','_')

# Concatenação horizontal
df = pd.concat([estacoes, coordenadas],axis=1)

# Conversão para csv
df.to_csv('estacoes_metro_coordenadasUTM.csv',index=False)

df