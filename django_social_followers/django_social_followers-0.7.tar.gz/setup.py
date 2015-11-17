from setuptools import setup
setup(
    name = 'django_social_followers',
    packages = ['django_social_followers'], # this must be the same as the name above
    version = '0.7',
    description = 'Get followers from Social Media channels',
    author = 'Will And Skill AB - Sweden',
    author_email = 'info@willandskill.se',
    url = 'https://github.com/willandskill/django_social_followers', # use the URL to the github repo
    download_url = 'https://github.com/willandskill/django_social_followers/releases/tag/0.7', # I'll explain this in a second
    keywords = ['social', 'followers', 'instagram', 'facebook', 'twitter'], # arbitrary keywords
    classifiers = [],
    install_requires=[
        'django'
        'facebook-sdk',
        'tweepy',
        'python-instagram'
    ],
    )