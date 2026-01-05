# YouTube ELT Pipeline with Airflow, Docker, and CI/CD

## Motivation

The goal of this project is to gain hands-on experience with modern data engineering tools by building an end-to-end **ELT (Extract, Load, Transform)** pipeline. The project uses **Python, Docker, and Apache Airflow** to orchestrate data ingestion and processing, while incorporating **unit testing, data quality checks, and CI/CD best practices** to ensure reliability and maintainability.

This repository demonstrates a production-style data pipeline with automated testing and deployment workflows.

---

## Dataset

The data source for this project is the **YouTube Data API**. By default, data is extracted from the **MrBeast** YouTube channel.

This project can be easily adapted for any other YouTube channel by updating the **channel ID or channel handle** in the configuration.

---

## Project Overview

This project uses **Apache Airflow** as the orchestration layer, running inside **Docker containers**, to manage an ELT workflow. The pipeline consists of the following steps:

1. **Extract**
   - Data is extracted from the YouTube API using Python scripts
   - The first run performs a full historical load

2. **Load**
   - Raw data is loaded into a **staging schema** in a Dockerized PostgreSQL database

3. **Transform**
   - Lightweight transformations are applied using Python
   - Data is upserted into a **core schema**

4. **Test & Validate**
   - Unit tests validate application logic
   - Data quality checks ensure data correctness in both staging and core layers

Once the core schema is populated and all tests pass, the data is ready for analysis.

---

## Extracted Fields

The following fields are extracted from the YouTube API:

- Video ID  
- Video Title  
- Upload Date  
- Duration  
- View Count  
- Like Count  
- Comment Count  

---

## Tools & Technologies

- **Containerization**: Docker, Docker Compose  
- **Orchestration**: Apache Airflow  
- **Data Storage**: PostgreSQL  
- **Languages**: Python, SQL  
- **Testing**: pytest, SODA Core  
- **CI/CD**: GitHub Actions  

---

## Containerization

Airflow is deployed using Docker Compose, based on the official Airflow `docker-compose.yaml` with custom modifications.

- A custom Airflow image is built using a `Dockerfile`
- The image is pushed to and pulled from **Docker Hub** via GitHub Actions
- Docker Compose is used to spin up all required services (Airflow components and PostgreSQL)

## Orchestration

Three DAGs exist, triggered one after the other. These can be accessed using the Airflow UI through http://localhost:8080. The DAGs are as follows:

- produce_json - DAG to produce JSON file with raw data
- update_db - DAG to process JSON file and insert data into booth staging and core schemas
- data_quality - DAG to check the data quality on both layers in the database

## Data Storage

To access the Youtube API data, you can either access the postgres docker container and use psql to interact with the database or access a database management tool like Dbeaver and run your queries from there.

## Testing

Both unit and data quality testing are implemented in this project using pystest and SODA core respectively.

## CI-CD

The CI-CD part of this project is needed for when you make a change the Airflow code, docker image, packages, etc and want to test that the DAGs are still working as expected. CI-CD is implemented using Github Actions.

