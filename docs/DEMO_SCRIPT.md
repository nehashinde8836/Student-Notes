# Demo Script — Student Notes DevOps Case Study

## 1. Show Repository Structure
```bash
ls -R   # or tree if installed
```
Explain: frontend/, backend/, k8s/, ansible/, .github/workflows/

---

## 2. Inventory and Connectivity Check
```bash
cd ansible
ansible-inventory --graph
ansible devops_targets -m ping
```
Expected: fedora-vm under devops_targets; ping returns pong.

---

## 3. Playbook Syntax Check
```bash
ansible-playbook playbook.yml --syntax-check
```
Expected: "playbook: playbook.yml" — no errors.

---

## 4. Run the Playbook
```bash
ansible-playbook playbook.yml --ask-become-pass
```
Walk through task groups as they execute:
- Package installation (dnf)
- Backend copy + pip install
- systemd service creation
- Nginx configuration + SELinux
- Kubernetes manifest staging
- URI verification checks
- Report generation and debug summary

---

## 5. Verify Services and Endpoints
```bash
sudo systemctl is-active nginx
sudo systemctl is-active studentnotes-backend

curl http://127.0.0.1:5000/health
curl -I http://127.0.0.1/
curl http://127.0.0.1/api/info
curl http://127.0.0.1/api/notes
```

---

## 6. Show Browser (http://localhost)
- Frontend loads with the Student Notes interface
- Add a note with subject and content
- Pin a note
- Delete a note
- Each action calls the Flask API through the Nginx proxy

---

## 7. Show Generated Report
```bash
cat /opt/studentnotes/deployment-artifacts/ANSIBLE_PREPARATION_REPORT.txt
```

---

## 8. Idempotency Run
```bash
ansible-playbook playbook.yml --ask-become-pass
```
Show: changed=0, confirming declarative configuration is repeatable.

---

## 9. Show Kubernetes Manifests (staged only)
```bash
ls /opt/studentnotes/deployment-artifacts/
cat /opt/studentnotes/deployment-artifacts/ingress.yaml
```
Explain path-based routing: / → frontend, /api → backend, /health → backend.
State clearly: no live Kubernetes cluster deployment was performed.
