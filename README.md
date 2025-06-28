# Pipeline de Scraping utilizando Google Cloud Platform

## 1. Visão geral do Projeto

Este projeto tem como objetivo realizar um scraping na categoria de televisão da [Kabum](https://www.kabum.com.br/tv) . Os dados serão armazenados no Google Cloud Storage, carregados no BigQuery e um alerta é enviado via Telegram com as informações de execução (funcionando como um alerta de logs). Por fim, o processo é orquestrado por uma DAG no Apache Airflow hospedado no Google Cloud Composer.

![image](https://github.com/user-attachments/assets/5297c884-bbe1-4120-8e7a-a95d4e26bffc)


## 2. Estrutura de pastas

![image](https://github.com/user-attachments/assets/41ee8eb7-1c6a-47a6-bcc7-2f8d0a369cdb)




### 2.1 Dataset no BigQuery

É necessário criar o *dataset\_kabum* no BigQuery.A tabela de produtos será criada automaticamente no primeiro step da DAG.

![image](https://github.com/user-attachments/assets/a31affb8-5637-4016-b30d-46569d027668)

## 3. Descrição de objetos

Utilizamos o Apache Airflow através do Google Cloud Composer para transformar scripts soltos em uma automação escalável e de fácil manutenção. Quatro tarefas que dão resultado ao projeto são realizadas em sequência.

![image](https://github.com/user-attachments/assets/b39c8659-c845-45cd-abd0-1a28c5452219)
![image](https://github.com/user-attachments/assets/2f071e87-8342-4289-bfb8-32c358eb32f7)


### 3.1 DAG - `dag_kabum_pipeline.py`

Orquestra as tasks:

* **Scraping\_data** → Coleta e padroniza os dados utilizando web scraping.
* **upload\_data** → Envia o CSV gerado para um bucket no Google Cloud Storage.
* **load\_bigquery** → Carrega os dados no BigQuery para consultas e análises.
* **send\_telegram\_notification** → Envia notificação no Telegram via API notificando o sucesso ou falha do processo (logs).

### 3.2 Processo de scraper - `scraping.py`

* Fazemos scraping da página utilizando BeautifulSoup.
* Após, criamos novas features com base nos dados capturados como: marca, polegadas, painel, resolução.
* O CSV é salvo e marcamos a contagem de produtos extraídos.

### 3.3 Funções auxiliares - `transformations.py`

Aqui armazenamos as funções que cuidam da extração dos dados, melhorando a organização visual do script.

### 3.4 Notificação no Telegram - `telegram_notifications.py`

* Formata mensagem com logs de execução.
* É necessário criar um bot no Telegram.
* É necessário ter credenciais de acesso para uso da API.

![image](https://github.com/user-attachments/assets/42357320-0ef4-4edf-8fbf-82f9c8f3f226)


### 3.5 Credenciais sensíveis - `constants.py`

Não podemos esquecer da segurança: todas as credenciais devem ser armazenadas em variáveis de ambiente ou no recurso interno do Airflow, e **não** dentro do script.

* `kabum_bq_table` → Identifica o destino no BigQuery onde os dados finais serão carregados.
* `kabum_bucket` → Nome do bucket no Google Cloud Storage usado pelo pipeline.
* `kabum_gcs_path` → Caminho dentro do bucket onde o arquivo CSV ficará armazenado.
* `kabum_local_output_path` → Local no filesystem do Airflow onde o scraper grava temporariamente o CSV.
* `TELEGRAM_CHAT_ID` → Identificador do chat para onde serão enviadas as mensagens.
* `TELEGRAM_TOKEN` → Token de autenticação do seu Bot no Telegram obtido pelo BotFather.

![image](https://github.com/user-attachments/assets/9abcc14d-8285-4ea6-8b9b-a0a4a64c634e)
![image](https://github.com/user-attachments/assets/289df805-5327-4166-8bf0-65a0d1079d46)


## 4. Pacotes necessários

No ambiente do Composer, são necessários os pacotes:

```bash
pip install beautifulsoup4 pandas python-dotenv python-telegram-bot apache-airflow-providers-google
```
![image](https://github.com/user-attachments/assets/bf3df282-4856-45a7-9f41-73bc89e971cd)



Também é necessário configurar permissões para:

* Criar tabelas no BigQuery.
* Executar jobs no BigQuery.
* Registrar logs e executar DAGs no Airflow via Cloud Composer.
  
![image](https://github.com/user-attachments/assets/9801f404-f434-4931-b405-95ed58453ae1)

## 5. Considerações Finais

Este padrão de pipeline é útil em ambientes em que exista a necessidade de coleta, transformação e disponibilização de dados de forma confiável e repetível, otimizando o tempo e foco do squad.

Cada etapa, desde a extração dos dados até a entrega de alertas, é orquestrada de forma simples e escalável, garantindo a fácil manutenção e entendimento de outros desenvolvedores no projeto.

Para dúvidas ou sugestões, me envie um email: [luizvicentediasjr@yahoo.com](mailto:luizvicentediasjr@yahoo.com)
