# Tech Challenge - Grupo 30 SOAT10 - Pós Tech Arquitetura de Software - FIAP

# Tópicos
- [Tech Challenge - Grupo 30 SOAT10 - Pós Tech Arquitetura de Software - FIAP](#tech-challenge---grupo-30-soat10---pós-tech-arquitetura-de-software---fiap)
- [Tópicos](#tópicos)
- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Executando o Projeto](#executando-o-projeto)
- [Comunicação com os demais serviços](#comunicação-com-os-demais-serviços)
- [Secrets Necessários](#secrets-necessários)


# Descrição do Projeto

O projeto visa atender à demanda de uma lanchonete de bairro, que, devido ao seu sucesso, necessita implementar um sistema de autoatendimento. 

Esta aplicação é parte de um ecossistema distribuído em quatro repositórios, executando inteiramente na AWS, com deploy via Terraform.

 [Topo](#tópicos)

# Tecnologias Utilizadas
- [Python 3.12](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [Kubernetes](https://kubernetes.io/)
- [Terraform](https://developer.hashicorp.com/terraform)
- [AWS Relational Database Service (RDS)](https://aws.amazon.com/pt/rds/)
- [AWS Elastic Kubernetes Service (EKS)](https://aws.amazon.com/pt/eks/)
- [AWS Elastic Container Registry (ECR)](https://aws.amazon.com/pt/ecr/)
- [AWS Lambda](https://aws.amazon.com/pt/lambda/)
- [AWS API Gateway](https://aws.amazon.com/pt/api-gateway/)
- [AWS Cognito](https://aws.amazon.com/pt/cognito/)
- [Github Actions](https://github.com/features/actions)

 [Topo](#tópicos)

# Executando o Projeto
Este projeto não é executado localmente. O deploy ocorre automaticamente na AWS via GitHub Actions, fazendo uso do Terraform.

Este repositório contém apenas o código fonte da aplicação. Os demais repositórios contém a infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase3-k8s), a infraestrutura de [banco de dados](https://github.com/tcsoat10/tech-challenger-soat10-phase3-db) e a [função Lambda](https://github.com/tcsoat10/tech-challenger-soat10-phase3-lambda) utilizada para autenticação de usuários.

 [Topo](#tópicos)

# Comunicação com os demais serviços

- A função AWS Lambda é acessível por meio de um AWS API Gateway integrado a ela, o endpoint da API é configurado como um secret no repositório da aplicação.
- O deploy da infra Kubernetes é feito em um cluster EKS. Dentro deste cluster, o deploy da aplicação é feito em um pod, e tem seu acesso gerenciado por um Load Balancer.
- O deploy do banco de dados libera o acesso do grupo de segurança do pod com a aplicação durante sua execução.
- A aplicação enxerga o banco de dados disponível e realiza as migrações necessárias.

 [Topo](#tópicos)

# Secrets Necessários
- AWS_ACCESS_KEY_ID: Access Key ID da conta AWS
- AWS_ACCOUNT_ID: Account ID da conta AWS
- AWS_SECRET_ACCESS_KEY: Secret Access Key da conta AWS
- AWS_SESSION_TOKEN: token de sessão da conta da AWS, necessário para contas temporárias, como da AWS Academy
- AWS_EKS_CLUSTER_NAME: nome do cluster EKS onde a aplicação estará hospedada
- MERCADO_PAGO_ACCESS_TOKEN: token de acesso da API do Mercado Pago
- MERCADO_PAGO_POS_ID: ID do PoS do Mercado Pago
- MERCADO_PAGO_USER_ID: ID do usuário do Mercado Pago
- MYSQL_DATABASE: nome do banco de dados MySQL
- MYSQL_HOST: hostname do banco MySQL, neste caso, o endpoint do RDS
- MYSQL_PORT: porta do banco
- MYSQL_USER: usuário do banco
- MYSQL_PASSWORD: senha do usuário do banco
- WEBHOOK_URL: url do webhook que recebe as respostas da API do Mercado Pago para confirmação do pagamento
- SECRET_KEY: chave secreta do token JWT

 [Topo](#tópicos)

# Diagrama de Arquitetura
![Diagrama Implantação Lanchonete20250603](https://github.com/user-attachments/assets/e3b0a0df-547d-4a85-b2fc-08f7dade1c13)

[Topo](#tópicos)
