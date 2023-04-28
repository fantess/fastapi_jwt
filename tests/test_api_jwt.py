import requests
import json


def test_fastapi():
    url = 'http://127.0.0.1:8080/'
    # login the application
    data_login = {
                "username": "FastAPIuser",
        "password": "5k5QdBhy%YLFWo42zO&J"

               }

    response_login = requests.post(f'{url}login',  json=data_login)
    resp_login_text = response_login.content.decode()

    token = json.loads(resp_login_text)['access_token']

    # get the headers in place
    headers = {'content-type': 'application/json', "Authorization":  f"Bearer {token}"}  # getting the token from above

    #collect required data
    data_app = {

        "firstname": "David",
        "lastname": "Balagué",
        "age": 59,
        "email": "dbalague@gmail.com"
    }
    # make the post with the end point, the new encryption token and the required data
    response_request = requests.post(f'{url}get_user_info', headers=headers,  json=data_app)
    resp_process_text = response_request.content.decode()
    try:
        print(json.loads(resp_process_text))
    except:
        print(resp_process_text)

    # make the get request
    response_request2 = requests.get(f'{url}get_message', headers = headers)
    resp_process_text = response_request2.content.decode()
    try:
        print(json.loads(resp_process_text))
    except:
        print(resp_process_text)
