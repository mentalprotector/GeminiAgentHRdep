# 👔 Gemini Agent HR Department

<details>
<summary><b>🇷🇺 Нажмите здесь, чтобы прочитать версию на русском языке</b></summary>

## 👔 Отдел Кадров AI-Агентов

**Автономная среда разработки для Gemini CLI.**

Этот проект превращает Gemini CLI в самостоятельного инженера, который управляет своей работой через "Внешнюю Память" (скрипты и JSON-очередь).

---

### 🌟 Философия: Автономия вместо чатов

Мы отошли от модели "человек просит — ИИ отвечает". В системе **Agent HRdep**:
1.  **ИИ управляет задачами:** Gemini сама создает JSON-билеты для подзадач.
2.  **ИИ переключает контекст:** Gemini сама вызывает Оркестратор, чтобы подгрузить нужные навыки (Skills).
3.  **Скрипты — это "Руки":** Python-скрипты позволяют ИИ фиксировать прогресс в файловой системе, что делает сессию устойчивой к сбоям.

---

### 🚀 Автономный Цикл (The Autonomous Loop)

#### 1. Инициализация (Bootstrap)
Вы даете Gemini файл `GEMINI.md`. С этого момента она знает, что инструменты управления — в её руках.

#### 2. Планирование и Роутинг
Вы даете общую цель (например, "Сделай поиск").
Gemini CLI **сама** вызывает:
`python scripts/agent_orchestrator.py add --role router --instruction "..."`

#### 3. Исполнение
Gemini CLI последовательно вызывает:
`python scripts/agent_orchestrator.py run`
...получает инструкции, пишет код...
`python scripts/agent_orchestrator.py complete TASK-ID`

#### 4. Контроль
Вы наблюдаете за процессом через **Nexus Dashboard** (`nexus.py`), где в реальном времени обновляются логи и статусы задач.

---

</details>

## 👔 Gemini Agent HR Department

**Autonomous Development Environment for Gemini CLI.**

This project transforms Gemini CLI into a self-sufficient engineer that manages its work via "External Memory" (scripts and a JSON task queue).

---

### 🌟 Philosophy: Autonomy over Chatting

We moved beyond the "human asks — AI responds" model. In the **Agent HRdep** system:
1.  **AI Manages Tasks:** Gemini creates its own JSON tickets for sub-tasks.
2.  **AI Switches Context:** Gemini calls the Orchestrator to inject relevant Skills dynamically.
3.  **Scripts are "Hands":** Python scripts allow the AI to persist progress in the filesystem, making the session crash-proof.

---

### 🚀 The Autonomous Loop

#### 1. Bootstrap
You feed Gemini the system context (`GEMINI.md`). From this point, the AI takes control of the orchestration tools.

#### 2. Planning & Routing
You provide a high-level goal (e.g., "Implement search").
Gemini CLI **automatically** executes:
`python scripts/agent_orchestrator.py add --role router --instruction "..."`

#### 3. Execution
Gemini CLI iterates through the queue:
`python scripts/agent_orchestrator.py run`
...receives injected skills, writes code...
`python scripts/agent_orchestrator.py complete TASK-ID`

#### 4. Oversight
You monitor the progress via the **Nexus Dashboard** (`nexus.py`), viewing real-time logs and task statuses.

---

### 📦 Requirements
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- **Designed for Gemini CLI:** Works best when the AI has permission to execute shell commands.
