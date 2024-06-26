import sys
import os

def error_message_info(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_msg="Error occurred in Script file [{0}] at line number [{1}] and error message [{2}]".format(
    file_name,exc_tb.tb_lineno,str(error)
    )
    return error_msg

class UsVisaException(Exception):

    def __init__(self,error_msg,error_detail):
        super().__init__(error_msg)
        self.error_msg=error_message_info(error_msg,error_detail=error_detail)

    def __str__(self):
        return self.error_msg


