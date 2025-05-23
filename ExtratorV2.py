# extrai_itens_pncp.py
import pymysql
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_pncp_url(numero_controle):
    # Exemplo: 01612781000138-1-000021/2022
    match = re.match(r"(\d+)-\d+-(\d+)/(\d+)", numero_controle)
    if not match:
        return None
    cnpj, edital, ano = match.groups()
    return f"https://pncp.gov.br/app/editais/{cnpj}/{ano}/{int(edital)}"

def extrai_itens_pncp(url):
    print(f"Acessando URL: {url}")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    itens = []
    try:
        print("Procurando aba 'Itens'...")
        try:
            itens_tab = driver.find_element(By.XPATH, "//li[contains(@class, 'tab-item')]//span[contains(text(), 'Itens')]/ancestor::button")
            print("Botão da aba 'Itens' encontrado. Clicando...")
            itens_tab.click()
            time.sleep(2)
        except Exception as e:
            print("Botão da aba 'Itens' não clicável ou já ativa.")
        print("Esperando tabela de itens aparecer...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//ngx-datatable"))
        )
        print("Tabela de itens encontrada.")
        # Descobre o total de itens
        pag_info = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination-information')]").text
        total_itens = int(re.search(r'de (\d+) itens', pag_info).group(1))
        print(f"Total de itens na tabela: {total_itens}")
        itens_coletados = 0
        while True:
            rows = driver.find_elements(By.XPATH, "//ngx-datatable//datatable-body-row")
            print(f"Coletando página, linhas encontradas: {len(rows)}")
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//datatable-body-cell")
                if len(cells) < 6:
                    continue
                item = {
                    'numero': cells[0].text.strip(),
                    'descricao': cells[1].text.strip(),
                    'quantidade': cells[2].text.strip(),
                    'valor_unitario': cells[3].text.strip(),
                    'valor_total': cells[4].text.strip()
                }
                # Filtro para evitar itens vazios
                if not any([item['numero'], item['descricao'], item['quantidade'], item['valor_unitario'], item['valor_total']]):
                    continue  # pula itens totalmente vazios
                if not item['descricao']:
                    continue  # pula itens sem descrição
                print(f"Item encontrado: {item}")
                itens.append(item)
            # Verifica paginação pelo texto do footer
            try:
                pag_info = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination-information')]").text
                match = re.search(r'(\d+)-(\d+) de (\d+) itens', pag_info)
                if match:
                    first_item, last_item, total_itens = map(int, match.groups())
                    print(f"Página: exibindo {first_item}-{last_item} de {total_itens} itens")
                    if last_item >= total_itens:
                        break  # Última página                    # Se ainda há mais itens, tenta clicar no botão próxima página
                    try:
                        # Primeiro tenta encontrar o botão de próxima página
                        next_btn = driver.find_element(By.XPATH, "//button[@id='btn-next-page']")
                        
                        # Verifica se o botão está habilitado
                        is_disabled = next_btn.get_attribute('disabled')
                        if is_disabled:
                            print("Botão próxima página está desabilitado, mas deveria haver mais itens.")
                            break
                        
                        print(f"Tentando clicar no botão próxima página...")
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                        time.sleep(1)
                        
                        # Salva o valor do último item antes de clicar
                        last_item_before = last_item
                        
                        # Clica usando JavaScript para maior confiabilidade
                        driver.execute_script("arguments[0].click();", next_btn)
                        
                        # Aguarda até que o número do último item exibido mude
                        page_changed = False
                        for attempt in range(15):
                            time.sleep(1)
                            try:
                                pag_info_new = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination-information')]").text
                                match_new = re.search(r'(\d+)-(\d+) de (\d+) itens', pag_info_new)
                                if match_new:
                                    _, last_item_new, _ = map(int, match_new.groups())
                                    if last_item_new != last_item_before:
                                        print(f"Página avançou para: {pag_info_new}")
                                        page_changed = True
                                        break
                            except:
                                continue
                        
                        if not page_changed:
                            print("A página não avançou após clicar no botão. Encerrando.")
                            break
                            
                    except Exception as e:
                        print(f"Erro ao tentar clicar na próxima página: {e}")
                        break
                else:
                    print("Não foi possível interpretar a paginação, encerrando.")
                    break
            except Exception as e:
                print(f"Erro ao ler paginação: {e}")
                break
        driver.quit()
        return itens
    except Exception as e:
        print(f"Erro ao extrair itens: {e}")
        driver.quit()
        return []

def main():
    conn = pymysql.connect(host='localhost', user='root', password='', db='ataspncp', charset='utf8mb4')
    cur = conn.cursor()
    # Cria a tabela de itens se não existir
    cur.execute('''CREATE TABLE IF NOT EXISTS atas_itens_pncp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ata_id INT,
        numero VARCHAR(20),
        descricao TEXT,
        quantidade VARCHAR(20),
        valor_unitario VARCHAR(50),
        valor_total VARCHAR(50)
    )''')
    # Seleciona os 10 primeiros registros da tabela atas_pncp
    cur.execute("SELECT id, numeroControlePNCPCompra FROM atas_pncp LIMIT 10")
    atas = cur.fetchall()
    for ata in atas:
        ata_id, numero_controle = ata
        url = get_pncp_url(numero_controle)
        if not url:
            print(f"Formato inválido: {numero_controle}")
            continue
        print(f"Extraindo itens de {url}")
        itens = extrai_itens_pncp(url)
        for item in itens:
            print(f"Item extraído: Número: {item['numero']}, Descrição: {item['descricao']}, Quantidade: {item['quantidade']}, Valor Unitário: {item['valor_unitario']}, Valor Total: {item['valor_total']}")
            cur.execute('''INSERT INTO atas_itens_pncp (ata_id, numero, descricao, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s, %s)''',
                (ata_id, item['numero'], item['descricao'], item['quantidade'], item['valor_unitario'], item['valor_total']))
        conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
