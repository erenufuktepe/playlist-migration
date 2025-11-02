from abc import ABC, abstractmethod
from typing import Mapping, Optional
from app.core.http import get_async_client
from app.core.config import settings
import secrets
from urllib.parse import urlencode
from fastapi import Request


class TokenProviderError(Exception):
    pass

class TokenProvider(ABC):
    @abstractmethod
    async def fetch_token(self, request: Optional[Request]) -> Mapping[str, object]:
        """
        Return at least:
          - access_token (str)
          - expires_in (int)  # seconds
        """
        ...
