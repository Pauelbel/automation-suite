import os
import allure
from core.ui.base_page import BasePage


class LoginPage(BasePage):

    @allure.step('Авторизация пользователя "{username}" на сайте')
    def login_user(self,url = None, username = None, password= None):

        url = url or os.environ.get("URL")
        username = username or os.environ.get("LOGIN")
        password = password or os.environ.get("PASSWORD")

        self.page.goto(url)
        self.element("Поле ввода 'логин'", "//input[@id='user-name']").fill(username)
        self.element("Поле ввода 'пароль'", "//input[@id='password']").fill(password)
        self.element("Кнопка 'логин'", "//input[@id='login-button']").click()

