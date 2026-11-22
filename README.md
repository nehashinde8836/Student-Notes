# Student Notes - DevOps Case Study & Ansible Automation

A microservices application for managing student study notes.  
Flask REST API (Gunicorn) + Nginx frontend, configured on Fedora with Ansible.  
Kubernetes manifests, Dockerfiles and a GitHub Actions CI workflow are included for analysis and artifact staging (no cluster deployment performed).

## Application Overview

| Component  | Technology                | Port | Role                                      |
|------------|---------------------------|------|-------------------------------------------|
| Frontend   | HTML/CSS/JavaScript, Nginx | 80   | Serves the web interface; proxies /api/   |
| Backend    | Python 3, Flask, Gunicorn  | 5000 | REST API for notes + /health endpoint     |
| K8s config | Deployments, Services, Ingress | — | Orchestration manifests (staged only)  |
| CI         | GitHub Actions            | —    | Lint, syntax check and Docker build       |

## Quick Start (Fedora VM)

```bash
sudo dnf install -y ansible-core git python3
cd ansible

# 1. Validate inventory
ansible-inventory --graph

# 2. Test connectivity
ansible devops_targets -m ping

# 3. Check playbook syntax
ansible-playbook playbook.yml --syntax-check

# 4. Run the playbook
ansible-playbook playbook.yml --ask-become-pass

# 5. Run again to confirm idempotency
ansible-playbook playbook.yml --ask-become-pass
```

Optional — clone from your own GitHub repo instead of the local folder:
```bash
ansible-playbook playbook.yml --ask-become-pass \
  -e repo_url=https://github.com/<you>/<repo>.git
```

## Verification

```bash
# Check both services are active
sudo systemctl is-active nginx studentnotes-backend

# Backend health
curl http://127.0.0.1:5000/health

# Frontend via Nginx
curl -I http://127.0.0.1/

# API info via Nginx proxy
curl http://127.0.0.1/api/info

# Notes list via Nginx proxy
curl http://127.0.0.1/api/notes

# View generated report
cat /opt/studentnotes/deployment-artifacts/ANSIBLE_PREPARATION_REPORT.txt
```

Then open **http://localhost** in a browser to use the Student Notes interface.

## Repository Layout

```
app/
  backend/   app.py, requirements.txt, Dockerfile
  frontend/  index.html, nginx.conf, Dockerfile
k8s/
  backend-deployment.yaml
  backend-service.yaml
  frontend-deployment.yaml
  frontend-service.yaml
  ingress.yaml
.github/workflows/ci.yml
ansible/
  ansible.cfg
  inventory.ini
  playbook.yml
  templates/
    nginx.conf.j2
    studentnotes.service.j2
    report.txt.j2
```
