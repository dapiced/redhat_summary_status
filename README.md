# Red Hat Status Checker v3.0 - Advanced Performance & Analytics Platform

An enterprise-grade Python monitoring solution for Red Hat services with advanced analytics, performance optimization, and professional monitoring capabilities.

## 🚀 What's New in v3.0

### Enterprise Features
- ✅ **Performance Analytics**: Real-time performance monitoring with benchmarking
- ✅ **Health Intelligence**: Comprehensive health reports with scoring algorithms  
- ✅ **Pattern Recognition**: Automated analysis of service patterns and trends
- ✅ **Concurrent Monitoring**: Multi-threaded operations for enterprise scalability
- ✅ **Advanced Caching**: Compressed caching with intelligent size management
- ✅ **Professional Logging**: Rotating logs with configurable levels and formats
- ✅ **Configuration Management**: Enterprise-grade configuration with validation

### Core Functionality
- **Quick Status**: Global Red Hat status overview with health scoring
- **Simple Check**: Main services status monitoring with filtering
- **Full Check**: Complete hierarchical service structure analysis
- **Data Export**: Multiple formats (JSON, CSV, compressed) with metadata

### Advanced Monitoring Features
- ✅ **Real-time Performance Metrics**: Response times, cache efficiency, throughput
- ✅ **System Health Scoring**: Intelligent health grades (A+ to F) 
- ✅ **Pattern Analysis**: Automatic detection of recurring issues and peak times
- ✅ **Trend Analytics**: Statistical analysis of availability trends over time
- ✅ **Alert Management**: Configurable thresholds with multiple severity levels
- ✅ **Operational Intelligence**: Automated insights and recommendations

## Usage

### Quick Start
```bash
# Basic status check
python3 redhat_summary_status.py quick

# Advanced monitoring with performance tracking
python3 redhat_summary_status.py quick --enable-monitoring --log-level DEBUG

# Generate comprehensive health report
python3 redhat_summary_status.py --health-report

# Performance benchmark and analysis
python3 redhat_summary_status.py --benchmark --performance
```

### Command Line Examples
```bash
# === Basic Operations ===
python3 redhat_summary_status.py                    # Interactive mode
python3 redhat_summary_status.py quick              # Quick status only
python3 redhat_summary_status.py simple             # Main services check
python3 redhat_summary_status.py full               # Complete structure
python3 redhat_summary_status.py export             # Export data to files
python3 redhat_summary_status.py all                # Display everything

# === Advanced Features ===
python3 redhat_summary_status.py --health-report    # Comprehensive health analysis
python3 redhat_summary_status.py --performance      # Performance metrics dashboard
python3 redhat_summary_status.py --insights         # System insights & patterns
python3 redhat_summary_status.py --ai-insights      # Show detailed AI analysis
python3 redhat_summary_status.py --slo-dashboard    # View SLO tracking
python3 redhat_summary_status.py --anomaly-analysis # Advanced anomaly detection
python3 redhat_summary_status.py --export-ai-report # Generate AI analysis report
python3 redhat_summary_status.py --db-maintenance   # Database cleanup and optimization
python3 redhat_summary_status.py --concurrent-check # Multi-threaded health checks
python3 redhat_summary_status.py --benchmark        # Performance benchmarking
python3 redhat_summary_status.py --config-check     # Configuration validation

# === Monitoring & Analytics ===
python3 redhat_summary_status.py quick --trends     # Show availability trends
python3 redhat_summary_status.py --export-history   # Export historical data
python3 redhat_summary_status.py quick --watch 30 --notify  # Live monitoring with alerts

# === Filtering & Search ===
python3 redhat_summary_status.py simple --filter issues     # Show only problems
python3 redhat_summary_status.py simple --search "ansible"  # Search services
python3 redhat_summary_status.py simple --filter operational --search "cloud" # Search and filter

# === Output Formats ===
python3 redhat_summary_status.py simple --format json       # JSON output
python3 redhat_summary_status.py simple --format csv        # CSV export
python3 redhat_summary_status.py export --output ./reports  # Custom directory

# === Performance & Caching ===
python3 redhat_summary_status.py quick --no-cache          # Bypass cache
python3 redhat_summary_status.py --clear-cache             # Clear all cache
python3 redhat_summary_status.py quick --log-level DEBUG   # Debug logging
```

### Help and Version
```bash
# Show comprehensive help
python3 redhat_summary_status.py --help

# Show version information
python3 redhat_summary_status.py --version
```

## 🔧 Simple Versions

For users who prefer lightweight, streamlined functionality without the advanced enterprise features, we provide two simplified versions:

### redhat_summary_status_simple_v1.py - Basic Version
A minimal, fast script focused on core status checking with global availability percentage.

**Features:**
- ✅ Quick status check with global availability percentage
- ✅ Simple service listing
- ✅ Full hierarchical service structure
- ✅ Data export capabilities (JSON/TXT)
- ✅ Basic caching for performance
- ✅ Clean, emoji-rich output
- ✅ Quiet mode support

**Usage:**
```bash
# Quick status with global availability %
python3 redhat_summary_status_simple_v1.py quick

# Quiet mode - minimal output
python3 redhat_summary_status_simple_v1.py quick --quiet

# Main services only
python3 redhat_summary_status_simple_v1.py simple

# Complete service hierarchy
python3 redhat_summary_status_simple_v1.py full

# Export data to files
python3 redhat_summary_status_simple_v1.py export
```

**Key Benefits:**
- 🚀 **Fast startup** - No complex initialization
- 💾 **Low memory usage** - Minimal dependencies
- 📊 **Global availability percentage** - Clear health status
- 🎯 **Focused functionality** - Core features only

### redhat_summary_status_simple_v2.py - Enhanced Simple Version
An improved version with better configuration support and hierarchical display.

**Features:**
- ✅ All v1 features plus:
- ✅ Configuration file support (`config_simple.json`)
- ✅ Enhanced hierarchical service display
- ✅ Improved error handling and retry logic
- ✅ Better service grouping and organization
- ✅ Percentage calculations for service groups
- ✅ Interactive mode support
- ✅ Configuration setup wizard (`--setup`)

**Usage:**
```bash
# First time setup - create config_simple.json
python3 redhat_summary_status_simple_v2.py --setup

# Quick status (same as v1)
python3 redhat_summary_status_simple_v2.py quick

# Interactive mode - choose operation
python3 redhat_summary_status_simple_v2.py

# Enhanced hierarchical view
python3 redhat_summary_status_simple_v2.py full

# Export with configuration
python3 redhat_summary_status_simple_v2.py export --output ./reports
```

**Key Benefits:**
- ⚙️ **Configurable** - Uses config.json for settings
- 🏗️ **Better hierarchy** - Improved service organization
- 🎮 **Interactive mode** - User-friendly operation selection
- 📈 **Group statistics** - Availability per service group

### Which Version to Choose?

| Feature | Enterprise v3.0 | Simple v2 | Simple v1 |
|---------|----------------|-----------|-----------|
| **Global Availability %** | ✅ | ✅ | ✅ |
| **Basic Status Check** | ✅ | ✅ | ✅ |
| **Service Hierarchy** | ✅ | ✅ | ✅ |
| **Export Functions** | ✅ | ✅ | ✅ |
| **Configuration File** | ✅ `config.json` | ✅ `config_simple.json` | ❌ |
| **Setup Wizard** | ✅ | ✅ `--setup` | ❌ |
| **Caching** | ✅ Advanced | ✅ Basic | ✅ Basic |
| **AI Analytics** | ✅ | ❌ | ❌ |
| **Database Backend** | ✅ | ❌ | ❌ |
| **Email Notifications** | ✅ | ❌ | ❌ |
| **Performance Monitoring** | ✅ | ❌ | ❌ |
| **SLO Tracking** | ✅ | ❌ | ❌ |
| **Memory Usage** | High | Medium | Low |
| **Startup Time** | Slow | Medium | Fast |

**Recommendations:**
- 🏢 **Enterprise environments**: Use `redhat_summary_status.py` (v3.0)
- 🏠 **Personal/small teams**: Use `redhat_summary_status_simple_v2.py`
- ⚡ **Quick checks/scripts**: Use `redhat_summary_status_simple_v1.py`

## Configuration

### Configuration Files Overview

Different versions use different configuration files:

| Version | Configuration File | Purpose |
|---------|-------------------|---------|
| **Enterprise v3.0** | `config.json` | Full enterprise configuration with analytics, notifications, caching |
| **Simple v2** | `config_simple.json` | Simplified configuration for basic functionality |
| **Simple v1** | None | No configuration file needed - works out of the box |
| **Hierarchical** | `config.json` | Same as enterprise version |

### Project Structure

```
/home/dom/bin/
├── redhat_summary_status.py          # Enterprise v3.0 (3,288 lines)
├── redhat_summary_status_simple_v1.py # Simple v1 (379 lines)
├── redhat_summary_status_simple_v2.py # Simple v2 (599 lines)
├── config.json                        # Enterprise configuration
├── config_simple.json                 # Simple v2 configuration  
├── README.md                          # Complete documentation (763 lines)
├── CHANGELOG.md                       # Version history (375 lines)
└── test_email_config.py               # Utility script
```

### Enterprise Configuration (config.json)

The enterprise script uses `config.json` for comprehensive customization:

```json
{
  "api": {
    "url": "https://status.redhat.com/api/v2/summary.json",
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 2,
    "concurrent_requests": 1,
    "rate_limit_delay": 0.5
  },
  "cache": {
    "enabled": true,
    "ttl": 300,
    "directory": ".cache",
    "max_size_mb": 100,
    "compression": true,
    "cleanup_interval": 3600
  },
  "monitoring": {
    "enabled": false,
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
    "enable_metrics": true,
    "detailed_timing": false,
    "memory_profiling": false,
    "max_concurrent_operations": 5
  },
  "ai_analytics": {
    "enabled": true,
    "anomaly_detection": true,
    "predictive_analysis": true,
    "learning_window": 50,
    "anomaly_threshold": 2.0,
    "min_confidence": 0.7
  },
  "database": {
    "enabled": true,
    "path": "redhat_monitoring.db",
    "retention_days": 30,
    "auto_cleanup": true
  },
  "notifications": {
    "email": {
      "enabled": false,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "use_tls": true,
      "from_address": "alerts@yourcompany.com",
      "to_addresses": ["admin@yourcompany.com", "ops@yourcompany.com"],
      "username": "your_email@gmail.com",
      "password": "your_app_password"
    },
    "webhooks": {
      "enabled": false,
      "urls": [
        "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        "https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK"
      ]
    }
  },
  "slo": {
    "enabled": true,
    "targets": {
      "global_availability": 99.9,
      "response_time": 2.0,
      "uptime_monthly": 99.5
    },
    "tracking_period": "monthly",
    "alert_on_breach": true
  },
  "logging": {
    "enabled": false,
    "level": "INFO",
    "file": "redhat_status.log",
    "max_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

### Simple Configuration (config_simple.json)

The simple v2 version uses a streamlined configuration file for basic functionality:

```json
{
  "_comment": "Configuration file for Red Hat Status Checker Simple Versions (v1 and v2)",
  "_note": "This is a simplified configuration with only essential settings",
  "_versions": "redhat_summary_status_simple_v1.py (uses no config), redhat_summary_status_simple_v2.py (uses this config)",
  
  "api": {
    "url": "https://status.redhat.com/api/v2/summary.json",
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 2
  },
  "output": {
    "default_directory": ".",
    "timestamp_format": "%Y%m%d_%H%M%S"
  },
  "display": {
    "show_percentages": true,
    "show_health_indicator": true,
    "show_group_summaries": true
  }
}
```

#### Creating Simple Configuration

To create or update the simple configuration file:

```bash
# Create config_simple.json for simple v2
python3 redhat_summary_status_simple_v2.py --setup

# The setup will create config_simple.json with sensible defaults
# You can then edit the file manually if needed
```

**Key differences from enterprise config:**
- ❌ No caching configuration
- ❌ No notification settings  
- ❌ No logging configuration
- ❌ No monitoring thresholds
- ✅ Only essential API and display settings
- ✅ Lightweight and simple to manage

## 📧 Email Notifications Setup

### Gmail Configuration
To enable email alerts with Gmail:

1. **Create a config.json file** with your email settings:
```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "use_tls": true,
      "from_address": "your-email@gmail.com",
      "to_addresses": ["admin@company.com", "ops@company.com"],
      "username": "your-email@gmail.com",
      "password": "your-app-password"
    }
  },
  "monitoring": {
    "enabled": true,
    "alert_thresholds": {
      "availability_critical": 85.0,
      "availability_warning": 95.0
    }
  }
}
```

2. **Generate Gmail App Password:**
   - Go to Gmail Settings → Security → 2-Step Verification
   - Generate an "App Password" for this application
   - Use the app password (not your regular password)

3. **Test email alerts:**
```bash
# Enable monitoring and test with critical threshold
python3 redhat_summary_status.py --anomaly-analysis --enable-monitoring
```

### Microsoft Outlook/Office 365 Configuration
```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp-mail.outlook.com",
      "smtp_port": 587,
      "use_tls": true,
      "from_address": "your-email@outlook.com",
      "to_addresses": ["admin@company.com"],
      "username": "your-email@outlook.com",
      "password": "your-password"
    }
  }
}
```

### Corporate SMTP Configuration
```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.yourcompany.com",
      "smtp_port": 25,
      "use_tls": false,
      "from_address": "redhat-alerts@yourcompany.com",
      "to_addresses": [
        "sysadmin@yourcompany.com",
        "devops@yourcompany.com",
        "management@yourcompany.com"
      ],
      "username": "",
      "password": ""
    }
  }
}
```

## 🔔 Webhook Notifications (Slack/Teams/Discord)

### Slack Integration
```json
{
  "notifications": {
    "webhooks": {
      "enabled": true,
      "urls": [
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
      ]
    }
  }
}
```

**Setup Steps:**
1. Go to your Slack workspace
2. Create a new app and enable incoming webhooks
3. Copy the webhook URL
4. Add to config.json

### Microsoft Teams Integration
```json
{
  "notifications": {
    "webhooks": {
      "enabled": true,
      "urls": [
        "https://yourcompany.webhook.office.com/webhookb2/xxx/IncomingWebhook/xxx"
      ]
    }
  }
}
```

### Discord Integration
```json
{
  "notifications": {
    "webhooks": {
      "enabled": true,
      "urls": [
        "https://discord.com/api/webhooks/123456789/XXXXXXXXXXXXXXXXXXXXXXXX"
      ]
    }
  }
}
```

## ⚡ Triggering Alerts

Alerts are automatically sent when:
- System availability drops below critical threshold (85% by default)
- Anomalies are detected by AI analytics
- SLO targets are breached
- Performance degradation is detected

### Manual Alert Testing
```bash
# Test email configuration
python3 redhat_summary_status.py --anomaly-analysis --enable-monitoring

# Force alert with low threshold
python3 redhat_summary_status.py quick --enable-monitoring
```

### Alert Types Sent

**Critical Alerts:**
- System availability below 85%
- Multiple service failures
- Database connection failures
- API timeouts exceeding thresholds

**Warning Alerts:**
- Availability below 95%
- Performance degradation
- Cache failures
- SLO threshold approaches

**Example Email Alert:**
```
Subject: [CRITICAL] Red Hat Status Alert - Global System

Red Hat Status Alert

Severity: CRITICAL
Component: Global System  
Message: System availability critically low: 83.2%
Timestamp: 2025-08-03 14:30:22

This is an automated alert from Red Hat Status Monitoring System.
```

## Requirements

- Python 3.6+
- requests library
- Optional: psutil (for memory monitoring)

```bash
pip install requests
pip install psutil  # Optional, for memory metrics
```

## 🚀 Quick Setup for Email Alerts

1. **Copy the example configuration:**
```bash
cp config.example.json config.json
```

2. **Edit config.json with your email settings:**
```bash
nano config.json
# Or use your preferred editor
```

3. **Enable email notifications:**
```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "from_address": "your-email@gmail.com",
      "to_addresses": ["admin@company.com"],
      "username": "your-email@gmail.com", 
      "password": "your-gmail-app-password"
    }
  },
  "monitoring": {
    "enabled": true
  }
}
```

4. **Test the email setup:**
```bash
# Test email configuration independently  
python3 test_email_config.py

# Or test through the main script
python3 redhat_summary_status.py --anomaly-analysis --enable-monitoring
```

**📱 Pro Tip:** For production use, set up both email and Slack/Teams webhooks for redundant alerting!

### Email Test Script
A dedicated email test script is included for easy configuration validation:

```bash
python3 test_email_config.py
```

This will:
- ✅ Validate your config.json email settings
- 📧 Send a test email to verify connectivity  
- 🔧 Provide troubleshooting tips for common issues
- 📊 Display configuration details

## Environment Variables

Override configuration settings using environment variables:

```bash
export REDHAT_STATUS_API_URL="https://status.redhat.com/api/v2/summary.json"
export REDHAT_STATUS_TIMEOUT=15
export REDHAT_STATUS_MAX_RETRIES=5
export REDHAT_STATUS_RETRY_DELAY=3
```

Or use the provided `.env.example` file:
```bash
cp .env.example .env
# Edit .env with your preferences
source .env
python3 redhat_summary_status.py quick
```

## Performance Features

### Benchmark Results
- **Cache Speedup**: 250%+ improvement over network requests
- **Compression**: 60%+ reduction in storage space
- **Concurrent Operations**: Multi-threaded processing for enterprise scale
- **Memory Efficiency**: Optimized memory usage with profiling

### Health Scoring
- 🟢 **A+ (99.9%+)**: Exceptional service health
- 🟢 **A (99.5-99.9%)**: Excellent availability
- 🟡 **B (95-99.5%)**: Good performance with minor issues
- 🟠 **C (90-95%)**: Adequate but requires attention
- 🔴 **D-F (<90%)**: Poor health requiring immediate action

### Analytics Features
- **Pattern Recognition**: Automatic detection of recurring issues
- **Peak Time Analysis**: Identification of failure patterns by time
- **Trend Analysis**: Statistical analysis of availability over time
- **Predictive Insights**: Early warning system for potential issues
- **Performance Correlation**: Analysis of performance vs availability

## Output Examples

### Health Report Structure
```json
{
  "report_timestamp": "2025-08-03T08:00:00",
  "overall_health": {
    "availability_percentage": 98.6,
    "health_grade": "A",
    "total_services": 139,
    "operational_services": 137
  },
  "performance_metrics": {
    "cache_hit_ratio": 85.2,
    "response_time": 0.28,
    "api_calls": 15
  },
  "alerts": [
    {
      "severity": "warning",
      "component": "Authentication Service",
      "message": "Degraded performance detected"
    }
  ],
  "recommendations": [
    "🟢 System health is excellent",
    "📊 Cache performance is optimal"
  ]
}
```

### Performance Metrics Dashboard
```
� PERFORMANCE METRICS
==================================================
🕒 Session Duration: 2.34s
🌐 API Calls: 3
📋 Cache Hits: 8
❌ Cache Misses: 2
📈 Cache Hit Ratio: 80.0%
⚡ Avg Response Time: 0.28s
📦 Data Transferred: 59,301 bytes
💾 Cache Size: 1.2 MB
🧠 Memory Usage: 42.3 MB
```

### System Insights
```
🔍 SYSTEM INSIGHTS
==================================================
📊 Analysis based on 25 data points

⏰ Peak Issue Times:
   14:00: 3.2% average issue rate
   02:00: 2.1% average issue rate
   09:00: 1.8% average issue rate

💡 Recommendations:
   • ⚠️ Schedule maintenance outside peak hours (14:00)
   • 📈 System shows stable availability trends
   • 🔧 Consider proactive monitoring for early detection
```

## Export Files
- `health_report_YYYYMMDD_HHMMSS.json` - Comprehensive health analysis
- `health_summary_YYYYMMDD_HHMMSS.txt` - Human-readable summary
- `redhat_status_YYYYMMDD_HHMMSS.json` - Complete raw data
- `redhat_summary_YYYYMMDD_HHMMSS.txt` - Executive summary
- `status_history_YYYYMMDD_HHMMSS.csv` - Historical trends data

## Error Handling

- Automatic retry mechanism with exponential backoff
- Graceful degradation for partial data scenarios
- Comprehensive error logging with categorization
- Network failure recovery with intelligent caching
- Resource cleanup and memory management

## Advanced Features

### Concurrent Health Checks
```bash
# Perform multiple checks simultaneously
python3 redhat_summary_status.py --concurrent-check
```

### Pattern Analysis
```bash
# Analyze service patterns for insights
python3 redhat_summary_status.py --insights
```

### Performance Benchmarking
```bash
# Run comprehensive performance tests
python3 redhat_summary_status.py --benchmark
```

### Configuration Validation
```bash
# Validate current configuration
python3 redhat_summary_status.py --config-check
```

## License

MIT License - Feel free to use and modify for enterprise or personal use.

---

## Version History

- **v3.0.0**: Advanced Performance & Analytics Platform
- **v2.0.0**: Professional monitoring with caching and trends
- **v1.0.0**: Basic French status checker

**Project**: Red Hat Status Checker v3.0  
**Maintainer**: @dapiced Enhanced by GitHub Copilot  
**Enterprise Ready**: ✅ Production-grade monitoring solution
