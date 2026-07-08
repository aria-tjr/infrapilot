from pydantic import BaseModel
from typing import Optional, List
import datetime


# === Auth ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str = "viewer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# === Systems ===
class SystemCreate(BaseModel):
    name: str
    hostname: str
    os_info: str = ""
    ip_address: str = ""
    tags: List[str] = []


class SystemResponse(BaseModel):
    id: int
    name: str
    hostname: str
    os_info: str
    ip_address: str
    status: str
    tags: List[str]
    last_seen: Optional[datetime.datetime]
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# === Metrics ===
class MetricPayload(BaseModel):
    system_name: str
    cpu_percent: float
    cpu_count: int = 0
    cpu_freq_current: float = 0.0
    memory_total: int = 0
    memory_used: int = 0
    memory_percent: float
    disk_total: int = 0
    disk_used: int = 0
    disk_percent: float
    net_bytes_sent: int = 0
    net_bytes_recv: int = 0
    net_packets_sent: int = 0
    net_packets_recv: int = 0
    process_count: int = 0
    load_1min: float = 0.0
    load_5min: float = 0.0
    load_15min: float = 0.0


class MetricResponse(BaseModel):
    id: int
    system_id: int
    timestamp: datetime.datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    process_count: int

    class Config:
        from_attributes = True


# === Alerts ===
class AlertConfigCreate(BaseModel):
    name: str
    metric_type: str
    operator: str = ">"
    threshold: float
    severity: str = "warning"
    enabled: bool = True
    notification_channel: str = "telegram"
    cooldown_minutes: int = 10


class AlertConfigResponse(BaseModel):
    id: int
    name: str
    metric_type: str
    operator: str
    threshold: float
    severity: str
    enabled: bool
    notification_channel: str
    cooldown_minutes: int

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    system_id: int
    system_name: Optional[str] = None
    alert_type: str
    severity: str
    metric_value: float
    threshold: float
    message: str
    acknowledged: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# === Dashboard ===
class DashboardSummary(BaseModel):
    total_systems: int
    active_systems: int
    total_alerts: int
    critical_alerts: int
    avg_cpu: float
    avg_memory: float
    avg_disk: float