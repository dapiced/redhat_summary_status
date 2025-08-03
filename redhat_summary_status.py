import requests
import json
import sys
import os
import argparse
import csv
import logging
import threading
import time
import signal
import gzip
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple, NamedTuple
from pathlib import Path
from dataclasses import dataclass, asdict, field
from functools import wraps, lru_cache
from contextlib import contextmanager
from collections import deque, defaultdict
from statistics import mean, stdev
from urllib.parse import urljoin
import hashlib
import pickle
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Optional imports for enhanced features
try:
    import psutil
except ImportError:
    psutil = None

# Configuration constants
@dataclass
class PerformanceMetrics:
    """Performance tracking metrics"""
    start_time: datetime
    end_time: Optional[datetime] = None
    api_calls: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    response_time: float = 0.0
    data_size: int = 0
    errors: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @property
    def duration(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()
    
    @property
    def cache_hit_ratio(self) -> float:
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0

@dataclass
class ServiceHealthMetrics:
    """Service health analysis"""
    name: str
    status: str
    last_seen: datetime
    uptime_percentage: float = 0.0
    avg_response_time: float = 0.0
    error_count: int = 0
    trend: str = "stable"  # improving, degrading, stable
    criticality: str = "normal"  # critical, high, normal, low

@dataclass
class SystemAlert:
    """System alert structure"""
    timestamp: datetime
    severity: str  # critical, warning, info
    component: str
    message: str
    acknowledged: bool = False
    auto_resolved: bool = False

@dataclass
class AnomalyDetection:
    """AI-powered anomaly detection results"""
    component_name: str
    metric_name: str
    current_value: float
    expected_value: float
    deviation_score: float
    severity: str  # low, medium, high, critical
    confidence: float
    recommendation: str
    detected_at: datetime = field(default_factory=datetime.now)

@dataclass 
class PredictiveAlert:
    """Predictive failure analysis"""
    component_name: str
    predicted_failure_time: datetime
    probability: float
    risk_factors: List[str]
    mitigation_steps: List[str]
    confidence_level: str  # low, medium, high
    
@dataclass
class ServiceLevelObjective:
    """SLA/SLO tracking"""
    service_name: str
    target_availability: float  # 99.9%
    current_availability: float
    monthly_downtime_budget: timedelta
    consumed_downtime: timedelta
    slo_status: str  # meeting, at_risk, breached
    days_remaining: int

class AIAnalytics:
    """Advanced AI-powered analytics engine"""
    
    def __init__(self):
        self.historical_data = deque(maxlen=1000)  # Keep last 1000 data points
        self.anomaly_threshold = 2.0  # Standard deviations
        self.learning_window = 50  # Minimum data points for learning
        
    def add_data_point(self, timestamp: datetime, availability: float, 
                      component_metrics: Dict[str, float]) -> None:
        """Add new data point for analysis"""
        data_point = {
            'timestamp': timestamp,
            'availability': availability,
            'components': component_metrics
        }
        self.historical_data.append(data_point)
    
    def detect_anomalies(self) -> List[AnomalyDetection]:
        """Detect anomalies using statistical analysis"""
        if len(self.historical_data) < self.learning_window:
            return []
        
        anomalies = []
        
        # Analyze overall availability
        availabilities = [dp['availability'] for dp in self.historical_data]
        if len(availabilities) >= self.learning_window:
            avg_availability = mean(availabilities)
            std_availability = stdev(availabilities) if len(availabilities) > 1 else 0
            current_availability = availabilities[-1]
            
            if std_availability > 0:
                z_score = abs(current_availability - avg_availability) / std_availability
                if z_score > self.anomaly_threshold:
                    severity = self._get_severity_from_zscore(z_score)
                    anomalies.append(AnomalyDetection(
                        component_name="Global System",
                        metric_name="availability",
                        current_value=current_availability,
                        expected_value=avg_availability,
                        deviation_score=z_score,
                        severity=severity,
                        confidence=min(0.95, z_score / 5.0),
                        recommendation=self._get_availability_recommendation(current_availability, avg_availability)
                    ))
        
        # Analyze individual components
        component_anomalies = self._analyze_component_anomalies()
        anomalies.extend(component_anomalies)
        
        return anomalies
    
    def _analyze_component_anomalies(self) -> List[AnomalyDetection]:
        """Analyze individual component patterns"""
        anomalies = []
        
        # Get all unique component names
        all_components = set()
        for dp in self.historical_data:
            all_components.update(dp['components'].keys())
        
        for component in all_components:
            # Extract values for this component
            values = []
            for dp in self.historical_data:
                if component in dp['components']:
                    values.append(dp['components'][component])
            
            if len(values) >= self.learning_window:
                avg_value = mean(values)
                std_value = stdev(values) if len(values) > 1 else 0
                current_value = values[-1]
                
                if std_value > 0:
                    z_score = abs(current_value - avg_value) / std_value
                    if z_score > self.anomaly_threshold:
                        severity = self._get_severity_from_zscore(z_score)
                        anomalies.append(AnomalyDetection(
                            component_name=component,
                            metric_name="health_score",
                            current_value=current_value,
                            expected_value=avg_value,
                            deviation_score=z_score,
                            severity=severity,
                            confidence=min(0.95, z_score / 5.0),
                            recommendation=self._get_component_recommendation(component, current_value, avg_value)
                        ))
        
        return anomalies
    
    def _get_severity_from_zscore(self, z_score: float) -> str:
        """Convert Z-score to severity level"""
        if z_score >= 4.0:
            return "critical"
        elif z_score >= 3.0:
            return "high"
        elif z_score >= 2.5:
            return "medium"
        else:
            return "low"
    
    def _get_availability_recommendation(self, current: float, expected: float) -> str:
        """Generate recommendation for availability anomaly"""
        if current < expected:
            return "System availability below normal - investigate recent deployments and check error logs"
        else:
            return "Unusually high availability detected - verify monitoring systems are functioning correctly"
    
    def _get_component_recommendation(self, component: str, current: float, expected: float) -> str:
        """Generate component-specific recommendations"""
        if current < expected:
            return f"Component {component} performing below baseline - check service health and dependencies"
        else:
            return f"Component {component} showing exceptional performance - document configuration for other services"
    
    def predict_failures(self) -> List[PredictiveAlert]:
        """Predict potential failures using trend analysis"""
        if len(self.historical_data) < self.learning_window:
            return []
        
        predictions = []
        
        # Analyze degradation trends
        recent_data = list(self.historical_data)[-20:]  # Last 20 data points
        
        for component in self._get_components_with_trends():
            trend = self._calculate_trend(component, recent_data)
            if trend['slope'] < -0.1:  # Declining trend
                predicted_failure = self._extrapolate_failure_time(component, trend)
                if predicted_failure:
                    predictions.append(predicted_failure)
        
        return predictions
    
    def _get_components_with_trends(self) -> List[str]:
        """Get components with sufficient data for trend analysis"""
        components = defaultdict(int)
        for dp in self.historical_data:
            for comp in dp['components']:
                components[comp] += 1
        
        return [comp for comp, count in components.items() if count >= self.learning_window // 2]
    
    def _calculate_trend(self, component: str, data: List[Dict]) -> Dict[str, float]:
        """Calculate trend for a component"""
        values = []
        times = []
        
        for i, dp in enumerate(data):
            if component in dp['components']:
                values.append(dp['components'][component])
                times.append(i)
        
        if len(values) < 3:
            return {'slope': 0, 'correlation': 0}
        
        # Simple linear regression
        n = len(values)
        sum_x = sum(times)
        sum_y = sum(values)
        sum_xy = sum(t * v for t, v in zip(times, values))
        sum_x2 = sum(t * t for t in times)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x * sum_x) != 0 else 0
        
        return {'slope': slope, 'values': values, 'times': times}
    
    def _extrapolate_failure_time(self, component: str, trend: Dict) -> Optional[PredictiveAlert]:
        """Extrapolate when component might fail"""
        if trend['slope'] >= 0:
            return None
        
        # Predict when value will reach critical threshold (e.g., 50)
        critical_threshold = 50.0
        current_value = trend['values'][-1]
        
        if current_value <= critical_threshold:
            return None
        
        # Time to reach threshold
        time_to_failure = (current_value - critical_threshold) / abs(trend['slope'])
        
        # Convert to real time (assuming data points are hourly)
        failure_time = datetime.now() + timedelta(hours=time_to_failure)
        
        # Calculate probability based on trend consistency
        probability = min(0.9, abs(trend['slope']) * 0.1)
        
        confidence = "high" if probability > 0.7 else "medium" if probability > 0.4 else "low"
        
        return PredictiveAlert(
            component_name=component,
            predicted_failure_time=failure_time,
            probability=probability,
            risk_factors=[
                f"Declining trend: {trend['slope']:.3f} per hour",
                f"Current value: {current_value:.1f}",
                "Consistent degradation pattern detected"
            ],
            mitigation_steps=[
                "Schedule preventive maintenance",
                "Review recent configuration changes",
                "Check system resource utilization",
                "Verify dependency health"
            ],
            confidence_level=confidence
        )

class DatabaseManager:
    """Advanced database manager for persistent storage"""
    
    def __init__(self, db_path: str = "redhat_monitoring.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Status history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    overall_status TEXT,
                    availability_percentage REAL,
                    total_components INTEGER,
                    operational_components INTEGER,
                    raw_data TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Component metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS component_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    component_name TEXT NOT NULL,
                    status TEXT,
                    health_score REAL,
                    response_time REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    severity TEXT NOT NULL,
                    component TEXT NOT NULL,
                    message TEXT NOT NULL,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    auto_resolved BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # SLO tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS slo_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT NOT NULL,
                    period_start DATETIME NOT NULL,
                    period_end DATETIME NOT NULL,
                    target_availability REAL NOT NULL,
                    actual_availability REAL,
                    downtime_minutes INTEGER,
                    slo_status TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def store_status_history(self, data: Dict[str, Any]) -> None:
        """Store status data in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            components = data.get('components', [])
            operational = sum(1 for c in components if c.get('status') == 'operational')
            total = len(components)
            availability = (operational / total * 100) if total > 0 else 0
            
            cursor.execute("""
                INSERT INTO status_history 
                (timestamp, overall_status, availability_percentage, 
                 total_components, operational_components, raw_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now(),
                data.get('status', {}).get('indicator', 'unknown'),
                availability,
                total,
                operational,
                json.dumps(data)
            ))
            
            # Store component metrics
            for component in components:
                health_score = get_service_health_score(
                    component.get('status', 'unknown'),
                    data.get('page', {}).get('updated_at', '')
                )
                
                cursor.execute("""
                    INSERT INTO component_metrics
                    (timestamp, component_name, status, health_score)
                    VALUES (?, ?, ?, ?)
                """, (
                    datetime.now(),
                    component.get('name', 'Unknown'),
                    component.get('status', 'unknown'),
                    health_score
                ))
            
            conn.commit()
    
    def get_historical_data(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Retrieve historical data for analysis"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, availability_percentage, raw_data
                FROM status_history
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp
            """.format(hours))
            
            results = []
            for row in cursor.fetchall():
                try:
                    raw_data = json.loads(row[2])
                    results.append({
                        'timestamp': datetime.fromisoformat(row[0]),
                        'availability': row[1],
                        'components': {
                            comp.get('name', 'Unknown'): get_service_health_score(
                                comp.get('status', 'unknown'),
                                raw_data.get('page', {}).get('updated_at', '')
                            )
                            for comp in raw_data.get('components', [])
                        }
                    })
                except Exception as e:
                    logging.warning(f"Failed to parse historical data: {e}")
                    continue
            
            return results
    
    def cleanup_old_data(self, days: int = 30) -> None:
        """Clean up old data beyond retention period"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            tables = ['status_history', 'component_metrics', 'alerts']
            for table in tables:
                cursor.execute(f"""
                    DELETE FROM {table}
                    WHERE created_at < datetime('now', '-{days} days')
                """)
            
            conn.commit()

class NotificationManager:
    """Advanced notification and alerting system"""
    
    def __init__(self):
        self.email_config = CONFIG.get("notifications", {}).get("email", {})
        self.webhook_config = CONFIG.get("notifications", {}).get("webhooks", {})
        self.rate_limits = defaultdict(datetime.now)  # Rate limiting
        
    def send_alert(self, alert: SystemAlert) -> bool:
        """Send alert through configured channels"""
        try:
            # Rate limiting - don't spam
            key = f"{alert.component}_{alert.severity}"
            if (datetime.now() - self.rate_limits[key]).total_seconds() < 300:  # 5 minutes
                return False
            
            self.rate_limits[key] = datetime.now()
            
            success = False
            
            # Send email alert
            if self.email_config.get("enabled", False):
                success |= self._send_email_alert(alert)
            
            # Send webhook alert
            if self.webhook_config.get("enabled", False):
                success |= self._send_webhook_alert(alert)
            
            return success
            
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")
            return False
    
    def _send_email_alert(self, alert: SystemAlert) -> bool:
        """Send email alert"""
        try:
            config = self.email_config
            
            msg = MIMEMultipart()
            msg['From'] = config.get('from_address')
            msg['To'] = ', '.join(config.get('to_addresses', []))
            msg['Subject'] = f"[{alert.severity.upper()}] Red Hat Status Alert - {alert.component}"
            
            body = f"""
Red Hat Status Alert

Severity: {alert.severity.upper()}
Component: {alert.component}
Message: {alert.message}
Timestamp: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

This is an automated alert from Red Hat Status Monitoring System.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port', 587)) as server:
                if config.get('use_tls', True):
                    server.starttls()
                if config.get('username') and config.get('password'):
                    server.login(config.get('username'), config.get('password'))
                
                server.send_message(msg)
            
            logging.info(f"Email alert sent for {alert.component}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")
            return False
    
    def _send_webhook_alert(self, alert: SystemAlert) -> bool:
        """Send webhook alert (Slack, Teams, Discord, etc.)"""
        try:
            webhook_urls = self.webhook_config.get('urls', [])
            
            for webhook_url in webhook_urls:
                payload = {
                    'text': f"🚨 Red Hat Status Alert",
                    'attachments': [{
                        'color': self._get_color_for_severity(alert.severity),
                        'fields': [
                            {'title': 'Severity', 'value': alert.severity.upper(), 'short': True},
                            {'title': 'Component', 'value': alert.component, 'short': True},
                            {'title': 'Message', 'value': alert.message, 'short': False},
                            {'title': 'Time', 'value': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'short': True}
                        ]
                    }]
                }
                
                response = requests.post(webhook_url, json=payload, timeout=10)
                if response.status_code == 200:
                    logging.info(f"Webhook alert sent to {webhook_url}")
                else:
                    logging.warning(f"Webhook failed: {response.status_code}")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to send webhook alert: {e}")
            return False
    
    def _get_color_for_severity(self, severity: str) -> str:
        """Get color code for severity"""
        colors = {
            'critical': '#FF0000',
            'warning': '#FFA500',
            'info': '#0000FF'
        }
        return colors.get(severity, '#808080')

# Global performance tracker and AI analytics (initialized after CONFIG)
PERFORMANCE = None
AI_ANALYTICS = None
DB_MANAGER = None
NOTIFICATION_MANAGER = None

DEFAULT_CONFIG = {
    "api": {
        "url": "https://status.redhat.com/api/v2/summary.json",
        "timeout": 10,
        "max_retries": 3,
        "retry_delay": 2,
        "concurrent_requests": 1,
        "rate_limit_delay": 0.5
    },
    "output": {
        "default_directory": ".",
        "create_summary_report": True,
        "timestamp_format": "%Y%m%d_%H%M%S",
        "max_file_size_mb": 50,
        "compression": False
    },
    "display": {
        "show_percentages": True,
        "show_health_indicator": True,
        "show_group_summaries": True,
        "show_performance_metrics": False,
        "color_output": True,
        "progress_bars": False
    },
    "cache": {
        "enabled": True,
        "ttl": 300,  # 5 minutes
        "directory": ".cache",
        "max_size_mb": 100,
        "compression": True,
        "cleanup_interval": 3600  # 1 hour
    },
    "logging": {
        "enabled": False,
        "level": "INFO",
        "file": "redhat_status.log",
        "max_size_mb": 10,
        "backup_count": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "monitoring": {
        "enabled": False,
        "alert_thresholds": {
            "availability_critical": 85.0,
            "availability_warning": 95.0,
            "response_time_warning": 5.0,
            "error_rate_warning": 5.0
        },
        "health_check_interval": 300,
        "auto_recovery_attempts": 3
    },
    "performance": {
        "enable_metrics": True,
        "detailed_timing": False,
        "memory_profiling": False,
        "max_concurrent_operations": 5
    },
    "ai_analytics": {
        "enabled": True,
        "anomaly_detection": True,
        "predictive_analysis": True,
        "learning_window": 50,
        "anomaly_threshold": 2.0,
        "min_confidence": 0.7
    },
    "database": {
        "enabled": True,
        "path": "redhat_monitoring.db",
        "retention_days": 30,
        "auto_cleanup": True
    },
    "notifications": {
        "email": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "from_address": "",
            "to_addresses": [],
            "username": "",
            "password": ""
        },
        "webhooks": {
            "enabled": False,
            "urls": []
        }
    },
    "slo": {
        "enabled": True,
        "targets": {
            "global_availability": 99.9,
            "response_time": 2.0,
            "uptime_monthly": 99.5
        },
        "tracking_period": "monthly",
        "alert_on_breach": True
    }
}

def initialize_global_components():
    """Initialize global components after CONFIG is loaded"""
    global PERFORMANCE, AI_ANALYTICS, DB_MANAGER, NOTIFICATION_MANAGER
    
    if PERFORMANCE is None:
        PERFORMANCE = PerformanceMetrics(start_time=datetime.now())
    
    if AI_ANALYTICS is None and CONFIG["ai_analytics"]["enabled"]:
        AI_ANALYTICS = AIAnalytics()
    
    if DB_MANAGER is None and CONFIG["database"]["enabled"]:
        try:
            DB_MANAGER = DatabaseManager()
        except Exception as e:
            logging.warning(f"Failed to initialize database: {e}")
    
    if NOTIFICATION_MANAGER is None:
        try:
            NOTIFICATION_MANAGER = NotificationManager()
        except Exception as e:
            logging.warning(f"Failed to initialize notifications: {e}")

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json or use defaults"""
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            for section, values in user_config.items():
                if section in config:
                    config[section].update(values)
                else:
                    config[section] = values
            
            return config
        except Exception as e:
            print(f"⚠️  Warning: Could not load config file ({e}), using defaults")
            return DEFAULT_CONFIG
    
    return DEFAULT_CONFIG

# Load configuration
CONFIG = load_config()

# Initialize global components after CONFIG is available
initialize_global_components()

# Environment variable overrides
API_URL = os.getenv('REDHAT_STATUS_API_URL', CONFIG["api"]["url"])
REQUEST_TIMEOUT = int(os.getenv('REDHAT_STATUS_TIMEOUT', str(CONFIG["api"]["timeout"])))
MAX_RETRIES = int(os.getenv('REDHAT_STATUS_MAX_RETRIES', str(CONFIG["api"]["max_retries"])))
RETRY_DELAY = int(os.getenv('REDHAT_STATUS_RETRY_DELAY', str(CONFIG["api"]["retry_delay"])))

def performance_monitor(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not CONFIG["performance"]["enable_metrics"]:
            return func(*args, **kwargs)
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            PERFORMANCE.api_calls += 1
            return result
        except Exception as e:
            PERFORMANCE.errors.append(f"{func.__name__}: {str(e)}")
            raise
        finally:
            if CONFIG["performance"]["detailed_timing"]:
                duration = time.time() - start_time
                logging.debug(f"{func.__name__} took {duration:.3f}s")
    return wrapper

@contextmanager
def performance_context(operation_name: str):
    """Context manager for performance tracking"""
    start_time = time.time()
    try:
        yield
    finally:
        if CONFIG["performance"]["detailed_timing"]:
            duration = time.time() - start_time
            logging.info(f"{operation_name} completed in {duration:.3f}s")

def setup_advanced_logging() -> None:
    """Setup advanced logging with rotation and formatting"""
    if CONFIG["logging"]["enabled"]:
        from logging.handlers import RotatingFileHandler
        
        log_level = getattr(logging, CONFIG["logging"]["level"].upper(), logging.INFO)
        log_file = CONFIG["logging"]["file"]
        max_size = CONFIG["logging"]["max_size_mb"] * 1024 * 1024
        backup_count = CONFIG["logging"]["backup_count"]
        log_format = CONFIG["logging"]["format"]
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup rotating file handler
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_size, 
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # Console handler for warnings and errors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler],
            format=log_format
        )
        
        logging.info("Advanced logging initialized")

def get_cache_size() -> Tuple[int, str]:
    """Get total cache directory size"""
    try:
        cache_dir = Path(CONFIG["cache"]["directory"])
        if not cache_dir.exists():
            return 0, "0 B"
        
        total_size = 0
        for file_path in cache_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        # Convert to human readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return total_size, f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        
        return total_size, f"{total_size:.1f} TB"
    except Exception as e:
        logging.warning(f"Failed to calculate cache size: {e}")
        return 0, "Unknown"

def cleanup_cache_by_size() -> None:
    """Clean up cache if it exceeds max size"""
    try:
        max_size_bytes = CONFIG["cache"]["max_size_mb"] * 1024 * 1024
        cache_size_bytes, _ = get_cache_size()
        
        if cache_size_bytes > max_size_bytes:
            cache_dir = Path(CONFIG["cache"]["directory"])
            cache_files = list(cache_dir.rglob("*.json"))
            
            # Sort by modification time (oldest first)
            cache_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest files until under limit
            current_size = cache_size_bytes
            removed_count = 0
            
            for cache_file in cache_files:
                if current_size <= max_size_bytes:
                    break
                
                file_size = cache_file.stat().st_size
                cache_file.unlink()
                current_size -= file_size
                removed_count += 1
                
            logging.info(f"Cache cleanup: removed {removed_count} files")
            
    except Exception as e:
        logging.warning(f"Cache cleanup failed: {e}")

@lru_cache(maxsize=32)
def get_service_health_score(status: str, last_update: str) -> float:
    """Calculate service health score based on status and update time"""
    base_scores = {
        'operational': 100.0,
        'degraded_performance': 75.0,
        'partial_outage': 50.0,
        'major_outage': 25.0,
        'maintenance': 90.0
    }
    
    score = base_scores.get(status, 0.0)
    
    # Adjust based on last update time
    try:
        last_update_time = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
        time_diff = datetime.now() - last_update_time.replace(tzinfo=None)
        hours_old = time_diff.total_seconds() / 3600
        
        # Reduce score if data is stale
        if hours_old > 24:
            score *= 0.8
        elif hours_old > 12:
            score *= 0.9
            
    except Exception:
        # If we can't parse time, apply penalty
        score *= 0.85
    
    return score

def get_cache_file(cache_key: str) -> Path:
    """Get cache file path for a given key"""
    cache_dir = Path(CONFIG["cache"]["directory"])
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{cache_key}.json"

def is_cache_valid(cache_file: Path) -> bool:
    """Check if cache file is valid and not expired"""
    if not cache_file.exists():
        return False
    
    try:
        file_age = datetime.now().timestamp() - cache_file.stat().st_mtime
        return file_age < CONFIG["cache"]["ttl"]
    except Exception as e:
        logging.warning(f"Cache validation error: {e}")
        return False

def save_to_cache(cache_key: str, data: Dict[str, Any]) -> None:
    """Save data to cache with optional compression"""
    if not CONFIG["cache"]["enabled"]:
        return
    
    try:
        cache_file = get_cache_file(cache_key)
        
        # Add cache metadata
        cache_data = {
            'data': data,
            'cached_at': datetime.now().isoformat(),
            'ttl': CONFIG["cache"]["ttl"],
            'version': '3.0'
        }
        
        if CONFIG["cache"]["compression"]:
            import gzip
            with gzip.open(f"{cache_file}.gz", 'wt', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved compressed data to cache: {cache_file}.gz")
        else:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved data to cache: {cache_file}")
        
        # Track cache statistics
        PERFORMANCE.data_size += len(json.dumps(data))
        
        # Cleanup if needed
        cleanup_cache_by_size()
        
    except Exception as e:
        logging.warning(f"Cache write error: {e}")

def load_from_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """Load data from cache with compression support"""
    if not CONFIG["cache"]["enabled"]:
        return None
    
    cache_file = get_cache_file(cache_key)
    
    # Try compressed version first
    if CONFIG["cache"]["compression"]:
        compressed_file = Path(f"{cache_file}.gz")
        if compressed_file.exists() and is_cache_valid(compressed_file):
            try:
                import gzip
                with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                if cache_data.get('version') == '3.0':
                    logging.info(f"Loaded compressed data from cache: {compressed_file}")
                    print("📋 Using cached data (compressed cache hit)")
                    PERFORMANCE.cache_hits += 1
                    return cache_data['data']
            except Exception as e:
                logging.warning(f"Compressed cache read error: {e}")
    
    # Try uncompressed version
    if is_cache_valid(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # Handle legacy format
            if 'data' in cache_data:
                data = cache_data['data']
            else:
                data = cache_data  # Legacy format
                
            logging.info(f"Loaded data from cache: {cache_file}")
            print("📋 Using cached data (cache hit)")
            PERFORMANCE.cache_hits += 1
            return data
        except Exception as e:
            logging.warning(f"Cache read error: {e}")
            
    PERFORMANCE.cache_misses += 1
    return None

@performance_monitor
def get_summary_data() -> Optional[Dict[str, Any]]:
    """Retrieve and parse summary.json with native json library"""
    cache_key = "summary_data"
    
    # Try to load from cache first
    cached_data = load_from_cache(cache_key)
    if cached_data:
        return cached_data
    
    start_time = datetime.now()
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🌐 Fetching Red Hat Status data... (attempt {attempt + 1}/{MAX_RETRIES})")
            logging.info(f"Fetching data from API (attempt {attempt + 1}/{MAX_RETRIES})")
            
            response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()  # Native JSON parsing!
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                print(f"✅ Data received: {len(response.text)} characters in {duration:.2f}s")
                logging.info(f"Data fetched successfully in {duration:.2f}s")
                
                # Add performance metadata
                data['_metadata'] = {
                    'fetch_time': end_time.isoformat(),
                    'response_time': duration,
                    'attempt': attempt + 1,
                    'cached': False
                }
                
                # Save to cache
                save_to_cache(cache_key, data)
                
                # Store in database for AI analysis
                if CONFIG["database"]["enabled"]:
                    try:
                        DB_MANAGER.store_status_history(data)
                    except Exception as e:
                        logging.warning(f"Failed to store data in database: {e}")
                
                # Update AI analytics
                if CONFIG["ai_analytics"]["enabled"]:
                    try:
                        components = data.get('components', [])
                        operational = sum(1 for c in components if c.get('status') == 'operational')
                        total = len(components)
                        availability = (operational / total * 100) if total > 0 else 0
                        
                        component_metrics = {
                            comp.get('name', 'Unknown'): get_service_health_score(
                                comp.get('status', 'unknown'),
                                data.get('page', {}).get('updated_at', '')
                            )
                            for comp in components
                        }
                        
                        AI_ANALYTICS.add_data_point(end_time, availability, component_metrics)
                    except Exception as e:
                        logging.warning(f"Failed to update AI analytics: {e}")
                
                return data
            else:
                error_msg = f"HTTP Error: {response.status_code}"
                print(f"❌ {error_msg}")
                logging.error(error_msg)
                if attempt < MAX_RETRIES - 1:
                    print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                    import time
                    time.sleep(RETRY_DELAY)
                
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                import time
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"🔄 Retrying in {RETRY_DELAY} seconds...")
                import time
                time.sleep(RETRY_DELAY)
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ {error_msg}")
            logging.error(error_msg)
            break
    
    error_msg = f"Failed to fetch data after {MAX_RETRIES} attempts"
    print(f"❌ {error_msg}")
    logging.error(error_msg)
    return None

def save_status_history(status_data: Dict[str, Any]) -> None:
    """Save status data to history for trend analysis"""
    try:
        history_dir = Path(CONFIG["cache"]["directory"]) / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = history_dir / f"status_{timestamp}.json"
        
        # Create simplified history entry
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'status': status_data.get('status', {}),
            'components_summary': {
                'total': len(status_data.get('components', [])),
                'operational': sum(1 for c in status_data.get('components', []) if c.get('status') == 'operational'),
                'issues': sum(1 for c in status_data.get('components', []) if c.get('status') != 'operational')
            }
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_entry, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Status history saved: {history_file}")
        
        # Clean old history files (keep last 100)
        cleanup_old_history(history_dir)
        
    except Exception as e:
        logging.warning(f"Failed to save status history: {e}")

def cleanup_old_history(history_dir: Path, keep_count: int = 100) -> None:
    """Clean up old history files, keeping only the most recent ones"""
    try:
        history_files = list(history_dir.glob("status_*.json"))
        if len(history_files) > keep_count:
            # Sort by modification time and remove oldest
            history_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for old_file in history_files[keep_count:]:
                old_file.unlink()
                logging.info(f"Cleaned up old history file: {old_file}")
    except Exception as e:
        logging.warning(f"Failed to cleanup history: {e}")

def get_status_trend() -> Optional[Dict[str, Any]]:
    """Analyze status trends from history"""
    try:
        history_dir = Path(CONFIG["cache"]["directory"]) / "history"
        if not history_dir.exists():
            return None
        
        history_files = list(history_dir.glob("status_*.json"))
        if len(history_files) < 2:
            return None
        
        # Get last 10 entries for trend analysis
        history_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        recent_files = history_files[:10]
        
        trend_data = []
        for file in reversed(recent_files):  # Oldest first
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    trend_data.append(data)
            except Exception:
                continue
        
        if len(trend_data) >= 2:
            # Calculate trend
            current = trend_data[-1]['components_summary']
            previous = trend_data[-2]['components_summary']
            
            return {
                'current_availability': (current['operational'] / current['total'] * 100) if current['total'] > 0 else 0,
                'previous_availability': (previous['operational'] / previous['total'] * 100) if previous['total'] > 0 else 0,
                'trend_direction': 'improving' if current['operational'] > previous['operational'] else 'degrading' if current['operational'] < previous['operational'] else 'stable',
                'data_points': len(trend_data)
            }
        
    except Exception as e:
        logging.warning(f"Failed to analyze trends: {e}")
    
    return None

def clear_cache() -> None:
    """Clear all cached data"""
    try:
        cache_dir = Path(CONFIG["cache"]["directory"])
        if cache_dir.exists():
            for cache_file in cache_dir.glob("*.json"):
                cache_file.unlink()
            print("🗑️  Cache cleared successfully")
            logging.info("Cache cleared")
        else:
            print("📭 No cache found")
    except Exception as e:
        print(f"❌ Failed to clear cache: {e}")
        logging.error(f"Failed to clear cache: {e}")

def export_history_to_csv() -> None:
    """Export status history to CSV file"""
    try:
        history_dir = Path(CONFIG["cache"]["directory"]) / "history"
        if not history_dir.exists():
            print("📭 No history data found")
            return
        
        history_files = list(history_dir.glob("status_*.json"))
        if not history_files:
            print("📭 No history files found")
            return
        
        # Sort by date
        history_files.sort(key=lambda x: x.stat().st_mtime)
        
        timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
        csv_file = f"status_history_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'status_indicator', 'status_description', 'total_components', 'operational', 'issues', 'availability_percent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for file in history_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    summary = data['components_summary']
                    availability = (summary['operational'] / summary['total'] * 100) if summary['total'] > 0 else 0
                    
                    writer.writerow({
                        'timestamp': data['timestamp'],
                        'status_indicator': data['status'].get('indicator', 'unknown'),
                        'status_description': data['status'].get('description', 'No description'),
                        'total_components': summary['total'],
                        'operational': summary['operational'],
                        'issues': summary['issues'],
                        'availability_percent': f"{availability:.1f}"
                    })
                except Exception as e:
                    logging.warning(f"Failed to process history file {file}: {e}")
                    continue
        
        print(f"📊 History exported to: {csv_file}")
        logging.info(f"History exported to CSV: {csv_file}")
        
    except Exception as e:
        print(f"❌ Failed to export history: {e}")
        logging.error(f"Failed to export history: {e}")

def analyze_service_patterns() -> Dict[str, Any]:
    """Analyze service patterns and provide insights"""
    try:
        history_dir = Path(CONFIG["cache"]["directory"]) / "history"
        if not history_dir.exists():
            return {"error": "No history data available"}
        
        history_files = list(history_dir.glob("status_*.json"))
        if len(history_files) < 5:
            return {"error": "Insufficient data for pattern analysis"}
        
        # Sort by modification time
        history_files.sort(key=lambda x: x.stat().st_mtime)
        
        patterns = {
            "recurring_issues": [],
            "peak_failure_times": {},
            "service_reliability": {},
            "trend_analysis": {},
            "recommendations": []
        }
        
        # Analyze last 50 entries for patterns
        recent_files = history_files[-50:]
        
        # Track issues by hour of day
        hourly_issues = {}
        service_failures = {}
        
        for file_path in recent_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                timestamp = datetime.fromisoformat(data['timestamp'])
                hour = timestamp.hour
                total_services = data['components_summary']['total']
                issues = data['components_summary']['issues']
                
                # Track hourly patterns
                if hour not in hourly_issues:
                    hourly_issues[hour] = []
                hourly_issues[hour].append(issues / total_services * 100)
                
                # Track service reliability
                availability = (data['components_summary']['operational'] / total_services * 100) if total_services > 0 else 0
                if availability < 95:  # Consider this an incident
                    patterns["recurring_issues"].append({
                        "timestamp": data['timestamp'],
                        "availability": availability,
                        "affected_services": issues
                    })
                
            except Exception as e:
                logging.warning(f"Failed to analyze file {file_path}: {e}")
                continue
        
        # Find peak failure times
        for hour, issue_rates in hourly_issues.items():
            avg_issue_rate = sum(issue_rates) / len(issue_rates)
            patterns["peak_failure_times"][f"{hour:02d}:00"] = f"{avg_issue_rate:.1f}%"
        
        # Generate recommendations
        if patterns["recurring_issues"]:
            patterns["recommendations"].append("⚠️  Recurring issues detected - consider implementing proactive monitoring")
        
        if len(patterns["peak_failure_times"]) > 0:
            worst_hour = max(patterns["peak_failure_times"].items(), key=lambda x: float(x[1].rstrip('%')))
            patterns["recommendations"].append(f"📊 Peak issues occur around {worst_hour[0]} - schedule maintenance outside this window")
        
        patterns["analysis_date"] = datetime.now().isoformat()
        patterns["data_points_analyzed"] = len(recent_files)
        
        return patterns
        
    except Exception as e:
        logging.error(f"Pattern analysis failed: {e}")
        return {"error": str(e)}

def generate_health_report() -> Dict[str, Any]:
    """Generate comprehensive health report"""
    try:
        with performance_context("Health Report Generation"):
            data = get_summary_data()
            if not data:
                return {"error": "Unable to fetch current data"}
            
            components = data.get('components', [])
            current_time = datetime.now()
            
            report = {
                "report_timestamp": current_time.isoformat(),
                "overall_health": {},
                "service_analysis": [],
                "performance_metrics": asdict(PERFORMANCE),
                "recommendations": [],
                "alerts": []
            }
            
            # Overall health calculation
            total_services = len(components)
            operational = sum(1 for c in components if c.get('status') == 'operational')
            availability = (operational / total_services * 100) if total_services > 0 else 0
            
            report["overall_health"] = {
                "availability_percentage": availability,
                "total_services": total_services,
                "operational_services": operational,
                "degraded_services": total_services - operational,
                "health_grade": get_health_grade(availability),
                "last_updated": data.get('page', {}).get('updated_at', 'Unknown')
            }
            
            # Service-level analysis
            for component in components:
                service_health = ServiceHealthMetrics(
                    name=component.get('name', 'Unknown'),
                    status=component.get('status', 'unknown'),
                    last_seen=current_time,
                    uptime_percentage=get_service_health_score(
                        component.get('status', 'unknown'),
                        data.get('page', {}).get('updated_at', '')
                    )
                )
                
                report["service_analysis"].append(asdict(service_health))
            
            # Generate alerts
            if availability < CONFIG["monitoring"]["alert_thresholds"]["availability_critical"]:
                report["alerts"].append(SystemAlert(
                    timestamp=current_time,
                    severity="critical",
                    component="Global",
                    message=f"System availability critically low: {availability:.1f}%"
                ).__dict__)
            elif availability < CONFIG["monitoring"]["alert_thresholds"]["availability_warning"]:
                report["alerts"].append(SystemAlert(
                    timestamp=current_time,
                    severity="warning",
                    component="Global",
                    message=f"System availability below threshold: {availability:.1f}%"
                ).__dict__)
            
            # Generate recommendations
            if availability < 95:
                report["recommendations"].append("🔴 Critical: System availability needs immediate attention")
            elif availability < 99:
                report["recommendations"].append("🟡 Warning: Monitor system closely for potential issues")
            else:
                report["recommendations"].append("🟢 System health is excellent")
            
            # Add cache performance info
            cache_size_bytes, cache_size_str = get_cache_size()
            report["cache_info"] = {
                "size": cache_size_str,
                "hit_ratio": PERFORMANCE.cache_hit_ratio,
                "enabled": CONFIG["cache"]["enabled"]
            }
            
            return report
            
    except Exception as e:
        logging.error(f"Health report generation failed: {e}")
        return {"error": str(e)}

def get_health_grade(availability: float) -> str:
    """Convert availability percentage to letter grade"""
    if availability >= 99.9:
        return "A+"
    elif availability >= 99.5:
        return "A"
    elif availability >= 99.0:
        return "A-"
    elif availability >= 95.0:
        return "B"
    elif availability >= 90.0:
        return "C"
    elif availability >= 80.0:
        return "D"
    else:
        return "F"

def export_health_report() -> None:
    """Export comprehensive health report"""
    try:
        report = generate_health_report()
        if "error" in report:
            print(f"❌ Failed to generate health report: {report['error']}")
            return
        
        timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
        filename = f"health_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📋 Health report exported to: {filename}")
        
        # Also create a human-readable summary
        summary_filename = f"health_summary_{timestamp}.txt"
        create_health_summary(report, summary_filename)
        
    except Exception as e:
        print(f"❌ Failed to export health report: {e}")
        logging.error(f"Health report export failed: {e}")

def create_health_summary(report: Dict[str, Any], filename: str) -> None:
    """Create human-readable health summary"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RED HAT SYSTEM HEALTH SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            # Overall health
            health = report["overall_health"]
            f.write(f"Overall Health Grade: {health['health_grade']}\n")
            f.write(f"System Availability: {health['availability_percentage']:.2f}%\n")
            f.write(f"Operational Services: {health['operational_services']}/{health['total_services']}\n")
            f.write(f"Degraded Services: {health['degraded_services']}\n\n")
            
            # Performance metrics
            perf = report.get("performance_metrics", {})
            if perf:
                f.write("Performance Metrics:\n")
                f.write(f"  API Calls: {perf.get('api_calls', 0)}\n")
                
                # Handle cache_hit_ratio safely
                cache_hits = perf.get('cache_hits', 0)
                cache_misses = perf.get('cache_misses', 0)
                total_cache_ops = cache_hits + cache_misses
                cache_hit_ratio = (cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0.0
                
                f.write(f"  Cache Hit Ratio: {cache_hit_ratio:.1f}%\n")
                f.write(f"  Response Time: {perf.get('response_time', 0.0):.2f}s\n")
                f.write(f"  Errors: {len(perf.get('errors', []))}\n\n")
            
            # Alerts
            alerts = report.get("alerts", [])
            if alerts:
                f.write("Active Alerts:\n")
                for alert in alerts:
                    f.write(f"  [{alert['severity'].upper()}] {alert['component']}: {alert['message']}\n")
                f.write("\n")
            
            # Recommendations
            recommendations = report.get("recommendations", [])
            if recommendations:
                f.write("Recommendations:\n")
                for rec in recommendations:
                    f.write(f"  • {rec}\n")
            
            f.write(f"\nReport generated: {report['report_timestamp']}\n")
        
        print(f"📄 Health summary created: {filename}")
        
    except Exception as e:
        logging.error(f"Failed to create health summary: {e}")
        print(f"⚠️  Health summary creation failed: {e}")

def show_performance_metrics() -> None:
    """Display current performance metrics"""
    print("\n📊 PERFORMANCE METRICS")
    print("=" * 50)
    
    print(f"🕒 Session Duration: {PERFORMANCE.duration:.2f}s")
    print(f"🌐 API Calls: {PERFORMANCE.api_calls}")
    print(f"📋 Cache Hits: {PERFORMANCE.cache_hits}")
    print(f"❌ Cache Misses: {PERFORMANCE.cache_misses}")
    print(f"📈 Cache Hit Ratio: {PERFORMANCE.cache_hit_ratio:.1f}%")
    print(f"⚡ Avg Response Time: {PERFORMANCE.response_time:.2f}s")
    print(f"📦 Data Transferred: {PERFORMANCE.data_size} bytes")
    
    if PERFORMANCE.errors:
        print(f"⚠️  Errors: {len(PERFORMANCE.errors)}")
        for error in PERFORMANCE.errors[-3:]:  # Show last 3 errors
            print(f"   • {error}")
    
    # Cache size information
    cache_size_bytes, cache_size_str = get_cache_size()
    print(f"💾 Cache Size: {cache_size_str}")
    
    # Memory usage (if available)
    try:
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        print(f"🧠 Memory Usage: {memory_mb:.1f} MB")
    except ImportError:
        pass  # psutil not available
    
    print()

def show_ai_insights() -> None:
    """Display AI-powered insights and anomaly detection"""
    print("\n🤖 AI-POWERED INSIGHTS")
    print("=" * 60)
    
    if not CONFIG.get("ai_analytics", {}).get("enabled", False):
        print("❌ AI Analytics is disabled in configuration")
        return
    
    if AI_ANALYTICS is None:
        print("❌ AI Analytics not initialized")
        return
    
    # Detect anomalies
    anomalies = AI_ANALYTICS.detect_anomalies()
    
    if anomalies:
        print(f"🚨 ANOMALIES DETECTED: {len(anomalies)} issues found")
        print("-" * 40)
        
        for anomaly in anomalies:
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠', 
                'medium': '🟡',
                'low': '🟢'
            }.get(anomaly.severity, '⚪')
            
            print(f"{severity_emoji} {anomaly.component_name}")
            print(f"   Metric: {anomaly.metric_name}")
            print(f"   Current: {anomaly.current_value:.2f}")
            print(f"   Expected: {anomaly.expected_value:.2f}")
            print(f"   Deviation: {anomaly.deviation_score:.2f}σ")
            print(f"   Confidence: {anomaly.confidence:.1%}")
            print(f"   💡 {anomaly.recommendation}")
            print()
    else:
        print("✅ No anomalies detected - all systems operating within normal parameters")
    
    # Predictive analysis
    print("\n🔮 PREDICTIVE ANALYSIS")
    print("-" * 40)
    
    predictions = AI_ANALYTICS.predict_failures()
    
    if predictions:
        print(f"⚠️  POTENTIAL ISSUES: {len(predictions)} predictions")
        
        for prediction in predictions:
            confidence_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(prediction.confidence_level, '⚪')
            
            time_until = prediction.predicted_failure_time - datetime.now()
            
            print(f"\n{confidence_emoji} {prediction.component_name}")
            print(f"   Predicted failure: {prediction.predicted_failure_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Time remaining: {time_until}")
            print(f"   Probability: {prediction.probability:.1%}")
            print(f"   Confidence: {prediction.confidence_level}")
            print(f"   🔍 Risk factors:")
            for factor in prediction.risk_factors:
                print(f"      • {factor}")
            print(f"   🛠️  Mitigation steps:")
            for step in prediction.mitigation_steps:
                print(f"      • {step}")
    else:
        print("✅ No potential failures predicted in the near term")
    
    # Learning status
    data_points = len(AI_ANALYTICS.historical_data)
    learning_threshold = AI_ANALYTICS.learning_window
    
    print(f"\n🧠 AI LEARNING STATUS")
    print("-" * 40)
    print(f"Data points collected: {data_points}")
    print(f"Learning threshold: {learning_threshold}")
    
    if data_points >= learning_threshold:
        print("✅ AI system is fully operational and learning")
    else:
        remaining = learning_threshold - data_points
        print(f"🟡 AI system needs {remaining} more data points to reach full accuracy")

def show_slo_dashboard() -> None:
    """Display SLO (Service Level Objectives) dashboard"""
    print("\n📊 SLO DASHBOARD")
    print("=" * 60)
    
    if not CONFIG["slo"]["enabled"]:
        print("❌ SLO tracking is disabled in configuration")
        return
    
    try:
        # Get current month data
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate current availability
        data = get_summary_data()
        if not data:
            print("❌ Unable to fetch current data for SLO calculation")
            return
        
        components = data.get('components', [])
        operational = sum(1 for c in components if c.get('status') == 'operational')
        total = len(components)
        current_availability = (operational / total * 100) if total > 0 else 0
        
        # SLO targets
        target_availability = CONFIG["slo"]["targets"]["global_availability"]
        target_uptime = CONFIG["slo"]["targets"]["uptime_monthly"]
        
        # Calculate monthly metrics
        days_in_month = (now.replace(month=now.month+1, day=1) - month_start).days if now.month < 12 else 31
        days_elapsed = (now - month_start).days + 1
        
        # Simulate downtime calculation (in a real system, this would come from historical data)
        estimated_monthly_availability = current_availability  # Simplified
        
        print(f"📅 Period: {month_start.strftime('%B %Y')}")
        print(f"📊 Days elapsed: {days_elapsed}/{days_in_month}")
        print()
        
        # Global availability SLO
        print("🎯 GLOBAL AVAILABILITY SLO")
        print("-" * 30)
        print(f"Target: {target_availability}%")
        print(f"Current: {estimated_monthly_availability:.2f}%")
        
        if estimated_monthly_availability >= target_availability:
            print("✅ SLO Status: MEETING TARGET")
        elif estimated_monthly_availability >= target_availability - 0.5:
            print("🟡 SLO Status: AT RISK")
        else:
            print("🔴 SLO Status: BREACHED")
        
        # Downtime budget
        monthly_minutes = days_in_month * 24 * 60
        target_downtime_budget = monthly_minutes * (100 - target_availability) / 100
        estimated_downtime = monthly_minutes * (100 - estimated_monthly_availability) / 100
        remaining_budget = target_downtime_budget - estimated_downtime
        
        print(f"\n⏰ DOWNTIME BUDGET")
        print("-" * 20)
        print(f"Monthly budget: {target_downtime_budget:.1f} minutes")
        print(f"Consumed: {estimated_downtime:.1f} minutes")
        print(f"Remaining: {remaining_budget:.1f} minutes")
        
        if remaining_budget > 0:
            print(f"✅ Budget status: {remaining_budget:.1f} minutes remaining")
        else:
            print(f"🔴 Budget status: EXCEEDED by {abs(remaining_budget):.1f} minutes")
        
        # Service-level SLOs
        print(f"\n🏢 SERVICE-LEVEL SLOs")
        print("-" * 25)
        
        service_slos = []
        for component in components[:10]:  # Top 10 services
            name = component.get('name', 'Unknown')
            status = component.get('status', 'unknown')
            health_score = get_service_health_score(status, data.get('page', {}).get('updated_at', ''))
            
            service_slos.append({
                'name': name,
                'availability': health_score,
                'status': 'operational' if status == 'operational' else 'degraded'
            })
        
        for slo in service_slos:
            status_emoji = "✅" if slo['status'] == 'operational' else "❌"
            print(f"{status_emoji} {slo['name'][:40]:<40} {slo['availability']:.1f}%")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 20)
        
        if estimated_monthly_availability < target_availability:
            print("🔴 Immediate action required to meet availability SLO")
            print("   • Investigate current service issues")
            print("   • Implement additional monitoring")
            print("   • Review incident response procedures")
        elif remaining_budget < 60:  # Less than 1 hour remaining
            print("🟡 Downtime budget running low")
            print("   • Postpone non-critical maintenance")
            print("   • Increase monitoring vigilance")
            print("   • Prepare incident response team")
        else:
            print("✅ SLOs are healthy - maintain current service levels")
        
    except Exception as e:
        print(f"❌ Error calculating SLOs: {e}")
        logging.error(f"SLO calculation error: {e}")

def advanced_anomaly_analysis() -> None:
    """Perform advanced anomaly analysis with detailed reporting"""
    print("\n🔬 ADVANCED ANOMALY ANALYSIS")
    print("=" * 60)
    
    if not CONFIG["ai_analytics"]["enabled"]:
        print("❌ AI Analytics is disabled")
        return
    
    if len(AI_ANALYTICS.historical_data) < AI_ANALYTICS.learning_window:
        print(f"❌ Insufficient data for analysis (need {AI_ANALYTICS.learning_window}, have {len(AI_ANALYTICS.historical_data)})")
        return
    
    print("🔍 Analyzing patterns in historical data...")
    
    # Statistical analysis
    availabilities = [dp['availability'] for dp in AI_ANALYTICS.historical_data]
    
    avg_availability = mean(availabilities)
    std_availability = stdev(availabilities) if len(availabilities) > 1 else 0
    min_availability = min(availabilities)
    max_availability = max(availabilities)
    
    print(f"\n📊 STATISTICAL OVERVIEW")
    print("-" * 30)
    print(f"Average availability: {avg_availability:.2f}%")
    print(f"Standard deviation: {std_availability:.2f}%")
    print(f"Range: {min_availability:.2f}% - {max_availability:.2f}%")
    
    # Trend analysis
    recent_data = availabilities[-20:]  # Last 20 points
    if len(recent_data) >= 10:
        first_half = mean(recent_data[:len(recent_data)//2])
        second_half = mean(recent_data[len(recent_data)//2:])
        trend = second_half - first_half
        
        print(f"\n📈 TREND ANALYSIS")
        print("-" * 20)
        if trend > 0.5:
            print(f"🟢 Improving trend: +{trend:.2f}%")
        elif trend < -0.5:
            print(f"🔴 Declining trend: {trend:.2f}%")
        else:
            print(f"🟡 Stable trend: {trend:.2f}%")
    
    # Component analysis
    print(f"\n🔧 COMPONENT ANALYSIS")
    print("-" * 25)
    
    component_stats = defaultdict(list)
    for dp in AI_ANALYTICS.historical_data:
        for comp_name, score in dp['components'].items():
            component_stats[comp_name].append(score)
    
    # Find most/least reliable components
    component_averages = {
        name: mean(scores) for name, scores in component_stats.items()
        if len(scores) >= 10
    }
    
    if component_averages:
        sorted_components = sorted(component_averages.items(), key=lambda x: x[1])
        
        print("🏆 Most reliable services:")
        for name, avg_score in sorted_components[-3:]:
            print(f"   ✅ {name[:40]:<40} {avg_score:.1f}")
        
        print("\n⚠️  Least reliable services:")
        for name, avg_score in sorted_components[:3]:
            print(f"   ❌ {name[:40]:<40} {avg_score:.1f}")
    
    # Alert generation
    anomalies = AI_ANALYTICS.detect_anomalies()
    critical_anomalies = [a for a in anomalies if a.severity in ['critical', 'high']]
    
    if critical_anomalies:
        print(f"\n🚨 CRITICAL ALERTS")
        print("-" * 20)
        
        for anomaly in critical_anomalies:
            alert = SystemAlert(
                timestamp=datetime.now(),
                severity=anomaly.severity,
                component=anomaly.component_name,
                message=f"Anomaly detected: {anomaly.metric_name} deviation {anomaly.deviation_score:.2f}σ"
            )
            
            # Send alert if notifications enabled
            if CONFIG["notifications"]["email"]["enabled"] or CONFIG["notifications"]["webhooks"]["enabled"]:
                NOTIFICATION_MANAGER.send_alert(alert)
                print(f"📧 Alert sent for {anomaly.component_name}")
            else:
                print(f"⚠️  {anomaly.component_name}: {anomaly.message}")

def database_maintenance() -> None:
    """Perform database maintenance and cleanup"""
    print("\n🗄️  DATABASE MAINTENANCE")
    print("=" * 50)
    
    if not CONFIG["database"]["enabled"]:
        print("❌ Database is disabled")
        return
    
    try:
        # Database size
        db_path = Path(CONFIG["database"]["path"])
        if db_path.exists():
            db_size = db_path.stat().st_size
            db_size_mb = db_size / (1024 * 1024)
            print(f"📊 Database size: {db_size_mb:.1f} MB")
        else:
            print("❌ Database file not found")
            return
        
        # Record counts
        with sqlite3.connect(CONFIG["database"]["path"]) as conn:
            cursor = conn.cursor()
            
            tables = ['status_history', 'component_metrics', 'alerts', 'slo_tracking']
            print(f"\n📋 RECORD COUNTS")
            print("-" * 20)
            
            total_records = 0
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                print(f"{table:<20} {count:>8,}")
            
            print(f"{'TOTAL':<20} {total_records:>8,}")
        
        # Cleanup old data
        if CONFIG["database"]["auto_cleanup"]:
            print(f"\n🧹 CLEANUP OPERATIONS")
            print("-" * 25)
            
            retention_days = CONFIG["database"]["retention_days"]
            print(f"Cleaning records older than {retention_days} days...")
            
            DB_MANAGER.cleanup_old_data(retention_days)
            print("✅ Cleanup completed")
        
        # Optimization
        print(f"\n⚡ OPTIMIZATION")
        print("-" * 15)
        print("Running VACUUM and ANALYZE...")
        
        with sqlite3.connect(CONFIG["database"]["path"]) as conn:
            conn.execute("VACUUM")
            conn.execute("ANALYZE")
        
        print("✅ Database optimized")
        
        # Updated size
        new_size = db_path.stat().st_size / (1024 * 1024)
        savings = db_size_mb - new_size
        print(f"📊 New size: {new_size:.1f} MB (saved {savings:.1f} MB)")
        
    except Exception as e:
        print(f"❌ Database maintenance failed: {e}")
        logging.error(f"Database maintenance error: {e}")

def export_ai_report() -> None:
    """Export comprehensive AI analysis report"""
    print("\n📄 EXPORTING AI ANALYSIS REPORT")
    print("=" * 50)
    
    try:
        timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
        filename = f"ai_analysis_report_{timestamp}.json"
        
        # Gather all AI data
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "3.0",
                "ai_enabled": CONFIG["ai_analytics"]["enabled"],
                "data_points": len(AI_ANALYTICS.historical_data)
            },
            "anomaly_detection": [],
            "predictive_analysis": [],
            "statistical_overview": {},
            "recommendations": []
        }
        
        if CONFIG["ai_analytics"]["enabled"] and len(AI_ANALYTICS.historical_data) >= AI_ANALYTICS.learning_window:
            # Anomalies
            anomalies = AI_ANALYTICS.detect_anomalies()
            report["anomaly_detection"] = [asdict(a) for a in anomalies]
            
            # Predictions
            predictions = AI_ANALYTICS.predict_failures()
            report["predictive_analysis"] = [asdict(p) for p in predictions]
            
            # Statistics
            availabilities = [dp['availability'] for dp in AI_ANALYTICS.historical_data]
            report["statistical_overview"] = {
                "average_availability": mean(availabilities),
                "standard_deviation": stdev(availabilities) if len(availabilities) > 1 else 0,
                "min_availability": min(availabilities),
                "max_availability": max(availabilities),
                "data_points": len(availabilities)
            }
            
            # Recommendations
            if anomalies:
                report["recommendations"].append("Investigate detected anomalies immediately")
            if predictions:
                report["recommendations"].append("Review predictive alerts and plan preventive actions")
            if not anomalies and not predictions:
                report["recommendations"].append("System operating normally - maintain current monitoring")
        
        # Save report
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ AI report exported: {filename}")
        
        # Also create human-readable version
        txt_filename = f"ai_analysis_summary_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("RED HAT AI ANALYSIS REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Points: {len(AI_ANALYTICS.historical_data)}\n\n")
            
            if report["anomaly_detection"]:
                f.write("ANOMALIES DETECTED:\n")
                f.write("-" * 20 + "\n")
                for anomaly in report["anomaly_detection"]:
                    f.write(f"• {anomaly['component_name']}: {anomaly['message']}\n")
                f.write("\n")
            
            if report["predictive_analysis"]:
                f.write("PREDICTIVE ALERTS:\n")
                f.write("-" * 18 + "\n")
                for prediction in report["predictive_analysis"]:
                    f.write(f"• {prediction['component_name']}: {prediction['probability']:.1%} failure risk\n")
                f.write("\n")
            
            if report["recommendations"]:
                f.write("RECOMMENDATIONS:\n")
                f.write("-" * 16 + "\n")
                for rec in report["recommendations"]:
                    f.write(f"• {rec}\n")
        
        print(f"📄 Summary created: {txt_filename}")
        
    except Exception as e:
        print(f"❌ Failed to export AI report: {e}")
        logging.error(f"AI report export failed: {e}")

def show_system_intelligence() -> None:
    """Display comprehensive system intelligence dashboard"""
    print("\n🧠 SYSTEM INTELLIGENCE DASHBOARD")
    print("=" * 60)
    
    # Current status
    data = get_summary_data()
    if data:
        components = data.get('components', [])
        operational = sum(1 for c in components if c.get('status') == 'operational')
        total = len(components)
        current_availability = (operational / total * 100) if total > 0 else 0
        
        print(f"🎯 CURRENT STATUS")
        print("-" * 20)
        print(f"Overall availability: {current_availability:.2f}%")
        print(f"Services operational: {operational}/{total}")
        print(f"Last updated: {data.get('page', {}).get('updated_at', 'Unknown')}")
    
    # AI Insights
    if CONFIG["ai_analytics"]["enabled"]:
        anomalies = AI_ANALYTICS.detect_anomalies()
        predictions = AI_ANALYTICS.predict_failures()
        
        print(f"\n🤖 AI ANALYSIS")
        print("-" * 15)
        print(f"Anomalies detected: {len(anomalies)}")
        print(f"Predictive alerts: {len(predictions)}")
        print(f"Learning data points: {len(AI_ANALYTICS.historical_data)}")
        
        if anomalies:
            critical_count = sum(1 for a in anomalies if a.severity == 'critical')
            if critical_count:
                print(f"🚨 Critical anomalies: {critical_count}")
    
    # Performance metrics
    print(f"\n⚡ PERFORMANCE")
    print("-" * 15)
    print(f"Cache hit ratio: {PERFORMANCE.cache_hit_ratio:.1f}%")
    print(f"API calls: {PERFORMANCE.api_calls}")
    print(f"Session duration: {PERFORMANCE.duration:.1f}s")
    
    # Database status
    if CONFIG["database"]["enabled"]:
        try:
            db_path = Path(CONFIG["database"]["path"])
            if db_path.exists():
                db_size = db_path.stat().st_size / (1024 * 1024)
                print(f"\n🗄️  DATABASE")
                print("-" * 12)
                print(f"Size: {db_size:.1f} MB")
                print(f"Status: Active")
            else:
                print(f"\n🗄️  DATABASE: Not initialized")
        except Exception:
            print(f"\n🗄️  DATABASE: Error accessing")
    
    print(f"\n💡 QUICK ACTIONS")
    print("-" * 17)
    print("• --ai-insights         Show detailed AI analysis")
    print("• --slo-dashboard       View SLO tracking")
    print("• --anomaly-analysis    Advanced anomaly detection")
    print("• --export-ai-report    Generate AI analysis report")
    print("• --db-maintenance      Database cleanup and optimization")

def concurrent_health_check() -> Dict[str, Any]:
    """Perform multiple health checks concurrently"""
    results = {}
    
    try:
        with ThreadPoolExecutor(max_workers=CONFIG["performance"]["max_concurrent_operations"]) as executor:
            # Submit multiple tasks
            future_to_task = {
                executor.submit(get_summary_data): "api_data",
                executor.submit(get_status_trend): "trend_analysis",
                executor.submit(analyze_service_patterns): "pattern_analysis",
                executor.submit(get_cache_size): "cache_info"
            }
            
            # Collect results
            for future in as_completed(future_to_task):
                task_name = future_to_task[future]
                try:
                    result = future.result(timeout=30)
                    results[task_name] = result if result is not None else {"info": "No data available"}
                except Exception as e:
                    results[task_name] = {"error": str(e)}
                    logging.error(f"Concurrent task {task_name} failed: {e}")
        
        return results
        
    except Exception as e:
        logging.error(f"Concurrent health check failed: {e}")
        return {"error": f"Concurrent check failed: {str(e)}"}
def show_trends() -> None:
    """Display availability trends"""
    trend_data = get_status_trend()
    
    if not trend_data:
        print("📭 No trend data available (requires at least 2 history entries)")
        return
    
    print("\n📈 AVAILABILITY TRENDS")
    print("=" * 50)
    
    current = trend_data['current_availability']
    previous = trend_data['previous_availability']
    direction = trend_data['trend_direction']
    points = trend_data['data_points']
    
    print(f"📊 Current Availability: {current:.1f}%")
    print(f"📊 Previous Availability: {previous:.1f}%")
    
    if direction == 'improving':
        print(f"📈 Trend: IMPROVING (+{current - previous:.1f}%)")
        print("🟢 Status is getting better")
    elif direction == 'degrading':
        print(f"📉 Trend: DEGRADING ({current - previous:.1f}%)")
        print("🔴 Status is getting worse")
    else:
        print("📊 Trend: STABLE (no change)")
        print("🟡 Status remains unchanged")
    
    print(f"📋 Based on {points} data points")
    """Display availability trends"""
    trend_data = get_status_trend()
    
    if not trend_data:
        print("📭 No trend data available (requires at least 2 history entries)")
        return
    
    print("\n📈 AVAILABILITY TRENDS")
    print("=" * 50)
    
    current = trend_data['current_availability']
    previous = trend_data['previous_availability']
    direction = trend_data['trend_direction']
    points = trend_data['data_points']
    
    print(f"📊 Current Availability: {current:.1f}%")
    print(f"📊 Previous Availability: {previous:.1f}%")
    
    if direction == 'improving':
        print(f"📈 Trend: IMPROVING (+{current - previous:.1f}%)")
        print("🟢 Status is getting better")
    elif direction == 'degrading':
        print(f"📉 Trend: DEGRADING ({current - previous:.1f}%)")
        print("🔴 Status is getting worse")
    else:
        print("📊 Trend: STABLE (no change)")
        print("🟡 Status remains unchanged")
    
    print(f"📋 Based on {points} data points")

def filter_services(services: List[Dict[str, Any]], status_filter: str, search_term: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter services based on status and search criteria"""
    filtered = services.copy()
    
    # Filter by status
    if status_filter == 'operational':
        filtered = [s for s in filtered if s.get('status') == 'operational']
    elif status_filter == 'issues':
        filtered = [s for s in filtered if s.get('status') != 'operational']
    
    # Filter by search term
    if search_term:
        search_lower = search_term.lower()
        filtered = [s for s in filtered if search_lower in s.get('name', '').lower()]
    
    return filtered

def format_output(data: Dict[str, Any], format_type: str, components: List[Dict[str, Any]]) -> None:
    """Format output based on specified format type"""
    if format_type == 'json':
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'page': data.get('page', {}),
            'status': data.get('status', {}),
            'components': components,
            'summary': {
                'total': len(components),
                'operational': sum(1 for c in components if c.get('status') == 'operational'),
                'issues': sum(1 for c in components if c.get('status') != 'operational')
            }
        }
        print(json.dumps(output_data, indent=2))
    elif format_type == 'csv':
        export_to_csv(components)
    # Default console format is handled by existing functions

def export_to_csv(components: List[Dict[str, Any]], filename: Optional[str] = None) -> None:
    """Export components to CSV format"""
    if not filename:
        timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
        filename = f"redhat_status_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'status', 'id', 'group_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for comp in components:
                writer.writerow({
                    'name': comp.get('name', ''),
                    'status': comp.get('status', ''),
                    'id': comp.get('id', ''),
                    'group_id': comp.get('group_id', '')
                })
        
        print(f"📊 CSV exported to: {filename}")
        
    except Exception as e:
        print(f"❌ CSV export error: {str(e)}")

def watch_mode(mode: str, interval: int, args, enable_notifications: bool = False) -> None:
    """Continuous monitoring mode"""
    import time
    import signal
    
    previous_status = None
    
    def signal_handler(signum, frame):
        print(f"\n⏹️  Watch mode stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"🔄 Watch mode started - refreshing every {interval} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    iteration = 0
    while True:
        try:
            iteration += 1
            if not args.quiet:
                print(f"\n📅 Update #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Get current status
            data = get_summary_data()
            if data:
                current_status = data.get('status', {}).get('indicator', 'unknown')
                
                # Check for status changes
                if enable_notifications and previous_status and current_status != previous_status:
                    print(f"🚨 STATUS CHANGE DETECTED: {previous_status} → {current_status}")
                
                previous_status = current_status
                
                # Run the requested mode
                if mode == "quick":
                    quick_status_check_no_fetch(data)
                elif mode == "simple":
                    quick_status_check_no_fetch(data)
                    simple_check_only_no_fetch(data, args)
            
            print(f"\n⏰ Next update in {interval} seconds...")
            time.sleep(interval)
            
        except Exception as e:
            print(f"❌ Error in watch mode: {str(e)}")
            time.sleep(interval)

def quick_status_check_no_fetch(data: Dict[str, Any]) -> None:
    """Quick status check without fetching data (for watch mode)"""
    if not data:
        return
    
    # Direct access to JSON data
    page_info = data.get('page', {})
    status_info = data.get('status', {})
    
    print(f"📍 Page: {page_info.get('name', 'N/A')}")
    print(f"🕒 Last Update: {page_info.get('updated_at', 'N/A')}")
    
    indicator = status_info.get('indicator', 'unknown')
    description = status_info.get('description', 'No description')
    
    # Status mapping with emojis
    status_map = {
        "none": ("🟢", "All Systems Operational"),
        "minor": ("🟡", "Minor Issues"),
        "major": ("🔴", "Major Outage"),
        "critical": ("🚨", "Critical Issues"),
        "maintenance": ("🔧", "Service Under Maintenance")
    }
    
    emoji, status_text = status_map.get(indicator, ("⚪", f"Unknown Status ({indicator})"))
    print(f"\n{emoji} STATUS: {description}")
    
    # Calculate and display global availability percentage
    components = data.get('components', [])
    if components:
        operational_count = sum(1 for comp in components if comp.get('status') == 'operational')
        total_count = len(components)
        
        if total_count > 0:
            global_percentage = (operational_count / total_count) * 100
            
            # Choose emoji based on availability percentage
            if global_percentage >= 95:
                availability_emoji = "🟢"
                health_status = "EXCELLENT"
            elif global_percentage >= 90:
                availability_emoji = "🟡"
                health_status = "GOOD"
            elif global_percentage >= 80:
                availability_emoji = "🟠"
                health_status = "FAIR"
            else:
                availability_emoji = "🔴"
                health_status = "POOR"
            
            print(f"{availability_emoji} GLOBAL AVAILABILITY: {global_percentage:.1f}% ({operational_count}/{total_count} services)")
            print(f"🏥 Overall Health: {health_status}")

def simple_check_only_no_fetch(data: Dict[str, Any], args) -> None:
    """Simple check without fetching data (for watch mode)"""
    if not data:
        return
    
    components = data.get('components', [])
    
    # Filter main services (group_id is null)
    main_services = [comp for comp in components if comp.get('group_id') is None]
    
    # Apply filters
    if hasattr(args, 'filter') and hasattr(args, 'search'):
        main_services = filter_services(main_services, args.filter, args.search)
    
    print(f"\n🎯 Main services found: {len(main_services)}")
    
    operational_count = 0
    problem_count = 0
    
    for service in main_services:
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        
        if status == "operational":
            print(f"✅ {name}")
            operational_count += 1
        else:
            print(f"❌ {name} - {status.upper()}")
            problem_count += 1
    
    print(f"📈 SUMMARY: {operational_count} operational, {problem_count} with issues")

def quick_status_check() -> None:
    """1. Global status - PYTHON3 VERSION"""
    print("\n" + "="*60)
    print("🚀 RED HAT GLOBAL STATUS")
    print("="*60)
    
    data = get_summary_data()
    if not data:
        return
    
    # Direct access to JSON data
    page_info = data.get('page', {})
    status_info = data.get('status', {})
    
    print(f"📍 Page: {page_info.get('name', 'N/A')}")
    print(f"🔗 URL: {page_info.get('url', 'N/A')}")
    print(f"🕒 Last Update: {page_info.get('updated_at', 'N/A')}")
    
    indicator = status_info.get('indicator', 'unknown')
    description = status_info.get('description', 'No description')
    
    # Status mapping with emojis
    status_map = {
        "none": ("🟢", "All Systems Operational"),
        "minor": ("🟡", "Minor Issues"),
        "major": ("🔴", "Major Outage"),
        "critical": ("🚨", "Critical Issues"),
        "maintenance": ("🔧", "Service Under Maintenance")
    }
    
    emoji, status_text = status_map.get(indicator, ("⚪", f"Unknown Status ({indicator})"))
    print(f"\n{emoji} STATUS: {description}")
    print(f"🏷️  Severity: {status_text}")
    
    # Calculate and display global availability percentage
    components = data.get('components', [])
    if components:
        operational_count = sum(1 for comp in components if comp.get('status') == 'operational')
        total_count = len(components)
        
        if total_count > 0:
            global_percentage = (operational_count / total_count) * 100
            
            # Choose emoji based on availability percentage
            if global_percentage >= 95:
                availability_emoji = "🟢"
                health_status = "EXCELLENT"
            elif global_percentage >= 90:
                availability_emoji = "🟡"
                health_status = "GOOD"
            elif global_percentage >= 80:
                availability_emoji = "🟠"
                health_status = "FAIR"
            else:
                availability_emoji = "🔴"
                health_status = "POOR"
            
            print(f"\n{availability_emoji} GLOBAL AVAILABILITY: {global_percentage:.1f}% ({operational_count}/{total_count} services)")
            print(f"🏥 Overall Health: {health_status}")
        else:
            print(f"\n⚪ GLOBAL AVAILABILITY: No component data available")
    else:
        print(f"\n⚪ GLOBAL AVAILABILITY: No component data available")

def simple_check_only() -> Optional[List[Dict[str, Any]]]:
    """2. Main services - PYTHON3 VERSION"""
    print("\n" + "="*60)
    print("🏢 RED HAT MAIN SERVICES")
    print("="*60)
    
    data = get_summary_data()
    if not data:
        return None
    
    components = data.get('components', [])
    print(f"📊 Total components in API: {len(components)}")
    
    # Filter main services (group_id is null)
    main_services = [comp for comp in components if comp.get('group_id') is None]
    
    print(f"🎯 Main services found: {len(main_services)}")
    print("-" * 60)
    
    operational_count = 0
    problem_count = 0
    
    for service in main_services:
        name = service.get('name', 'Unnamed service')
        status = service.get('status', 'unknown')
        
        if status == "operational":
            print(f"✅ {name}")
            operational_count += 1
        else:
            print(f"❌ {name} - {status.upper()}")
            problem_count += 1
    
    print("-" * 60)
    print(f"📈 SUMMARY: {operational_count} operational, {problem_count} with issues")
    
    # Calculate and display percentage
    total_services = operational_count + problem_count
    if total_services > 0 and CONFIG["display"]["show_percentages"]:
        percentage = (operational_count / total_services) * 100
        print(f"📊 Availability: {percentage:.1f}%")
    
    return main_services

def full_check_with_services() -> None:
    """3. ALL services with hierarchy - PYTHON3 VERSION"""
    print("\n" + "="*80)
    print("🏗️  COMPLETE RED HAT STRUCTURE - ALL SERVICES")
    print("="*80)
    
    data = get_summary_data()
    if not data:
        return
    
    components = data.get('components', [])
    
    # Organize by hierarchy
    main_services = {}
    sub_services = {}
    
    # Create dictionaries to facilitate organization
    for comp in components:
        comp_id = comp.get('id')
        name = comp.get('name', 'Unnamed service')
        status = comp.get('status', 'unknown')
        group_id = comp.get('group_id')
        
        if group_id is None:
            # Main service
            main_services[comp_id] = {
                'name': name,
                'status': status,
                'id': comp_id
            }
        else:
            # Sub-service
            if group_id not in sub_services:
                sub_services[group_id] = []
            sub_services[group_id].append({
                'name': name,
                'status': status,
                'id': comp_id
            })
    
    print(f"📊 STATISTICS:")
    print(f"   • Main services: {len(main_services)}")
    print(f"   • Sub-service groups: {len(sub_services)}")
    print(f"   • Total components: {len(components)}")
    print()
    
    total_operational = 0
    total_problems = 0
    service_details = []  # For summary statistics
    
    # Display hierarchical structure
    for service_id, service_info in main_services.items():
        name = service_info['name']
        status = service_info['status']
        
        # Main service
        if status == "operational":
            print(f"🟢 {name}")
            total_operational += 1
            service_details.append({'name': name, 'status': 'operational', 'type': 'main'})
        else:
            print(f"🔴 {name} - {status.upper()}")
            total_problems += 1
            service_details.append({'name': name, 'status': status, 'type': 'main'})
        
        # Display sub-services of this group
        if service_id in sub_services:
            sub_list = sub_services[service_id]
            print(f"   📁 {len(sub_list)} sub-services:")
            
            sub_operational = 0
            sub_problems = 0
            
            for sub in sub_list:
                sub_name = sub['name']
                sub_status = sub['status']
                
                if sub_status == "operational":
                    print(f"      ✅ {sub_name}")
                    total_operational += 1
                    sub_operational += 1
                    service_details.append({'name': sub_name, 'status': 'operational', 'type': 'sub'})
                else:
                    print(f"      ❌ {sub_name} - {sub_status.upper()}")
                    total_problems += 1
                    sub_problems += 1
                    service_details.append({'name': sub_name, 'status': sub_status, 'type': 'sub'})
            
            # Sub-group summary
            if sub_operational + sub_problems > 0 and CONFIG["display"]["show_group_summaries"]:
                sub_percentage = (sub_operational / (sub_operational + sub_problems)) * 100
                print(f"   📈 Group availability: {sub_percentage:.1f}%")
        
        print()  # Empty line between groups
    
    # Display "orphan" sub-services (groups without identified parent)
    orphan_groups = set(sub_services.keys()) - set(main_services.keys())
    if orphan_groups:
        print("🔧 OTHER SERVICES:")
        for group_id in orphan_groups:
            sub_list = sub_services[group_id]
            print(f"   📁 Group {group_id[:8]}... ({len(sub_list)} services):")
            
            for sub in sub_list:
                sub_name = sub['name']
                sub_status = sub['status']
                
                if sub_status == "operational":
                    print(f"      ✅ {sub_name}")
                    total_operational += 1
                    service_details.append({'name': sub_name, 'status': 'operational', 'type': 'orphan'})
                else:
                    print(f"      ❌ {sub_name} - {sub_status.upper()}")
                    total_problems += 1
                    service_details.append({'name': sub_name, 'status': sub_status, 'type': 'orphan'})
    
    print("=" * 80)
    print(f"📊 TOTAL OVERALL: {total_operational} operational, {total_problems} with issues")
    
    # Calculate percentage
    total_services = total_operational + total_problems
    if total_services > 0:
        percentage = (total_operational / total_services) * 100
        if CONFIG["display"]["show_percentages"]:
            print(f"📈 Availability rate: {percentage:.1f}%")
        
        # Additional statistics
        if CONFIG["display"]["show_group_summaries"]:
            main_count = len([s for s in service_details if s['type'] == 'main'])
            sub_count = len([s for s in service_details if s['type'] == 'sub'])
            orphan_count = len([s for s in service_details if s['type'] == 'orphan'])
            
            print(f"🔢 Service breakdown: {main_count} main, {sub_count} sub-services, {orphan_count} other")
        
        # Health indicator
        if CONFIG["display"]["show_health_indicator"]:
            if percentage >= 95:
                print("🟢 Overall health: EXCELLENT")
            elif percentage >= 90:
                print("🟡 Overall health: GOOD")
            elif percentage >= 80:
                print("🟠 Overall health: FAIR")
            else:
                print("🔴 Overall health: POOR")

def export_to_file(output_dir: str = ".") -> None:
    """Bonus: Export data to file"""
    print("\n💾 DATA EXPORT")
    print("-" * 40)
    
    data = get_summary_data()
    if not data:
        return
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime(CONFIG["output"]["timestamp_format"])
    filename = os.path.join(output_dir, f"redhat_status_{timestamp}.json")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Get file size
        file_size = os.path.getsize(filename)
        file_size_kb = file_size / 1024
        
        print(f"✅ Data exported to: {filename}")
        print(f"📊 File size: {file_size_kb:.1f} KB ({file_size} bytes)")
        print(f"📅 Export time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Also create a summary report if configured
        if CONFIG["output"]["create_summary_report"]:
            summary_filename = os.path.join(output_dir, f"redhat_summary_{timestamp}.txt")
            create_summary_report(data, summary_filename)
        
    except Exception as e:
        print(f"❌ Export error: {str(e)}")

def create_summary_report(data: Dict[str, Any], filename: str) -> None:
    """Create a human-readable summary report"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("RED HAT STATUS SUMMARY REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            # Page info
            page_info = data.get('page', {})
            f.write(f"Page: {page_info.get('name', 'N/A')}\n")
            f.write(f"URL: {page_info.get('url', 'N/A')}\n")
            f.write(f"Last Update: {page_info.get('updated_at', 'N/A')}\n\n")
            
            # Status info
            status_info = data.get('status', {})
            f.write(f"Status: {status_info.get('description', 'No description')}\n")
            f.write(f"Indicator: {status_info.get('indicator', 'unknown')}\n\n")
            
            # Components summary
            components = data.get('components', [])
            operational = sum(1 for comp in components if comp.get('status') == 'operational')
            total = len(components)
            issues = total - operational
            
            f.write(f"Components Summary:\n")
            f.write(f"  Total: {total}\n")
            f.write(f"  Operational: {operational}\n")
            f.write(f"  With Issues: {issues}\n")
            if total > 0:
                percentage = (operational / total) * 100
                f.write(f"  Availability: {percentage:.1f}%\n")
            
            f.write(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"📋 Summary report created: {filename}")
        
    except Exception as e:
        print(f"❌ Error creating summary report: {str(e)}")

def show_system_insights() -> None:
    """Display system insights and patterns (legacy function for compatibility)"""
    show_system_intelligence()

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Red Hat Status Checker v3.0 - Advanced monitoring with performance analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive mode
  %(prog)s quick              # Quick status only
  %(prog)s simple             # Main services check
  %(prog)s full               # Complete structure
  %(prog)s export             # Export data to files
  %(prog)s all                # Display everything
  %(prog)s export --output ./reports  # Export to specific directory
  %(prog)s simple --filter issues     # Show only services with issues
  %(prog)s simple --search "ansible"  # Search for services containing "ansible"
  %(prog)s quick --watch 30           # Monitor status every 30 seconds
  %(prog)s simple --format json       # Output in JSON format
  %(prog)s simple --format csv        # Export to CSV
  %(prog)s quick --trends             # Show availability trends
  %(prog)s --clear-cache              # Clear all cached data
  %(prog)s --export-history           # Export status history to CSV
  %(prog)s quick --no-cache           # Disable caching for this request
  %(prog)s quick --log-level DEBUG    # Enable debug logging
  %(prog)s --health-report            # Generate comprehensive health report
  %(prog)s --performance              # Show performance metrics
  %(prog)s --insights                 # Display system insights and patterns
  %(prog)s --concurrent-check         # Perform concurrent health checks
  %(prog)s quick --enable-monitoring  # Enable advanced monitoring features
        """
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['quick', 'simple', 'full', 'export', 'all'],
        default=None,
        help='Operation mode (if not specified, interactive mode is used)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory for exported files (default: current directory)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode - minimal output'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Red Hat Status Checker v3.0 - Advanced Edition'
    )
    
    parser.add_argument(
        '--filter',
        choices=['operational', 'issues', 'all'],
        default='all',
        help='Filter services by status (default: all)'
    )
    
    parser.add_argument(
        '--search',
        help='Search for services containing this text (case-insensitive)'
    )
    
    parser.add_argument(
        '--format',
        choices=['console', 'json', 'csv'],
        default='console',
        help='Output format (default: console)'
    )
    
    parser.add_argument(
        '--watch', '-w',
        type=int,
        metavar='SECONDS',
        help='Watch mode - refresh every N seconds'
    )
    
    parser.add_argument(
        '--notify',
        action='store_true',
        help='Enable notifications when status changes (requires watch mode)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable caching for this request'
    )
    
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Clear all cached data'
    )
    
    parser.add_argument(
        '--trends',
        action='store_true',
        help='Show availability trends (requires history data)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Set logging level for this session'
    )
    
    parser.add_argument(
        '--export-history',
        action='store_true',
        help='Export status history to CSV'
    )
    
    # New advanced features
    parser.add_argument(
        '--health-report',
        action='store_true',
        help='Generate comprehensive health report'
    )
    
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Show performance metrics and statistics'
    )
    
    parser.add_argument(
        '--insights',
        action='store_true',
        help='Display system insights and pattern analysis'
    )
    
    parser.add_argument(
        '--concurrent-check',
        action='store_true',
        help='Perform concurrent health checks for faster results'
    )
    
    parser.add_argument(
        '--enable-monitoring',
        action='store_true',
        help='Enable advanced monitoring and alerting features'
    )
    
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run performance benchmark tests'
    )
    
    parser.add_argument(
        '--config-check',
        action='store_true',
        help='Validate configuration and display current settings'
    )
    
    # AI-powered features
    parser.add_argument(
        '--ai-insights',
        action='store_true',
        help='Show AI-powered anomaly detection and predictive analysis'
    )
    
    parser.add_argument(
        '--slo-dashboard',
        action='store_true',
        help='Display Service Level Objectives dashboard'
    )
    
    parser.add_argument(
        '--anomaly-analysis',
        action='store_true',
        help='Perform advanced anomaly analysis with detailed reporting'
    )
    
    parser.add_argument(
        '--export-ai-report',
        action='store_true',
        help='Export comprehensive AI analysis report'
    )
    
    parser.add_argument(
        '--db-maintenance',
        action='store_true',
        help='Perform database maintenance and cleanup operations'
    )
    
    parser.add_argument(
        '--system-intelligence',
        action='store_true',
        help='Show comprehensive system intelligence dashboard'
    )
    
    return parser

def main():
    """Main function with enhanced argument handling and new features"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging
    if args.log_level:
        CONFIG["logging"]["enabled"] = True
        CONFIG["logging"]["level"] = args.log_level
    setup_advanced_logging()
    
    # Enable monitoring if requested
    if args.enable_monitoring:
        CONFIG["monitoring"]["enabled"] = True
        CONFIG["performance"]["enable_metrics"] = True
    
    # Handle special operations first
    if args.config_check:
        show_config_info()
        return
    
    if args.clear_cache:
        clear_cache()
        return
    
    if args.export_history:
        export_history_to_csv()
        return
    
    if args.health_report:
        export_health_report()
        return
    
    if args.performance:
        show_performance_metrics()
        return
    
    if args.insights:
        show_system_insights()
        return
    
    if args.concurrent_check:
        results = concurrent_health_check()
        print("\n🔄 CONCURRENT HEALTH CHECK RESULTS")
        print("=" * 50)
        
        for task_name, result in results.items():
            if "error" in result:
                print(f"❌ {task_name}: {result['error']}")
            else:
                print(f"✅ {task_name}: Completed successfully")
        return
    
    if args.benchmark:
        run_performance_benchmark()
        return
    
    # New AI-powered operations
    if args.ai_insights:
        show_ai_insights()
        return
    
    if args.slo_dashboard:
        show_slo_dashboard()
        return
    
    if args.anomaly_analysis:
        advanced_anomaly_analysis()
        return
    
    if args.export_ai_report:
        export_ai_report()
        return
    
    if args.db_maintenance:
        database_maintenance()
        return
    
    if args.system_intelligence:
        show_system_intelligence()
        return
        results = concurrent_health_check()
        print("🔄 CONCURRENT HEALTH CHECK RESULTS")
        print("=" * 50)
        if results:
            for task, result in results.items():
                if isinstance(result, dict) and "error" in result:
                    print(f"❌ {task}: {result['error']}")
                else:
                    print(f"✅ {task}: Completed successfully")
        else:
            print("❌ Concurrent check failed to return results")
        return
    
    if args.benchmark:
        run_performance_benchmark()
        return
    
    # Disable cache if requested
    if args.no_cache:
        CONFIG["cache"]["enabled"] = False
    
    if not args.quiet:
        print("🎯 RED HAT STATUS CHECKER - ADVANCED v3.0")
        print("=" * 60)
        
        if CONFIG["performance"]["enable_metrics"]:
            print("📊 Performance monitoring: ENABLED")
        if CONFIG["monitoring"]["enabled"]:
            print("🔔 Advanced monitoring: ENABLED")
    
    mode = args.mode
    
    # Interactive mode if no arguments provided
    if mode is None:
        print("Available modes:")
        print("  quick    - Global status only")
        print("  simple   - Main services")
        print("  full     - Complete structure")
        print("  export   - Export data")
        print("  all      - Display all")
        print()
        mode = input("Choose a mode (or press Enter for 'all'): ").lower()
        if not mode:
            mode = "all"
        
        # Validate interactive input
        if mode not in ['quick', 'simple', 'full', 'export', 'all']:
            print(f"❌ Mode '{mode}' not recognized")
            return
    
    try:
        # Start performance tracking
        PERFORMANCE.start_time = datetime.now()
        
        # Handle trends display
        if args.trends:
            show_trends()
            if mode in ['quick', 'simple']:
                print()  # Add spacing before main content
        
        # Handle watch mode
        if args.watch:
            if mode not in ['quick', 'simple']:
                print("❌ Watch mode only supports 'quick' and 'simple' modes")
                return
            watch_mode(mode, args.watch, args, args.notify)
            return
        
        # Handle different output formats
        if args.format != 'console' and mode in ['quick', 'simple']:
            data = get_summary_data()
            if data:
                # Save to history for trends
                save_status_history(data)
                
                components = data.get('components', [])
                if mode == 'simple':
                    components = [comp for comp in components if comp.get('group_id') is None]
                
                # Apply filters
                components = filter_services(components, args.filter, args.search)
                format_output(data, args.format, components)
            return
        
        # Standard modes with history tracking
        data_for_history = None
        
        if mode == "quick":
            data_for_history = quick_status_check_with_history()
        elif mode == "simple":
            data_for_history = quick_status_check_with_history()
            if data_for_history and args.format == 'console':
                components = data_for_history.get('components', [])
                main_services = [comp for comp in components if comp.get('group_id') is None]
                main_services = filter_services(main_services, args.filter, args.search)
                
                # Display filtered results
                if args.filter != 'all' or args.search:
                    print(f"\n🔍 FILTERED RESULTS:")
                    if args.filter != 'all':
                        print(f"   Filter: {args.filter}")
                    if args.search:
                        print(f"   Search: '{args.search}'")
                    print("-" * 60)
                    
                    for service in main_services:
                        name = service.get('name', 'Unnamed service')
                        status = service.get('status', 'unknown')
                        
                        if status == "operational":
                            print(f"✅ {name}")
                        else:
                            print(f"❌ {name} - {status.upper()}")
                else:
                    simple_check_only()
        elif mode == "full":
            data_for_history = quick_status_check_with_history()
            simple_check_only()
            full_check_with_services()
        elif mode == "export":
            export_to_file(args.output)
        elif mode == "all":
            data_for_history = quick_status_check_with_history()
            simple_check_only()
            full_check_with_services()
            export_to_file(args.output)
        
        # Save status history
        if data_for_history:
            save_status_history(data_for_history)
        
        # Show performance metrics if enabled
        if CONFIG["performance"]["enable_metrics"] and not args.quiet:
            PERFORMANCE.end_time = datetime.now()
            print(f"\n⚡ Session completed in {PERFORMANCE.duration:.2f}s")
            if PERFORMANCE.cache_hits > 0:
                print(f"📋 Cache efficiency: {PERFORMANCE.cache_hit_ratio:.1f}%")
            
        if not args.quiet:
            print(f"\n✅ Operation completed successfully!")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

def show_config_info() -> None:
    """Display current configuration information"""
    print("⚙️  CONFIGURATION INFORMATION")
    print("=" * 50)
    
    print("📡 API Configuration:")
    print(f"   URL: {CONFIG['api']['url']}")
    print(f"   Timeout: {CONFIG['api']['timeout']}s")
    print(f"   Max Retries: {CONFIG['api']['max_retries']}")
    print(f"   Retry Delay: {CONFIG['api']['retry_delay']}s")
    
    print("\n💾 Cache Configuration:")
    print(f"   Enabled: {CONFIG['cache']['enabled']}")
    print(f"   TTL: {CONFIG['cache']['ttl']}s")
    print(f"   Directory: {CONFIG['cache']['directory']}")
    print(f"   Max Size: {CONFIG['cache']['max_size_mb']} MB")
    
    cache_size_bytes, cache_size_str = get_cache_size()
    print(f"   Current Size: {cache_size_str}")
    
    print("\n📝 Logging Configuration:")
    print(f"   Enabled: {CONFIG['logging']['enabled']}")
    print(f"   Level: {CONFIG['logging']['level']}")
    print(f"   File: {CONFIG['logging']['file']}")
    
    print("\n🔔 Monitoring Configuration:")
    print(f"   Enabled: {CONFIG['monitoring']['enabled']}")
    print(f"   Critical Threshold: {CONFIG['monitoring']['alert_thresholds']['availability_critical']}%")
    print(f"   Warning Threshold: {CONFIG['monitoring']['alert_thresholds']['availability_warning']}%")
    
    print("\n📊 Performance Configuration:")
    print(f"   Metrics Enabled: {CONFIG['performance']['enable_metrics']}")
    print(f"   Detailed Timing: {CONFIG['performance']['detailed_timing']}")
    print(f"   Max Concurrent Ops: {CONFIG['performance']['max_concurrent_operations']}")
    
    print()

def run_performance_benchmark() -> None:
    """Run performance benchmark tests"""
    print("🏃‍♂️ PERFORMANCE BENCHMARK")
    print("=" * 50)
    
    print("Running benchmark tests...")
    
    # Test 1: API response time
    start_time = time.time()
    data = get_summary_data()
    api_time = time.time() - start_time
    
    if data:
        print(f"✅ API Response Time: {api_time:.3f}s")
        data_size = len(json.dumps(data))
        print(f"📦 Data Size: {data_size:,} bytes")
        print(f"🚀 Throughput: {data_size / api_time:.0f} bytes/s")
    else:
        print("❌ API test failed")
    
    # Test 2: Cache performance
    if CONFIG["cache"]["enabled"]:
        start_time = time.time()
        cached_data = load_from_cache("summary_data")
        cache_time = time.time() - start_time
        
        if cached_data:
            print(f"📋 Cache Read Time: {cache_time:.6f}s")
            speedup = api_time / cache_time if cache_time > 0 else float('inf')
            print(f"⚡ Cache Speedup: {speedup:.1f}x")
        else:
            print("📭 No cached data available")
    
    # Test 3: JSON processing
    if data:
        start_time = time.time()
        for _ in range(100):
            json.dumps(data)
        json_time = (time.time() - start_time) / 100
        print(f"🔄 JSON Serialization: {json_time:.6f}s per operation")
    
    # Test 4: History analysis
    start_time = time.time()
    patterns = analyze_service_patterns()
    analysis_time = time.time() - start_time
    
    if "error" not in patterns:
        print(f"🔍 Pattern Analysis: {analysis_time:.3f}s")
        print(f"📊 Data Points Analyzed: {patterns.get('data_points_analyzed', 0)}")
    else:
        print(f"❌ Pattern analysis failed: {patterns['error']}")
    
    print(f"\n📈 Benchmark completed in {time.time() - start_time:.3f}s total")
    print()

def quick_status_check_with_history() -> Optional[Dict[str, Any]]:
    """Quick status check that returns data for history tracking"""
    print("\n" + "="*60)
    print("🚀 RED HAT GLOBAL STATUS")
    print("="*60)
    
    data = get_summary_data()
    if not data:
        return None
    
    # Direct access to JSON data
    page_info = data.get('page', {})
    status_info = data.get('status', {})
    
    print(f"📍 Page: {page_info.get('name', 'N/A')}")
    print(f"🔗 URL: {page_info.get('url', 'N/A')}")
    print(f"🕒 Last Update: {page_info.get('updated_at', 'N/A')}")
    
    indicator = status_info.get('indicator', 'unknown')
    description = status_info.get('description', 'No description')
    
    # Status mapping with emojis
    status_map = {
        "none": ("🟢", "All Systems Operational"),
        "minor": ("🟡", "Minor Issues"),
        "major": ("🔴", "Major Outage"),
        "critical": ("🚨", "Critical Issues"),
        "maintenance": ("🔧", "Service Under Maintenance")
    }
    
    emoji, status_text = status_map.get(indicator, ("⚪", f"Unknown Status ({indicator})"))
    print(f"\n{emoji} STATUS: {description}")
    print(f"🏷️  Severity: {status_text}")
    
    # Calculate and display global availability percentage
    components = data.get('components', [])
    if components:
        operational_count = sum(1 for comp in components if comp.get('status') == 'operational')
        total_count = len(components)
        
        if total_count > 0:
            global_percentage = (operational_count / total_count) * 100
            
            # Choose emoji based on availability percentage
            if global_percentage >= 95:
                availability_emoji = "🟢"
                health_status = "EXCELLENT"
            elif global_percentage >= 90:
                availability_emoji = "🟡"
                health_status = "GOOD"
            elif global_percentage >= 80:
                availability_emoji = "🟠"
                health_status = "FAIR"
            else:
                availability_emoji = "🔴"
                health_status = "POOR"
            
            print(f"\n{availability_emoji} GLOBAL AVAILABILITY: {global_percentage:.1f}% ({operational_count}/{total_count} services)")
            print(f"🏥 Overall Health: {health_status}")
        else:
            print(f"\n⚪ GLOBAL AVAILABILITY: No component data available")
    else:
        print(f"\n⚪ GLOBAL AVAILABILITY: No component data available")
    
    return data

if __name__ == "__main__":
    main()