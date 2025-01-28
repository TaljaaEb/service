"" 
import requests

# Fill in your details here to be posted to the login form.
payload = {
    'login': 'user',
    'password': 'userpass'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('http://127.0.0.1:8000/accounts/login/?next=/order-summary/', data=payload)
    # print the HTML returned or something more intelligent to see if it's a successful login page.
    #print(p.text)

    # An authorised request.
    req = s.get('http://127.0.0.1:8000/order-summary/')
    #print(r.text)
        # etc...

test_str = req.text

import re

def extract_strings_recursive(test_str, tag):
    # finding the index of the first occurrence of the opening tag
    start_idx = test_str.find("<" + tag + ">")
 
    # base case
    if start_idx == -1:
        return []
 
    # extracting the string between the opening and closing tags
    end_idx = test_str.find("</" + tag + ">", start_idx)
    res = [test_str[start_idx+len(tag)+2:end_idx]]
 
    # recursive call to extract strings after the current tag
    res += extract_strings_recursive(test_str[end_idx+len(tag)+3:], tag)
 
    return res

tag = "b"
lines = extract_strings_recursive(test_str, "ln")
for line in lines:
    print(line)
