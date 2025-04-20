
# Text Summarizer — AWS-Powered NLP Pipeline

This project is a serverless, cloud-native text summarization pipeline using **FastAPI**, **AWS Lambda**, and **S3**. Upload a `.txt` file, and get an automatic summary saved back to your bucket.

---
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [1. Connect to the EC2 instance](#-1-connect-to-the-ec2-instance)
  - [2. Clone the repository](#-2-clone-the-repository)
  - [3. Run the setup script](#-3-run-the-setup-script)
  - [4. Set up Nginx reverse proxy](#-4-set-up-nginx-reverse-proxy)
  - [5. Deploy the Lambda Function](#-5-deploy-the-lambda-function)
- [Usage](#usage)
  - [Example](#example)

## Overview

1. Upload a `.txt` file to your **S3 bucket** (e.g., `input/myfile.txt`)
2. An **AWS Lambda** function is triggered
3. It sends the content to a **FastAPI app** hosted on an EC2 instance
4. The FastAPI app summarizes the text using the **`t5-small` transformer model** via Hugging Face Transformers
5. The Lambda function saves it to `output/myfile_summary.txt` in S3 

---

## Features

- **FastAPI** — for building the summarizer API
- **AWS Lambda** — serverless function for processing input
- **S3** — storage for input/output files
- **Nginx** — reverse proxy for production API access
- **Transformers (BART)** — for the actual summarization logic

---

## Setup

### 🔹 1. Connect to the EC2 instance

```bash
ssh -i ec2-key.pem ubuntu@<ec2-ip>
```

---
### 🔹 2. Clone the repository

Once inside the EC2 instance:

```bash
git clone https://github.com/m-nasereslami/text-summarizer-aws-pipeline.git
cd text-summarizer-aws-pipeline
```

---
### 🔹 3. Run the setup script

This repo includes a `setup.sh` script that installs dependencies, sets up a virtual environment, and runs the FastAPI app.

```bash
chmod +x setup.sh
./setup.sh
```

This starts the app on `127.0.0.1:8000`.

---

### 🔹 4. Set up Nginx reverse proxy

```bash
sudo nano /etc/nginx/sites-available/fastapi
```

Paste:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then run:

```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```



Once Nginx is set up and the app is running, open your browser and go to:

```
http://<ec2-ip>/docs
```

This will load the FastAPI UI where you can test the `/summarize` endpoint.

---

### 🔹 5. Deploy the Lambda Function

The Lambda function `lambda_function.py` reads uploaded `.txt` files from S3, sends the content to FastAPI API, and saves the summarized result back to S3.

```python
response = requests.post("http://<ec2-ip>/summarize", json={"text": text})
```

It requires the `requests` library to be packaged in a `.zip` before deploying.

---

## Usage

### 🔹 1. Upload a `.txt` file to:

```
s3://your-bucket-name/input/yourfile.txt
```

### 🔹 2. The output will appear in:

```
s3://your-bucket-name/output/yourfile_summary.txt
```

---



### Example

**Input file (saved to `input/Dmitri_Mendeleev.txt`):**
> Dmitri Ivanovich Mendeleev[b] (/ˌmɛndəlˈeɪəf/ MEN-dəl-AY-əf;[2][c][a] 8 February [O.S. 27 January] 1834 – 2 February [O.S. 20 January] 1907) was a Russian chemist known for formulating the periodic law and creating a version of the periodic table of elements. He used the periodic law not only to correct the then-accepted properties of some known elements, such as the valence and atomic weight of uranium, but also to predict the properties of three elements that were yet to be discovered (germanium, gallium and scandium).

**Result (saved to `output/Dmitri_Mendeleev_summary.txt`):**
> Dmitri Ivanovich Mendeleev was a chemist known for formulating the periodic law . he used the law not only to correct the then-accepted properties of some known elements, such as the valence and atomic weight of uranium .

---




