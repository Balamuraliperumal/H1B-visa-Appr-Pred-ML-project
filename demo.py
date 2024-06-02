import sys
from US_Visa.logger import logging
from US_Visa.exception import UsVisaException

try:
    a=1/0
except Exception as e:
    raise UsVisaException(e,sys) from e