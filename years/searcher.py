from __future__ import division
from datetime import datetime
from urllib import quote
from json import loads
from threading import Thread, RLock
from Queue import Queue
import requests as r
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import urllib2  #maybe python3
from xmltodict import parse
from linkedin import linkedin
import amazonproduct


#site	title	desc	url	author	location	length	date
#alltop	title	need desc	url	TBD	N/A	length?	need date?
#amazon	title	need desc	need url	author	N/A	length?	pub date?
#coursera	title	need desc	url (change name)	N/A	N/A	length	date
#indeed	title	need desc	need url	company(change)	location(change)	sal(as length)	N/A
#itunes	change(trackName)	change(genres)	change (trackViewUrl)	change(collectionName)		TBD	change(release-date)
#linkedin	change(name)	change(??)	url	N/A	change(location)	sal(as length)	TBD
#meetup	title	description	url	N/A	change(location)	need end time	date
#unl	title	change(descriptions)	need url	N/A	change(location)	need end time	date (and time)



def __init__(self):
    self.data = []

def get_json(url):
    return loads(r.get(url).content)


def flatten(lst):
    return [item for sublist in lst for item in sublist]


# --------- ALL TOP --------------------------


class Alltop(object):
    # need to add code to determine which URL to hit.
    URL = 'http://database.alltop.com/'
    #URL = newFunction(object):

    @staticmethod
    def get_results(*args):
        html = urllib2.urlopen(Alltop.URL)
        soup = BeautifulSoup(html)
        topular_ul = soup.find('ul', {'id': 'top-five'})
        results = []
        if len(topular_ul) > 0:
            #page has topular sites, for some topics it's empty
            for idx, entries in enumerate(topular_ul.find_all('li', {'class':  'hentry'})):
                a = entries.find('a')
                en = a.get_text().encode('ascii', 'ignore')
                hr = a.get('href')
            for entry in entries.find_all('div', {'class':  'full-post'}):
                site = entry.find('div', {'class':  'site-title'}).get_text().encode('ascii', 'ignore')
                date = entry.find('div', {'class':  'published'}).get_text().encode('ascii', 'ignore')
                desc = entry.find('div', {'class':  'entry-bound'}).get_text().encode('ascii', 'ignore')
                results.append({
                    'title': en,
                    'url': hr,
                    'desc': desc,
                    'date': date,
                    'author': site,
                    'content_type' : 'article',
                    'time_sensetive': 'no'

                })
        return results


# --------- AMAZON -----------------------------

# class Amazon():
#     ACCESS_KEY = 'AKIAIAW7JXESRBCM2BLA'
#     SECRET_KEY = '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'
#     ASSOCIATE_TAG = '4319-1549-2008'

#     @staticmethod
#     def get_results(job_title):
#         api = amazonproduct.API(access_key_id=Amazon.ACCESS_KEY, secret_access_key=Amazon.SECRET_KEY,associate_tag=Amazon.ASSOCIATE_TAG, locale='us')
#         items = api.item_search('Books', Keywords=job_title)
#         results = []
#         for item in items[0:5]:
#             try:
#                 tite = str(item.ItemAttributes.Title)
#                 author = str(item.ItemAttributes.Author)
#                 results.append({
#                                 'author': author,
#                                 'title': tite
#                                 })
#             #Some rows don't have the author or title attributes
#             except AttributeError:
#                 pass
#         return results


class Amazon():
    ACCESS_KEY = 'AKIAIAW7JXESRBCM2BLA'
    SECRET_KEY = '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'
    ASSOCIATE_TAG = '4319-1549-2008'

    @staticmethod
    def get_results(job_title):
        api = amazonproduct.API(access_key_id=Amazon.ACCESS_KEY, secret_access_key=Amazon.SECRET_KEY,associate_tag=Amazon.ASSOCIATE_TAG, locale='us')
        items = api.item_search('Books', Keywords=job_title)
        results = []
        for item in items[0:5]:
            try:
                tite = item.ItemAttributes.Title
                author = item.ItemAttributes.Author
                results.append({
                                'author': author,
                                'title': tite
                                })
            #Some rows don't have the author or title attributes
            except AttributeError:
                pass
        return results


# ------- COURSERA --------------------------------

class Coursera(object):
    URL = 'https://api.coursera.org/api/catalog.v1/courses?q=search&query=%s&includes=sessions'
    SESSION_URL = 'https://api.coursera.org/api/catalog.v1/sessions?ids=%s&fields=startYear,startMonth,startDay,name,durationString,shortDescription'

    @staticmethod
    def get_results(job_title):
        searched_items = get_json(Coursera.URL % quote(job_title))['elements']
        results = []
        for item in searched_items:
            session_ids = [session_id for session_id in item['links']['sessions']]
            url = Coursera.SESSION_URL % (','.join(map(str, session_ids)))
            sessions_json = get_json(url)['elements']
            for session_json in sessions_json:
                try:
                    course_date = datetime(int(session_json['startYear']), int(session_json['startMonth']),
                                           int(session_json['startDay']))
                except KeyError:
                    course_date = datetime(10, 1, 1, 1, 1, 1)  #some rows don't specify dates, ignore those
                if datetime.today() < course_date:
                    results.append({'title': item['name'], 'length': session_json['durationString'],
                                    'url': session_json['homeLink'],
                                    'date': course_date})     #'desc':session_json['shortDescription']

        return results


# -------- INDEED ------------------------------------

class Indeed():
    URL = 'http://api.indeed.com/ads/apisearch?publisher=9988125764049772&q=&l=austin%2C+tx&sort=&radius=&st=&jt=&start=&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip%20=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2'

    @staticmethod
    def get_results(job_title):
        url = Indeed.URL.replace('&q=', '&q=' + quote(job_title))
        content = r.get(url).content
        result_dict = parse(content)
        jobs = result_dict['response']['results']['result'][:3]
        results = [{'title': job['jobtitle'], 'location': job['formattedLocationFull'], 'author': job['source'], 'url':job['url'], 'desc':job['snippet'], 'date':job['date']} for
                   job in jobs]
        return results


# -------- ITUNES --------------------------------

class ItunesU(object):
    URL = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch?term=%s&media=iTunesU&entity=podcast'

    @staticmethod
    def get_results(job_title):
        url = ItunesU.URL % quote(job_title)
        json = get_json(url)
        results = []
        for row in json['results'][0:5]:
            results.append({'title': row['trackName'], 'desc':row['genres'], 'url':row['trackViewUrl'],
                        'author': row['collectionName'],
                        'date': row['releaseDate'] } )

        return results


#class ItunesPodcasts(object):
#    URL = 'https://itunes.apple.com/search?term=%s&entity=podcast'

#    @staticmethod
#    def get_results(job_title):
#        results = []
#        url = ItunesPodcasts.URL % quote(job_title)
#        results.append({'title': item['trackName'], 'desc':session_json['genres'], 'url':session_json['trackViewUrl'],
#                        'author': session_json['collectionName'], 'length': session_json['durationString'],
#                        'date': session_json['releaseDate'] } )

#        return results

# -------- LINKEDIN --------------------------------

class LinkedIn(object):
    API_KEY = '75i3mk2maw6ogl'
    SECRET_KEY = 'MDasUmDtjPbYa1I9'
    USER_TOKEN = '6b759135-60ec-4885-81e3-8bc025ac3591'
    USER_SECRET = '344b6e0c-0a22-4896-baaa-9457ffdb621c'
    RETURN_URL = ''

    @staticmethod
    def get_results(job_title, zip_code, country_code):
        authentication = linkedin.LinkedInDeveloperAuthentication(LinkedIn.API_KEY, LinkedIn.SECRET_KEY,
                                                                  LinkedIn.USER_TOKEN, LinkedIn.USER_SECRET,
                                                                  LinkedIn.RETURN_URL,
                                                                  linkedin.PERMISSIONS.enums.values())
        application = linkedin.LinkedInApplication(authentication)
        selectors = [{'people': ['first-name', 'last-name', 'headline']}]
        params = {'keywords': job_title, 'postal-code': zip_code, 'country-code': country_code}
        results = application.search_profile(selectors=selectors, params=params)
        return results



# ---------- MEETUP -------------------

class Meetup():
    API_KEY = '7369551518c62716596b04c10b57'
    TOPIC_URL = 'http://api.meetup.com/recommended/group_topics?text=%s&page=20&sign=true&key=%s'
    EVENTS_URL = 'https://api.meetup.com/2/open_events?&sign=true&topic=%s&page=20&radius=%s&zip=%s&key=%s'
    GROUPS_URL = 'http://api.meetup.com/2/groups?zip=11211&topic=moms3&order=members4&key=ABDE12456AB23244455'

    GROUPS = 'http://api.meetup.com/find/groups?zip=%s&text=%s&radius=%s&key=%s'


    @staticmethod
    # JUST GETS YOU A LIST OF TOPICS.  SENDS THAT TOPIC TO THE EVENT SEARCH
    def get_topic(job_title):
        url = Meetup.TOPIC_URL % (quote(job_title), Meetup.API_KEY)
        json = get_json(url)
        try:
            return json[0]['urlkey']
        except IndexError:
            return ''

    #NEED THIS SEARCH TO BE VERRY 'FUZZY'  - TRY THIS OUT!

    @staticmethod
    def get_group(job_title):
        url = Meetup.GROUP_URL % (quote(job_title), Meetup.API_KEY)
        json = get_json(url)
        try:
            return json[0]['urlkey']
        except IndexError:
            return ''

    @staticmethod
    def get_results(job_title, radius, zip_code):
        keywords = job_title.split(' ')
        radiuses = [radius for k in keywords]
        zip_codes = [zip_code for k in keywords]
        result = map(Meetup.get_single_event, keywords, radiuses, zip_codes)
        return flatten(result)

    @staticmethod
    def get_single_event(split_job_title, radius, zip_code):
        topic = Meetup.get_topic(split_job_title)
        url = Meetup.EVENTS_URL % (topic, radius, zip_code, Meetup.API_KEY)
        json = get_json(url)
        results = []
        for result in json['results']:
            cleaned_epoch = (result['time'] + result['utc_offset']) / 1000
            formatted_date = datetime.utcfromtimestamp(cleaned_epoch)

            try:
                if result['venue']:
                    venue = result['venue']
                else:
                    venue = ""
                if result['group']:
                    group = result['group']
                else:
                    group = ""

                single_res = {'description': result['description'], 'title': result['name'],
                              'date': formatted_date, 'url': result['event_url'],
                              'location':venue['city'], 'author':group['name']
                              }
                results.append(single_res)
            except:
                 a = 1

    #    return results

    #@staticmethod
    #def get_group_event(split_job_title, radius, zip_code):

        url2 = Meetup.GROUPS % (zip_code, topic, radius, Meetup.API_KEY)
        json2 = get_json(url2)
        results = []
        for res in json2:
            group = res['category']

            try:
                single_res = res['next_event']

                time = single_res['time']
                cleaned_epoch = (time - 18000000) / 1000

                rezults = {
                'date' : datetime.utcfromtimestamp(cleaned_epoch),
                'location' : res['city'],
                'desc' : res['description'],
                'url' : res['link'],
                'author' : res['name'],
                'title' : single_res['name']}

                results.append(rezults)
            except:
                a=1

        return results


# --------- ONET ------------------------------------

class Onet(object):
    URL = 'http://services.onetcenter.org/ws/mnm/search?keyword=%s'

    @staticmethod
    def get_jobs(keyword):
        xml_result = r.get(Onet.URL % quote(keyword), auth=HTTPBasicAuth('metro_community', 'jnf8739')).content
        doc = parse(xml_result)
        try:
            careers = doc['careers']['career']
            if isinstance(careers, dict):
                #the job is an exact match, example keyword - lumberjack
                return [dict(title=careers['title'])]
            else:
                results = [
                    dict(title=career['title'])
                    for career in careers]
        except KeyError:
            results = []
        return results

# ----------- UNL -------------------------------------

class UNL():
    URL = 'https://events.unl.edu/search/?q=%s&submit=Search&search=search'

    @staticmethod
    def get_results(job_title):
        keywords = job_title.split(' ')
        result = map(UNL.get_single_result, keywords)
        return flatten(result)

    @staticmethod
    def get_single_result(keyword):
        url = UNL.URL % quote(keyword)
        content = r.get(url).content
        soup = BeautifulSoup(content)
        dates = soup.find_all('td', attrs={'class': 'date'})[:5]
        titles = soup.find_all('a', attrs={'class': 'url summary'})[:5]
        descriptions = soup.find_all('blockquote', attrs={'class': 'description'})[:5]
        locations = soup.find_all('span', attrs={'class':'location'})[:5]
        results = []
        for i in range(len(dates)):
            single_result = {'title': titles[i].get_text().encode('ascii', 'ignore'),
                             'desc': descriptions[i].get_text().encode('ascii', 'ignore'),
                             'date': dates[i].get_text().encode('ascii', 'ignore'),
                             'location': locations[i].get_text().encode('ascii','ignore')}
            results.append(single_result)
        return results



# ------ GENERAL SCRAPER CLASS -----------------------


queue = Queue()
lock = RLock()
result = {}


class ScraperThread(Thread):
    def __init__(self, site_name, site, job_title, radius, zip_code):
        Thread.__init__(self)
        self.site = site
        self.job_title = job_title
        self.site_name = site_name
        self.radius = radius
        self.zip_code = zip_code

    def run(self):
        try:
            if self.site != Meetup:
                site_result = self.site.get_results(self.job_title)
            else:
                site_result = self.site.get_results(self.job_title, self.radius, self.zip_code)
            queue.put((self.site_name, site_result))

        except:
            #In case opf rare errors, ignore site and return empty list
            queue.put((self.site_name, []))



class SearchClass():
    """description of class"""
    def __init__(self, *args, **kw):
        pass

    def scrape_jobs(self, keyword):
        return Onet.get_jobs(keyword)


    def scrape_sites(self, siter, job_title, radius, zip_code):

        sites = {'UNL': ['UNL', UNL], 'Amazon':['Amazon', Amazon], 'Alltop':['Alltop', Alltop],
            'Meetup':['Meetup', Meetup], 'Indeed':['Indeed', Indeed], 'Coursera':['Coursera', Coursera],
            'ItunesU':['ItunesU', ItunesU], 'LinkedIn':['LinkedIn', LinkedIn]}

        site_name = sites[siter][0]

        site = sites[siter][1]

        threads = []

        t = ScraperThread(site_name, site, job_title, radius, zip_code)
        t.start()
        with lock:
            threads.append(t)

        for thread in threads:
            thread.join()
            with lock:
                site_name, site_result = queue.get()
                result[site_name] = site_result
        return result


        #def scrape_sites(self, siter, job_title, radius, zip_code):
        #sites = {'unl': ['UNL', UNL], 'amazon':['Amazon', Amazon], 'alltop':['Alltop', Alltop],
        #    'meeetup':['Meetup', Meetup], 'indeed':['Indeed', Indeed], 'coursera':['Coursera', Coursera],
        #    'itunes':['ItunesU', ItunesU], 'linked':['LinkedIn', LinkedIn]}

        #site_name = sites[siter][0]
        #site = sites[siter][1]

        #site_result = ScraperThread(site_name, site, job_title, radius, zip_code)

        #result[site_name] = site_result
        #return result


# job_title = "science workshop"
# radius = 50
# zip_code = 68106
# l = LinkingIn()
# a = l.scrape_sites(job_title, radius, zip_code)
# print a
