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

if not os.path.isfile(Check_Common.ConfigFileLocation):
    print("Config File: {} not found.".format(
        Check_Common.ConfigFileLocation))
    sys.exit(1)

# Import config file & parameters
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

# CHANGED
logger.addHandler(logging.StreamHandler())

logging.info('***')
logging.info('***')
logging.info('***')
logging.info('*** Started Archived File Removal Application')

# Check for dependencies
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

# List Archived Files
# CHANGED
ArchivedFiles = []
with open(TrackerDoc, 'rt') as TrackerFile:
    ArchivedFiles = json.loads(TrackerFile.read())

# Check if Archived Files have expired
TimeToday = datetime.now()
KeepArchived = []
DeleteArchived = []
for i in ArchivedFiles:
    ExpY, ExpM, ExpD = i['ExpiryDate'].split('-')
    ExpDate = datetime.strptime(ExpY + ExpM + ExpD, '%Y%m%d')
    if ExpDate <= TimeToday:
        DeleteArchived.append(i)
    else:
        KeepArchived.append(i)
        continue

# Delete Files
for j in DeleteArchived:
    FileNameToDelete = j['FileName']
    logger.info('Searching for file: ' + FileNameToDelete)
    # CHANGED
    if os.path.isfile(os.path.join(ArchiveDir, FileNameToDelete)):
        os.remove(os.path.join(ArchiveDir, FileNameToDelete))
        logger.info('Deleted file: ' + FileNameToDelete)
    else:
        logger.info('File: ' + FileNameToDelete + ' could not be deleted')
        continue

# Update TrackerDoc
# CHANGED
with open(TrackerDoc, 'w+') as WriteFile:
    WriteFile.write(json.dumps(KeepArchived, indent=2))
