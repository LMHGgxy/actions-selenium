from undetected_chromedriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

class ScrollAction:
    """Handles scrolling on the page."""
    def __init__(self, driver: Chrome, to: str, percent: float):
        self.driver = driver
        self.to = to.lower()
        self.percent = percent

    def execute(self):
        if self.to not in ['top', 'down']:
            raise ValueError("Scroll direction must be 'top' or 'down'.")

        # Aseguramos que el porcentaje esté entre 0 y 1
        percent = max(0, min(self.percent, 1))

        if self.to == "down":
            script = """
                const scrollAmount = (document.body.scrollHeight - window.innerHeight) * arguments[0];
                window.scrollTo({ top: scrollAmount, behavior: 'smooth' });
            """
        else:  # top
            script = """
                const scrollAmount = (document.body.scrollHeight - window.innerHeight) * arguments[0];
                window.scrollTo({ top: document.body.scrollHeight - scrollAmount, behavior: 'smooth' });
            """

        self.driver.execute_script(script, percent)

class ClickAction:
    """Handles click actions on web elements."""
    def __init__(self, element: WebElement, delay: float = 0.1):
        self.element = element
        self.delay = delay
# 
    def execute(self):
        """Click the web element."""
        time.sleep(self.delay)  # Optional delay before clicking
        self.element.click()


class WriteAction:
    """Handles writing text into input fields."""
    def __init__(self, element: WebElement, text: str, delay: float = 0.1):
        self.element = element
        self.text = text
        self.delay = delay

    def execute(self):
        self.element.clear()
        for char in self.text:
            self.element.send_keys(char)
            time.sleep(self.delay)


class ExecuteJs:
    """Handles executing JavaScript on a web element."""
    def __init__(self, driver: Chrome, js_code: str, element: WebElement = None):
        self.driver = driver
        self.js_code = js_code
        self.element = element

    def execute(self):
        if self.element:
            return self.driver.execute_script(self.js_code, self.element)
        return self.driver.execute_script(self.js_code)

class GetAction:
    """Handles getting a URL."""
    def __init__(self, driver: Chrome, url: str):
        self.driver = driver
        self.url = url

    def execute(self):
        self.driver.get(self.url)

class ActionObject:
    """Creates and executes an action from the predefined list."""
    ACTIONS = {
        "click": ClickAction,
        "write": WriteAction,
        "execute": ExecuteJs,
        "get": GetAction,
        "scroll": ScrollAction,
    }

    def __init__(self, action: str, args: dict):
        if action not in self.ACTIONS:
            raise ValueError(f"Invalid action '{action}'. Allowed actions: {list(self.ACTIONS.keys())}")

        self.action = action
        self.args = args
        self.result = None

    def execute(self):
        """Dynamically execute the selected action with provided arguments."""
        action_class = self.ACTIONS[self.action]
        
        if self.action == "click":
            action_instance = action_class(self.args["element"], self.args.get("delay", 0.1))
        elif self.action == "write":
            action_instance = action_class(self.args["element"], self.args["text"], self.args.get("delay", 0.1))
        elif self.action == "execute":
            action_instance = action_class(self.args["driver"], self.args["jsCode"], self.args.get("element"))
        elif self.action == "get":
            action_instance = action_class(self.args["driver"], self.args["url"])
        elif self.action == "scroll":
            action_instance = action_class(self.args["driver"], self.args["to"], self.args["percent"])

        self.result = action_instance.execute()
        return self.result


class Actions:
    """Handles locating elements and executing predefined actions."""
    def __init__(self, driver: Chrome, locator_type: By, wait: int):
        self.driver = driver
        self.locator_type = locator_type
        self.wait_time = wait

    def __wait(self, locator: str):
        """Wait for an element to be visible and return it."""
        return WebDriverWait(self.driver, self.wait_time).until(
            EC.visibility_of_element_located((self.locator_type, locator))
        )
    
    def execute(self, command: dict):
        """Finds the element, updates arguments, and executes the action."""
        if command['action'] == 'wait':
            time.sleep(command['args']['time'])
            return

        elif command["action"] not in ["execute","get","scroll"]:
            element = self.__wait(command['args']['element'])
            command['args']['element'] = element
        
        action = ActionObject(command["action"], command["args"])
        return action.execute()
    
    def send_keys(self, text: str):
        """Sends keys to the active element using ActionChains."""

        actions = ActionChains(self.driver)
        for char in text:
            actions.send_keys(char)
        actions.perform()
    
    def send_action(self, action):
        """Sends a specific action to the active element using ActionChains."""
        actions = ActionChains(self.driver)
        if action == "tab":
            actions.send_keys("\ue004")  # Unicode for the Tab key
        elif action == "click":
            actions.click()
        actions.perform()