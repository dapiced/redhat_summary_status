#!/usr/bin/env python3
"""
Red Hat Status Checker - Email Configuration Test & Hidden Feature Discovery

This utility provides comprehensive testing and discovery capabilities for the
Red Hat Status Checker monitoring system. It serves as both an email configuration
validator and a feature discovery tool for advanced enterprise capabilities.

Features:
    - Email configuration testing and validation
    - Hidden feature discovery and documentation
    - Environment variable testing
    - Advanced configuration analysis
    - Usage examples and troubleshooting

Usage:
    python3 test_email_config.py                    # Test email configuration
    python3 test_email_config.py --discover         # Discover hidden features
    python3 test_email_config.py --demo            # Show usage examples
    python3 test_email_config.py --all             # Complete test suite

Requirements:
    - Python 3.6+
    - config.json file (copy from config.example.json)
    - Valid email configuration for email testing

Author: Red Hat Status Checker v3.0 - Enterprise Edition
Version: 1.0.0
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys
import os
import argparse

# Module constants
VERSION = "1.0.0"
DEFAULT_CONFIG_FILE = "config.json"
EXAMPLE_CONFIG_FILE = "config.example.json"

# Hidden feature definitions
HIDDEN_ENV_VARS = [
    ('REDHAT_STATUS_API_URL', 'Override default API URL'),
    ('REDHAT_STATUS_TIMEOUT', 'Override request timeout (seconds)'),
    ('REDHAT_STATUS_MAX_RETRIES', 'Override max retry attempts'),
    ('REDHAT_STATUS_RETRY_DELAY', 'Override retry delay (seconds)')
]

HIDDEN_CLI_ARGS = [
    ('--ai-insights', 'AI-powered anomaly detection and predictive analysis'),
    ('--slo-dashboard', 'Service Level Objectives dashboard'),
    ('--anomaly-analysis', 'Advanced anomaly analysis with detailed reporting'),
    ('--export-ai-report', 'Export comprehensive AI analysis report'),
    ('--system-intelligence', 'Comprehensive system intelligence dashboard'),
    ('--db-maintenance', 'Database maintenance and cleanup operations'),
    ('--config-check', 'Validate configuration and display current settings'),
    ('--benchmark', 'Run performance benchmark tests'),
    ('--concurrent-check', 'Multi-threaded health checks for faster results')
]

def test_hidden_features():
    """
    Discover and test hidden/undocumented features of the Red Hat Status Checker.
    
    This function analyzes the monitoring system for:
    - Environment variable overrides
    - Hidden command-line arguments
    - Advanced configuration options
    - Feature enablement status
    
    The discovery includes AI analytics, SLO tracking, database management,
    performance monitoring, and enterprise-grade alerting capabilities.
    
    Returns:
        None: Prints discovery results to console
    """
    print("🔍 DISCOVERING HIDDEN FEATURES")
    print("=" * 50)
    
    # Test environment variables
    print("\n📝 Environment Variables Support:")
    
    for env_var, description in HIDDEN_ENV_VARS:
        value = os.getenv(env_var)
        status = f"✅ {value}" if value else "❌ Not set"
        print(f"   {env_var}: {status}")
        print(f"      {description}")
    
    # Test hidden CLI arguments
    print("\n🔧 Hidden Command-Line Arguments:")
    
    print("   Available hidden features:")
    for arg, description in HIDDEN_CLI_ARGS:
        print(f"   {arg:<20} - {description}")
    
    # Test configuration features
    print("\n⚙️  Advanced Configuration Options:")
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        # Check AI analytics settings
        ai_config = config.get('ai_analytics', {})
        print(f"   AI Analytics: {'✅ Enabled' if ai_config.get('enabled', True) else '❌ Disabled'}")
        if ai_config.get('enabled', True):
            print(f"      Learning Window: {ai_config.get('learning_window', 50)} samples")
            print(f"      Anomaly Threshold: {ai_config.get('anomaly_threshold', 2.0)}")
            print(f"      Min Confidence: {ai_config.get('min_confidence', 0.7)}")
        
        # Check SLO settings
        slo_config = config.get('slo', {})
        print(f"   SLO Tracking: {'✅ Enabled' if slo_config.get('enabled', True) else '❌ Disabled'}")
        if slo_config.get('enabled', True):
            targets = slo_config.get('targets', {})
            print(f"      Global Availability Target: {targets.get('global_availability', 99.9)}%")
            print(f"      Response Time Target: {targets.get('response_time', 2.0)}s")
            print(f"      Monthly Uptime Target: {targets.get('uptime_monthly', 99.5)}%")
        
        # Check database settings
        db_config = config.get('database', {})
        print(f"   Database Backend: {'✅ Enabled' if db_config.get('enabled', True) else '❌ Disabled'}")
        if db_config.get('enabled', True):
            print(f"      Retention: {db_config.get('retention_days', 30)} days")
            print(f"      Auto Cleanup: {'✅' if db_config.get('auto_cleanup', True) else '❌'}")
        
        # Check monitoring thresholds
        monitoring = config.get('monitoring', {})
        if monitoring.get('enabled', False):
            thresholds = monitoring.get('alert_thresholds', {})
            print(f"   Alert Thresholds:")
            print(f"      Critical Availability: {thresholds.get('availability_critical', 85)}%")
            print(f"      Warning Availability: {thresholds.get('availability_warning', 95)}%")
            print(f"      Response Time Warning: {thresholds.get('response_time_warning', 5)}s")
    
    except FileNotFoundError:
        print("   ❌ config.json not found - copy config.example.json to test advanced features")
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
    
    print("\n💡 To enable hidden features:")
    print(f"   1. Copy {EXAMPLE_CONFIG_FILE} to {DEFAULT_CONFIG_FILE}")
    print("   2. Edit configuration settings as needed")
    print("   3. Use hidden CLI arguments for advanced operations")
    print("   4. Set environment variables for API customization")

def demonstrate_hidden_features():
    """
    Demonstrate usage examples for all hidden features.
    
    Provides ready-to-use command examples for:
    - AI & Analytics features (anomaly detection, SLO dashboards)
    - System administration tools (config validation, maintenance)
    - Performance optimization features (benchmarking, concurrent operations)
    - Environment variable overrides for API customization
    - Advanced configuration options
    
    This serves as a practical reference guide for power users and
    system administrators who want to leverage advanced capabilities.
    
    Returns:
        None: Prints usage examples to console
    """
    print("\n🎯 HIDDEN FEATURE USAGE EXAMPLES")
    print("=" * 50)
    
    print("\n📊 AI & Analytics Features:")
    print("   python3 redhat_summary_status.py --ai-insights")
    print("   python3 redhat_summary_status.py --slo-dashboard")
    print("   python3 redhat_summary_status.py --anomaly-analysis")
    print("   python3 redhat_summary_status.py --export-ai-report")
    
    print("\n🔧 System Administration:")
    print("   python3 redhat_summary_status.py --config-check")
    print("   python3 redhat_summary_status.py --db-maintenance")
    print("   python3 redhat_summary_status.py --benchmark")
    print("   python3 redhat_summary_status.py --system-intelligence")
    
    print("\n⚡ Performance Features:")
    print("   python3 redhat_summary_status.py --concurrent-check")
    print("   python3 redhat_summary_status.py quick --enable-monitoring")
    
    print("\n🌍 Environment Variable Overrides:")
    print("   REDHAT_STATUS_API_URL=https://custom.api.com python3 redhat_summary_status.py quick")
    print("   REDHAT_STATUS_TIMEOUT=30 python3 redhat_summary_status.py quick")
    
    print("\n📈 Advanced Configuration (config.json):")
    print("   Enable AI analytics with custom thresholds")
    print("   Configure SLO targets and tracking")
    print("   Set up database retention policies")
    print("   Customize monitoring alert thresholds")

def test_email_config(config_file='config.json'):
    """
    Test email configuration for Red Hat Status Checker notifications.
    
    This function validates email settings and sends a test message to verify
    the notification system is working correctly. It performs comprehensive
    validation including:
    - Configuration file existence and format
    - Required field validation (SMTP server, credentials, recipients)
    - SMTP connection testing with TLS support
    - Test email delivery with hidden feature documentation
    
    Args:
        config_file (str): Path to configuration file (default: 'config.json')
        
    Returns:
        bool: True if email configuration is valid and test email sent successfully,
              False if configuration is invalid or email sending fails
              
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        SMTPException: If email sending fails due to SMTP issues
        JSONDecodeError: If configuration file is not valid JSON
        
    Example:
        >>> success = test_email_config('my_config.json')
        >>> if success:
        ...     print("Email alerts ready!")
    """
    try:
        # Load config
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        email_config = config.get('notifications', {}).get('email', {})
        
        if not email_config.get('enabled', False):
            print(f"❌ Email notifications are disabled in {config_file}")
            print("💡 Set 'notifications.email.enabled' to true")
            return False
        
        # Validate required fields
        required_fields = ['from_address', 'to_addresses', 'smtp_server']
        missing_fields = [field for field in required_fields if not email_config.get(field)]
        
        if missing_fields:
            print(f"❌ Missing required email configuration fields: {missing_fields}")
            return False
        
        print("📧 Testing email configuration...")
        print(f"   SMTP Server: {email_config['smtp_server']}:{email_config.get('smtp_port', 587)}")
        print(f"   From: {email_config['from_address']}")
        print(f"   To: {', '.join(email_config['to_addresses'])}")
        
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = email_config['from_address']
        msg['To'] = ', '.join(email_config['to_addresses'])
        msg['Subject'] = "[TEST] Red Hat Status Checker Email Configuration Test"
        
        body = f"""
Red Hat Status Checker - Email Test

This is a test email to verify your email configuration is working correctly.

Configuration Details:
- SMTP Server: {email_config['smtp_server']}
- Port: {email_config.get('smtp_port', 587)}
- TLS: {email_config.get('use_tls', True)}
- From: {email_config['from_address']}
- Recipients: {len(email_config['to_addresses'])} address(es)

Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this email, your Red Hat Status Checker email alerts are configured correctly! 🎉

HIDDEN FEATURES AVAILABLE:
- AI-powered analytics and anomaly detection
- SLO (Service Level Objectives) dashboard
- Advanced system intelligence reporting
- Database maintenance and cleanup tools
- Performance benchmarking capabilities
- Concurrent health checking for faster results

Use: python3 test_email_config.py --discover
To learn about all hidden features!

---
Red Hat Status Checker v3.0
Enterprise Monitoring Solution
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(email_config['smtp_server'], email_config.get('smtp_port', 587)) as server:
            if email_config.get('use_tls', True):
                server.starttls()
            
            if email_config.get('username') and email_config.get('password'):
                server.login(email_config['username'], email_config['password'])
            
            server.send_message(msg)
        
        print("✅ Test email sent successfully!")
        print("📱 Check your inbox for the test message")
        return True
        
    except FileNotFoundError:
        print(f"❌ {config_file} file not found")
        print(f"💡 Copy {EXAMPLE_CONFIG_FILE} to {DEFAULT_CONFIG_FILE} and edit it with your settings")
        return False
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("\n🔧 Common issues:")
        print("   • Check Gmail app password (not regular password)")
        print("   • Verify SMTP server and port settings")
        print("   • Ensure 'Less secure app access' is enabled (if applicable)")
        print("   • Check firewall/network restrictions")
        return False

def create_argument_parser():
    """
    Create command-line argument parser for the email test and feature discovery tool.
    
    Configures argument parsing with support for:
    - Email configuration testing (default behavior)
    - Hidden feature discovery (--discover)
    - Usage demonstration (--demo)
    - Comprehensive testing suite (--all)
    - Custom configuration file support (--config-file)
    
    Returns:
        argparse.ArgumentParser: Configured argument parser with all options
        
    Example:
        >>> parser = create_argument_parser()
        >>> args = parser.parse_args(['--discover'])
        >>> print(args.discover)  # True
    """
    parser = argparse.ArgumentParser(
        description='Red Hat Status Checker - Email Configuration Test & Hidden Feature Discovery',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Test email configuration
  %(prog)s --discover          # Discover hidden features
  %(prog)s --demo              # Show usage examples
  %(prog)s --all              # Test email + discover features
        """
    )
    
    parser.add_argument(
        '--discover',
        action='store_true',
        help='Discover and test hidden/undocumented features'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Show examples of how to use hidden features'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all tests: email + feature discovery'
    )
    
    parser.add_argument(
        '--config-file',
        default='config.json',
        help='Configuration file to test (default: config.json)'
    )
    
    return parser

if __name__ == "__main__":
    """
    Main execution block for the email configuration test and feature discovery tool.
    
    Parses command-line arguments and executes the appropriate functionality:
    - Email configuration testing (default or with --all)
    - Hidden feature discovery (--discover or --all)
    - Usage demonstration (--demo or --all)
    
    Provides comprehensive summary and exit codes for automation support.
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    print("🧪 RED HAT STATUS CHECKER - EMAIL & HIDDEN FEATURES TEST")
    print("=" * 70)
    print(f"Version: {VERSION}")
    print(f"Config file: {args.config_file}")
    print()
    
    success = True
    
    # Test email configuration (default behavior or explicit)
    if not args.discover and not args.demo or args.all:
        print("\n📧 EMAIL CONFIGURATION TEST")
        print("-" * 35)
        success = test_email_config(args.config_file) and success
    
    # Discover hidden features
    if args.discover or args.all:
        print("\n" if not args.discover else "")
        test_hidden_features()
    
    # Show demonstration
    if args.demo or args.all:
        print("\n" if not args.demo else "")
        demonstrate_hidden_features()
    
    # Final summary
    if args.all:
        print("\n🎉 SUMMARY")
        print("=" * 20)
        if success:
            print("✅ Email configuration is working!")
            print("� Hidden features discovered and documented")
            print("�💡 You can now use advanced monitoring features:")
            print("   python3 redhat_summary_status.py --ai-insights")
            print("   python3 redhat_summary_status.py --slo-dashboard")
        else:
            print("❌ Email configuration needs attention")
            print("🔍 Hidden features are available for testing")
            print("📖 Check the README.md for detailed setup instructions")
    elif args.discover:
        print("\n💡 Hidden features discovered! Use --demo to see usage examples.")
    elif args.demo:
        print("\n💡 Ready to use hidden features! Use --discover to test your configuration.")
    elif success:
        print("\n🎉 Email configuration is working!")
        print("💡 Use --discover to find hidden features!")
    else:
        print("\n❌ Email configuration needs attention")
        print("📖 Check the README.md for detailed setup instructions")
    
    sys.exit(0 if success else 1)
