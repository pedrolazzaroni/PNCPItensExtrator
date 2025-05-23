# PNCP Itens Extractor

## Descrição

O **PNCP Itens Extractor** é uma ferramenta automatizada desenvolvida em Python para extrair informações detalhadas de itens de editais/atas de licitação do Portal Nacional de Contratações Públicas (PNCP).

O sistema acessa automaticamente as páginas de editais no PNCP e extrai dados completos dos itens licitados, incluindo:
- Número do item
- Descrição detalhada
- Quantidade
- Valor unitário estimado
- Valor total estimado

## Funcionalidades

- **Extração Automatizada**: Utiliza Selenium WebDriver para navegar automaticamente pelas páginas do PNCP
- **Navegação por Paginação**: Percorre todas as páginas de itens quando há múltiplas páginas
- **Armazenamento em Banco**: Salva os dados extraídos em banco de dados MySQL
- **Tratamento de Erros**: Sistema robusto com tratamento de exceções
- **Modo Headless**: Execução silenciosa sem interface gráfica

## Estrutura do Projeto

```
PNCPItensExtrator/
├── ExtratorV1.py          # Versão básica (apenas primeira página)
├── ExtratorV2.py          # Versão completa (todas as páginas)
├── extrai_itens_pncp.py   # Versão mais recente com melhorias
└── README.md              # Este arquivo
```

## Pré-requisitos

### Software Necessário

- Python 3.7+
- Google Chrome Browser
- ChromeDriver
- MySQL Server
- XAMPP (recomendado para ambiente local)

### Bibliotecas Python

```bash
pip install selenium
pip install pymysql
pip install requests
pip install beautifulsoup4
```

## Configuração do Banco de Dados

1. Crie um banco de dados MySQL chamado `ataspncp`
2. Crie a tabela principal de atas:

```sql
CREATE TABLE atas_pncp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numeroControlePNCPCompra VARCHAR(100)
);
```

3. A tabela de itens será criada automaticamente pelo script:

```sql
CREATE TABLE atas_itens_pncp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ata_id INT,
    numero VARCHAR(20),
    descricao TEXT,
    quantidade VARCHAR(20),
    valor_unitario VARCHAR(50),
    valor_total VARCHAR(50)
);
```

## Como Usar

### 1. Preparação dos Dados

Insira os números de controle PNCP na tabela `atas_pncp`:

```sql
INSERT INTO atas_pncp (numeroControlePNCPCompra) VALUES 
('01612781000138-1-000021/2022'),
('02345678000190-1-000015/2023');
```

### 2. Execução do Script

Execute o extrator:

```bash
python ExtratorV2.py
```

### 3. Acompanhamento

O script irá:
1. Conectar ao banco de dados
2. Buscar os 10 primeiros registros da tabela `atas_pncp`
3. Para cada registro:
   - Gerar a URL do PNCP
   - Acessar a página do edital
   - Navegar para a aba "Itens"
   - Extrair todos os itens (navegando por todas as páginas se necessário)
   - Salvar os dados no banco

## Exemplo de Saída

```
Acessando URL: https://pncp.gov.br/app/editais/01612781000138/2022/21
Procurando aba 'Itens'...
Botão da aba 'Itens' encontrado. Clicando...
Tabela de itens encontrada.
Total de itens na tabela: 160
Coletando página, linhas encontradas: 5
Item encontrado: {'numero': '1', 'descricao': 'Agenda executiva...', 'quantidade': '100', 'valor_unitario': 'R$ 33,28', 'valor_total': 'R$ 3.328,00'}
Página: exibindo 1-5 de 160 itens
Tentando clicar no botão próxima página...
Página avançou para: 6-10 de 160 itens
...
```

## Configurações Importantes

### Configuração do Chrome

O script utiliza o Chrome em modo headless com as seguintes opções:
- `--headless`: Execução sem interface gráfica
- `--no-sandbox`: Melhora compatibilidade
- `--disable-dev-shm-usage`: Reduz uso de memória

### Configuração do Banco

Ajuste as credenciais no código se necessário:

```python
conn = pymysql.connect(
    host='localhost', 
    user='root', 
    password='', 
    db='ataspncp', 
    charset='utf8mb4'
)
```

## Formato dos Números de Controle

O sistema espera números de controle no formato:
```
CNPJ-DIGITO-NUMEROEDITAL/ANO
Exemplo: 01612781000138-1-000021/2022
```

## Tratamento de Paginação

O sistema automaticamente:
- Detecta o total de itens disponíveis
- Navega por todas as páginas clicando em "Próxima página"
- Aguarda o carregamento de cada página
- Verifica se a navegação foi bem-sucedida
- Para quando todos os itens foram coletados

## Resolução de Problemas

### Erro de ChromeDriver
- Certifique-se de que o ChromeDriver está no PATH
- Verifique se a versão do ChromeDriver é compatível com o Chrome instalado

### Erro de Conexão com Banco
- Verifique se o MySQL está rodando
- Confirme as credenciais de conexão
- Certifique-se de que o banco `ataspncp` existe

### Elementos Não Encontrados
- O PNCP pode ter alterado a estrutura da página
- Verifique se a URL está correta e acessível
- Alguns editais podem não ter a aba "Itens"

## Versões

- **V1**: Extração básica, apenas primeira página de itens
- **V2**: Versão completa com navegação por todas as páginas
- **Atual**: Versão otimizada com melhor tratamento de erros e navegação

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## Licença

Este projeto é de uso livre para fins educacionais e de transparência pública.