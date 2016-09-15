#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #START LINE from 52!!!!!!!!!! i changed the type and added value
import re
import webapp2

page_header = """
<!DOCTYPE html>

<html>
    <head><style>span.error {
    color: red;
    }
    </style>



    <title>SignUp</title>
</head>
<body>

 """
page_footer= """
</body>
</html>
 """

page_content="""


<title>SignUp!</title>

<body>
<h1>SignUp!</h1>
    <form action="/" method="post">
 <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="{username}" required>
                        <span class="error">{error_username}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" value="{pass1}" required>
                        <span class="error">{error_pass1}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" value"{verify}" required>
                        <span class="error">{error_verify}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="{email}">
                        <span class="error">{error_email}</span>
                    </td>
                </tr>
            </table>
            <input type="submit">

</form>
</body>

"""

PASS_RE= re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)
EMAIL_RE= re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

class Index(webapp2.RequestHandler):
    def write_form(self, pass1="", username="",email="", error_username="", error_pass1="", verify="", error_email="", error_verify=""):
         self.response.write(page_header+ page_content.format(username = username, pass1=pass1, error_pass1=error_pass1, email = email, error_username=error_username, verify=verify, error_verify=error_verify, error_email=error_email) + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        username=self.request.get("username")
        pass1=self.request.get("password")
        pass2=self.request.get("verify")
        email=self.request.get("email")
        error_flag= False
        params = dict(username=username, email=email)
#has to be done for locality sake
        if not valid_username(username):
            params['error_username']= "Not a valid Username!"
            error_flag=True
        if not valid_password(pass1):
            params['error_pass1']="Not a valid Password!"
            error_flag=True
        if email != "" and not valid_email(email):
            params['error_email']="Not a valid Email!"
            error_flag=True
        if pass1 != pass2:
            params['error_verify']="Passwords do not match!"
            error_flag=True
        if error_flag:
            self.write_form(**params)
        else:
            self.response.write("Welcome " + username+ "!")

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
