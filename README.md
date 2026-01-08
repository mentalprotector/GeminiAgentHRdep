# 👔 Gemini Agent HR Department

<details>
<summary><b>🇷🇺 Нажмите здесь, чтобы прочитать версию на русском языке</b></summary>

## 👔 Отдел Кадров AI-Агентов

**Управление штатом AI-сотрудников для Gemini CLI.**

Этот проект решает главную проблему работы с LLM: **потерю контекста и хаос в задачах.**
Мы превращаем Gemini CLI в автономную среду разработки, где скрипты выступают в роли "Внешней Памяти" и "Менеджера Контекста".

---

### 🌟 Философия: Зачем это нужно?

Gemini — гениальный исполнитель, но плохой менеджер. Она забывает задачи, путает файлы и теряет нить.
**Gemini Agent HRdep** дает ей структуру:

1.  **State Management (Оркестратор):** Скрипты хранят состояние проекта в JSON-файлах. Даже если сессия умрет, задачи останутся.
2.  **Context Injection (Скиллы):** Вместо того чтобы каждый раз объяснять "Как мы пишем на React", Оркестратор **автоматически** вклеивает нужные гайды в промпт перед выполнением задачи.
3.  **Role Play (Реестр):** Мы заставляем Gemini переключаться между строгими ролями (Coder, QA, Planner), чтобы она не была "мастером на все руки".

**Результат:** Вы общаетесь с Gemini в чате, а скрипты на фоне управляют файлами, контекстом и очередью задач.

---

### 🚀 Рабочий Процесс (The Loop)

#### 1. Инициализация (Bootstrap)
Вы скармливаете Gemini системный промпт (`GEMINI_TEMPLATE.md`). Теперь она знает, что работает не одна, а в паре с Оркестратором.

#### 2. Постановка задачи (Router)
Вы говорите Gemini: *"Нам нужно добавить авторизацию"*.
Gemini (как Роутер) генерирует команду для терминала:
`python agent_orchestrator.py add --role planner ...`

#### 3. Магия Оркестратора (Automation)
Вы запускаете эту команду. Скрипт:
*   Создает JSON-задачу.
*   Сканирует проект и находит нужные **Скиллы** (например, `auth_best_practices.md`).
*   Формирует идеальный промпт для следующего шага.

#### 4. Исполнение (Execution)
Вы запускаете `python agent_orchestrator.py run`. Скрипт выдает промпт. Вы кидаете его в Gemini.
Gemini видит: *"Ты Coder. Вот задача. Вот файлы. Вот правила безопасности. Пиши код."*

---

### 📂 Инструменты

#### 1. Nexus Dashboard (`nexus.py`)
TUI-панель для управления проектами. Позволяет видеть очередь задач и "нанимать" (устанавливать) новых агентов из Реестра.

<details>
<summary><b>📸 Скриншот: Dashboard</b></summary>
> `![Dashboard](INSERT_LINK_HERE)`
</details>

#### 2. Master Registry (`master_prompts/`)
Библиотека ролей и навыков. Хотите добавить тесты? Установите `QA Expert`. Хотите deploy? Установите `DevOps`.

<details>
<summary><b>📸 Скриншот: Installer</b></summary>
> `![Installer](INSERT_LINK_HERE)`
</details>

#### 3. Orchestrator (`agent_orchestrator.py`)
Движок, который живет в каждом вашем проекте. Он связывает ваши желания с файловой системой. **API-ключи не нужны**, так как он просто готовит текст для чата.

<details>
<summary><b>📸 Скриншот: Task Queue</b></summary>
> `![Task Queue](INSERT_LINK_HERE)`
</details>

---

</details>

## 👔 Gemini Agent HR Department

**Managing an AI Workforce for Gemini CLI.**

This project solves the main problem of working with LLMs: **context loss and task chaos.**
We turn Gemini CLI into an autonomous development environment where Python scripts act as "External Memory" and "Context Manager".

---

### 🌟 Philosophy: Why?

Gemini is a genius executor but a terrible manager. It forgets tasks, confuses files, and loses track.
**Gemini Agent HRdep** provides the missing structure:

1.  **State Management (Orchestrator):** Scripts persist project state in JSON files. Even if the session dies, the work remains.
2.  **Context Injection (Skills):** Instead of explaining "How we write React" every time, the Orchestrator **automatically** injects the relevant guides into the prompt right before execution.
3.  **Role Play (Registry):** We force Gemini to switch between strict roles (Coder, QA, Planner) to avoid the "jack of all trades" degradation.

**Result:** You chat with Gemini, while scripts in the background manage files, context, and the task queue.

---

### 🚀 The Loop

#### 1. Initialization (Bootstrap)
You feed the system prompt (`GEMINI_TEMPLATE.md`) to Gemini. Now it knows it's not working alone but paired with the Orchestrator.

#### 2. Task Assignment (Router)
You tell Gemini: *"We need to add auth"*.
Gemini (acting as Router) generates a terminal command:
`python agent_orchestrator.py add --role planner ...`

#### 3. Orchestrator Magic (Automation)
You run that command. The script:
*   Creates a JSON task entry.
*   Scans the project for relevant **Skills** (e.g., `auth_best_practices.md`).
*   Constructs the perfect context-rich prompt for the next step.

#### 4. Execution
You run `python agent_orchestrator.py run`. The script outputs a prompt. You paste it to Gemini.
Gemini sees: *"You are Coder. Here is the task. Here are the files. Here are the security rules. Write code."*

---

### 📂 The Toolkit

#### 1. Nexus Dashboard (`nexus.py`)
A TUI dashboard to manage your projects. View task queues and "hire" (install) new agents from the Registry.

<details>
<summary><b>📸 Screenshot: Dashboard</b></summary>
> `![Dashboard](INSERT_LINK_HERE)`
</details>

#### 2. Master Registry (`master_prompts/`)
A library of Roles and Skills. Need testing? Install `QA Expert`. Need deployment? Install `DevOps`.

<details>
<summary><b>📸 Screenshot: Installer</b></summary>
> `<img width="1294" height="718" alt="image" src="https://github.com/user-attachments/assets/2a17de1b-aa98-4faa-ae37-e43266136b0e" />
`
</details>

#### 3. Orchestrator (`agent_orchestrator.py`)
The engine that lives inside each of your projects. It bridges your intent with the file system. **No API Keys required**, as it simply prepares text for the chat interface.

<details>
<summary><b>📸 Screenshot: Task Queue</b></summary>
> `![Task Queue](INSERT_LINK_HERE)`
</details>

---

### 📦 Requirements
- Python 3.10+
- `rich`, `textual`, `pyyaml`, `pyperclip`
- **Zero-Config:** Works with any LLM interface (CLI, Web, API).
