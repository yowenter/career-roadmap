from job_crawler.storage.driver import excel
from job_crawler.storage.driver import mongo

storage_drivers = type('storage_drivers', (), dict(
    excel=excel.ExcelDriver,
    mongo=mongo.MongoDriver

))


def get_storage_driver():
    from job_crawler.settings import STORAGE_DRIVER
    driver = getattr(storage_drivers, STORAGE_DRIVER, None)
    assert driver is not None, "Driver `%s` not found" % STORAGE_DRIVER

    return driver


