import requests
import json

print("Para que funcione, el seller debe de estar configurado correctamente!!")
collector_id = input("cuál es el collector ID? ")


def get_appli(fcollector):
    url = "https://internal-api.mercadolibre.com/applications/search?owner_id="+fcollector
    res = requests.get(url)
    appli_json = res.json()
    appli_to_python = json.dumps(appli_json)
    appli_to_json = json.loads(appli_to_python)
    return appli_to_json

collector_obtained = get_appli(collector_id)
dict_obtained = collector_obtained[0]  #Estamos obteniendo el elemento 0 que es un diccionario
final_app_id = str(dict_obtained["id"])

def get_keys(ffinal_app_id,fcollector_id):
    url = "https://internal-api.mercadolibre.com/applications/" + ffinal_app_id + "/credentials?caller.id=" + fcollector_id
    res = requests.get(url)
    keys_json = res.json()
    keys_to_python = json.dumps(keys_json)
    keys_to_json = json.loads(keys_to_python)
    return keys_to_json


result = get_keys(final_app_id, collector_id)
final_access = result["access_token"]
final_public = result["public_key"]

def tokenizar(Tpublic_key):
    #url = "https://api.mercadopago.com/v1/card_tokens?public_key=APP_USR-eb48a47d-b8ad-418a-9a11-dc58ea267d73"
    url = "https://api.mercadopago.com/v1/card_tokens?public_key="+Tpublic_key
    payload = {
                "card_number": "4984607278707868",
                "expiration_month": "11",
                "expiration_year": "2025",
                "security_code": "123",
                "cardholder": {
                    "name": "APRO",
                },
            }
    payload_params = json.dumps(payload)
    res = requests.post(url, data=payload_params)
    return res.json()

pre_token = tokenizar(final_public)
token = pre_token["id"]

def hacer_pago(Ftoken,Faccess_token):
    url = "https://api.mercadopago.com/v1/payments"
    headers = {"Authorization": "Bearer "+Faccess_token}
    payload = {
                "payer":
                {
                    "first_name": "Jake",
                    "last_name": "Peralta",
                    "email": "specializedmxbuyer+711062489@testuser.com"
                },
                "external_reference": "90011",
                "description" : "Automatic testing",
                "transaction_amount": 500,
                "payment_method_id": "visa",
                "token": Ftoken,
                "installments": 1,
                "notification_url": "https://www.yourdomain.com/notification",
                "additional_info":
                {
                    "items": [
                    {
                        "id": "281762",
                        "title": "Automatic purchase",
                        "description": "Compra automatica TN",
                        "quantity": 1,
                        "unit_price": "1000",
                        "category_id": "Other"
                    }],
                    "payer":
                    {
                        "first_name": "Jake",
                        "last_name": "Peralta",
                        "phone":
                        {
                            "area_code": "52",
                            "number": "5555555555"
                        },
                        "address": {
                            "zip_code": "03100",
                            "street_name": "Calle",
                            "street_number": "123"
                        },
                    },
                }
            }
    payload_params = json.dumps(payload)
    res = requests.post(url, data=payload_params, headers=headers)
    return res.json()

pago = hacer_pago(token,final_access)
payment_id = pago["id"]
print("Payment ID: "+ str(payment_id))


def fdevolucion(payment,access_token):
    url = "https://api.mercadopago.com/v1/payments/"+str(payment)+"/refunds"
    headers = {"Authorization": "Bearer "+access_token}
    res = requests.post(url, headers=headers)
    return res.json()

devolucion = fdevolucion(payment_id,final_access)
dev_id = devolucion["id"]
print("Devolución ID: "+str(dev_id))






