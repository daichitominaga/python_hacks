#!/usr/bin/env python

import scanner


target_url = ""
links_to_ignore = ["logout_page"]
data = {"username": "", "password": "", "login": "submit"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
res = vuln_scanner.session.post("login_page", data=datat)
vuln_scanner.crawl()

forms = vuln_scanner.extract_forms("form_url")
res = vuln_scanner.submit_form(forms[0], "test", "form_url")

res = vuln_scanner.test_xss_in_link("")