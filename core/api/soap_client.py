import os
import time
import textwrap
import datetime
import json
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.plugins import Plugin
from lxml import etree
from handles import LOG_TO_FILE

class SoapApiClient:

    @staticmethod
    def _wsse():
        try:
            wsdl = os.environ.get("SOAP_WSDL")
            port = os.environ.get("SOAP_PORT")
            login = os.environ.get("SOAP_WSSE_LOGIN")
            password = os.environ.get("SOAP_WSSE_PASSWORD")

            wsse = UsernameToken(login, password) if login and password else None
            client = Client(
                wsdl=wsdl,
                wsse=wsse,
                port_name=port,
                plugins=[Logger()]
            )

            client.transport.session.verify = False
            return client.service

        except Exception as e:
            raise RuntimeError(f"Не удалось подключиться: {e}")

    @staticmethod
    def request(method, **params):
        service = SoapApiClient._wsse()
        if service is None:
            raise RuntimeError("Не удалось подключиться к SOAP сервису")
        return getattr(service, method)(**params)


class Logger(Plugin):
    """
    Класс для логирования запросов и ответов
    LOG_TO_FILE - True or False - Для записи лога в файл
    """
    LOG_TO_FILE = LOG_TO_FILE
    
    FILE_NAME = f"logs/soap_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    
    @classmethod
    def _write_log_to_file(cls, data):
        if cls.LOG_TO_FILE:
            with open(cls.FILE_NAME, 'a', encoding='utf-8') as logger_file:
                logger_file.write(data + '\n')
    
    @classmethod
    def _write_log_to_stdout(cls, data):
        print(data)

    @classmethod
    def egress(cls, envelope, http_headers, binding_options, operation):
        cls.start_time = time.time()
        
        body_str = etree.tostring(envelope, pretty_print=True, encoding="unicode")
        
        log_message = textwrap.dedent('''
            Test: {test_name}
            ------------------- Request --------------------
            Operation: {operation}
            Options: {binding_options}
            Headers: {header}
            --------------------- Body ---------------------
            Body: 
            {body}
        ''').format(
            operation=str(operation),
            binding_options=binding_options,
            header=json.dumps(http_headers, indent=4, ensure_ascii=False),
            body=body_str,
            test_name=os.environ.get('PYTEST_CURRENT_TEST', 'Unknown Test')
        )
        cls._write_log_to_file(log_message)
        cls._write_log_to_stdout(log_message)

    @classmethod  
    def ingress(cls, envelope, http_headers, operation):
        end_time = time.time()
        execution_time = end_time - cls.start_time
        
        data_str = etree.tostring(envelope, pretty_print=True, encoding="unicode")
        
        log_message = textwrap.dedent('''
            ------------------- Response --------------------
            Headers: {header}
            --------------------- Data ----------------------
            Data: 
            {data}
            ---------------- Execution Time -----------------
            Тест: {test_name} выполнялся {execution_time:.2f} секунд
        ''').format(
            header=json.dumps(dict(http_headers), indent=4, ensure_ascii=False),
            data=data_str,
            execution_time=execution_time,
            test_name=os.environ.get('PYTEST_CURRENT_TEST', 'Unknown Test')
        )
        cls._write_log_to_file(log_message)
        cls._write_log_to_stdout(log_message)