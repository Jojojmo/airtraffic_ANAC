# Análise de Dados do Transporte Aéreo Brasileiro

## Visão Geral

Bem-vindo ao repositório de Análise de Dados do Transporte Aéreo Brasileiro! Desenvolvi esta análise com base em uma extensa base de dados contendo 400 mil registros sobre o transporte aéreo brasileiro ao longo da última década. A abordagem analítica e de pesquisa visa extrair informações valiosas e insights significativos.

- Explore /notebooks para acessar análises detalhadas e estudos.
- Visite /package para visualizar e obter suplementos das classes e funções utilizadas nos /notebooks.

## Objetivos

Meu principal objetivo é aplicar técnicas avançadas de análise de dados, estatística e explorar o uso de machine learning nas próximas versões, contribuindo para uma compreensão mais profunda do cenário do transporte aéreo brasileiro.

## Base de Dados Utilizada

- [Acesso à Base de Dados](https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/)
- Nome do Arquivo: Dados_Estatisticos_2011_a_2020.json
- [Descrição dos Metadados](https://www.anac.gov.br/acesso-a-informacao/dados-abertos/areas-de-atuacao/voos-e-operacoes-aereas/dados-estatisticos-do-transporte-aereo)

Os dados foram inicialmente disponibilizados em formato .json e posteriormente modelados em um banco de dados PostgreSQL. O tratamento consistiu na exclusão de registros nos quais todas as colunas de valores qualitativos estavam vazias ou zeradas.

## Contexto

Os dados fornecidos pela ANAC (Agência Nacional de Aviação Civil) oferecem uma rica perspectiva sobre o panorama do transporte aéreo no Brasil. Esta análise considera esses dados como uma fonte valiosa de informações, bem como uma oportunidade única para explorar e compreender padrões, desafios e tendências que moldam a indústria da aviação civil no país.

Ao examinar os metadados, esta análise aprofunda-se em detalhes específicos que abrangem desde informações operacionais até estatísticas cruciais. Esses insights são fundamentais para a formulação de estratégias, tomada de decisões informada e contribuem para um entendimento mais profundo e abrangente do setor aéreo brasileiro.

## Como Instalar o Repositório

1. Importe o banco de dados em um SGBD. Recomendo o uso do pgAdmin4 com PostgreSQL, as tecnologias utilizadas neste projeto.
2. Execute os seguintes comandos em seu terminal, certificando-se de ter a linguagem Python instalada e as permissões necessárias:

    ```bash
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

3. Modifique o arquivo `settings_bd.json` de acordo com suas configurações no banco de dados.

## Lista de Arquivos do Projeto

- .gitignore: Arquivo que especifica os padrões de arquivos e diretórios a serem ignorados pelo Git.
- /notebooks: Contém Jupyter notebooks com análises de dados e estudos.
  - /notebooks/first_look.ipynb: Análise exploratória e inicial do banco de dados.
- /package: Contém scripts e suplementos para o uso dos notebooks.
  - /package/styles: Diretório para armazenar os arquivos de estilo.
    - /package/styles/my_styles.json: Arquivo utilizado na classe My_styles para configurar estilos pré-estabelecidos no Seaborn.
  - /package/bd_classes.py: Funções e classes que fazem a conexão no banco de dados, assim como queries pré-estabelecidas.
  - /package/my_style_classes.py: Funções e classes utilizadas para gerar os gráficos em Seaborn deste projeto.
  - /package/supply_format.py: Script que contém funções para formatação de valores e atributos em geral.
- airtraffic.sql: Arquivo para a importação do banco de dados.
- README.md: Contém informações e documentações do projeto.
- requirements.txt: Dependências e pacotes que precisam ser instalados para o uso deste projeto.
- settings_bd.json: Arquivo que configura e faz a conexão entre o seu banco de dados.

