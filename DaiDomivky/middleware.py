import datetime
import logging
import time


logger = logging.getLogger(__name__)


class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # using get_response to process response

    def __call__(self, request):
        epoch = time.time()
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%d/%m/%y | %H:%M:%S')

        logger.debug(f'\nNew Request: [{formatted_datetime}]')
        logger.debug(f'Request method: {request.method}')
        logger.debug(f'Request path: {request.path}')

        # before request
        response = self.get_response(request)
        # after request

        estimation = round((time.time() - epoch) * 1000)
        logger.debug(f'Execution time: {estimation} ms')
        logger.debug(f'Response status: {response.status_code}')

        return response
