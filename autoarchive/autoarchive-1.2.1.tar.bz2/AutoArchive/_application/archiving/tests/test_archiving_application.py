# test_archiving_application.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2015 Róbert Čerňanský



""":class:`TestArchivingApplication`."""



__all__ = ["TestArchivingApplication"]



# {{{ INCLUDES

import unittest

from mock import Mock

from AutoArchive._infrastructure.py_additions import event
from AutoArchive._infrastructure.configuration import Options
from AutoArchive._services.archiver import ArchiverFeatures
from AutoArchive._ui.cmdline._cmdline_ui import CmdlineUi
from .. import ArchivingApplication, ArchiveSpecInfo
from AutoArchive.tests import ComponentTestUtils
from AutoArchive._infrastructure.configuration.tests import ConfigurationTestUtils
from AutoArchive._services.archiver.tests import ArchiverTestUtils
from .archiving_test_utils import ArchivingTestUtils

# }}} INCLUDES



# {{{ CLASSES

class TestArchivingApplication(unittest.TestCase):
    """Test of :meth:`.ArchivingApplication` class."""

    @classmethod
    def setUpClass(cls):
        ArchivingTestUtils._setUpClassArchivingComponent()



    @classmethod
    def tearDownClass(cls):
        ArchivingTestUtils._tearDownClassArchivingComponent()



    def setUp(self):
        ArchivingTestUtils._setUpArchivingComponent()
        self.__archiverMock = ArchiverTestUtils.createArchiverMock()
        self.__componentUiMock = Mock(spec_set = CmdlineUi)
        self.__archivingApplication = None

        self.__componentUiMock.messageShown = self.__messageShownEventMock
        options = {Options.ARCHIVE_SPECS_DIR: ComponentTestUtils.getComponentTestContext().archiveSpecsDir}
        configurationMock = ConfigurationTestUtils.createConfigurationMock(options)
        applicationContextMock = ArchivingTestUtils._setUpApplicationContextMock(configurationMock = configurationMock)
        serviceAccessorMock = ArchivingTestUtils._setUpServiceAccessorMock()
        ArchivingTestUtils._setUpArchiverServices(serviceAccessorMock, self.__archiverMock,
                                                  supportedFeatures = frozenset({ArchiverFeatures.Incremental}))

        self.__archivingApplication = ArchivingApplication(self.__componentUiMock, applicationContextMock,
                                                           serviceAccessorMock)



    def tearDown(self):
        ArchivingTestUtils._tearDownArchivingComponent()



    def test_createAction(self):
        """Tests the create action.

        Sets up two archive specification files and passes them to tested method.  Checks that service method for
        backup creation was called two times."""

        selectedArchiveSpecs = (ArchiveSpecInfo("any name 1", ArchivingTestUtils._makeArchiveSpecFile()),
                                ArchiveSpecInfo("any name 2", ArchivingTestUtils._makeArchiveSpecFile()))

        self.__archivingApplication.executeCreateAction(selectedArchiveSpecs)

        self.assertEqual(len(selectedArchiveSpecs), self.__archiverMock.backupFiles.call_count)



    def test_listAction(self):
        """Tests the list action.

        Sets up two archive specification files and passes them to tested method.  Checks that UI method for showing
        lines was called two times."""

        selectedArchiveSpecs = (ArchiveSpecInfo("any name 1", ArchivingTestUtils._makeArchiveSpecFile()),
                                ArchiveSpecInfo("any name 2", ArchivingTestUtils._makeArchiveSpecFile()))

        self.__archiverMock.getStoredBackupIds.return_value = ()
        self.__archiverMock.getMaxBackupLevel.return_value = 3 # any int

        self.__archivingApplication.executeListAction(selectedArchiveSpecs)

        self.assertEqual(len(selectedArchiveSpecs), self.__componentUiMock.presentMultiFieldLine.call_count)



    def test_purgeAction(self):
        """Tests the purge action.

        Sets up two archive info classes that represents non existing archives and passes them to tested method.
        Checks that service method for purging stored backup data was called for each archive and each service
        provider."""

        selectedArchiveSpecs = (ArchiveSpecInfo("test ID 1", ""),
                                ArchiveSpecInfo("test ID 2", ""))

        self.__archiverMock.getStoredBackupIds.return_value = (selectedArchiveSpecs[0].name, selectedArchiveSpecs[1].name)

        self.__archivingApplication.executePurgeAction(selectedArchiveSpecs)

        # check that purge was called on the service; for each selected archive ID twice because it is executed by
        # each service provider
        self.assertEqual(len(selectedArchiveSpecs) * 2, self.__archiverMock.purgeStoredBackupData.call_count)



    @event
    def __messageShownEventMock(messageKind):
        pass

# }}} CLASSES
