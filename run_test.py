import pytest
import os
from utilities.logger import logger

def run_tests():
    # Setup report directory
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    logger.info("Starting test execution")
    
    pytest.main([
        "-v",
        "--html=reports/test_report.html",
        "--self-contained-html",
        "--capture=sys",
        "-m", "not skip"
    ])
    
    logger.info("Test execution completed")

if __name__ == "__main__":
    run_tests()