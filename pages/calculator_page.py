from pages.base_page import BasePage
from pages.locators.calculator_locators import CalculatorLocators


class CalculatorPageError(Exception):
    """
    Custom exception for CalculatorPage errors.
    """


class CalculatorPage(BasePage):
    """
    Page object for the Calculator application.
    Provides methods to interact with the calculator.
    """

    def __init__(self, driver):
        """
        Initializes the calculator page.

        Parameters
        ----------
        driver : WebDriver
            The Appium WebDriver instance.
        """
        super().__init__(driver)

    def press_number(self, number):
        """
        Presses a number button.

        Parameters
        ----------
        number : int
            The number to press.
        """

        self.click(*CalculatorLocators.get_numeric_locator(number))

    def press_operator(self, operator):
        """
        Presses a operator button.

        Parameters
        ----------
        operator : str
            The operator to press.
        """
        self.click(*CalculatorLocators.get_operator_locator(operator))

    def press_equal(self):
        """
        Presses the equal ('=') button to calculate the result.
        """
        self.click(*CalculatorLocators.get_operator_locator("="))

    def get_result(self):
        """
        Retrieves the current result from the calculator display.

        Returns
        -------
        str
            The displayed result.
        """
        return self.get_text(*CalculatorLocators.get_result_locator())

    def clear_calculator(self):
        """
        Presses the 'C' button to clear the calculator.
        """
        self.click(*CalculatorLocators.get_operator_locator("C"))

    def get_empty_result(self):
        """
        Retrieves the empty result from the calculator display.

        Returns
        -------
        str
            The displayed result.
        """
        return self.get_text(*CalculatorLocators.get_empty_result())
