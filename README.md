# Red Hat Status Checker v2.0

An enhanced Python script to monitor Red Hat services status with improved features and reliability.

## Features

### Core Functionality
- **Quick Status**: Global Red Hat status overview
- **Simple Check**: Main services status monitoring
- **Full Check**: Complete hierarchical service structure
- **Data Export**: JSON and human-readable summary reports

### Improvements in v2.0
- ✅ **Enhanced Error Handling**: Retry mechanism with configurable attempts
- ✅ **Better CLI Interface**: Proper argument parsing with help and examples  
- ✅ **Configuration File**: Customizable settings via `config.json`
- ✅ **Type Hints**: Better code documentation and IDE support
- ✅ **Health Indicators**: Visual health status (EXCELLENT/GOOD/FAIR/POOR)
- ✅ **Group Statistics**: Sub-service availability percentages
- ✅ **Quiet Mode**: Minimal output for automation
- ✅ **File Organization**: Configurable output directories
- ✅ **Summary Reports**: Human-readable export files

## Usage

### Command Line Examples
```bash
# Interactive mode
python3 redhat_summary_status.py

# Quick status check
python3 redhat_summary_status.py quick

# Main services only
python3 redhat_summary_status.py simple

# Complete structure
python3 redhat_summary_status.py full

# Export data to files
python3 redhat_summary_status.py export

# Export to specific directory
python3 redhat_summary_status.py export --output ./reports

# Quiet mode (minimal output)
python3 redhat_summary_status.py quick --quiet

# Display everything
python3 redhat_summary_status.py all
```

### Help and Version
```bash
# Show help
python3 redhat_summary_status.py --help

# Show version
python3 redhat_summary_status.py --version
```

## Configuration

The script uses `config.json` for customization:

```json
{
  "api": {
    "url": "https://status.redhat.com/api/v2/summary.json",
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 2
  },
  "output": {
    "default_directory": ".",
    "create_summary_report": true,
    "timestamp_format": "%Y%m%d_%H%M%S"
  },
  "display": {
    "show_percentages": true,
    "show_health_indicator": true,
    "show_group_summaries": true
  }
}
```

## Requirements

- Python 3.6+
- requests library

```bash
pip install requests
```

## Output Examples

### Health Indicators
- 🟢 **EXCELLENT** (95-100% availability)
- 🟡 **GOOD** (90-94% availability)  
- 🟠 **FAIR** (80-89% availability)
- 🔴 **POOR** (<80% availability)

### Export Files
- `redhat_status_YYYYMMDD_HHMMSS.json` - Complete raw data
- `redhat_summary_YYYYMMDD_HHMMSS.txt` - Human-readable summary

## Error Handling

- Automatic retry on network failures
- Graceful degradation for partial data
- User-friendly error messages
- Keyboard interrupt handling

## License

MIT License - Feel free to use and modify as needed.
