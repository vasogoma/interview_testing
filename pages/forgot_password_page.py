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
        
        # Email sent confirmation message
        self.sent_message = page.locator("span.text-green-400")
        
        # Email resent confirmation message (alert appears)
        self.resend_banner_role = page.get_by_role("alert")


    def enter_email(self, email: str):
        self.email_input.fill(email)

    def click_send(self):
        self.send_button.click()

    def get_error_message(self) -> str: #returns string with the error message
        if self.error_message.is_visible():
            return self.error_message.inner_text()
        return ""
    
    def is_error_message_visible(self) -> bool:  # returns True if error message is visible
        return self.error_message.is_visible()

    def get_sent_message(self) -> str:  # returns string with the sent confirmation message
        if self.sent_message.is_visible():
            return self.sent_message.inner_text()
        return ""
    
    def get_resend_banner_text(self) -> str: # returns string with the resent confirmation message
        try:
            self.resend_banner_role.wait_for(timeout=5000)
            return self.resend_banner_role.inner_text()
        except TimeoutError:
            return ""  # If the alert is not there, return an empty string