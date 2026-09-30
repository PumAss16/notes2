# Подтема 7: SystemD и OOM Killer

---

## Часть 1. Теория

### 1.1. Что такое SystemD

**SystemD** — система инициализации и менеджер сервисов в современных Linux-дистрибутивах. Запускается ядром как **PID 1**.

**Что делает:**
- Запускает сервисы при загрузке.
- Управляет зависимостями.
- Перезапускает упавшие сервисы.
- Ведёт логи (journald).
- Управляет таймерами (аналог cron).
- Управляет монтированием ФС.

**До SystemD** был **init** (SysV init) — простой скрипт, запускал сервисы последовательно. SystemD работает параллельно, быстрее.

**Основные понятия:**
- **Unit** — единица управления (сервис, таймер, mount, socket).
- **Service** — сервис (демон).
- **Target** — группа юнитов (аналог runlevel).
- **Journal** — логи.

**Фраза для собеса:**
> SystemD — система инициализации, PID 1. Управляет сервисами, зависимостями, логами, таймерами. Работает параллельно, быстрее старого init.

---

### 1.2. Типы юнитов

| Тип | Расширение | Что делает |
|:---|:---|:---|
| **Service** | `.service` | Демон (nginx, sshd) |
| **Timer** | `.timer` | Аналог cron |
| **Mount** | `.mount` | Точка монтирования |
| **Socket** | `.socket` | Сокет для активации |
| **Target** | `.target` | Группа юнитов |
| **Path** | `.path` | Следит за файлами |

---

### 1.3. Как написать свой systemd-юнит

**Структура service-файла:**
```ini
[Unit]
Description=My Python HTTP Server
After=network.target

[Service]
Type=simple
User=myuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/server.py
Restart=on-failure
RestartSec=5
MemoryLimit=100M

[Install]
WantedBy=multi-user.target
```

**Разбор секций:**

**[Unit]** — описание и зависимости:
- `Description` — что за сервис.
- `After` — после каких юнитов запускать.
- `Requires` — жёсткая зависимость.

**[Service]** — как запускать:
- `Type` — тип (simple, forking, oneshot, notify).
- `User` — от какого пользователя.
- `WorkingDirectory` — рабочая директория.
- `ExecStart` — команда запуска.
- `ExecStop` — команда остановки.
- `Restart` — когда перезапускать (no, on-failure, always).
- `RestartSec` — через сколько секунд.
- `MemoryLimit` — лимит памяти (через cgroups).

**[Install]** — когда включать:
- `WantedBy=multi-user.target` — запускать при обычной загрузке.

**Как установить:**
```bash
sudo cp myservice.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable myservice
sudo systemctl start myservice
sudo systemctl status myservice
```

**Фраза для собеса:**
> Юнит-файл состоит из [Unit], [Service], [Install]. В [Service] — ExecStart, Restart, User, MemoryLimit. После установки — daemon-reload, enable, start.

---

### 1.4. Основные команды systemctl

```bash
systemctl start nginx        # запустить
systemctl stop nginx         # остановить
systemctl restart nginx      # перезапустить
systemctl reload nginx       # перечитать конфиг
systemctl status nginx       # статус
systemctl enable nginx       # автозапуск
systemctl disable nginx      # убрать автозапуск
systemctl is-active nginx    # проверить
systemctl list-units         # список юнитов
systemctl list-unit-files    # все юнит-файлы
systemctl daemon-reload      # перечитать юнит-файлы
```

---

### 1.5. Логи — journalctl

SystemD ведёт логи через **journald**.

```bash
journalctl                   # все логи
journalctl -u nginx          # логи конкретного сервиса
journalctl -f                # в реальном времени
journalctl --since "1 hour ago"
journalctl -p err            # только ошибки
journalctl -b                # с последней загрузки
```

---

### 1.6. OOM Killer

**OOM Killer (Out-Of-Memory Killer)** — механизм ядра, который убивает процессы, когда заканчивается RAM.

**Как работает:**
1. Ядро видит, что RAM заканчивается.
2. Выбирает процесс-жертву по **oom_score**.
3. Убивает его сигналом SIGKILL.
4. Освобождает память.

**Как считается oom_score:**
- Больше памяти занимает — выше score.
- Процессы root получают бонус (меньше score).
- Можно настроить через `oom_score_adj` (от -1000 до +1000).

**Как защитить важный процесс:**
```bash
echo -500 > /proc/<PID>/oom_score_adj
```

**Как запретить убийство:**
```bash
echo -1000 > /proc/<PID>/oom_score_adj
```

**Как посмотреть score:**
```bash
cat /proc/<PID>/oom_score
```

**Логи:**
```bash
dmesg | grep -i oom
journalctl -k | grep -i oom
```

**Пример вывода:**
```
Out of memory: Killed process 12345 (python3) total-vm:2048000kB, anon-rss:1024000kB
```

**Фраза для собеса:**
> OOM Killer убивает процессы при нехватке RAM. Выбирает по oom_score. Можно защитить через oom_score_adj. В Kubernetes работает внутри cgroups.

---

### 1.7. Пересечение с Kubernetes

В Kubernetes OOM Killer работает внутри контейнеров:
- У каждого пода есть **memory limit**.
- Если под превышает лимит — его убивает **cgroup OOM Killer**.
- Это приводит к рестарту пода.

**Как диагностировать:**
```bash
kubectl describe pod <pod>   # смотреть OOMKilled
kubectl get events
```

---

## Часть 2. Команды с флагами

### 2.1. systemctl

```bash
systemctl start <unit>           # запустить
systemctl stop <unit>            # остановить
systemctl restart <unit>         # перезапустить
systemctl reload <unit>          # перечитать конфиг
systemctl status <unit>          # статус
systemctl enable <unit>          # автозапуск
systemctl disable <unit>         # убрать автозапуск
systemctl is-active <unit>       # проверить
systemctl is-enabled <unit>      # проверить автозапуск
systemctl list-units             # список юнитов
systemctl list-unit-files        # все юнит-файлы
systemctl list-units --type=service
systemctl daemon-reload          # перечитать юнит-файлы
systemctl cat <unit>             # показать юнит-файл
systemctl edit <unit>            # редактировать override
systemctl show <unit>            # все параметры
```

---

### 2.2. journalctl

```bash
journalctl                       # все логи
journalctl -u <unit>             # логи сервиса
journalctl -f                    # follow (в реальном времени)
journalctl --since "1 hour ago"
journalctl --since "2024-01-01" --until "2024-01-02"
journalctl -p err                # только ошибки
journalctl -b                    # с последней загрузки
journalctl -b -1                 # предыдущая загрузка
journalctl -n 100                # последние 100 строк
journalctl --disk-usage          # размер логов
journalctl --vacuum-time=7d      # удалить логи старше 7 дней
journalctl --vacuum-size=500M    # оставить только 500 МБ
```

---

### 2.3. OOM Killer

```bash
dmesg | grep -i oom              # логи OOM
journalctl -k | grep -i oom      # через journalctl
cat /proc/<PID>/oom_score        # score процесса
cat /proc/<PID>/oom_score_adj    # adj процесса
echo -500 > /proc/<PID>/oom_score_adj   # защитить
echo -1000 > /proc/<PID>/oom_score_adj  # запретить убийство
```

**В systemd-юните:**
```ini
[Service]
OOMScoreAdjust=-500
MemoryLimit=100M
```

---

### 2.4. Управление таймерами

```bash
systemctl list-timers            # список таймеров
systemctl status <timer>         # статус
systemctl start <timer>          # запустить
systemctl enable <timer>         # автозапуск
```

---

## Часть 3. 10 вопросов с собеседований (подробно)

---

### Вопрос 1. Что такое SystemD и зачем он нужен?

**Ответ:**

**SystemD** — система инициализации и менеджер сервисов. Запускается ядром как **PID 1**.

**Что делает:**
- Запускает сервисы при загрузке.
- Управляет зависимостями.
- Перезапускает упавшие сервисы.
- Ведёт логи (journald).
- Управляет таймерами.
- Управляет монтированием ФС.

**До SystemD** был init (SysV init) — запускал сервисы последовательно. SystemD работает параллельно, быстрее.

**Фраза для собеса:**
> SystemD — система инициализации, PID 1. Управляет сервисами, зависимостями, логами, таймерами. Работает параллельно, быстрее старого init.

---

### Вопрос 2. Какие типы юнитов бывают в SystemD?

**Ответ:**

| Тип | Расширение | Что делает |
|:---|:---|:---|
| **Service** | `.service` | Демон |
| **Timer** | `.timer` | Аналог cron |
| **Mount** | `.mount` | Точка монтирования |
| **Socket** | `.socket` | Сокет для активации |
| **Target** | `.target` | Группа юнитов |
| **Path** | `.path` | Следит за файлами |

**Фраза для собеса:**
> Основные типы: service, timer, mount, socket, target, path.

---

### Вопрос 3. Как написать свой systemd-юнит?

**Ответ:**

Создать файл `/etc/systemd/system/myservice.service`:
```ini
[Unit]
Description=My Service
After=network.target

[Service]
Type=simple
User=myuser
ExecStart=/usr/bin/python3 /opt/myapp/server.py
Restart=on-failure
RestartSec=5
MemoryLimit=100M

[Install]
WantedBy=multi-user.target
```

Установить:
```bash
sudo systemctl daemon-reload
sudo systemctl enable myservice
sudo systemctl start myservice
sudo systemctl status myservice
```

**Фраза для собеса:**
> Юнит-файл состоит из [Unit], [Service], [Install]. В [Service] — ExecStart, Restart, User, MemoryLimit. После установки — daemon-reload, enable, start.

---

### Вопрос 4. Что такое OOM Killer и как он работает?

**Ответ:**

**OOM Killer** — механизм ядра, который убивает процессы при нехватке RAM.

**Как работает:**
1. Ядро видит, что RAM заканчивается.
2. Выбирает процесс-жертву по **oom_score**.
3. Убивает SIGKILL.
4. Освобождает память.

**Как считается score:**
- Больше памяти — выше score.
- Процессы root получают бонус.
- Можно настроить через `oom_score_adj` (от -1000 до +1000).

**Фраза для собеса:**
> OOM Killer убивает процессы при нехватке RAM. Выбирает по oom_score. Можно защитить через oom_score_adj.

---

### Вопрос 5. Как защитить важный процесс от OOM Killer?

**Ответ:**

**Способ 1: через /proc**
```bash
echo -500 > /proc/<PID>/oom_score_adj
echo -1000 > /proc/<PID>/oom_score_adj   # полностью запретить
```

**Способ 2: в systemd-юните**
```ini
[Service]
OOMScoreAdjust=-500
```

**Способ 3: в Kubernetes**
```yaml
resources:
  limits:
    memory: "512Mi"
```

**Фраза для собеса:**
> `echo -500 > /proc/<PID>/oom_score_adj` или `OOMScoreAdjust=-500` в systemd-юните. -1000 запрещает убийство.

---

### Вопрос 6. Как посмотреть логи SystemD?

**Ответ:**

```bash
journalctl                       # все логи
journalctl -u nginx              # логи сервиса
journalctl -f                    # follow
journalctl --since "1 hour ago"
journalctl -p err                # только ошибки
journalctl -b                    # с последней загрузки
```

**Фраза для собеса:**
> `journalctl -u <service>` — логи сервиса. `-f` — follow, `-p err` — ошибки, `-b` — с загрузки.

---

### Вопрос 7. Что такое cgroup OOM Killer в Kubernetes?

**Ответ:**

В Kubernetes у каждого пода есть **memory limit**. Если под превышает лимит:
1. cgroup OOM Killer убивает процесс внутри контейнера.
2. Kubernetes видит, что контейнер упал с **OOMKilled**.
3. Под перезапускается.

**Как диагностировать:**
```bash
kubectl describe pod <pod>   # смотреть OOMKilled
kubectl get events
```

**Фраза для собеса:**
> В Kubernetes OOM Killer работает внутри cgroups. Если под превышает memory limit — его убивает cgroup OOM Killer. Смотреть `kubectl describe pod`.

---

### Вопрос 8. Чем SystemD отличается от старого init?

**Ответ:**

| Характеристика | SystemD | SysV init |
|:---|:---|:---|
| Запуск | Параллельный | Последовательный |
| Зависимости | Автоматические | Ручные |
| Логи | journald | syslog |
| Перезапуск | Автоматический | Нет |
| Таймеры | Да | Нет (cron) |
| Скорость | Быстрее | Медленнее |

**Фраза для собеса:**
> SystemD работает параллельно, управляет зависимостями, перезапускает сервисы, ведёт логи через journald. Старый init — последовательный, без зависимостей.

---

### Вопрос 9. Как перезапустить сервис при падении?

**Ответ:**

В systemd-юните:
```ini
[Service]
Restart=on-failure
RestartSec=5
```

**Варианты Restart:**
- `no` — не перезапускать.
- `on-failure` — только при ошибке.
- `always` — всегда.
- `on-abnormal` — при сигналах и таймаутах.

```bash
sudo systemctl daemon-reload
sudo systemctl restart myservice
```

**Фраза для собеса:**
> В юните: `Restart=on-failure`, `RestartSec=5`. После изменения — `daemon-reload`, `restart`.

---

### Вопрос 10. Как посмотреть, какие сервисы запущены?

**Ответ:**

```bash
systemctl list-units --type=service
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service
systemctl --failed
```

**Фраза для собеса:**
> `systemctl list-units --type=service` — все запущенные. `--failed` — упавшие. `list-unit-files` — все юнит-файлы.