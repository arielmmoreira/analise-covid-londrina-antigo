# Análise Covid Londrina
Este projeto tem como objetivo fazer um levantamento da situação da covid-19 no município de Londrina. Através do site da prefeitura extraímos alguns dados e passamos por um tratamento que será detalhado logo abaixo.

## Projeto

### 1ª Etapa
O projeto consiste em duas etapas. Primeiro é feito um web scraping através do selenium driver, usando python


    driver = webdriver.Chrome(r'C:\chromedriver/chromedriver.exe')
    driver.get("https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482")
    time.sleep(10)
    itens = driver.find_elements_by_xpath("//*[@id='ember160']/margin-container/full-container")
    time.sleep(10)
    
As funções time.sleep() são para dar o tempo de carregamento necessário.
Após criar as variáveis necessárias iremos separar os dados dos casos por bairros, como mostrado no site da prefeitura.

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
                
Ao final desse código temos um dicionário em que as 'keys' são os bairros e os 'values' sao o número de casos de covid. 
Por fim passamos toda essa informação para um arquivo no formato csv

    # Escrever um arquivo csv baseado no dicionário criado
    a_file = open("total.csv", "w")
    writer = csv.writer(a_file)
    writer.writerow(["Bairro", "Casos"])
    for key, value in total.items():
        writer.writerow([key, value])
    a_file.close()
    
### 2ª Etapa
Com o arquivo csv em mãos, iremos usar o pandas, atraves do jupyter notebook, para criar uma tabela e um gráfico para uma melhor visualização dos dados. Para uma melhor visualização acesse o arquivo "covid.ipynb".
Em resumo, criamos uma tabela através desse codigo:
 
    total_df = pd.read_csv('total.csv', encoding='ISO-8859-1')
    total_df = total_df.sort_values("Casos", ascending=False)
    
Em seguida preparamos os dados para gerar o gráfico

    bairro = total_df["Bairro"]
    casos = total_df["Casos"]
    total_df = total_df.sort_values("Casos")
    total_df.plot.barh("Bairro", figsize=(100, 200), fontsize=130)
    
    
## Passos seguintes
Baseado em alguns trabalhos (citados na referência) queremos entender se a cidade de Londrina segue um certo padrão observado em outros lugares: a relação de casos e mortes por covid com a situação socioeconômica.
Para isso é preciso coletar mais alguns dados, como por exemplo:
1. Mortes por bairro
2. População total de cada bairro
3. Condições de tratamento das pessoas que foram a óbito

## Referências
https://drive.google.com/file/d/1tSU7mV4OPnLRFMMY47JIXZgzkklvkydO/view
http://repositorio.ipea.gov.br/bitstream/11058/10155/1/NT_72_Diset_AspecSocioeconCOVID-19RJ.pdf