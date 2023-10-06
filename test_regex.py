import re

check_name = re.compile(r"^(\d)*\.(jpg|png)$")

print(check_name.findall("1681917695-3630-i273058.png"))