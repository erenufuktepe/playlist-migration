from abc import ABC, abstractmethod
from typing import Mapping, Optional


class TokenProviderError(Exception):
    pass


class TokenProvider(ABC):
    @abstractmethod
    async def fetch_token(self, code: Optional[str]) -> Mapping[str, object]:
        """
        Return at least:
          - access_token (str)
          - expires_in (int)  # seconds
        """
        ...
