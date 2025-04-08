Claro, aquí tienes un ejemplo de README completo en inglés para tu repositorio, con instalación, ejemplos de uso y una estructura clara:

---

# 🧠 Selenium Action Framework

A lightweight and modular Python library for browser automation using Selenium and `undetected-chromedriver`. This library simplifies repetitive web interactions by wrapping common actions like clicking, typing, scrolling, and JavaScript execution into reusable classes.

## ✨ Features

- Modular design: Each action is encapsulated in its own class.
- Unified action execution via `ActionObject`.
- Element waiting logic included.
- Smooth scrolling by percentage.
- Simulated typing with configurable delays.
- JavaScript execution support.
- Built-in ActionChains for key actions like `Tab` or `Click`.

## 📦 Installation

```bash
pip install selenium undetected-chromedriver
```

> Make sure your environment supports a compatible version of Chrome/Chromium.

## 🔧 Usage

```python
from actions import Actions
from selenium.webdriver.common.by import By
from undetected_chromedriver.v2 import Chrome

driver = Chrome()
actions = Actions(driver, By.CSS_SELECTOR, wait=10)

# Navigate to a URL
actions.execute({
    "action": "get",
    "args": { "driver": driver, "url": "https://example.com" }
})

# Wait for and write into an input field
actions.execute({
    "action": "write",
    "args": { "element": "#username", "text": "myUser", "delay": 0.05 }
})

# Click a button
actions.execute({
    "action": "click",
    "args": { "element": "#submit", "delay": 0.1 }
})

# Scroll down 70% of the page
actions.execute({
    "action": "scroll",
    "args": { "driver": driver, "to": "down", "percent": 0.7 }
})
```

## 🔨 Supported Actions

| Action    | Description                            |
|-----------|----------------------------------------|
| `click`   | Clicks an element                      |
| `write`   | Types into an input field              |
| `scroll`  | Scrolls the page up or down by percent |
| `execute` | Runs JavaScript on a page or element   |
| `get`     | Navigates to a URL                     |
| `wait`    | Sleeps for a defined time (in seconds) |

## 🧪 Example: Sending a Key Action

```python
actions.send_action("tab")  # Simulates pressing the Tab key
```

## 🧰 Requirements

- Python 3.7+
- Google Chrome installed
- `selenium`, `undetected-chromedriver`

## 📄 License

MIT

---
