import pytest, allure, os
from test_data.ui import *
from tests.ui.pages.login_page import LoginPage


@allure.title('Авторизация пользователя на сайте')
@pytest.mark.skip_auth
def test_login(page):
    login_page = LoginPage(page)
    login_page.login_user()

