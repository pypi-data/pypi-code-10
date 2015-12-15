# -*- coding: utf-8 -*-
"""
couch-bulk-multiprocess

To upload a big amount of document to a CouchDB, it is recommended to use the
built-in bulk-upload functionality of CouchDB.
This module provides an async IO interface to store a stream of incoming
documents.
This is done by collecting the documents and push them as a bulk upload to the
database as soon as a given threshold is reached. By the use of threads these
uploads are performed in parallel und are performed while the original program
keeps on running.

Make sure to call mpcouchPusher.finish() at the end!
"""

import multiprocessing as mpt
import multiprocessing.dummy as mpd
mp = None
import couchdb
import time

class mpcouchPusher():
    """A class that collects documents and uploads them as bulk as soon as a
    certain limit has been reached.

    Methods
    -------
    __init__(db,limit,jobslimit):
        Initializes the mpcouchPusher object.

        db: must be a valid CouchDB database object

        limit: specifies the amount of documents that need to be collected
               before they are pushed to the databases collectively.
               Defaults to 30000
        
        jobslimit: The amount of processes used in parallel for uploading.
                   Defaults to 1 and should NOT be changed at this time.
        
        jobsbuffersizemax: The amount of upload-processes that will be buffered.
                           If this value is too high, the systems memory might
                           be used up completely.
                           Defaults to 10

    pushData(data):
        Stores the content of data to the databas specified at creation date.

        data: must be a valid CouchDB document in JSON format.

    finish(waitForCompletion):
        must be called after the last document has been pushed to the pushData
        function to ensure that all started processes finish and no data is
        lost.
    
    get_waitingjobscount():
        Get the count of uploading batch-jobs still in the queue. Can be used to
        pause the generation of new documents, if they are produced faster than
        the upload happens.
    """
    def __init__(self, dburl, limit = 30000, jobsbuffersizemax = 10, jobslimit = 1,threads = False):
        global mp
        if threads == False:
            mp = mpt
        else:
            mp = mpd
        self.collectedData = []
        self.dbname = "/".join(dburl.split("/")[-1:])
        self.dbhost = "/".join(dburl.split("/")[:-1])
        self.server = couchdb.Server(self.dbhost)
        # if a database with the given name does not exist, it is created
        try:
            self.db = self.server[self.dbname]
        except couchdb.ResourceNotFound:
            self.db = self.server.create(self.dbname)
        self.limit = limit
        self.totalcount = 0
        self.jobs = []
        self.threadcount = 0
        self.jobsbuffer = []
        self.jobslimit = jobslimit
        self.finished = False
        self.jobsbuffersizemax = jobsbuffersizemax
    
    def pushData(self, data):
        self.collectedData.append(data)
        self.totalcount += 1
        if len(self.collectedData) >= self.limit:
            # generate a new process and store in in the jobsbuffer
            p = mp.Process(target=self.db.update, args=(self.collectedData,))
            # if the maximum amount of buffered jobs has been generated, initiate a pause
            if len(self.jobsbuffer) >= self.jobsbuffersizemax:
                # we have to use a variable to determine the end of the waiting time which
                # is changed from outside the main code - otherwise the pause-end condition
                # will never occure. (a paused code will not update the control-variable)
                # In this case, we use the list of currently acive processes.
                while len([None for y in self.jobs if y.is_alive() is True]) > 0:
                    time.sleep(0.05)
            self.jobsbuffer.append(p)
            print("spawned process {}".format(len(self.jobs)+len(self.jobsbuffer)))
            self.collectedData = []
        self.threadcount = len([None for y in self.jobs if y.is_alive() is True]) # analysis:ignore
        if self.threadcount < self.jobslimit:
            # there is room for a new job, so take one from the jobsbuffer
            if len(self.jobsbuffer) > 0:
                newp = self.jobsbuffer.pop()
                self.jobs.append(newp)
                newp.start()
                #[self.jobs.pop(y) for y in self.jobs if y.is_alive() is False]
                self.jobs = [y for y in self.jobs if y.is_alive() is True]
                self.threadcount = len(self.jobs)
                print("processcount: {} process-queue: {}  collected so far: {}".format(self.threadcount, len(self.jobsbuffer), self.totalcount))
        return len(self.jobsbuffer)

    def finish(self, waitForCompletion = True): # waitForCompletion is for later implementation, not yet functional
        print("generate final upload process ...")
        if len(self.collectedData) > 0:
            p = mp.Process(target=self.db.update, args=(self.collectedData,))
            self.jobsbuffer.append(p)
        while len(self.jobsbuffer) > 0:
            # as long as there are still jobs in the queue, exectue them
            self.jobs = [y for y in self.jobs if y.is_alive() is True]
            self.threadcount = len(self.jobs)
            #self.threadcount = len([None for y in self.jobs if y.is_alive() is True]) # analysis:ignore
            if self.threadcount < self.jobslimit:
                newp = self.jobsbuffer.pop()
                self.jobs.append(newp)
                newp.start()
                self.threadcount = len([None for y in self.jobs if y.is_alive() is True]) # analysis:ignore
                print("processcount: {} process-queue: {}  collected so far: {}".format(self.threadcount, len(self.jobsbuffer), self.totalcount))            

        # now, the jobsqueue is empty, we have to wait for the remaining jobs to complete
        if waitForCompletion == True:
            # but only, if we were told to do so by the argument "waitForCompletion" (not yet fully implemented)
            for proc in [runningJob for runningJob in self.jobs if runningJob.is_alive() is True]:
                print("waiting for upload-process {0} to finish ...".format(proc))
                proc.join()
                del proc
                self.finished = True
        else:
            # if we should not wait for it, just update the self.finished variable
            # this makes it possible for the parent app to check, whether it is save to quit already
            while len([None for runningJob in self.jobs if runningJob.is_alive() is True]) > 0:
                self.finished = False
            self.finished = True
        for proc in self.jobs:
            del proc
        message = len(self.collectedData)
        self.collectedData = []
        return message
    
    def get_waitingjobscount(self):
        return len(self.jobsbuffer)
    
    def has_finished(self):
        return self.finished

    def destroyDatabase(self):
        self.server.delete(self.dbname)
