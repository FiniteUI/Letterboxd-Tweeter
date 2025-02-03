import twikit
import os

class Tweet:
    def __init__(self, user, email, password):
        self.client = twikit.Client()
        self.user = user
        self.email = email
        self.password = password

    def __cookiePath(self):
        path = os.path.join(os.getcwd(), 'Data', 'Twikit')
        if not os.path.isdir(path):
            os.makedirs(path)

        path = os.path.join(path, f'{self.user}-cookies.json')
        return path

    async def login(self):
        if os.path.exists(self.__cookiePath()):
            self.client.load_cookies(self.__cookiePath())
        else:
            await self.client.login(auth_info_1 = self.user, auth_info_2 = self.email, password = self.password)

            self.client.save_cookies(self.__cookiePath())

    async def post(self, contents):
        await self.login()

        #send tweet
        try:
            await self.client.create_tweet(contents)
        except twikit.errors.DuplicateTweet:
            pass


