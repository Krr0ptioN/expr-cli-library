import random as rand
import string


class Entity:

    @staticmethod
    def randomHashId(length: int = 8) -> str:
        """Generateing Random hash id

        Args:
            length: Length of the hsah

        Returns:
            [TODO:return]
        """
        has_chars = [
            rand.choice(string.ascii_letters)
            for _ in range(length)
        ]

        return "".join(has_chars)
