import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Dict, Tuple

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, rate_limit: int = 10, time_window: int = 60):
        """
        :param rate_limit: Max requests allowed per window
        :param time_window: Time window in seconds
        """
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        # In-memory store: {client_ip: (tokens, last_update_time)}
        self.request_counts: Dict[str, Tuple[float, float]] = {}

    async def dispatch(self, request: Request, call_next):
        # Identify client by IP address
        client_ip = request.client.host if request.client else "unknown"
        
        # Get current time
        now = time.time()
        
        # Get current bucket state or initialize (tokens, last_update)
        tokens, last_update = self.request_counts.get(client_ip, (self.rate_limit, now))
        
        # Calculate time passed since last request
        time_passed = now - last_update
        
        # Refill tokens based on time passed
        # Refill rate = limit / window
        refill_amount = time_passed * (self.rate_limit / self.time_window)
        tokens = min(self.rate_limit, tokens + refill_amount)
        
        if tokens >= 1:
            # Allow request, consume 1 token
            self.request_counts[client_ip] = (tokens - 1, now)
            
            # Process the request
            response = await call_next(request)
            
            # Add headers to let client know their status
            response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(int(tokens - 1))
            return response
        else:
            # Deny request
            return Response(
                content="Rate limit exceeded. Please try again later.", 
                status_code=429
            )