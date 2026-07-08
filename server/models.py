import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base


class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, indexable=False)
    hostname = Column(String(255))
    os_info = Column(String(500))
    ip_address = Column(String(45))
    agent_version = Column(String(50))
    status = Column(String(20), default="active")  # active, inactive, error
    tags = Column(JSON, default=list)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    metrics = relationship("MetricRecord", back_populates="system", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="system", cascade="all, delete-orphan")


class MetricRecord(Base):
    __tablename__ = "metric_records"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # CPU
    cpu_percent = Column(Float)
    cpu_count = Column(Integer)
    cpu_freq_current = Column(Float)

    # Memory
    memory_total = Column(Integer)
    memory_used = Column(Integer)
    memory_percent = Column(Float)

    # Disk
    disk_total = Column(Integer)
    disk_used = Column(Integer)
    disk_percent = Column(Float)

    # Network
    net_bytes_sent = Column(Integer)
    net_bytes_recv = Column(Integer)
    net_packets_sent = Column(Integer)
    net_packets_recv = Column(Integer)

    # Processes
    process_count = Column(Integer)

    # Load
    load_1min = Column(Float)
    load_5min = Column(Float)
    load_15min = Column(Float)

    system = relationship("System", back_populates="metrics")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    alert_type = Column(String(50))  # cpu, memory, disk, custom
    severity = Column(String(20))  # info, warning, critical
    metric_name = Column(String(100))
    metric_value = Column(Float)
    threshold = Column(Float)
    message = Column(Text)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    system = relationship("System", back_populates="alerts")


class AlertConfig(Base):
    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    metric_type = Column(String(50))  # cpu, memory, disk, custom
    operator = Column(String(10), default=">")  # >, <, >=, <=, ==
    threshold = Column(Float)
    severity = Column(String(20), default="warning")
    enabled = Column(Boolean, default=True)
    notification_channel = Column(String(50), default="telegram")  # telegram, email, both
    cooldown_minutes = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    role = Column(String(20), default="viewer")  # admin, operator, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)