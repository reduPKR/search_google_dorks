import sys
import time
import requests
from bs4 import BeautifulSoup
import argparse
import urllib.parse

def dork_search(site, dork_file, delay):
  try:
    with open(dork_file, 'r') as f:
      num_dorks = sum(1 for line in f)
      f.seek(0)
      for i, line in enumerate(f):
        dork = line.strip()
        encoded_dork = urllib.parse.quote(dork)
        query_url = f"https://www.google.com/search?q=site:{site}+{encoded_dork}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        r = requests.get(query_url, headers=headers)
        if r.status_code == 200:
          soup = BeautifulSoup(r.text, 'html.parser')
          num_results = int(soup.select_one('#result-stats').text.split()[1].replace(',', ''))
          
          if num_results > 0:
            print(f"\033[32m{dork}: {num_results}\033[0m")
          else:
            print(f"\033[31m{dork}: {num_results}\033[0m")
          time.sleep(delay)
        else:
          print(f"Erro ao realizar consulta para a dork {dork}: status code {r.status_code}")
  except FileNotFoundError:
    print(f"Arquivo {dork_file} não encontrado.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("site", help="site a ser pesquisado")
  parser.add_argument("arquivo", help="arquivo com as dorks")
  parser.add_argument("-d", "--delay", type=int, default=10, help="delay entre as consultas em segundos")

  args = parser.parse_args()
  dork_search(args.site, args.arquivo, args.delay)
