from job_crawler.storage.driver import excel
from job_crawler.storage.driver import mongo
from job_crawler.settings import STORAGE_DRIVER, EXCEL_FILE_PATH

storage_drivers = type('storage_drivers', (), dict(
    excel=excel.ExcelDriver,
    mongo=mongo.MongoDriver

))


def get_storage_driver(keys):
    driver = getattr(storage_drivers, STORAGE_DRIVER, None)
    assert driver is not None, "Driver `%s` not found" % STORAGE_DRIVER
    if STORAGE_DRIVER == 'excel':
        return driver(EXCEL_FILE_PATH, 'JOBS', keys)

    return None
