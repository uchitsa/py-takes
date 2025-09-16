"""
Object-oriented web framework inspired by Java Takes.
"""
from abc import ABC, abstractmethod
from typing import Final

class Take(ABC):
    """
    Fundamental processing unit that transforms Request into Response.
    
    Example:
        class HelloTake(Take):
            def act(self, request):
                return Response(text="Hello World")
    """
    
    @abstractmethod
    def act(self, request):
        """
        Process incoming request and produce response.
        
        Args:
            request: Incoming request object
            
        Returns:
            Response object
        """
        pass

class Response:
    """
    HTTP response with status, headers, and body.
    
    Example:
        Response(status=200, headers={}, body=io.BytesIO(b"Hello"))
    """
    
    def __init__(self, status, headers, body):
        self._status = status
        self._headers = headers
        self._body = body

class Request:
    """
    HTTP request with method, path, headers, and body.
    
    Example:
        Request(method="GET", path="/", headers={}, body=io.BytesIO(b""))
    """
    
    def __init__(self, method, path, headers, body):
        self._method = method
        self._path = path
        self._headers = headers
        self._body = body

class BasicTake(Take):
    """
    Take implementation that routes requests based on path.
    
    Example:
        take = BasicTake()
        take.route("/", IndexTake())
    """
    
    def __init__(self):
        self._routes = {}
    
    def route(self, path, take):
        """
        Associate path with specific take implementation.
        
        Args:
            path: URL path to match
            take: Take implementation for this path
        """
        self._routes[path] = take
    
    def act(self, request):
        try:
            take = self._routes.get(request.path())
            if take is None:
                return Response(status=404, headers={}, body=io.BytesIO(b"Not found"))
            return take.act(request)
        except Exception as error:
            return self.handle_error(error)
    
    def handle_error(self, error):
        """
        Generate error response from exception.
        
        Args:
            error: Exception instance
            
        Returns:
            Error response
        """
        return Response(
            status=500,
            headers={},
            body=io.BytesIO(f"Internal error: {error}".encode())
        )
