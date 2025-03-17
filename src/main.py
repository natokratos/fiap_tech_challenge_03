import os 

from scrapper import Scrapper
from aws_s3 import AwsS3

def run():

    '''
    Execução do scrapper para extracao dos dados
    '''
    
    scraper = Scrapper()

    dest_files = scraper.run()

    for f in dest_files:
        if "Dia_" in f and ".parquet" not in f:
            aws_s3 = AwsS3()
            aws_s3.upload_file("dados-brutos", f)

if __name__ == '__main__':

    run()
