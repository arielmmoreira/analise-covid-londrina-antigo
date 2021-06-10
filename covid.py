from selenium import webdriver
import time, csv

# Criando as variáveis do driver
driver = webdriver.Chrome(r'C:\chromedriver/chromedriver.exe')
driver.get("https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482")
time.sleep(10)
itens = driver.find_elements_by_xpath("//*[@id='ember160']/margin-container/full-container")
time.sleep(10)

# Separa cada quebra de linha da string em um item de uma lista
lista = itens[0].text.split("\n")
lista.pop(0)
total = {}

# Loop sobre cada item da lista para pegar o total de casos por bairro
for item in lista:
    bairro = ""
    casos = ""
    for i, char in enumerate(item):
        if char == "-":
            bairro = item[:i - 1]
            casos = item[i + 2:-8]

    if bairro != "" and casos != "":
        if len(casos) > 3:
            casos = int(float(casos) * 1000)
            total[bairro] = casos
        else:
            total[bairro] = int(casos)

# Escrever um arquivo csv baseado no dicionário criado
a_file = open("total.csv", "w")
writer = csv.writer(a_file)
writer.writerow(["Bairro", "Casos"])
for key, value in total.items():
    writer.writerow([key, value])
a_file.close()
