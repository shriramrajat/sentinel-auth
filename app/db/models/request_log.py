from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Request Info
    method = Column(String(10), index=True)
    path = Column(String(255), index=True)
    query_params = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # User Info (if authenticated)
    user_id = Column(Integer, nullable=True, index=True)
    
    # Response Info
    status_code = Column(Integer, index=True)
    process_time_ms = Column(Float)
    error_detail = Column(Text, nullable=True)