import requests
from base64 import b64encode
try:
    import simplejson as json
except:
    import json


# Get page (all attributes and content)
# Set page content

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
            print "Error getting page."

        self.page_data = r.json()

    def get_page_id(self, page=None,space=None):
        if self.page_data is None:
            load_page_data(page,space)
        try:
            page_id = self.page_data['results'][0]['id']
        except:
            print "Error: Unable to get page id."
            page_id = None

        return page_id

    def get_page_version(self, page=None, space=None):
        if self.page_data is None:
            load_page_data(page,space)

        try:
            page_version = self.page_data['version']
        except:
            print "Error: Unable to get page version."
            page_version = None

        return page_version

    # MUST ADD VERSION NUMBER!
    def post_to_page(self, page=None, space=None, content):
        page_id = get_page_id(page,space)
        page_version = get_page_version(page,space)
        if page_id is None or page_version is None:
            return
        payload = {"version": {"number": page_version}, "id":page_id, "type":"page", "title":page,"space":{"key":space}, "body":{"storage":{"value": content,"representation":"storage"}}}
        url = self.url + "/" + page_id
        r = requests.put(url, params=payload, headers=self.headers)

#{"type":"page", "id": "50333204", "body": {"storage": {"representation": "storage", "value": "<p>This is a new page</p>"}}, "space": {"key": "OPS3"}, "title": "PSI 11 Analysis","version":{"number":33}}
