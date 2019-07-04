# Import libraries
import sys
import json
import os
import shutil
from datetime import datetime
from datetime import timedelta
from datetime import date
import logging
import Check_Common


# CHANGED
if not os.path.isfile(Check_Common.ConfigFileLocation):
    print("Config File: {} not found.".format(
        Check_Common.ConfigFileLocation))
    sys.exit(1)

# Import config file & parameters
# CHANGED
with open(Check_Common.ConfigFileLocation, 'rt') as ConfigFile:
    ConfigData = json.load(ConfigFile)

Files = ConfigData['FilesToArchive']
FileDir = ConfigData['FileDir']
ArchiveDir = ConfigData['ArchiveDir']
LogDoc = ConfigData['LogDoc']
TrackerDoc = ConfigData['TrackerDoc']
ArchiveDays = int(ConfigData['ArchiveDays'])

# Setup Logger
logging_format = '%(asctime)s - %(message)s'
logging.basicConfig(filename=LogDoc, level=logging.DEBUG,
                    format=logging_format)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logging.info('***')
logging.info('***')
logging.info('***')
logging.info('*** Started Archiving Application')

# Check for dependencies
logger.info('Searching for FileDir')
if os.path.exists(FileDir):
    logger.info('Found FileDir')
else:
    logger.info(
        'Did not find FileDir. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
    sys.exit()

logger.info('Searching for ArchiveDir')
if os.path.exists(ArchiveDir):
    logger.info('Found ArchiveDir')
else:
    logger.info(
        'Did not find ArchiveDir. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
    sys.exit()

logger.info('Searching for TrackerDoc')
if os.path.isfile(TrackerDoc):
    logger.info('Found TrackerDoc')
else:
    # Try creating it
    # CHANGED
    logger.info("{} was not found. Trying to create it.".format(TrackerDoc))
    with open(TrackerDoc, 'w+t') as tfp:
        tfp.write("[]")

    if os.path.isfile(TrackerDoc):
        logger.info('TrackerDoc created successfully')
    else:
        logger.info(
            'Did not find TrackerDoc. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
        sys.exit()

logger.info('Searching for LogDoc')
if os.path.isfile(LogDoc):
    logger.info('Found LogDoc')
else:
    logger.info(
        'Did not find LogDoc. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
    sys.exit()

# Search and archive files
os.chdir(FileDir)
for i in Files:
    logger.info('Searching for file: ' + i)
    if os.path.exists(i):
        logger.info('Found file: ' + i)
        FileName, FileExt = os.path.splitext(i)
        TimeNow = str(datetime.now().strftime("%Y%m%d%H%M%S"))
        TimeToday = date.today()
        TimeDelayDate = TimeToday + timedelta(days=ArchiveDays)
        FileNameNew = FileName + TimeNow

        try:
            # CHANGED
            shutil.move(os.path.join(FileDir, i),
                        ArchiveDir + FileNameNew + FileExt)
        except Exception as e:
            logger.info('File: ' + i + ' could not be archived.')
            print(e)
        else:
            logger.info('Archived file: ' + i)

            NewListEntry = {'FileName': FileNameNew + FileExt,
                            'ArchiveDate': str(TimeToday), 'ExpiryDate': str(TimeDelayDate)}

            with open(TrackerDoc, 'rt') as ReadFile:
                # CHANGED
                ListEntries = json.loads(ReadFile.read())
                ListEntries.append(NewListEntry)
                with open(TrackerDoc, 'w+t') as WriteFile:
                    WriteFile.write(json.dumps(ListEntries, indent=2))
    else:
        logger.info('Did not find file: ' + i)
        continue
