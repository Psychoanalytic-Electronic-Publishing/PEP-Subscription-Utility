class NoIssueUpdatesException(Exception):
    def __init__(self, message="No new articles to send to this user"):
        self.message = message
        super().__init__(self.message)