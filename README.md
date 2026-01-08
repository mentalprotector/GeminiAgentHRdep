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
2.  **HR-менеджер (`nexus.py`)**: TUI-панель для просмотра проектов, мониторинга **Очереди Задач** и "установки" агентов.
3.  **Оркестратор (`agent_orchestrator.py`)**: Менеджер уровня проекта. Он работает локально, управляет JSON-файлами задач и генерирует промпты для LLM. **API-ключи не нужны!**
4.  **Queue Driven Development**: Мы не используем чаты для управления работой. Мы используем **Очередь Задач** (JSON).

---

### 🚀 Как это работает (The Gemini CLI Flow)

Этот инструмент создан для работы в паре с **Gemini CLI** (или веб-интерфейсом).

#### 1. Инициализация Сессии
В начале работы с проектом, скормите Gemini CLI системный контекст. Обычно он лежит в `GEMINI.md`.
> "Вот контекст моего проекта. Изучи его перед началом работы."

#### 2. Постановка Задачи (Router)
В терминале (не в чате!) создайте задачу для Роутера:
```bash
python scripts/agent_orchestrator.py add --role router --instruction "Нужно добавить кнопку лайка"
```

#### 3. Магия Роутера (System Agent)
Запустите оркестратор: `python scripts/agent_orchestrator.py run`
*   **Важно:** Роутер — это **Системный Агент**. У него нет статического промпта.
*   Оркестратор сканирует папку `.gemini/agents` в вашем проекте.
*   Он собирает список всех установленных агентов (Coder, QA) и скиллов (React, SQL).
*   Он формирует "Меню" и внедряет его в промпт Роутера.
*   **Вы копируете этот промпт и отправляете в Gemini CLI.**

#### 4. Решение
Gemini (в роли Роутера) анализирует запрос и выдает JSON-план. Вы сохраняете этот JSON (или скрипт делает это за вас).

#### 5. Мониторинг
Запустите `nexus.py` и откройте вкладку **Tasks**. Вы увидите всю очередь задач в красивом интерфейсе.

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
```

---

### 📦 Требования
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- **Никаких API ключей:** Всё взаимодействие происходит через ваш текущий интерфейс чата (CLI/Web). Скрипты управляют только файловой системой.

</details>

## 👔 Gemini Agent HR Department

**Stop managing prompts in text files. Start managing an AI Workforce.**

This repository serves as the **Central Headquarters (HR Department)** for your autonomous AI agents. It provides a CLI dashboard to "hire" (install) agents into your projects, manage their "skills" (context modules), and orchestrate their work.

---

### 🌟 Philosophy

We moved beyond simple "chat with LLM". We treat AI Agents as **employees** with specific roles and skills.

1.  **The Registry (`master_prompts/`)**: The golden source of truth for your agent personas (Roles) and technical knowledge (Skills).
2.  **The HR Manager (`nexus.py`)**: A TUI dashboard to view your projects, monitor the **Task Queue**, and "install" agents.
3.  **The Orchestrator (`agent_orchestrator.py`)**: The project-level manager. It runs locally, manages JSON task files, and generates prompts for the LLM. **No API Keys required!**
4.  **Queue Driven Development**: We don't use "chats" to manage work state. We use a **Task Queue** (JSON).

---

### 🚀 The Gemini CLI Workflow

This toolset is designed to empower your **Gemini CLI** (or Web Interface) sessions.

#### 1. Session Bootstrap
Start your session by feeding the context to Gemini. Usually found in `GEMINI.md`.
> "Here is the project context. Analyze it."

#### 2. Assign a Task (Router)
In your terminal (not chat!), assign a task to the Router:
```bash
python scripts/agent_orchestrator.py add --role router --instruction "Add a like button"
```

#### 3. Router Magic (The System Agent)
Run the orchestrator: `python scripts/agent_orchestrator.py run`
*   **Note:** The Router is a **System Agent**. It does not have a static prompt.
*   The Orchestrator scans your project's `.gemini/agents` folder.
*   It discovers installed Agents (Coder, QA) and Skills (React, SQL).
*   It builds a "Menu" and **dynamically injects** it into the Router's prompt.
*   **You copy this prompt and paste it into Gemini CLI.**

#### 4. Decision
Gemini (acting as Router) analyzes the request and outputs a JSON plan.

#### 5. Monitoring
Run `nexus.py` and switch to the **Tasks** tab. You can visualize the entire queue status in real-time.

---

### 📂 Structure

```
GeminiAgentHRdep/
├── nexus.py                 # Admin TUI (Dashboard & Installer)
├── templates/
│   └── agent_orchestrator.py # V3 Orchestrator (Copy this to your projects!)
├── master_prompts/          # The Golden Registry
│   ├── roles/               # Agent Personas (Coder, Planner, Reviewer)
│   ├── skills/              # Hard Skills (Tech Stacks, Frameworks)
│   └── ...
```

---

### 📦 Requirements
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- **NO API KEYS REQUIRED:** All interaction happens via your existing Chat Interface (CLI/Web). The Python scripts simply manage the file system state.
