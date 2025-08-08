from playwright.sync_api import Page

class ForgotPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        # The email input has dynamic IDs and no stable attributes (e.g., name, placeholder, etc),
        # Instead use generic type selector (works because it's the only input[type='text'] on the page)
        self.email_input = page.locator("input[type='text']")
        # Button to send the password reset request
        self.send_button = page.get_by_role("button", name="Send")
        # Error message below email input when it is empty or invalid
        self.error_message = page.locator("div.destructive-text span")


    def enter_email(self, email: str):
        self.email_input.fill(email)

    def click_send(self):
        self.send_button.click()

    def get_error_message(self) -> str: #returns string with the error message
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""