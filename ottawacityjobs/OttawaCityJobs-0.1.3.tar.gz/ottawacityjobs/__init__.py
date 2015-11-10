import requests

def get_website_content(language="en"):
    """
    Retrieve the website content

    arg: language
    type: REQUIRED
    i.e.: get_website_content('fr')
    return: json object
    """
    print('Retrieving all the jobs...')
    language = "en" if str(language).lower() == "en" else "fr"
    website = 'http://www.ottawacityjobs.ca/'+language+'/data/'
    results = requests.get(website)
    results = results.json()
    print('Done!')
    return results
    
def get_jobs(results):
    """
    Get the list of jobs in a dict format
    return: dict object
    """
    emplois = []
    for job in results['jobs']:
        emplois.append({"POSITION":job['POSITION'], 'JOBURL':job['JOBURL'], 'EXPIRYDATE': job['EXPIRYDATE'] })
    return emplois


if __name__ == '__main__':
    results = get_website_content('fr')
    jobs = get_jobs(results)
    for job in jobs:
    	job_position = ( "Offre d'empoi de la ville D'#Ottawa: " +job['POSITION']) if (len( "Offre d'empoi de la ville D'#Ottawa: " +job['POSITION']) < 117) else job['POSITION'][0:116]
    	print(job_position)

