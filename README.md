# 🚀 PNCP Itens Extractor - Sistema Completo

<div align="center">

![PNCP Badge](https://img.shields.io/badge/PNCP-Portal%20Nacional-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![PHP](https://img.shields.io/badge/PHP-7.4+-purple)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)
![Status](https://img.shields.io/badge/Status-Ativo-success)

</div>

## 📋 Descrição

O **PNCP Itens Extractor** é uma suíte completa de ferramentas desenvolvida para automatizar a extração, armazenamento e visualização de informações detalhadas de itens de editais/atas de licitação do Portal Nacional de Contratações Públicas (PNCP).

### 🎯 **Sistema Integrado Completo:**
- **🤖 Extração Automatizada**: Scripts Python com Selenium WebDriver
- **💾 Armazenamento Inteligente**: Banco de dados MySQL otimizado
- **🌐 Interface Web**: Página de consulta e pesquisa avançada
- **🔗 Integração PNCP**: Links diretos para editais originais

### 📊 **Dados Extraídos:**
- ✅ Número do item
- ✅ Descrição detalhada completa
- ✅ Quantidade especificada
- ✅ Valor unitário estimado
- ✅ Valor total estimado
- ✅ Informações do órgão licitante
- ✅ Dados completos da ata/edital
- ✅ Datas de inclusão e atualização

## 🌟 Funcionalidades Principais

### 🤖 **Extração Automatizada Inteligente**
- **Navegação Automática**: Utiliza Selenium WebDriver para navegar pelas páginas do PNCP
- **Paginação Completa**: Percorre automaticamente todas as páginas de itens
- **Filtro por Data**: Busca itens baseado na data de inclusão das atas
- **Tratamento de Erros**: Sistema robusto com tratamento de exceções
- **Modo Headless**: Execução silenciosa sem interface gráfica

### 💾 **Armazenamento Avançado**
- **Banco MySQL**: Estrutura otimizada para grandes volumes de dados
- **Dados Completos**: Armazena informações da ata + itens extraídos
- **Histórico**: Mantém registro de datas de inclusão e atualização
- **Integridade**: Relacionamento entre atas e itens preservado

### 🌐 **Interface Web Moderna**
- **Busca Avançada**: Pesquisa por descrição, órgão, número de controle
- **Paginação Inteligente**: Navegação eficiente entre resultados
- **Links Diretos**: Acesso direto aos editais originais no PNCP
- **Design Responsivo**: Funciona perfeitamente em desktop e mobile
- **Filtros Dinâmicos**: Resultados em tempo real conforme você digita

### 🔗 **Integração PNCP Total**
- **URLs Automáticas**: Geração automática de links para editais
- **Validação de Formato**: Verifica números de controle PNCP
- **Acesso Direto**: Botões para visualizar editais originais
- **Sincronização**: Dados sempre atualizados com a fonte oficial

## 📁 Estrutura do Projeto

```
PNCPItensExtrator/
├── 📄 extrai_itens_pncp.py      # 🚀 Versão dev - versão de testes e desenvolvimento
├── 📄 ExtratorV1.py             # 📚 Versão básica (apenas primeira página)
├── 📄 ExtratorV2.py             # 🔄 Versão com paginação completa
├── 📄 ExtratorV3.py             # ⚡ Versão atual - Extrator com filtro por data
├── 🌐 index.php                  # 💻 Interface web para visualização
├── 📖 README.md                 # 📋 Documentação completa
└── 🗂️ docs/                     # 📚 Documentação adicional
```

## 🎯 Versões Disponíveis

### 🚀 **ExtratorV3 (Versão Atual)**
**Funcionalidades:**
- ✅ Filtro por data de inclusão das atas
- ✅ Ordenação cronológica (mais antigas primeiro)
- ✅ Campos completos da ata (29 campos)
- ✅ Paginação inteligente
- ✅ Validação de dados de entrada
- ✅ Todos os campos da ata incluídos nos itens
- ✅ Estrutura de dados expandida

**Ideal para:** Extração incremental e atualização periódica

### 🔄 **ExtratorV2.py**
**Funcionalidades:**
- ✅ Navegação por todas as páginas
- ✅ Extração completa de todos os itens
- ✅ Campos básicos (6 campos principais)
- ✅ Sistema de paginação automática

**Ideal para:** Extração completa de editais específicos

### 📚 **ExtratorV1.py**
**Funcionalidades:**
- ✅ Extração básica da primeira página
- ✅ Campos essenciais do item
- ✅ Implementação simples

**Ideal para:** Testes e desenvolvimento inicial

## 🌐 Interface Web (index.php)

### 🎨 **Design Moderno e Responsivo**
- **Interface Intuitiva**: Design limpo e profissional
- **Cores Harmoniosas**: Paleta azul/cinza empresarial
- **Responsividade**: Adaptação perfeita para todos os dispositivos

### 🔍 **Sistema de Busca Avançado**
- **Busca Inteligente**: Pesquisa em múltiplos campos simultaneamente
- **Campos Pesquisáveis:**
  - 📝 Descrição do item
  - 🔢 Número do item
  - 🏛️ Nome do órgão
  - 📋 Número de controle PNCP
- **Busca em Tempo Real**: Resultados instantâneos
- **Filtros Dinâmicos**: Limpeza rápida dos filtros

### 📊 **Visualização de Dados**
- **Tabela Otimizada**: Exibição clara e organizada
- **Paginação Inteligente**: 50 itens por página
- **Ordenação**: Por ID decrescente (mais recentes primeiro)
- **Campos Exibidos:**
  - 🆔 ID único
  - 🔢 Número do item
  - 📝 Descrição completa
  - 📊 Quantidade
  - 💰 Valor unitário
  - 💰 Valor total
  - 🏛️ Órgão responsável
  - 📋 Número de controle
  - 📅 Data de inclusão
  - 🔗 Link para edital

### 🔗 **Integração PNCP Direta**
- **Botões de Acesso**: Link direto para cada edital
- **Geração Automática**: URLs criadas automaticamente
- **Validação**: Verificação do formato do número de controle
- **Nova Aba**: Abre o PNCP sem sair da consulta

### 📱 **Recursos Mobile**
- **Design Responsivo**: Adaptação automática para smartphones
- **Touch Friendly**: Botões e links otimizados para toque
- **Navegação Fácil**: Interface simplificada em telas pequenas

## 💻 Pré-requisitos

### 🔧 Software Necessário

- **Python 3.7+** - Linguagem principal
- **Google Chrome Browser** - Navegador para extração
- **ChromeDriver** - Driver para automação
- **MySQL Server** - Banco de dados
- **XAMPP** - Ambiente de desenvolvimento (recomendado)

### 📦 Bibliotecas Python

```bash
pip install selenium
pip install pymysql
pip install requests
pip install beautifulsoup4
```

### 🛠️ Configuração do ChromeDriver

1. Baixe o ChromeDriver compatível com sua versão do Chrome
2. Adicione o ChromeDriver ao PATH do sistema
3. Ou coloque na pasta do projeto

## 🗄️ Configuração do Banco de Dados

### 1. Criação do Banco

```sql
CREATE DATABASE ataspncp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Tabela Principal de Atas

```sql
CREATE TABLE atas_pncp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numeroControlePNCPAta VARCHAR(100),
    numeroAtaRegistroPreco VARCHAR(100),
    anoAta VARCHAR(10),
    numeroControlePNCPCompra VARCHAR(100),
    cancelado BOOLEAN,
    dataCancelamento DATETIME,
    dataAssinatura DATETIME,
    vigenciaInicio DATETIME,
    vigenciaFim DATETIME,
    dataPublicacaoPncp DATETIME,
    dataInclusao DATETIME,
    dataAtualizacao DATETIME,
    dataAtualizacaoGlobal DATETIME,
    usuario VARCHAR(100),
    objetoContratacao TEXT,
    cnpjOrgao VARCHAR(20),
    nomeOrgao VARCHAR(255),
    cnpjOrgaoSubrogado VARCHAR(20),
    nomeOrgaoSubrogado VARCHAR(255),
    codigoUnidadeOrgao VARCHAR(50),
    nomeUnidadeOrgao VARCHAR(255),
    codigoUnidadeOrgaoSubrogado VARCHAR(50),
    nomeUnidadeOrgaoSubrogado VARCHAR(255)
);
```

### 3. Tabela de Itens (Criada Automaticamente)

A tabela `atas_itens_pncp` é criada automaticamente pelo script com 29 campos completos:

```sql
CREATE TABLE atas_itens_pncp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ata_id INT,
    numero VARCHAR(20),
    descricao TEXT,
    quantidade VARCHAR(20),
    valor_unitario VARCHAR(50),
    valor_total VARCHAR(50),
    -- ... mais 22 campos da ata original
);
```

## 🚀 Como Usar

### 📊 1. Interface Web - Consulta Rápida

1. **Acesse**: `http://localhost/Laravel/PNCPItensExtrator/index.php`
2. **Pesquise**: Use a barra de busca para filtrar itens
3. **Navegue**: Use a paginação para explorar resultados
4. **Acesse Editais**: Clique no botão "🔗 Ver Edital" para abrir o PNCP

### 🤖 2. Extração Automatizada

#### Versão Atual (Recomendada)
```bash
python ExtratorV3.py
```
- Digite a data inicial (ex: 2024-05-25)
- O sistema busca atas inseridas após essa data
- Processamento em ordem cronológica

#### Versão V2 (Paginação Completa)
```bash
python ExtratorV2.py
```
- Extrai todos os itens de editais específicos
- Navegação automática por páginas
- Campos básicos essenciais

#### Versão V1 (Teste)
```bash
python ExtratorV1.py
```
- Extração simples da primeira página
- Ideal para testes rápidos

### 📋 3. Preparação dos Dados

Insira números de controle PNCP na tabela principal:

```sql
INSERT INTO atas_pncp (numeroControlePNCPCompra, dataInclusao) VALUES 
('01612781000138-1-000021/2022', '2024-05-25 00:00:00'),
('02345678000190-1-000015/2023', '2024-05-26 00:00:00');
```

## 📈 Exemplo de Execução

### 🖥️ Saída do Console

```
Digite a data de inclusão inicial (formato YYYY-MM-DD, ex: 2024-05-25): 2024-05-25
Buscando atas com dataInclusao posterior a 2024-05-25 (depois das 23:59:59)...
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
Item extraído: Número: 1, Descrição: Agenda executiva..., Quantidade: 100, Valor Unitário: R$ 33,28, Valor Total: R$ 3.328,00
```

### 📊 Dados Salvos no Banco

```sql
SELECT numero, descricao, quantidade, valor_unitario, valor_total, nomeOrgao, dataInclusao 
FROM atas_itens_pncp 
LIMIT 5;
```

## ⚙️ Configurações Importantes

### 🌐 Configuração do Chrome

```python
chrome_options = Options()
chrome_options.add_argument('--headless')          # Execução sem interface
chrome_options.add_argument('--no-sandbox')        # Melhora compatibilidade
chrome_options.add_argument('--disable-dev-shm-usage')  # Reduz uso de memória
```

### 🗄️ Configuração do Banco

```python
conn = pymysql.connect(
    host='localhost',     # Servidor MySQL
    user='root',          # Usuário do banco
    password='',          # Senha (vazia no XAMPP)
    db='ataspncp',        # Nome do banco
    charset='utf8mb4'     # Codificação UTF-8
)
```

### 🔗 Formato dos Números de Controle

```
Padrão: CNPJ-DIGITO-NUMEROEDITAL/ANO
Exemplo: 01612781000138-1-000021/2022

Onde:
- CNPJ: 01612781000138
- Dígito: 1
- Número: 000021
- Ano: 2022
```

## 🔧 Funcionalidades Técnicas

### 🤖 Sistema de Paginação Inteligente

- **Detecção Automática**: Identifica total de itens disponíveis
- **Navegação Robusta**: Clica automaticamente em "Próxima página"
- **Verificação de Estado**: Confirma se a página avançou
- **Timeout Inteligente**: Para quando todos os itens foram coletados

### 🛡️ Tratamento de Erros

- **Retry Logic**: Tenta novamente em caso de falha
- **Validação de Dados**: Verifica se os dados estão completos
- **Log Detalhado**: Registra todas as operações
- **Graceful Shutdown**: Fecha recursos em caso de erro

### 📊 Otimizações de Performance

- **Modo Headless**: Execução mais rápida sem interface
- **Batch Processing**: Processa múltiplas atas em sequência
- **Memory Management**: Gerenciamento eficiente de memória
- **Connection Pooling**: Reutilização de conexões de banco

## 🔍 Resolução de Problemas

### ❌ Erro de ChromeDriver
```bash
# Solução 1: Verificar versão
google-chrome --version
chromedriver --version

# Solução 2: Atualizar ChromeDriver
# Baixe a versão compatível em: https://chromedriver.chromium.org/
```

### ❌ Erro de Conexão com Banco
```python
# Verificar se o MySQL está rodando
# XAMPP: Iniciar Apache e MySQL
# Verificar credenciais no código
```

### ❌ Elementos Não Encontrados
```
# O PNCP pode ter alterado a estrutura
# Verificar se a URL está acessível
# Alguns editais podem não ter aba "Itens"
```

### ❌ Timeout de Página
```python
# Aumentar timeout se necessário
WebDriverWait(driver, 30)  # 30 segundos
```

## 📋 Versões e Changelog

### 🚀 **Versão Atual (ExtratorV3.py)**
- ✅ Filtro por data de inclusão
- ✅ Ordenação cronológica
- ✅ 29 campos completos
- ✅ Validação de entrada
- ✅ Tratamento robusto de erros

### 🔄 **V2 (ExtratorV2.py)**
- ➕ Paginação completa
- ➕ Navegação automática
- ➕ Campos básicos

### 📚 **V1 (ExtratorV1.py)**
- ➕ Extração básica
- ➕ Primeira página apenas
- ➕ Implementação inicial

## 🤝 Contribuição

### 🛠️ Como Contribuir

1. **Fork** do repositório
2. **Clone** para sua máquina
3. **Crie** uma branch para sua feature
4. **Desenvolva** e teste suas alterações
5. **Commit** com mensagens descritivas
6. **Push** para sua branch
7. **Abra** um Pull Request

### 💡 Ideias para Melhorias

- **Dashboard Analytics**: Gráficos e estatísticas
- **Export Excel/CSV**: Exportação de dados
- **API REST**: Endpoints para integração
- **Scheduler**: Execução automática periódica
- **Notificações**: Alertas de novos itens

## 📄 Licença

Este projeto é de **uso livre** para fins:
- 📚 **Educacionais**
- 🏛️ **Transparência pública**
- 🔬 **Pesquisa acadêmica**
- 💼 **Desenvolvimento não comercial**

## 📞 Suporte

Para dúvidas, sugestões ou reportar bugs:
- 📧 **Issues**: Use o sistema de issues do GitHub
- 📝 **Documentação**: Consulte este README
- 🔧 **Debug**: Ative logs detalhados nos scripts

---

<div align="center">

**🎯 Desenvolvido para democratizar o acesso a dados públicos**

![GitHub stars](https://img.shields.io/github/stars/usuario/PNCPItensExtractor?style=social)
![GitHub forks](https://img.shields.io/github/forks/usuario/PNCPItensExtractor?style=social)

</div>