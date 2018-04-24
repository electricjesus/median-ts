# ~* coding: utf-8 *~
from time import sleep

from hamcrest import assert_that, equal_to, is_not, not_, has_items, has_item, contains_inanyorder, contains_string, calling, raises
from unittest import TestCase
from freezegun import freeze_time

from main import MedianData, service


class TestTestCase(TestCase):
    """
    Pytest sanity
    """
    def test_the_test_system(self):
        assert_that(True, equal_to(True))
        assert_that(True, is_not(equal_to(False)))
    

class MedianCoreUnitTests(TestCase):    
    """
    Core functions tests
    """
    def test_put_integer(self):
        """
        Regular put_integer tests
        """
        md = MedianData()

        md.put_integer(1)
        md.put_integer(2)
        assert_that(len(md.data), equal_to(2))
        assert_that(md.data[1], has_item(1))
        assert_that(md.data[1], has_item(2))
    
    def test_median(self):
        """
        Regular median tests
        """
        md = MedianData()
        md.put_integer(1)
        md.put_integer(2)
        assert_that(md.get_median_last_min(), equal_to(1.5))

    def test_median_with_time_constraints(self):
        """
        Prove that the moving time window median works
        """
        md = MedianData()

        with freeze_time("2001-01-01 01:01:00"):
            md.put_integer(1)
        
        with freeze_time("2001-01-01 01:01:50"):
            md.put_integer(2)
            assert_that(md.get_median_last_min(), equal_to(1.5))

        with freeze_time("2001-01-01 01:02:00"):
            md.put_integer(3)
            assert_that(md.get_median_last_min(), equal_to(2.5))

        with freeze_time("2001-01-01 01:02:30"):
            assert_that(md.get_median_last_min(), equal_to(2.5))

        with freeze_time("2001-01-01 01:02:51"):
            assert_that(md.get_median_last_min(), equal_to(3.0))
        

class MedianServiceTests(TestCase):
    """
    Median Service tests (tests request and response formats, times, etc.)
    """

    def setUp(self):
        service.testing = True
        self.app = service.test_client()

    def tearDown(self):
        pass

    def test_median_empty_dataset(self):
        r = self.app.get('/median')
        assert_that(r.data, contains_string('No data'))

    def test_service_valid_inputs(self):
        r = self.app.post('/put', data="1")
        assert_that(r.status_code, equal_to(200))
        m = self.app.get('/median')
        assert_that(m.data, equal_to('1.0'))
        r = self.app.post('/put', data="2")
        assert_that(r.status_code, equal_to(200))
        m = self.app.get('/median')
        assert_that(m.data, equal_to('1.5'))

    def test_service_invalid_inputs(self):
        assert_that(calling(self.app.post).with_args('/put', data="not_valid"), raises(Exception))

    def test_service_bad_requests(self):
        r = self.app.post('/median')
        assert_that(r.status_code, equal_to(405))