import os
import sys

cwd = os.getcwd()
app_name = os.path.basename(cwd)

# give our tests access to our app's code
if app_name not in sys.path: # pragma: no cover
	sys.path = [app_name] + sys.path
