 #!/usr/bin/env python
import requests

x = requests.get("http://starwars.wikia.com/wiki/Rule_of_Two")

print x, "Hello Sith World"
