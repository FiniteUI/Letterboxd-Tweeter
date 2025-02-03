import feedparser
from ConfigurationFile import ConfigurationFile
from Tweet import Tweet
from datetime import datetime
from time import mktime, sleep
import asyncio
import os
import dotenv

def run():
    print('Process starting. Initializing...')

    #grab settings
    valid = True

    #if we are running on docker, envs are supplied directly. If not, we load the file
    from_docker = os.getenv('DOCKER')
    if from_docker is None:
        print("Running locally...")
        dotenv.load_dotenv('Letterboxd-Poster.env')
    else:
        print("Running in Docker...")

    letterboxd_account = os.getenv('LETTERBOXD_ACCOUNT')
    if letterboxd_account == '' or letterboxd_account is None:
        valid = False
        print("Error: Required key [LETTERBOXD_ACCOUNT] missing from configuration file [Letterboxd-Poster.env]]")

    twitter_user = os.getenv('TWITTER_USER')
    if twitter_user == '' or twitter_user is None:
        valid = False
        print("Error: Required key [TWITTER_USER] missing from configuration file [Letterboxd-Poster.env]]")

    twitter_email = os.getenv('TWITTER_EMAIL')
    if twitter_email == '' or twitter_email is None:
        valid = False
        print("Error: Required key [TWITTER_EMAIL] missing from configuration file [Letterboxd-Poster.env]]")

    twitter_password = os.getenv('TWITTER_PASSWORD')
    if twitter_password == '' or twitter_password is None:
        valid = False
        print("Error: Required key [TWITTER_PASSWORD] missing from configuration file [Letterboxd-Poster.env]]")

    #if this is the first time running, initialize the variables, do not run
    registry = ConfigurationFile('registry')
    if not registry.getValue("loaded", False):
        registry.setValue("loaded", True)
        registry.setValue('last_post', datetime.now())

    if valid:
        while True:
            print("Checking for new entries...")

            #load tweet poster
            tweeter = Tweet(twitter_user, twitter_email, twitter_password)

            #now grab rss feed
            rss_url = f'https://letterboxd.com/{letterboxd_account}/rss'
            rss_feed = feedparser.parse(rss_url)

            #grab last post
            last_post = datetime.fromisoformat(registry.getValue('last_post'))

            #check for any new diary entries on letterboxd
            posted = False
            for item in rss_feed.entries:
                item_date = datetime.fromtimestamp(mktime(item.published_parsed))
                if item_date > last_post:
                    posted = True
                    post_text = f'Just watched {item.letterboxd_filmtitle} ({item.letterboxd_filmyear}) and rated it {item.letterboxd_memberrating} on Letterboxd:\n{item.link}'
                    registry.setValue('last_post_contents', post_text)

                    print(f'Sending tweet: [{post_text}]')
                    asyncio.run(tweeter.post(post_text))

                    registry.setValue('total_posts', registry.getValue('total_posts', 0) + 1)
                else:
                    break

            if posted:
                registry.setValue('last_post', datetime.now())

            registry.setValue('last_process', datetime.now())
            print("Process complete. Waiting...")

            sleep(300)
    else:
        print('Aborting process.')

#run program
if __name__ == '__main__':
    run()