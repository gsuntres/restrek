from Cookie import SimpleCookie
from requests.utils import dict_from_cookiejar


SET_COOKIE_KEY = 'Set-Cookie'


def get_cookies_ignore_origin(response):
    cookies = dict_from_cookiejar(response.cookies)

    if 0 == len(cookies) and SET_COOKIE_KEY in response.headers:
        simple_cookie = SimpleCookie(response.headers[SET_COOKIE_KEY])
        for key, morsel in simple_cookie.items():
            cookies[key] = morsel.value

    return cookies
