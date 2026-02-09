from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


def handle_stale(func):
    def wrapper(self, *args, **kwargs):
        tries_stale = kwargs.pop("tries_stale", 3)
        try:
            return func(self, *args, **kwargs)
        except StaleElementReferenceException as e:
            if tries_stale:
                sleep(1)
                new_el = self.refresh()
                return wrapper(new_el, *args, tries_stale=tries_stale - 1, **kwargs)
            raise e

    return wrapper
