from appium.webdriver.common.appiumby import AppiumBy


class CalculatorLocatorsError(Exception):
    """
    Custom exception for CalculatorLocators errors.
    """


class CalculatorLocators:
    """
    Locator for the calculator application
    """

    BASE_BTN_XPATH = "//android.widget.ImageButton[@content-desc='{button}']"
    BASE_BTN_ID = "com.google.android.calculator:id/{button}"
    RESULT_ID = "com.google.android.calculator:id/result_final"
    EMPTY_RESULT_ID = "com.google.android.calculator:id/formula"

    @classmethod
    def get_numeric_locator(cls, number):
        """
        Returns the locator for a number button.

        Parameters:
        -----
        num : int
            The number button to locate.

        Returns:
        --------
        Tuple
            The locator tuple (AppiumBy.XPATH, formatted locator).
        """
        numeric_map = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine"
        }
        if number not in numeric_map:
            raise CalculatorLocatorsError(f"Invalid number: {number}. Allowed: 0, 1, 2, 3, 4, etc.")
        return AppiumBy.XPATH, cls.BASE_BTN_XPATH.format(button=number)

    @classmethod
    def get_operator_locator(cls, operator):
        """
        Returns the locator for an operator button.

        Args:
        -----
        operator : str
            The operator button to locate (e.g., "+", "-", "*", "/").

        Returns:
        --------
        Tuple
            The locator tuple (AppiumBy.XPATH, formatted locator).

        Raises:
        -------

        """
        operator_map = {
            "+": "op_add",
            "-": "op_sub",
            "*": "op_mul",
            "/": "op_div",
            "=": "eq",
            "C": "clr"
        }
        if operator not in operator_map:
            raise CalculatorLocatorsError(f"Invalid operator: {operator}. Allowed: +, -, *, /, =, C")
        return AppiumBy.ID, cls.BASE_BTN_ID.format(button=operator_map[operator])

    @classmethod
    def get_result_locator(cls):
        """
        Returns the locator for the result field.

        Returns:
        --------
        Tuple
            The locator tuple (AppiumBy.ID, RESULT_ID).
        """
        return AppiumBy.ID, cls.RESULT_ID

    @classmethod
    def get_empty_result(cls):
        """
        Returns the locator for the result field.

        Returns:
        --------
        Tuple
            The locator tuple (AppiumBy.ID, RESULT_ID).
        """
        return AppiumBy.ID, cls.EMPTY_RESULT_ID
