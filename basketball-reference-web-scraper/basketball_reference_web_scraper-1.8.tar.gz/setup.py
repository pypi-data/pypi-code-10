from distutils.core import setup
setup(
  name = 'basketball_reference_web_scraper',
  packages = [
      'basketball_reference_web_scraper/',
      'basketball_reference_web_scraper/helper_functions/',
      'basketball_reference_web_scraper/helper_functions/schedule/',
      'basketball_reference_web_scraper/helper_functions/box_score/',
      'basketball_reference_web_scraper/helper_functions/player_season_statistics/',
      'basketball_reference_web_scraper/json_encoders/',
      'basketball_reference_web_scraper/models/'
  ],
  version = '1.8',
  description = 'An API for NBA data that is scraped from Basketball Reference',
  author = 'Jae Bradley',
  author_email = 'jae.b.bradley@gmail.com',
  url = 'https://github.com/jaebradley/basketball_reference_web_scraper',
  download_url = 'https://github.com/jaebradley/basketball_reference_web_scraper/tarball/0.5',
  keywords = ['basketball', 'web scraping', 'nba', 'data'], # arbitrary keywords
  classifiers = [],
  install_requires = [
      'lxml',
      'logging',
      'urllib3',
      'pytz'
  ]
)