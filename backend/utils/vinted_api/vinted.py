from backend.utils.vinted_api.items import Items
from backend.utils.vinted_api.requester import requester


class Vinted:
    """
    This class is built to connect with the vinted_api API.

    It's main goal is to be able to retrieve items from a given url search.\n

    """

    def __init__(self, proxy=None):
        """
        Args:
            Proxy : proxy to be used to bypass vinted's limite rate

        """

        if proxy is not None:
            requester.session.proxies.update(proxy)

        self.items = Items()


