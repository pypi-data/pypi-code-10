import os

# These are required variables, by default read from the environment variables, you can put your own directly here. Register at http://www.stupeflix.com to get your API keys
stupeflixAccessKey = os.getenv("STUPEFLIX_ACCESS_KEY")
stupeflixSecretKey = os.getenv("STUPEFLIX_SECRET_KEY")
stupeflixHost = os.getenv("STUPEFLIX_HOST") or 'http://services.stupeflix.com/'

