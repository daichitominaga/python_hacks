#!/usr/bin/env python

import re
import requests
import urlparse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url= url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links_from(self, url):
        res = self.session.get(url)
        return re.findall('?:(href=")(.*)"', str(res.content.decode(errors="ignore")))

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawl(link)
        
    def extract_forms(self, url):
        res = self.session.get(url)
        parsed_html = BeautifulSoup(res.content)
        return parsed_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = action.get("method")

        inputs_list = form.findAll("input")
        data = {}
        for input_tag in inputs_list:
            input_name = input_tag.get("name")
            input_type = input_tag.get("type")
            input_val = input_tag.get("value")
            if input_type == "text":
                input_val = value

            data[input_name] = input_val
        if method == "post":
            return self.session.post(post_url, data=data)
        return self.session.get(post_url, params=data)
    
    def test_xss_in_link(self, url):
        xss_test_script = "<sCriPt>alert('test')</sCriPt>"
        url = url.replace("=", "=" + xss_test_script)
        res = self.session.get(url)
        return xss_test_script in res.content


    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCriPt>alert('test')</sCriPt>"
        res = self.submit_form(form, xss_test_script, url)
        return xss_test_script in res.content

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form ,link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in " + link + " in the following form")
                    print(form)
                if "=" in link:
                    print("\n\n[+] Testing " + link)
                    is_vulnerable_to_xss = self.test_xss_in_link(link)
                    if is_vulnerable_to_xss:
                        print("[***] XSS discovered in " + link)
                        print(form)
