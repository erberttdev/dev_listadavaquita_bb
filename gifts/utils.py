import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

def scrape_product_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        hostname = urlparse(url).hostname

        if 'amazon.com.br' in hostname:
            return _scrape_amazon(soup, url)
        else:
            logger.warning(f"Scraping não suportado para o domínio: {hostname}")
            return {'error': 'Loja não suportada'}

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar URL {url}: {e}")
        return {'error': f'Requisição falhou: {e}'}
    except Exception as e:
        logger.error(f"Erro ao fazer scraping da URL {url}: {e}")
        return {'error': f'Scraping falhou: {e}'}

def _scrape_amazon(soup, url):
    data = {'name': None, 'image_url': None, 'price': None, 'error': None}
    try:
        name_tag = soup.find('span', id='productTitle')
        if name_tag:
            data['name'] = name_tag.text.strip()
        else:
            logger.warning(f"Não foi possível encontrar o nome do produto na Amazon: {url}")

        image_container = soup.find('div', id='imgTagWrapperId')
        if image_container:
            img_tag = image_container.find('img')
            if img_tag and img_tag.get('src'):
                if img_tag.get('data-a-dynamic-image'):
                    import json
                    try:
                        dynamic_images = json.loads(img_tag['data-a-dynamic-image'])
                        if dynamic_images:
                            data['image_url'] = list(dynamic_images.keys())[-1]
                    except (json.JSONDecodeError, IndexError, KeyError) as json_err:
                        logger.warning(f"Erro ao parsear JSON da imagem dinâmica da Amazon: {url}, fallback. Erro: {json_err}")
                        data['image_url'] = img_tag.get('src')
                else:
                    data['image_url'] = img_tag.get('src')

        if not data['image_url']:
            landing_image = soup.find('img', id='landingImage')
            if landing_image and landing_image.get('src'):
                data['image_url'] = landing_image.get('src')

        price_selectors = [
            'span.a-offscreen',
            'span.a-price span.a-offscreen',
            'span#priceblock_ourprice',
            'span#priceblock_dealprice',
            'span.a-price-whole',
            'span.a-color-price',
            'span.a-text-price span.a-offscreen',
            'span[data-a-color="price"]'
        ]

        for selector in price_selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price_text = price_tag.text.strip()
                if 'R$' in price_text:
                    try:
                        price_text = price_text.replace('R$', '').replace('.', '').replace(',', '.').strip()
                        data['price'] = float(price_text)
                        break
                    except ValueError:
                        continue

        if data['price'] is None:
            meta_price = soup.find('meta', {'property': 'og:price:amount'})
            if meta_price and meta_price.get('content'):
                try:
                    data['price'] = float(meta_price.get('content').replace(',', '.'))
                except ValueError:
                    pass

        if data['price'] is None:
            import re
            price_pattern = re.compile(r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)')
            for elem in soup.select('span, div, p'):
                if 'R$' in elem.text:
                    match = price_pattern.search(elem.text)
                    if match:
                        try:
                            price_str = match.group(1).replace('.', '').replace(',', '.')
                            data['price'] = float(price_str)
                            break
                        except ValueError:
                            continue

        missing = []
        if data['name'] is None: missing.append('nome')
        if data['image_url'] is None: missing.append('imagem')
        if data['price'] is None: missing.append('preço')

        if missing:
            data['error'] = f'Não foi possível extrair {", ".join(missing)} da Amazon.'
            logger.warning(f"Falha ao extrair dados da Amazon: {url}")

    except Exception as e:
        logger.error(f"Erro ao processar página da Amazon {url}: {e}")
        data['error'] = f'Erro ao processar página da Amazon: {e}'

    return data
