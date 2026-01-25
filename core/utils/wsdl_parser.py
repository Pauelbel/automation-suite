from zeep import Client
from zeep.wsse.username import UsernameToken

def parse_wsdl():
    wsdl_url = "http://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL"

    client = Client(wsdl=wsdl_url)

    print(f"\nСервисы в WSDL: {wsdl_url}\n")

    for service_name, service in client.wsdl.services.items():
        print(f"Сервис ----> {service_name}")

        for port_name, port in service.ports.items():
            print(f"Порт ------> {port_name}")

            for op_name, operation in port.binding._operations.items():
                input_sig = operation.input.signature() if operation.input else "None"
                output_sig = operation.output.signature() if operation.output else "None"

                print(f"Операция --> {op_name}")
                print(f"   Input params:  [ {input_sig} ]")
                print(f"   Output:        [ {output_sig} ]")
        print()

if __name__ == "__main__":
    parse_wsdl()
