# Screenshot & Submission Checklist

## Screenshots to Capture

- [ ] `ansible-inventory --graph` output showing fedora-vm under devops_targets
- [ ] `ansible devops_targets -m ping` returning pong (SUCCESS)
- [ ] `ansible-playbook playbook.yml --syntax-check` passing
- [ ] Full playbook run output (scroll to show all task groups)
- [ ] PLAY RECAP line: ok=N changed=4 unreachable=0 failed=0
- [ ] Debug summary task showing HTTP 200 for all endpoints
- [ ] `sudo systemctl is-active nginx` → active
- [ ] `sudo systemctl is-active studentnotes-backend` → active
- [ ] `curl -I http://127.0.0.1/` → HTTP 200
- [ ] `curl http://127.0.0.1/health` → {"status":"ok"}
- [ ] `curl http://127.0.0.1/api/info` → JSON with app, version, host
- [ ] `curl http://127.0.0.1/api/notes` → JSON array
- [ ] Browser at http://localhost showing the Student Notes UI
- [ ] Browser: add a note, pin it, then delete it
- [ ] Generated ANSIBLE_PREPARATION_REPORT.txt content
- [ ] Second idempotency run showing changed=0

## Submission Files

- [ ] GitHub repository link (public)
- [ ] Recorded video demonstration (5–10 minutes)
- [ ] Written report / PDF (DevOps lifecycle analysis + Ansible explanation)

## DevOps Lifecycle Checklist

- [ ] Plan: application requirements, component table, port assignments
- [ ] Code: Flask API, HTML frontend, Dockerfiles, K8s YAML, Ansible YAML
- [ ] Build: Dockerfiles described (image build not executed in Ansible run)
- [ ] Test: ping, syntax-check, URI health/frontend/API checks
- [ ] Release: manifests and Helm chart staged in Git
- [ ] Deploy: Ansible configures Fedora, installs deps, starts services
- [ ] Operate: systemd keeps services running, enabled on boot
- [ ] Monitor: HTTP status checks, service state, generated report
