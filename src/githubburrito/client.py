from typing import Any 

from requests import Session
from returns.result import Result

from githubburrito.errors import Errors

from .types import Headers



class GHClient:
    """
    The main client
    """

    token: str
    custom_headers: Headers

    def __init__(
        self,
        *,
        token: str,
        custom_headers: Headers | None = None,
    ):
        self.headers = custom_headers or dict()
        self.token = token


    def _handle_error(self, response):
        match response.status_code:
            case 401: return Errors.UNAUTHENTIFIED
            case 403: return Errors.UNAUTHORIZED
            case 500: return Errors.SERVER_ERROR
            case _: return Errors.UNKNOWN

    def connect(self) -> Result["ConnectedGHClient", str]:
        """
        Connect the client with the provided token and encapsulate the return value.

        The encapsulation forces you to cleanly handle the case when the client isn't
        connected
        """

        session = Session()
        session.headers.update({"Authentication": f"Bearer {self.token}"})

        response = session.get("https://api.github.com/events")
            
        print(response.headers)
        print(response.status_code)

        if not response.ok:
            return Result.from_failure(self._handle_error(response))

        return Result.from_value(
            ConnectedGHClient(custom_headers=self.headers, token=self.token, session=session)
        )


class ConnectedGHClient(GHClient):
    """
    Represents a connected GHClient, with a usable session
    """

    __session: Session

    def __init__(self, /, **kwargs):
        session = kwargs.pop("session")

        super().__init__(**kwargs)

        self.__session = session


    def request(self, method, url: str, data: dict[str, Any] | None = None, headers: dict | None = None) -> Result[dict, Errors]:
        response = self.__session.request(method, url=url, data=data, headers=headers)


        if not response.ok:
            return Result.from_failure(self._handle_error(response))

        return Result.from_value(response.json())


    def get(self, url: str, headers: dict | None = None) -> Result[dict, Errors]:
        return self.request("get", url, None, headers)

    def events(self) -> Result:
        return self.get(url="/events")
        
