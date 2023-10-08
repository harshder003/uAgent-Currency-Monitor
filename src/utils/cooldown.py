import time


class Cooldown:
    """

    Attributes:
        per (int): Cooldown period
        _cooldown (dict[str, float]): Dictionary containing the key and the time when the key was last used

    """

    def __init__(self, per: int) -> None:
        self.per = per
        self._cooldown: dict[str, float] = {}

    def on_waiting(self, key: str) -> bool:
        """

        Args:
            key (str): Key to check

        Returns:
            bool: True if key is on cooldown, False otherwise

        """
        current = time.time()  # get current time in seconds since epoch
        if current - self._cooldown.get(key, 0) < self.per:
            return True
        return False

    def update(self, key: str) -> None:
        """

        Args:
            key (str): Key to update

        Returns:
            None

        """
        self._cooldown[key] = time.time()
