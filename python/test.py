import re

string = "LGL(self,ON)"
action_param = None
action_param_match = re.search(r'\((.*?)\)', string)
if action_param_match:
    action_param = action_param_match.group(1)
    print(action_param)
else:
    print("No match found")
    print(f"Input string: {string}")


