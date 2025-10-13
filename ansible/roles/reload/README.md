# 3xui-recover

Роль для быстрой «реанимации» 3x-ui:
- чистит/удаляет раздутый docker json.log контейнера;
- убивает лишние процессы `/app/x-ui` на хосте (не трогая PID контейнера);
- рестартит контейнер.

## Переменные (defaults)
- `xui_container_name`: "3x-ui"
- `xui_clean_logs`: true/false
- `xui_kill_stray_processes`: true/false
- `xui_restart_container`: true/false

## Пример playbook
```yaml
- hosts: xui_hosts
  become: true
  roles:
    - role: reload
      vars:
        xui_container_name: "3x-ui"
        xui_clean_logs: true
        xui_kill_stray_processes: true
        xui_restart_container: true


ansible-playbook -i inventories/main reload-playbook.yml
