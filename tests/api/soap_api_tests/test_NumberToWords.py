from core.api.soap_client import  SoapApiClient
from core.utils.soap_assters import *

def test_NumberToWords():
        result = SoapApiClient.request("NumberToWords", ubiNum=123)

        assert result.strip() == "one hundred and twenty three"
        