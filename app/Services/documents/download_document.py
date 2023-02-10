import sys
import http.client as http
http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

import urllib.request, urllib.error
from urllib import request

class DownloadDocument:


    """
    Download document from origin

    Download file from CVM portal and store it
    in storage folder
    
    """ 
    def download(storage_path, document, year):

        # Get origin path based on document type
        origin = DownloadDocument.getOriginPath(document, year)

        # Define where file will be stored
        destiny = storage_path + "/" + document + "/" + str(year) + ".zip"

        if(origin != False):
            print('  |- Fazendo download: ' + document + ' | ' + str(year), flush=True, file=sys.stdout)

            try:
                conn = urllib.request.urlopen(origin)
            except urllib.error.HTTPError as e:
                # Return code error (e.g. 404, 501, ...)
                print('     HTTPError: {}'.format(e.code), flush=True)

            except urllib.error.URLError as e:
                # Not an HTTP-specific error (e.g. connection refused)
                print('     URLError: {}'.format(e.reason), flush=True)

            else:
                # 200
                request.urlretrieve(origin, destiny)


    """
    Get original path to data

    Concatenate the url for document source
    at CVM portal based on document type and
    period of release.
    
    """
    def getOriginPath(document, year):

        if(document == 'DFP' and year >= 2010):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_" + str(year) + ".zip"

        if(document == 'ITR' and year >= 2011):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/ITR_CIA_ABERTA_" + str(year) + ".zip"

        if(document == 'FCA' and year >= 2018):
            return "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_" + str(year) + ".zip"

        return False