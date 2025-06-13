import requests
from bs4 import BeautifulSoup

def scrape_product_data(url):
    """
    Tenta extrair dados do produto a partir do link informado.
    Retorna um dicionário com os campos:
    - name: nome do produto
    - photo: url da foto do produto
    - price: preço do produto (Decimal)
    - store_name: nome da loja
    - store_type: tipo da loja ('online' ou 'physical')
    Retorna None se não for possível extrair os dados.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Exemplo genérico: tentar extrair título, imagem e preço
        # Isso deve ser adaptado para sites específicos conforme necessário

        # Nome do produto
        name_tag = soup.find('meta', property='og:title')
        name = name_tag['content'] if name_tag else None

        # Foto do produto
        photo_tag = soup.find('meta', property='og:image')
        photo = photo_tag['content'] if photo_tag else None

        # Preço do produto
        price = None
        price_tag = soup.find('meta', property='product:price:amount')
        if price_tag:
            try:
                price = float(price_tag['content'])
            except:
                price = None

        # Nome da loja
        store_name = None
        store_tag = soup.find('meta', property='og:site_name')
        if store_tag:
            store_name = store_tag['content']

        # Tipo da loja - assumindo online para scraping
        store_type = 'online'

        if name and price is not None:
            return {
                'name': name,
                'photo': photo,
                'price': price,
                'store_name': store_name,
                'store_type': store_type,
            }
        else:
            return None

    except Exception as e:
        return None
