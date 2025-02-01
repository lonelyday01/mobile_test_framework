from appium.webdriver.common.appiumby import AppiumBy

class BasePageError(Exception):
    """
    Custom exception for BasePage errors.
    Used to handle specific issues related with the elements intaction
    """

class BasePage:
    """
    Base class for all page in the app
    Provides common methods or interactin with elements
    """
    def  __init__(self, driver):
        """
        initializes the base page with a WebDriver instance.

        Parameters
        -----------
        driver : WebDriver
            The appiunm WebDriver instance
        """
        self.driver = driver
        self.driver.implicitly_wait(10)

    def find_element(self, locator_type, locator_value):
        """
        Finds  a single element

        Parameters
        ----------
        locator_type : AppiumBy
            The type of locator (e.g., AppiumBy.ID, AppiumBy.XPATH).
        locator_value : str
            The actual locator value.

        Returns
        -------
        WebElement
            The found element.
        """
        return self.driver.find_element(locator_type, locator_value)

    def click(self,  locator_type, locator_value):
        """
        Clicks an element.

        Parameters
        ----------
        locator_type : AppiumBy
            The type of locator.
        locator_value : str
            The locator value.
        """
        element = self.find_element(locator_type, locator_value)
        element.click()

    def send_keys(self, locator_type, locator_value, text):
        """
        Sends text to an input field.

        Parameters
        ----------
        locator_type : AppiumBy
            The type of locator.
        locator_value : str
            The locator value.
        text : str
            The text to send.
        """
        element = self.find_element(locator_type, locator_value)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator_type, locator_value):
        """
        Gets text from an element.

        Parameters
        ----------
        locator_type : AppiumBy
            The type of locator.
        locator_value : str
            The locator value.

        Returns
        -------
        str
            The text content of the element.
        """
        element = self.find_element(locator_type, locator_value)
        return element.text