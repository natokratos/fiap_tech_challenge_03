from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import glob
import shutil
import platform 
import time
import datetime

class Scrapper:

    def __init__(self):
        self.source_url = 'https://sistemaswebb3-listados.b3.com.br/indexPage'
        #self.source_url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'

    def download_data(self, url):
        '''
        Realizar a requisição HTTP e retornar o conteúdo
        '''

        print(f"Plataforma [{platform.system()}] ...")

        if "Linux" in platform.system():
            service = Service(executable_path="./geckodriver-linux")
        elif "Windows" in platform.system():
            service = Service(executable_path="./geckodriver.exe")
        else:
            service = Service(executable_path="./geckodriver")

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url) 
        elems = driver.find_elements(By.XPATH,  "//*[contains(@href, 'indexPage/')]")
        try:
            content = {}
            for elem in elems:
                if not elem.get_attribute('href').endswith("indexPage/"):
                    content[elem.text] = elem.get_attribute('href')
                    #content[elem.text.replace(' ','_').replace('-','').replace('.','').replace('ª','')] = elem.get_attribute('href')
            driver.quit()
            return content
        except Exception as e:
            print(f"Exception {repr(e)}")
            driver.quit()
            return None

    def download_csv(self, download_url, folder_path, file_name):

        '''
        Realizar o download e escrita do CSV
        '''

        print(f"Plataforma [{platform.system()}] ...")
        print(f"Baixando [{download_url}] ...")

        if "Linux" in platform.system():
            service = Service(executable_path="./geckodriver-linux")
        elif "Windows" in platform.system():
            service = Service(executable_path="./geckodriver.exe")
        else:
            service = Service(executable_path="./geckodriver")

        options = Options()
        options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        abs_folder = os.path.abspath("temp_files")
        options.set_preference("browser.download.dir", abs_folder + "/downloaded")
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

        driver = webdriver.Firefox(service=service, options=options)
        try:
            driver.get(download_url)

            element = driver.find_element(By.XPATH, "//div[@class='backdrop']")
            driver.execute_script("arguments[0].remove", element)
            driver.refresh()
        except NoSuchElementException as e:
            print(f"O div backdrop nao existe, continuando ...")

        try:
            driver.get(download_url) 

            a_text = file_name.split('-')
            if len(a_text) > 1:
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='card-menu menu-vertical']//ul[@class='nav flex-column menu-vertical']//li[@class='nav-item']//a[contains(text(),'{a_text[0]}')]//span[contains(text(),'-{a_text[1]}')]"))
                )
            else:
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@class='card-menu menu-vertical']//ul[@class='nav flex-column menu-vertical']//li[@class='nav-item']//a[contains(text(),'{a_text[0]}')]"))
                )
            driver.execute_script("arguments[0].click(); return true;", element)

            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='content']//p[@class='primary-text']//a[contains(text(),'Download')]"))
            )            
            driver.execute_script("arguments[0].click(); return true;", element)
            time.sleep(10)

            now = datetime.datetime.now()
            directory = f"{now.strftime(f'%Y%m%d')}/"
            isExist = os.path.exists(f"{abs_folder}/{directory}")
            if not isExist:
                os.makedirs(f"{abs_folder}/{directory}")
            src_files = glob.glob(f"{abs_folder}/downloaded/*")
            for files in src_files:
                print(f"Movendo os arquivos de [{files}] para [{files.replace("downloaded/",f"{directory}")}] ...")
                shutil.copy(files, f"./temp_files/{directory}")
                lines = open(files.replace("downloaded/",f"{directory}"), encoding="ISO-8859-1").readlines()
                with open(files.replace("downloaded/",f"{directory}"), 'w') as f:
                    f.writelines(lines[1:])
                os.remove(files)
            
            driver.quit()
            return glob.glob(f"{abs_folder}/{directory}*")
        except Exception as e:
            print(f"Exception {repr(e)}")
            driver.quit()
            return None

    def run(self):

        print(f"Baixando os dados da B3 ...\n")
        data= self.download_data(self.source_url + "/theorical/IBOV?language=pt-br")

#https://sistemaswebb3-listados.b3.com.br/indexPage/theorical/IBOV?language=pt-br
#https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br
        content = ""
        for d in data:
            if d != "Download":
                print(f"[{d}] [{data[d]}]")
                file_name = f"{d}"
                if "-" not in d:
                    file_name = f"{d} -"
                file_path = './temp_files'
                print(f"Download CSV [{d}] ...")
                content = self.download_csv(data[d], file_path, file_name)

        print(f"{content}\n")

        #dest_files = glob.glob(f"temp_files/*") # * means all if need specific format then *.csv

        return content