import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from playwright.sync_api import sync_playwright, Page, expect
from pages.forgot_password_page import ForgotPasswordPage

URL = "https://app.enshift.com/forgot-password"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_forgot_password_empty_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("")
    forgot_password_page.click_send()
    error_message = forgot_password_page.get_error_message()
    assert error_message != ""

def test_forgot_password_invalid_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("invalid-email")
    forgot_password_page.click_send()
    error_message = forgot_password_page.get_error_message()
    assert error_message != ""

def test_forgot_password_valid_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("vasogoma@hotmail.com")
    forgot_password_page.click_send()
    error_message = forgot_password_page.get_error_message()
    assert error_message == ""


