import requests
from base64 import b64encode
try:
    import simplejson as json
except:
    import json

# Get page (all attributes and content)
# Set page content
class ConfluenceException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ConfluenceREST():
    def __init__(self, url, username, password, page=None, space=None):
        self.url = url + '/rest/api'
        self.auth_string = self._encode_username_password(username, password)
        self.data = {}
        self.headers = {"contentType": "application/json; charset=utf-8", "dataType":"json", "authorization":"Basic " + self.auth_string}
        self.page = page
        self.space = space
        self.page_data = None

    def _encode_username_password(self,username,password):
        return b64encode(username + ":" + password)

    def load_page_data(self, page=None,space=None):
        if page is not None:
            self.page = page
        if space is not None:
            self.space = space

        payload = {"title":self.page, "spaceKey":self.space}
        try:
            r = requests.get(self.url + '/content', params=payload, headers=self.headers)
        except:
            raise ConfluenceException("Error getting page.")

        self.page_data = r.json()

    def get_page_id(self, page=None,space=None):
        if self.page_data is None:
            load_page_data(page,space)
        try:
            page_id = self.page_data['results'][0]['id']
        except:
            raise ConfluenceException("Error: Unable to get page id.")

        return page_id

    def get_page_version(self, page=None, space=None):
        if self.page_data is None:
            load_page_data(page,space)

        try:
            page_version = self.page_data['version']
        except:
            raise ConfluenceException("Error: Unable to get page version.")

        return page_version

    def post_to_page(self, page=None, space=None, content=None):
        page_id = get_page_id(page,space)
        page_version = get_page_version(page,space)
        if page_id is None or page_version is None:
            return
        payload = {"version": {"number": page_version}, "id":page_id, "type":"page", "title":page,"space":{"key":space}, "body":{"storage":{"value": content,"representation":"storage"}}}
        url = self.url + "/" + page_id
        r = requests.put(url, params=payload, headers=self.headers)
        if r.status_code != 200:
            raise ConfluenceException("Error: Unable to send data.")
