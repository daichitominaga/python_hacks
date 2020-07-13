#!/usr/bin/env python

import requests
import urlparse
from bs4 import BeautifulSoup



def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = ""
res = request(target_url)
parsed_html = BeautifulSoup(res.content)
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    method = action.get("method")

    inputs_list = form.findAll("input")
    post_data = {}
    for input_tag in inputs_list:
        input_name = input_tag.get("name")
        input_type = input_tag.get("type")
        input_val = input_tag.get("value")
        if input_type == "text":
            input_val = "test"

        post_data[input_name] = input_val
    requests.post(post_url, data=data)

