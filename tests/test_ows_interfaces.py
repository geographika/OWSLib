# This test checks that the OWSLib service interfaces are the same across all service type:
# Author: Dominic Lowe, 17th September 2009
# Part of OWSLib package.
from tests.utils import service_ok

import pytest

from tests.utils import resource_file
import owslib
from owslib.csw import CatalogueServiceWeb
from owslib.wms import WebMapService
from owslib.wcs import WebCoverageService
from owslib.wfs import WebFeatureService
from owslib.util import OrderedDict


def test_ows_interfaces_csw():
    # live service at https://demo.pycsw.org/cite/csw?service=CSW&version=2.0.2&request=GetCapabilities
    cswxml = open(resource_file('csw_pycwsCapabilities.xml'), 'rb').read()
    service = CatalogueServiceWeb('url', version='2.0.2', xml=cswxml)
    # Check each service instance conforms to OWSLib interface
    service.alias = 'CSW'
    isinstance(service, owslib.catalogue.csw2.CatalogueServiceWeb)
    # URL attribute
    assert service.url == 'url'
    # version attribute
    assert service.version == '2.0.2'
    # Identification object
    assert hasattr(service, 'identification')
    # Check all ServiceIdentification attributes
    assert service.identification.type == 'CSW'
    for attribute in ['type', 'version', 'title', 'abstract', 'keywords', 'accessconstraints', 'fees']:
        assert hasattr(service.identification, attribute)
    # Check all ServiceProvider attributes
    for attribute in ['name', 'url', 'contact']:
        assert hasattr(service.provider, attribute)
    # Check all operations implement IOperationMetadata
    for op in service.operations:
        for attribute in ['name', 'formatOptions', 'methods']:
            assert hasattr(op, attribute)
    # Check all contents implement IContentMetadata as a dictionary
    # CSW does not work in this way so use dummy
    service.contents = {'dummy': '1'}
    isinstance(service.contents, dict)
    # Check any item (WCS coverage, WMS layer etc) from the contents of each service
    # Check it conforms to IContentMetadata interface
    # CSW does not conform to this


def test_ows_interfaces_wms():
    wmsxml = open(resource_file('wms_JPLCapabilities.xml'), 'rb').read()
    service = WebMapService('url', version='1.1.1', xml=wmsxml)
    # Check each service instance conforms to OWSLib interface
    service.alias = 'WMS'
    isinstance(service, owslib.map.wms111.WebMapService_1_1_1)
    # URL attribute
    assert service.url == 'url'
    # version attribute
    assert service.version == '1.1.1'
    # Identification object
    assert hasattr(service, 'identification')
    # Check all ServiceIdentification attributes
    assert service.identification.type == 'OGC:WMS'
    for attribute in ['type', 'version', 'title', 'abstract', 'keywords', 'accessconstraints', 'fees']:
        assert hasattr(service.identification, attribute)
    # Check all ServiceProvider attributes
    for attribute in ['name', 'url', 'contact']:
        assert hasattr(service.provider, attribute)
    # Check all operations implement IOperationMetadata
    for op in service.operations:
        for attribute in ['name', 'formatOptions', 'methods']:
            assert hasattr(op, attribute)
    # Check all contents implement IContentMetadata as a dictionary
    isinstance(service.contents, OrderedDict)
    # Check any item (WCS coverage, WMS layer etc) from the contents of each service
    # Check it conforms to IContentMetadata interface
    # get random item from contents dictionary -has to be a nicer way to do this!
    content = service.contents[list(service.contents.keys())[0]]
    for attribute in ['id', 'title', 'boundingBox', 'boundingBoxWGS84', 'crsOptions', 'styles', 'timepositions']:
        assert hasattr(content, attribute)


def test_ows_interfaces_wcs():
    # live service at https://thredds.ucar.edu/thredds/wcs/grib/NCEP/NAM/CONUS_80km/best/?service=WCS&version=1.0.0&request=GetCapabilities
    url = 'https://example.com'
    url = 'https://thredds.ucar.edu/thredds/wcs/grib/NCEP/NAM/CONUS_80km/best/'
    wcsxml = open(resource_file('wcs_threddsCapabilities.xml'), 'rb').read()
    wcsxml = None
    service = WebCoverageService(url, version='1.0.0', xml=wcsxml)
    # Check each service instance conforms to OWSLib interface
    service.alias = 'WCS'
    isinstance(service, owslib.coverage.wcs100.WebCoverageService_1_0_0)
    # URL attribute
    assert service.url == url
    # version attribute
    assert service.version == '1.0.0'
    # Identification object
    assert hasattr(service, 'identification')
    # Check all ServiceIdentification attributes
    assert service.identification.type == 'OGC:WCS'
    for attribute in ['type', 'version', 'title', 'abstract', 'keywords', 'fees']:
        assert hasattr(service.identification, attribute)
    # Check all ServiceProvider attributes
    for attribute in ['name', 'url', 'contact']:
        assert hasattr(service.provider, attribute)
    # Check all operations implement IOperationMetadata
    for op in service.operations:
        for attribute in ['name', 'methods']:
            assert hasattr(op, attribute)
    # Check all contents implement IContentMetadata as a dictionary
    isinstance(service.contents, dict)
    # Check any item (WCS coverage, WMS layer etc) from the contents of each service
    # Check it conforms to IContentMetadata interface
    # get random item from contents dictionary -has to be a nicer way to do this!
    content = service.contents[list(service.contents.keys())[0]]
    for attribute in ['id', 'title', 'boundingBox', 'boundingBoxWGS84', 'crsOptions', 'styles']:
        assert hasattr(content, attribute)

    # 'timepositions'
    # 'https://thredds.ucar.edu/thredds/wcs/grib/NCEP/NAM/CONUS_80km/best/?service=WCS&request=DescribeCoverage&version=1.0.0&coverage=Convective_Available_Potential_Energy_layer_between_two_pressure_difference_from_ground_layer'

def test_ows_interfaces_wfs():
    wfsxml = open(resource_file('mapserver-wfs-cap.xml'), 'rb').read()
    service = WebFeatureService('url', version='1.0', xml=wfsxml)
    # Check each service instance conforms to OWSLib interface
    service.alias = 'CSW'
    isinstance(service, owslib.feature.wfs100.WebFeatureService_1_0_0)
    # URL attribute
    assert service.url == 'url'
    # version attribute
    assert service.version == '1.0'
    # Identification object
    assert hasattr(service, 'identification')
    # Check all ServiceIdentification attributes
    assert service.identification.type == 'MapServer WFS'
    for attribute in ['type', 'version', 'title', 'abstract', 'keywords', 'accessconstraints', 'fees']:
        assert hasattr(service.identification, attribute)
    # Check all ServiceProvider attributes
    for attribute in ['name', 'url']:
        assert hasattr(service.provider, attribute)
    # Check all operations implement IOperationMetadata
    for op in service.operations:
        for attribute in ['name', 'formatOptions', 'methods']:
            assert hasattr(op, attribute)
    # Check all contents implement IContentMetadata as a dictionary
    isinstance(service.contents, dict)
    # Check any item (WCS coverage, WMS layer etc) from the contents of each service
    # Check it conforms to IContentMetadata interface
    # get random item from contents dictionary -has to be a nicer way to do this!
    content = service.contents[list(service.contents.keys())[0]]
    for attribute in ['id', 'title', 'boundingBox', 'boundingBoxWGS84', 'crsOptions', 'styles', 'timepositions']:
        assert hasattr(content, attribute)

test_ows_interfaces_wcs()
# test_ows_interfaces_csw()