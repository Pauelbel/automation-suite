import requests
import datetime
import json
import os
import time

from handles import LOG_TO_FILE, PRINT

class RestApiClient:
    """
    Основной клиент для отправки запросов к апи
    """
    @staticmethod
    def get(url: str, log: bool = True, **kwargs):
        """GET запрос с опциональным логированием"""
        if log:
            Logger.add_request(url, method="GET", **kwargs)
        response = requests.get(url, **kwargs)
        if log:
            Logger.add_response(response)
        return response if not response.content else response.json()

    @staticmethod
    def post(url: str, log: bool = True, **kwargs):
        """POST запрос с опциональным логированием"""
        if log:
            Logger.add_request(url, method="POST", **kwargs)
        response = requests.post(url, **kwargs)
        if log:
            Logger.add_response(response)
        return response if not response.content else response.json()

    @staticmethod
    def put(url: str, log: bool = True, **kwargs):
        """PUT запрос с опциональным логированием"""
        if log:
            Logger.add_request(url, method="PUT", **kwargs)
        response = requests.put(url, **kwargs)
        if log:
            Logger.add_response(response)
        return response if not response.content else response.json()

    @staticmethod
    def delete(url: str, log: bool = True, **kwargs):
        """DELETE запрос с опциональным логированием"""
        if log:
            Logger.add_request(url, method="DELETE", **kwargs)
        response = requests.delete(url, **kwargs)
        if log:
            Logger.add_response(response)
        return response if not response.content else response.json()

class Logger:
    """
    Вспомогательный класс для вывода красивого лога
    """
    FILE_NAME = f"logs/rest_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        if LOG_TO_FILE:
            os.makedirs(os.path.dirname(cls.FILE_NAME), exist_ok=True)
            with open(cls.FILE_NAME, 'a', encoding='utf-8') as logger_file:
                logger_file.write(data)

    @classmethod
    def _log(cls, message: str):
        cls._write_log_to_file(message)
        if PRINT:
            print(message)

    @classmethod
    def add_request(cls, url: str, method: str, **kwargs):
        """
        Логирует HTTP-запрос. Принимает любые параметры через **kwargs.
        Ожидаемые параметры: data, json, headers, cookies, params и др.
        """
        cls.start_time = time.time()

        test_name = os.environ.get('PYTEST_CURRENT_TEST', 'Unknown Test')
        timestamp = datetime.datetime.now()

        
        data = kwargs.get('data')
        json_body = kwargs.get('json')
        headers = kwargs.get('headers')
        cookies = kwargs.get('cookies')
        params = kwargs.get('params')

        log_message = (
            f"\n----------\n"
            f"Test: {test_name}\n"
            f"Time: {timestamp}\n"
            f"Request method: {method}\n"
            f"Request URL: {url}\n"
            f"Request params: {params}\n"
            f"Request Headers: {headers}\n"
            f"Request cookies: {cookies}\n"
            f"Request data: {data}\n"
            f"Request json: {json_body}\n"
            f"\n"
        )

        cls._log(log_message)

    @classmethod
    def add_response(cls, response: requests.Response):
        """
        Логирует HTTP-ответ.
        """
        end_time = time.time()
        execution_time = end_time - cls.start_time

        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)
        result_text = None

        try:
            result_text = response.json()
        except ValueError:
            result_text = response.text

        
        def safe_json_dumps(obj, indent=4, ensure_ascii=False, sort_keys=True):
            try:
                return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys)
            except (TypeError, ValueError):
                return str(obj)

        log_message = (
            f"Response code: {response.status_code}\n"
            f"Response headers:\n{safe_json_dumps(headers_as_dict)}\n"
            f"Response cookies:\n{safe_json_dumps(cookies_as_dict)}\n"
            f"Response text:\n{safe_json_dumps(result_text)}\n"
            f"Execution Time: {execution_time:.6f} seconds\n"
            f"\n----------\n"
        )

        cls._log(log_message)