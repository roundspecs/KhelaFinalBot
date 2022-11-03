API_BASE_URL = 'https://codeforces.com/api/'

def solved_today_count(handle: str, count: int = 20) -> int:
    params = {
        'handle': handle,
        'count': count
    }
    _query_api('user.status', params=params)
    return 0

def _query_api(path: str, params: dict):
    url = API_BASE_URL + '/' + path
    if(params):
        url = url + '?'
    url = url + '&'.join([f'{k}={v}' for k,v in params.items()])
    print(url)

solved_today_count('roundspecs')