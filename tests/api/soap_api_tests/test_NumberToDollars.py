from core.api.soap_client import  SoapApiClient


def test_NumberToDollars():
        result = SoapApiClient.request("NumberToDollars", dNum=123)

        assert result.strip() == "one hundred and twenty three dollars"
        


        