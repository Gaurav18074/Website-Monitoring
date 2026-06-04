![Build Status](https://github.com/Gaurav18074/Website-Monitoring/actions/workflows/deploy.yml/badge.svg)
# Website-Monitoring
# Cloud-Based Website Monitoring System

A cloud-ready website monitoring platform built using FastAPI, PostgreSQL, Docker, Nginx and APScheduler.

## Features

- Monitor website uptime
- Track response times
- Store monitoring logs
- Dashboard visualization
- REST API using FastAPI
- Dockerized deployment
- PostgreSQL database
- Automated scheduled health checks

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Nginx
- APScheduler
- Chart.js

## Architecture

User
  ↓
Nginx
  ↓
FastAPI
  ↓
PostgreSQL
  ↓
Monitoring Logs

APScheduler → Website Health Checks

## API Endpoints

GET /api/sites
POST /api/sites
DELETE /api/sites/{site_id}
GET /api/logs/{site_id}

## Run Locally

docker compose up --build

Visit:
Visit: http://localhost:8000/docs

## Key Highlights

- Built a website monitoring platform using FastAPI and PostgreSQL
- Implemented scheduled health checks using APScheduler
- Containerized application using Docker and Docker Compose
- Configured Nginx reverse proxy
- Integrated GitHub Actions for automated testing
