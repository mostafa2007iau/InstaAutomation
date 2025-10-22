from instagrapi import Client
from instagrapi.exceptions import LoginRequired

class InstagramService:
    def __init__(self, proxy=None):
        self.cl = Client()
        if proxy:
            self.cl.set_proxy(proxy)

    def login(self, username, password):
        """
        Logs in to Instagram using username and password.
        Returns the session data.
        """
        self.cl.login(username, password)
        return self.cl.get_settings()

    def login_with_session(self, session_data):
        """
        Logs in to Instagram using session data.
        Returns the username if successful.
        """
        self.cl.set_settings(session_data)
        # The following line is to check if the session is valid
        self.cl.get_timeline_feed()
        return self.cl.user_info(self.cl.user_id).username

    def get_user_posts(self, user_id, amount=10):
        """
        Fetches the most recent posts for a given user.
        """
        return self.cl.user_medias(user_id, amount=amount)

    def send_comment(self, post_id, text):
        """
        Sends a comment to a post.
        """
        self.cl.media_comment(post_id, text)

    def send_direct_message(self, user_id, text):
        """
        Sends a direct message to a user.
        """
        self.cl.direct_send(text, user_ids=[user_id])