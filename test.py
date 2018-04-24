# ~* coding: utf-8 *~
from time import sleep

from hamcrest import assert_that, equal_to, is_not, has_items, has_item, contains_inanyorder
from unittest import TestCase

from main import MedianData


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
        md = MedianData()

        md.put_integer(1)
        md.put_integer(2)
        assert_that(len(md.data), equal_to(2))
        assert_that(md.data[1], has_item(1))
        assert_that(md.data[1], has_item(2))
    
    def test_median(self):
        md = MedianData()
        md.put_integer(1)
        md.put_integer(2)
        assert_that(md.get_median_last_min(), equal_to(1.5))

    def test_median_with_time_constraints(self):
        md = MedianData()
        md.put_integer(1)
        sleep(50)
        md.put_integer(2)
        assert_that(md.get_median_last_min(), equal_to(1.5))
        sleep(10)
        md.put_integer(2)
        assert_that(md.get_median_last_min(), equal_to(2.0))


class MedianServiceTests(TestCase):
    """
    Median Service tests (tests request and response formats, times, etc.)
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_valid_inputs(self):
        pass

    def test_service_invalid_inputs(self):
        pass

    def test_service_bad_requests(self):
        pass