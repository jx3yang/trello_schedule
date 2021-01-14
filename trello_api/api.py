import json
import requests

from .constants import *

from data_models import TrelloCredentials as Credentials

def get_credentials(file=CRED_FILE):
    return Credentials(json.load(open(file)))

def get_boards(credentials: Credentials):
    return __make_request(
        credentials=credentials,
        path='/members/me/boards',
        params={ 'fields': 'name,url' }
    )

def get_board_id(credentials: Credentials, board_name: str):
    boards = json.loads(get_boards(credentials).text)
    for board in boards:
        if board['name'] == board_name:
            return board['id']
    return None

def get_list_id(credentials: Credentials, board_id: str, list_name: str):
    lists = json.loads(get_lists(credentials, board_id).text)
    for lst in lists:
        if lst['name'] == list_name:
            return lst['id']
    return None

def get_custom_fields(credentials: Credentials, board_id: str):
    return __make_request(
        credentials=credentials,
        path=f'/boards/{board_id}/customFields'
    )

def get_lists(credentials: Credentials, board_id: str):
    return __make_request(
        credentials=credentials,
        path=f'/boards/{board_id}/lists'
    )

def get_cards(credentials: Credentials, list_id: str):
    return __make_request(
        credentials=credentials,
        path=f'/lists/{list_id}/cards'
    )

def create_card(credentials: Credentials, list_id: str, params={}):
    return __make_request(
        credentials=credentials,
        path='/cards',
        params={ **params, 'idList': list_id }
    )

def update_card_custom_field(credentials: Credentials, card_id: str, field_id: str, field_value: str):
    return __make_request(
        credentials=credentials,
        path=f'/cards/{card_id}/customField/{field_id}/item',
        data={ 'value': field_value },
        method='PUT'
    )

def __make_request(
    credentials: Credentials,
    path: str,
    method='GET',
    params={},
    data=None,
    headers={ 'Accept': 'application/json' },
    base_url=BASE_URL
):
    params = {**params, **credentials}
    if data:
        data = json.dumps(data)
        headers['Content-Type'] = 'application/json; charset=utf-8'
    
    return requests.request(
        method=method,
        url=f'{base_url}{path}',
        params=params,
        data=data,
        headers=headers
    )
    