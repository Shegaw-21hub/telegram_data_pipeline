import sys
import pytest
from packaging import version

# Minimum required Python version
MIN_PYTHON_VERSION = "3.11.0"

def test_python_version():
    """Verify system meets minimum Python version requirement"""
    current_version = version.parse(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    required_version = version.parse(MIN_PYTHON_VERSION)
    
    assert current_version >= required_version, (
        f"Python {MIN_PYTHON_VERSION}+ required. "
        f"Current version: {sys.version}"
    )

def test_ci_environment():
    """Verify running in CI environment when expected"""
    assert "CI" in os.environ, "Test should run in CI environment"
    