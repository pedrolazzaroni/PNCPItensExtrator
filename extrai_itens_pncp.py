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
        rows = driver.find_elements(By.XPATH, "//ngx-datatable//datatable-body-row")
        print(f"Total de linhas encontradas: {len(rows)}")
        for idx, row in enumerate(rows[:10]):
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
            # Detalhamento do item
            try:
                detalhar_buttons = driver.find_elements(By.XPATH, "//ngx-datatable//datatable-body-row//button[@aria-label='Detalhar']")
                if idx < len(detalhar_buttons):
                    detalhar_buttons[idx].click()
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal') and contains(@class, 'show')]"))
                    )
                    modal = driver.find_element(By.XPATH, "//div[contains(@class, 'modal') and contains(@class, 'show')]")
                    modal_text = modal.text
                    def extrai_modal_val(campo):
                        padrao = rf"{campo}: (.*)"
                        m = re.search(padrao, modal_text)
                        return m.group(1).strip() if m else ''
                    item['criterio_julgamento'] = extrai_modal_val('Critério de julgamento')
                    item['situacao'] = extrai_modal_val('Situação')
                    item['tipo'] = extrai_modal_val('Tipo')
                    item['categoria_leilao'] = extrai_modal_val('Categoria do item de leilão')
                    item['incentivo_produtivo'] = extrai_modal_val('Incentivo produtivo básico')
                    item['beneficio'] = extrai_modal_val('Benefício')
                    item['margem_preferencia_normal'] = extrai_modal_val('Margem de preferência normal')
                    item['margem_preferencia_adicional'] = extrai_modal_val('Margem de preferência adicional')
                    item['unidade_medida'] = extrai_modal_val('Unidade de medida')
                    item['valor_unitario_homologado'] = extrai_modal_val('Valor unitário homologado')
                    item['valor_total_homologado'] = extrai_modal_val('Valor total homologado')
                    item['quantidade_homologada'] = extrai_modal_val('Quantidade homologada')
                    item['fornecedor_cnpj'] = extrai_modal_val('CNPJ/CPF ou Nº de identificação do fornecedor')
                    item['fornecedor_nome'] = extrai_modal_val('Nome ou razão social do fornecedor')
                    item['porte_empresa'] = extrai_modal_val('Porte da empresa')
                    item['percentual_desconto'] = extrai_modal_val('Percentual de desconto aplicado ao critério de julgamento')
                    item['data_resultado_homologacao'] = extrai_modal_val('Data do resultado da homologação')
                    close_btn = modal.find_element(By.XPATH, ".//button[contains(@class, 'close') or contains(text(), 'Fechar')]")
                    close_btn.click()
                    time.sleep(1)
                else:
                    for k in ['criterio_julgamento','situacao','tipo','categoria_leilao','incentivo_produtivo','beneficio','margem_preferencia_normal','margem_preferencia_adicional','unidade_medida','valor_unitario_homologado','valor_total_homologado','quantidade_homologada','fornecedor_cnpj','fornecedor_nome','porte_empresa','percentual_desconto','data_resultado_homologacao']:
                        item[k] = ''
            except Exception as e:
                print(f"Erro ao detalhar item: {e}")
                for k in ['criterio_julgamento','situacao','tipo','categoria_leilao','incentivo_produtivo','beneficio','margem_preferencia_normal','margem_preferencia_adicional','unidade_medida','valor_unitario_homologado','valor_total_homologado','quantidade_homologada','fornecedor_cnpj','fornecedor_nome','porte_empresa','percentual_desconto','data_resultado_homologacao']:
                    item[k] = ''
            print(f"Item encontrado: {item}")
            itens.append(item)
    finally:
        driver.quit()
    return itens

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
        valor_total VARCHAR(50),
        criterio_julgamento VARCHAR(100),
        situacao VARCHAR(100),
        tipo VARCHAR(100),
        categoria_leilao VARCHAR(100),
        incentivo_produtivo VARCHAR(100),
        beneficio VARCHAR(100),
        margem_preferencia_normal VARCHAR(100),
        margem_preferencia_adicional VARCHAR(100),
        unidade_medida VARCHAR(100),
        valor_unitario_homologado VARCHAR(50),
        valor_total_homologado VARCHAR(50),
        quantidade_homologada VARCHAR(50),
        fornecedor_cnpj VARCHAR(50),
        fornecedor_nome VARCHAR(255),
        porte_empresa VARCHAR(100),
        percentual_desconto VARCHAR(50),
        data_resultado_homologacao VARCHAR(50)
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
