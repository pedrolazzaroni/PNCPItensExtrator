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

def extrair_uf_pncp(driver):
    """
    Extrai a UF (Unidade Federativa) da página do PNCP
    """
    try:
        # Aguarda mais tempo para garantir que a página carregou completamente
        time.sleep(8)
        
        print("Iniciando extração da UF...")
        
        # Método 1: Busca todos os spans com classe ng-star-inserted que contêm barra
        try:
            print("Método 1: Procurando spans com ng-star-inserted que contêm barra...")
            spans = driver.find_elements(By.XPATH, "//span[contains(@class, 'ng-star-inserted') and contains(text(), '/')]")
            print(f"Encontrados {len(spans)} spans com ng-star-inserted e barra")
            
            for i, span in enumerate(spans):
                texto = span.text.strip()
                print(f"Span {i+1}: '{texto}'")
                
                if '/' in texto:
                    partes = texto.split('/')
                    if len(partes) >= 2:
                        possivel_uf = partes[-1].strip()
                        # Verifica se parece com UF (2 caracteres, letras)
                        if len(possivel_uf) == 2 and possivel_uf.isalpha():
                            print(f"UF encontrada pelo Método 1: '{possivel_uf}'")
                            return possivel_uf.upper()
        except Exception as e1:
            print(f"Método 1 falhou: {e1}")
          # Método 2: Busca especificamente por texto que contém "Local:" no HTML
        try:
            print("Método 2: Procurando elementos que contêm 'Local:'...")
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Local:')]")
            print(f"Encontrados {len(elements)} elementos com 'Local:'")
            
            for i, element in enumerate(elements):
                texto_completo = element.text.strip()
                print(f"Elemento {i+1}: '{texto_completo}'")
                
                if '/' in texto_completo:
                    # Extrai a parte após "Local:" 
                    if 'Local:' in texto_completo:
                        local_part = texto_completo.split('Local:')[-1].strip()
                        if '/' in local_part:
                            uf = local_part.split('/')[-1].strip()
                            if len(uf) == 2 and uf.isalpha():
                                print(f"UF encontrada pelo Método 2: '{uf}'")
                                return uf.upper()
        except Exception as e2:
            print(f"Método 2 falhou: {e2}")
        
        # Método 2.5: Debug - Lista TODOS os spans para entender o que está na página
        try:
            print("Método 2.5 (Debug): Listando TODOS os spans da página...")
            all_spans = driver.find_elements(By.XPATH, "//span")
            print(f"Total de spans encontrados: {len(all_spans)}")
            
            for i, span in enumerate(all_spans[:20]):  # Mostra apenas os primeiros 20
                texto = span.text.strip()
                classe = span.get_attribute('class')
                if texto:  # Só mostra spans com texto
                    print(f"Span {i+1}: Classe='{classe}' | Texto='{texto}'")
                    
                    # Se encontrar algum span com barra, tenta extrair UF
                    if '/' in texto:
                        partes = texto.split('/')
                        if len(partes) >= 2:
                            possivel_uf = partes[-1].strip()
                            if len(possivel_uf) == 2 and possivel_uf.isalpha():
                                print(f"*** UF encontrada no debug: '{possivel_uf}' ***")
                                return possivel_uf.upper()
        except Exception as e25:
            print(f"Método 2.5 falhou: {e25}")
        
        # Método 3: Busca por todos os spans que contêm barra (mais genérico)
        try:
            print("Método 3: Procurando todos os spans com barra...")
            spans = driver.find_elements(By.XPATH, "//span[contains(text(), '/')]")
            print(f"Encontrados {len(spans)} spans com barra")
            
            for i, span in enumerate(spans):
                texto = span.text.strip()
                print(f"Span {i+1}: '{texto}'")
                
                if '/' in texto:
                    partes = texto.split('/')
                    if len(partes) >= 2:
                        possivel_uf = partes[-1].strip()
                        # Verifica se parece com UF (2 caracteres, letras)
                        if len(possivel_uf) == 2 and possivel_uf.isalpha():
                            print(f"UF encontrada pelo Método 3: '{possivel_uf}'")
                            return possivel_uf.upper()
        except Exception as e3:
            print(f"Método 3 falhou: {e3}")
        
        # Método 4: Análise por regex no código fonte da página
        try:
            print("Método 4: Analisando código fonte da página...")
            page_source = driver.page_source
            
            # Procura por padrão: cidade/UF onde UF são 2 letras maiúsculas
            padrao = r'(\w+)/([A-Z]{2})\b'
            matches = re.findall(padrao, page_source)
            
            # Lista de UFs válidas do Brasil
            ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
            
            print(f"Encontrados {len(matches)} padrões cidade/UF")
            for cidade, uf in matches:
                print(f"Padrão: {cidade}/{uf}")
                if uf in ufs_validas:
                    print(f"UF válida encontrada pelo Método 4: '{uf}'")
                    return uf
        except Exception as e4:
            print(f"Método 4 falhou: {e4}")
        
        print("Todos os métodos falharam ao extrair a UF")
        return None
            
    except Exception as e:
        print(f"Erro geral ao extrair UF: {e}")
        return None

def extrai_itens_pncp(url):
    print(f"Acessando URL: {url}")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    itens = []
    uf = None
    
    try:
        # Primeiro extrai a UF da página
        uf = extrair_uf_pncp(driver)
        
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
                    'valor_total': cells[4].text.strip(),
                    'uf': uf  # Adiciona a UF ao item
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
                        break  # Última página
                    
                    # Se ainda há mais itens, tenta clicar no botão próxima página
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
    # Pergunta ao usuário a partir de qual data ele quer buscar
    data_inicio = input("Digite a data de inclusão inicial (formato YYYY-MM-DD, ex: 2024-05-25): ").strip()
    
    # Valida o formato da data
    try:
        from datetime import datetime
        datetime.strptime(data_inicio, '%Y-%m-%d')
    except ValueError:
        print("Formato de data inválido! Use o formato YYYY-MM-DD")
        return
    
    conn = pymysql.connect(host='localhost', user='root', password='', db='ataspncp', charset='utf8mb4')
    cur = conn.cursor()    # Cria a tabela de itens se não existir apenas com campos essenciais
    cur.execute('''CREATE TABLE IF NOT EXISTS atas_itens_pncp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ata_id INT,
        numero VARCHAR(20),
        descricao TEXT,
        quantidade VARCHAR(20),
        valor_unitario VARCHAR(50),
        valor_total VARCHAR(50),
        uf VARCHAR(2),
        numeroControlePNCPAta VARCHAR(100),
        numeroControlePNCPCompra VARCHAR(100)
    )''')
    
    # Seleciona apenas as atas com dataInclusao posterior à data informada
    # Converte a data para incluir o horário completo (23:59:59) para pegar tudo do dia seguinte em diante
    data_inicio_completa = f"{data_inicio} 23:59:59"
    print(f"Buscando atas com dataInclusao posterior a {data_inicio} (depois das 23:59:59)...")
    cur.execute("""SELECT id, numeroControlePNCPAta, numeroControlePNCPCompra 
                   FROM atas_pncp WHERE dataInclusao > %s ORDER BY dataInclusao ASC""", (data_inicio_completa,))
    
    atas = cur.fetchall()
    for ata in atas:
        (ata_id, numeroControlePNCPAta, numeroControlePNCPCompra) = ata
        
        url = get_pncp_url(numeroControlePNCPCompra)
        if not url:
            print(f"Formato inválido: {numeroControlePNCPCompra}")
            continue
            
        print(f"Extraindo itens de {url}")
        itens = extrai_itens_pncp(url)
        for item in itens:
            print(f"Item extraído: Número: {item['numero']}, Descrição: {item['descricao']}, Quantidade: {item['quantidade']}, Valor Unitário: {item['valor_unitario']}, Valor Total: {item['valor_total']}, UF: {item['uf']}")
            cur.execute('''INSERT INTO atas_itens_pncp (
                ata_id, numero, descricao, quantidade, valor_unitario, valor_total, uf,
                numeroControlePNCPAta, numeroControlePNCPCompra
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (ata_id, item['numero'], item['descricao'], item['quantidade'], item['valor_unitario'], item['valor_total'], item['uf'],
                 numeroControlePNCPAta, numeroControlePNCPCompra))
        
        conn.commit()
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
