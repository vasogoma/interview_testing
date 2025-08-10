import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from playwright.sync_api import sync_playwright, Page, expect
from pages.forgot_password_page import ForgotPasswordPage

URL = "https://app.enshift.com/forgot-password"

EXPECTED_ERROR_MESSAGES = {
    "empty": "Please enter E-Mail.",
    "invalid": "Please enter valid email address.",
}

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

# Email text input is empty
def test_forgot_password_empty_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("")
    forgot_password_page.click_send()
    assert forgot_password_page.get_error_message() == EXPECTED_ERROR_MESSAGES["empty"]

# Email text input is invalid
def test_forgot_password_invalid_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("invalid-email")
    forgot_password_page.click_send()
    assert forgot_password_page.get_error_message() == EXPECTED_ERROR_MESSAGES["invalid"]

# Email text input is SQL injection attempt
def test_forgot_password_sql_injection_attempt(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("' OR '1'='1")
    forgot_password_page.click_send()
    assert forgot_password_page.get_error_message() == EXPECTED_ERROR_MESSAGES["invalid"]

# Email text input is valid
def test_forgot_password_valid_email(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("vasogoma@hotmail.com")
    forgot_password_page.click_send()
    error_message = forgot_password_page.get_error_message()
    assert error_message == ""

# Email sent confirmation message is displayed
def test_forgot_password_sent_confirmation(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("vasogoma@hotmail.com")
    forgot_password_page.click_send()
    sent_message = forgot_password_page.get_sent_message()
    assert sent_message != ""

# Email resent confirmation message is displayed
def test_forgot_password_resend_confirmation(page: Page):
    page.goto(URL)
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.enter_email("vasogoma@hotmail.com")
    forgot_password_page.click_send()
    forgot_password_page.click_send()  # Resend the email
    resend_message = forgot_password_page.get_resend_banner_text()
    assert resend_message != ""

