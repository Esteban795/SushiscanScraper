import re

check_name = re.compile(r"^(?:\d|_)*\.(?:jpg|png)$")
string = "8.jpg"
if re.match(check_name,string):
    print("ok")
else:
    print("nope")