import feedparser
import pynotify
import urllib
import os
from time import mktime
from datetime import datetime
from datetime import timedelta
import subprocess
import threading
import time


class notify():

    def __init__(self):
        # Configure the notification
        pynotify.init("Basic")
        # Define the image download path
        self.image_download_path = '/tmp/github_read/'
        # Check if the path exists
        self.check_image_download_path()
        # Image extension
        self.image_extension = 'jpg'
        # Image absolute path
        self.image_absolute_path = self.image_download_path

    def message(self, title=None, body=None, image=None):
        # Download the image
        self.download_image(image)
        # Create the notification
        self.n = pynotify.Notification(
            title,
            body,
            self.image_absolute_path)
        # Play a dummy sound
        subprocess.Popen([
            'paplay',
            '/usr/share/sounds/freedesktop/stereo/message.oga'
        ])
        # Show a notification
        self.n.show()

    def download_image(self, image_url):
        """
        Downloading image from the web
        """
        # Setting up the extension
        self.image_extension = image_url.split(".")[-1]
        # Join all the parts for full path
        self.image_absolute_path = "".join((
            self.image_download_path,
            "1.",
            self.image_extension
        ))
        # Download the image
        urllib.urlretrieve(
            image_url,
            self.image_absolute_path
        )

    def check_image_download_path(self):
        """
        Checking if the directory exists
        """
        if not os.path.exists(self.image_download_path):
            os.makedirs(self.image_download_path)


class github_read():

    def __init__(self):
        # Notification stuff
        self.notif = notify()
        # Feed reader stuff
        self.url = 'https://github.com/dummas.atom'
        # Feed
        self.feed = feedparser.parse(self.url)
        # Make the last check date as now
        self.last_check_date = datetime.now()
        # Timezone adjustments
        self.last_check_date = self.last_check_date + timedelta(hours=-2)

    def parse_feed(self):
        """
        Parsing the feed
        """
        print "Parsing the feed"
        self.feed = feedparser.parse(self.url)

    def check_feed(self):
        """
        Checking the feed
        """
        # Update the feed
        self.parse_feed()

        for entry in self.feed.entries:
            # Make the time
            entry_date = datetime.fromtimestamp(
                mktime(entry['updated_parsed'])
            )
            print entry_date
            print self.last_check_date
            # Check if the notification is newer than
            # the last check date
            if entry_date > self.last_check_date:
                # Display the notification
                print "Display the notification"
                self.notif.message(
                    title=entry['author'],
                    body=entry['title'],
                    image=entry['media_thumbnail'][0]['url'])
            else:
                # Update last check date, with timezone adjustments
                self.last_check_date = datetime.now() + timedelta(hours=-2)
                return

    def debug(self):
        entry = self.feed.entries[0]
        self.notif.message(
            title=entry['author'],
            body=entry['title'],
            image=entry['media_thumbnail'][0]['url'])


class App(threading.Thread):

    def __init__(self):
        """
        Super-awesome application
        """
        threading.Thread.__init__(self)
        self.github_r = github_read()

    def run(self):
        """
        Running in the rain, ohh, I'm running in the rain
        """
        print "Starting the pool"
        while True:
            print "Checking"
            self.github_r.check_feed()
            print "Sleeping for 60s"
            time.sleep(300)  # 5min sleep


if __name__ == '__main__':
    ap = App()
    ap.start()
