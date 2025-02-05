import pytest
from pages.calculator_page import CalculatorPage

def test_press_individual_buttons(driver):
    """
    Test pressing individual buttons on the calculator.
    Ensures that buttons can be clicked without performing an operation.
    """
    calculator_page = CalculatorPage(driver)

    calculator_page.press_number(9)
    calculator_page.press_operator("+")
    calculator_page.press_number(3)
    calculator_page.press_equal()

    result = calculator_page.get_result()
    assert result == "12", f"Expected 12, but got {result}"

def test_clear_calculator(driver):
    """
    Test clearing the calculator.
    Ensures that the calculator resets after pressing 'C'.
    """
    calculator_page = CalculatorPage(driver)

    calculator_page.press_number(5)
    calculator_page.press_operator("+")
    calculator_page.press_number(2)
    calculator_page.clear_calculator()

    result = calculator_page.get_empty_result()
    assert result == "", f"Expected empty result, but got {result}"
