# 👔 Gemini Agent HR Department

<details>
<summary><b>🇷🇺 Нажмите здесь, чтобы прочитать версию на русском языке</b></summary>

## 👔 Отдел Кадров AI-Агентов

**Хватит хранить промпты в текстовых файлах. Начните управлять штатом AI-сотрудников.**

Этот репозиторий служит **Центральным Штабом (HR-департаментом)** для ваших автономных агентов. Он предоставляет CLI-панель (Nexus) для "найма" (установки) агентов в ваши проекты, управления их "навыками" и оркестрации работы.

---

### 🌟 Философия

Мы вышли за рамки простого "чата с LLM". Мы относимся к AI-агентам как к **сотрудникам** с конкретными ролями и навыками.

1.  **Реестр (`master_prompts/`)**: "Золотой источник" правды для личностей агентов (Ролей) и технических знаний (Навыков).
2.  **HR-менеджер (`nexus.py`)**: TUI-панель для просмотра проектов, мониторинга очередей задач и "установки" агентов.
3.  **Оркестратор (`agent_orchestrator.py`)**: Менеджер уровня проекта, который раздает задачи, динамически внедряет навыки и выполняет рабочие процессы.
4.  **Queue Driven Development**: Мы не используем чаты для управления работой. Мы используем **Очередь Задач** (JSON). Если задачи нет в очереди — её не существует.

---

### 🚀 Быстрый Старт

#### 1. Установка
Клонируйте этот репозиторий рядом с вашими проектами:
```bash
git clone https://github.com/mentalprotector/GeminiAgentHRdep.git
cd GeminiAgentHRdep
pip install -r requirements.txt
```

#### 2. Настройка Нового Проекта
Скопируйте "Движок" (Оркестратор) в ваш целевой проект:
```bash
mkdir my-new-project/.gemini/agents
cp GeminiAgentHRdep/templates/agent_orchestrator.py my-new-project/scripts/
```

#### 3. Запуск HR-панели
Запустите Nexus TUI из папки HR:
```bash
python nexus.py
```
*   Выберите проект из списка.
*   Нажмите **`i`**, чтобы открыть **Инсталлятор**.
*   Выберите Роли (например, `Coder`, `QA Expert`) и Навыки (например, `Flask`, `React`).
*   Нажмите **Install**.

---

### 🤖 Рабочий Процесс (V3.0)

#### Шаг 1: Постановка Задачи
В терминале вашего проекта скажите Роутеру, что нужно сделать:
```bash
python scripts/agent_orchestrator.py add --role router --instruction "Рефакторинг страницы входа с использованием новой дизайн-системы"
```

#### Шаг 2: Авто-Обнаружение
Оркестратор просыпается. Он сканирует папку `.gemini/agents/prompts/` в проекте.
*   "Я вижу, у нас есть **Coder**."
*   "Я вижу, у нас есть навык **React Design System**."
Он передает это "меню" Роутеру.

#### Шаг 3: Маршрутизация
Роутер (LLM) анализирует запрос:
> "Пользователь хочет рефакторинг UI. Назначаю **Coder** с навыком **React Design System**."

#### Шаг 4: Исполнение
Оркестратор запускает Кодера, внедряя конкретные дизайн-токены и правила из файла Навыка в контекст. Кодер пишет код, который действительно работает.

---

### 📂 Структура

```
GeminiAgentHRdep/
├── nexus.py                 # Admin TUI (Дашборд и Инсталлятор)
├── templates/
│   └── agent_orchestrator.py # V3 Оркестратор (Скопируйте это в свои проекты!)
├── master_prompts/          # Золотой Реестр
│   ├── roles/               # Личности (Coder, Planner, Reviewer)
│   ├── skills/              # Хард-скиллы (Стеки, Фреймворки)
│   └── ...
└── requirements.txt         # Зависимости (Rich, Textual)
```

</details>

**Stop managing prompts in text files. Start managing an AI Workforce.**

This repository serves as the **Central Headquarters (HR Department)** for your autonomous AI agents. It provides a CLI dashboard to "hire" (install) agents into your projects, manage their "skills" (context modules), and orchestrate their work.

---

## 🌟 Philosophy

We moved beyond simple "chat with LLM". We treat AI Agents as **employees** with specific roles and skills.

1.  **The Registry (`master_prompts/`)**: The golden source of truth for your agent personas (Roles) and technical knowledge (Skills).
2.  **The HR Manager (`nexus.py`)**: A TUI dashboard to view your projects, monitor task queues, and "install" agents.
3.  **The Orchestrator (`agent_orchestrator.py`)**: The project-level manager that assigns tasks, injects skills dynamically, and executes workflows.
4.  **Queue Driven Development**: We don't use "chats" to manage work. We use a **Task Queue** (JSON). If it's not in the queue, it doesn't exist.

---

## 🚀 Quick Start

### 1. Installation
Clone this repo alongside your other projects:
```bash
git clone https://github.com/mentalprotector/GeminiAgentHRdep.git
cd GeminiAgentHRdep
pip install -r requirements.txt
```

### 2. Setup a New Project
Copy the "Engine" (Orchestrator) to your target project:
```bash
mkdir my-new-project/.gemini/agents
cp GeminiAgentHRdep/templates/agent_orchestrator.py my-new-project/scripts/
```

### 3. Launch the HR Dashboard
Run the Nexus TUI from the HR folder:
```bash
python nexus.py
```
*   Select your project from the list.
*   Press **`i`** to open the **Installer**.
*   Select Roles (e.g., `Coder`, `QA Expert`) and Skills (e.g., `Flask`, `React`).
*   Click **Install**.

---

## 🤖 The Workflow (V3.0)

### Step 1: Assign a Task
In your project terminal, tell the Router what you need.
```bash
python scripts/agent_orchestrator.py add --role router --instruction "Refactor the login page to use new design system"
```

### Step 2: Auto-Discovery
The Orchestrator wakes up. It scans your project's `.gemini/agents/prompts/` folder.
*   "I see we have a **Coder**."
*   "I see we have the **React Design System** skill."
It feeds this "menu" to the Router.

### Step 3: Routing
The Router (LLM) analyzes the request:
> "User wants UI refactor. Assigning to **Coder** with skill **React Design System**."

### Step 4: Execution
The Orchestrator runs the Coder, injecting the specific design tokens and rules from the Skill file into the context. The Coder writes code that actually compiles.

---

## 📂 Structure

```
GeminiAgentHRdep/
├── nexus.py                 # The Admin TUI (Dashboard & Installer)
├── templates/
│   └── agent_orchestrator.py # V3 Orchestrator (Copy this to your projects!)
├── master_prompts/          # The Golden Registry
│   ├── roles/               # Agent Personas (Coder, Planner, Reviewer)
│   ├── skills/              # Hard Skills (Tech Stacks, Frameworks)
│   └── ...
└── requirements.txt         # Dependencies (Rich, Textual)
```

## 🧠 Advanced: Creating New Agents

1.  Create a file in `master_prompts/roles/my_new_agent.md`.
2.  Add YAML metadata:
    ```yaml
    ---
    role: Database Wizard
    description: Expert in SQL optimization.
    ---
    ```
3.  Open `nexus.py` and install it into your project.
4.  The Router will automatically detect it next time you run a task!

---

## 📦 Requirements
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- Google Gemini API Key (set as `GEMINI_API_KEY` env var in your projects)
