from typing import Union
import requests
import re
import os
from bs4 import BeautifulSoup
from fastapi import FastAPI


class Api:

    def __init__(self):
        self.app = FastAPI()
        self.source_url = 'http://vitibrasil.cnpuv.embrapa.br'

        def handle_csv(year, opt, sub_opt):
            file_path = "src/database/temp_files/"
            sopt = ""
            if sub_opt:
                sopt = f"_subopt_{sub_opt}([^ ]+|)"
            pattern = re.compile(f"{opt}([^ ]+|){sopt}.csv")
            print(f"pattern {pattern}")
            for fp in os.listdir(file_path):
                print(f"fp [{fp}]")
                match = pattern.match(fp)
                print(f"match {match}")
                found = False
                if match:
                    print(f"O CSV correspondente [{fp}] existe, tamanho [{os.path.getsize(file_path)}]")
                    response = {}
                    header=""
                    idx=0
                    sum=0
                    with open(f"{file_path}{fp}", 'rb') as f:
                        lines = f.readlines()
                        for l in lines:
                            print(f"l {l}")
                            if not header:
                                header = l
                                print(f"header {re.split("[;,\t]", header.decode())}")
                                idx = re.split("[;,\t]", header.decode()).index(f"{year}")
                                print(f"idx {idx}")
                                response["Produto"] = "Quantidade (L.)"
                            else:
                                response[re.split("[;,\t]", l.decode())[2].strip()]=re.split("[;,\t]", l.decode())[idx]
                                value = "0"
                                if re.split("[;,\t]", l.decode())[1] != re.split("[;,\t]", l.decode())[2]:
                                    sum = sum + int(re.split("[;,\t]", l.decode())[idx])
                        response["Total"] = str(sum)
                        print(f"response {response}")
                    found = True
                if found:
                    return response

        def handle_html(content):
            soup = BeautifulSoup(content)
            table = soup.find("table", attrs={"class":"tb_base tb_dados"})

            # The first tr contains the field names.
            headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]

            datasets = {}
            datasets[headings[0]] = headings[1]
            for row in table.find_all("tr")[1:]:
                line = [td.get_text().strip() for td in row.find_all("td")]
                datasets[line[0].strip()] = line[1].replace(".", "").replace("-", "0")
            
            print(f"{datasets}")
            return datasets

        def save_to_db(response):
            print("SAVE")


        @self.app.get("/")
        async def read_root():
            return {"API": "V1"}
        
        @self.app.get("/producao")
        async def get_producao(ano: int):
            try:
                url = f"{self.source_url}/index.php?opcao=opt_02"
                if ano:
                    url = url + f"&ano={str(ano)}" 

                response = requests.get(url)
                response.raise_for_status()
                response = handle_html(response.content)
            except requests.RequestException as e:
                response = handle_csv(ano, "opt_02", "")
                if not response:
                    print(f'\nURL [{url}] \nERRO: [{e}]\n')
                    return None                

            save_to_db(response)

            return response

        @self.app.get("/processamento")
        async def get_processamento(sub_opcao: str, ano: int):
            try:
                print(f"sub_opcao {sub_opcao}")
                url = f"{self.source_url}/index.php?opcao=opt_03&subopcao=subopt_{sub_opcao}"
                if ano:
                    url = url + f"&ano={str(ano)}" 

                response = requests.get(url)
                response.raise_for_status()
                #raise requests.RequestException
                response = handle_html(response.content)
                return response
            except requests.RequestException as e:
                response = handle_csv(ano, "opt_03", sub_opcao)
                if not response:
                    print(f'\nURL [{url}] \nERRO: [{e}]\n')
                    return None                

            return response

        @self.app.get("/comercializacao")
        async def get_comercializacao(ano: int):
            try:
                url = f"{self.source_url}/index.php?opcao=opt_04"
                if ano:
                    url = url + f"&ano={str(ano)}" 

                response = requests.get(url)
                response.raise_for_status()
                #raise requests.RequestException
                response = handle_html(response.content)
                return response
            except requests.RequestException as e:
                response = handle_csv(ano, "opt_04", "")

            return response

        @self.app.get("/importacao")
        async def get_importacao(ano: int, sub_opcao: str = ""):
            try:
                print(f"sub_opcao {sub_opcao}")
                url = f"{self.source_url}/index.php?opcao=opt_05"
                if sub_opcao:
                    url = url + f"&subopcao=subopt_{sub_opcao}" 
                if ano:
                    url = url + f"&ano={str(ano)}" 

                response = requests.get(url)
                response.raise_for_status()
                #raise requests.RequestException
                response = handle_html(response.content)
                return response
            except requests.RequestException as e:
                response = handle_csv(ano, "opt_05", sub_opcao)
                if not response:
                    print(f'\nURL [{url}] \nERRO: [{e}]\n')
                    return None                

            return response
        
        @self.app.get("/exportacao")
        async def get_exportacao(sub_opcao: str, ano: int):
            try:
                print(f"sub_opcao {sub_opcao}")
                url = f"{self.source_url}/index.php?opcao=opt_06&subopcao=subopt_{sub_opcao}"
                if ano:
                    url = url + f"&ano={str(ano)}" 

                response = requests.get(url)
                response.raise_for_status()
                #raise requests.RequestException
                response = handle_html(response.content)
                return response
            except requests.RequestException as e:
                response = handle_csv(ano, "opt_06", sub_opcao)
                if not response:
                    print(f'\nURL [{url}] \nERRO: [{e}]\n')
                    return None                

            return response
        
server = Api()