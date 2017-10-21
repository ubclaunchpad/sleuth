import json
from enum import Enum

class ErrorTypes(Enum):
    '''
    Defines errors that can occur when making calls to the Sleuth API. This makes
    it easier for the front-end to handle errors appropriately.
    '''
    # Occurs when an unexpected error occurs duing the handling of a request
    UNEXPECTED_SERVER_ERROR = 0
    # Occurs when Django cannot reach the Solr instance.
    SOLR_CONNECTION_ERROR = 1
    # Occurs when Solr returns an error response to a search query.
    SOLR_SEARCH_ERROR = 2
    # Occurs when a search term or core name is missing from a search request.
    INVALID_SEARCH_REQUEST = 3

class SleuthError(Exception):
    '''
    Represents an error that occurred during the processing of a request to the
    Sleuth API.
    '''

    def __init__(self, error_type, message=None):
        '''
        Takes an HTTP status code and an error message (must be one of ErrorTypes)
        to return to the client and creates a SleuthError that can be converted
        to JSON.
        '''
        self.error_type = error_type

        if message is not None:
            self.message = message
            return

        if error_type is ErrorTypes.UNEXPECTED_SERVER_ERROR:
            self.message = 'An unexpected error occurred in the Sleuth ' + \
                'backend during the handling of your request.'
        elif error_type is ErrorTypes.SOLR_CONNECTION_ERROR:
            self.message = 'Failed to connect to the Solr instance'
        elif error_type is ErrorTypes.SOLR_SEARCH_ERROR:
            self.message = 'Solr returned an error response to the search query.'
        elif error_type is ErrorTypes.INVALID_SEARCH_REQUEST:
            self.message = 'Must supply a search term with the parameters "q" and "core".'
        else:
            raise ValueError('Invalid error type. Must be on of ErrorTypes.')

    def json(self):
        '''
        Returns the error in the following JSON format
            {
                message: <self.message>
                errorType: <self.error_type>
            }
        '''
        error = {
            'message': self.message,
            'errorType': self.error_type.name,
        }
        return json.dumps(error)