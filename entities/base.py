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
        return str([
            rand.choice(string.ascii_letters)
            for _ in range(length)
        ])
