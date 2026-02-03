import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            status_code = response.status_code
            error_detail = None
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            status_code = 500
            error_detail = str(e)
            raise e  # Re-raise to let FastAPI handle it
        finally:
            # Log to DB in the background (or here for simplicity)
            # Ideally this should be a background task to not block response
            self.log_request(request, status_code, process_time, error_detail)

        return response

    def log_request(self, request: Request, status_code: int, process_time: float, error_detail: str = None):
        
        from app.db.session import SessionLocal
        from app.db.models.request_log import RequestLog

        try:
            db = SessionLocal()
            
            # Extract basic info
            log_entry = RequestLog(
                method=request.method,
                path=request.url.path,
                query_params=str(request.query_params),
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                status_code=status_code,
                process_time_ms=process_time,
                error_detail=error_detail
            )
            
            # TODO: Extract user_id if authenticated (requires parsing token or context)
            
            db.add(log_entry)
            db.commit()
            db.close()
        except Exception as e:
            print(f"Failed to log request: {e}")