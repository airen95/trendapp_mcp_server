import aiohttp
from abc import ABC, abstractmethod
from typing import Optional, Any
from loguru import logger
import asyncio

class BaseAsyncRequest(ABC):
    def __init__(self,
                url: str,
                headers: dict[str, str]):
        
        self.url = url
        self.headers = headers
        self._session = None

    def set_content_type(self, content_type: str) -> None:
        self.default_content_type = content_type
        self.headers["Content-Type"] = content_type

    def _get_full_endpoint(self, path: str) -> str:
        """
        Construct the full endpoint URL.
        """
        # Ensure path starts with / if not empty
        if path and not path.startswith("/"):
            path = f"/{path}"
            
        return f"{self.url}{path}"
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create the aiohttp session.
        """
        return aiohttp.ClientSession(headers=self.headers)
    
    async def close(self):
        """Close the aiohttp session."""
        pass
    
    async def __aenter__(self):
        """Support for async context manager."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Support for async context manager."""
        await self.close()
    
    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        data: Any = None,
        params: Optional[dict[str, Any]] = None,
        timeout: float = 60.0 * 3,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Make an API request to Databricks.
        """

        session = await self._get_session()
        url = self._get_full_endpoint(path)
        
        # Use custom headers for this request if provided, otherwise use default headers
        request_headers = headers if headers is not None else self.headers
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            async with session.request(method,
                                    url,
                                    json = json,
                                    data=data,
                                    params=params,
                                    timeout=timeout,
                                    headers = request_headers) as response:
                response.raise_for_status()

                if response.content_type == 'application/json':
                    return await response.json()
                else:
                    text = await response.text()
                    return {"response": text}
        except aiohttp.ClientResponseError as e:
            logger.error(f"Request failed with status {e.status}: {e.message}")
            raise e
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Request error: {str(e)}")
            raise e
        finally:
            # cleaning after each request
            if session and not session.closed:
                await session.close()

    
    async def get(self, path: str = "", params: dict[str, Any] = None, headers: Optional[dict[str, str]] = None, timeout: float = 30.0) -> dict[str, Any]:
        return await self._request("GET", path, params=params, headers=headers, timeout=timeout)
    
    async def post(self, path: str = "", data: Any = None, json: dict = None, headers: Optional[dict[str, str]] = None, timeout: float = 30.0) -> dict[str, Any]:
        return await self._request("POST", path, json = json, data=data, headers=headers, timeout=timeout)
    
    async def put(self, path: str = "", data: Any = None, headers: Optional[dict[str, str]] = None, timeout: float = 30.0) -> dict[str, Any]:
        return await self._request("PUT", path, data=data, headers=headers, timeout=timeout)
    
    async def delete(self, path: str = "", headers: Optional[dict[str, str]] = None, timeout: float = 30.0) -> dict[str, Any]:
        return await self._request("DELETE", path, headers=headers, timeout=timeout)
    
    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        pass