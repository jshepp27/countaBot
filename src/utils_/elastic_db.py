import logging
import os
from tqdm import tqdm

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, parallel_bulk
from tqdm.auto import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#logger.info(" Establishing Elasticsearch Database ... ")

class ElasticDB(object):

    def __init__(self, elastic_port=None):
        """
        Args:
            :param elastic_port: Port for Elasticsearch instance
            :param elastic_index: Index name
            :param elastic_fields: Search fields
        """
        # Connect
        logger.info('Connecting to %s ' % elastic_port)

        self.es = Elasticsearch(elastic_port, retry_on_timeout=True)
        self.elastic_port = elastic_port
        logger.info('Connected to %s ' % self.es)

    def add_index(self, index):
        self.es.indices.create(index=index)
        logger.info('Connected to %s ' % index)

    def set_index(self, index):
        self.es.index = index
        logger.info('Set Index to to %s ' % self.es.index)

    def add_doc(self, doc):
        """ Add doc to DB """
        response = self.es.index(
            index = self.elastic_index,
            document = doc,
        )

        logger.info('Added document id %s' % response["_id"])

    def bulk_add(self, files, index_name, generator, source, iterator, chunk_size, len_):
        
        errors_before_interrupt = 5
        successes = 0
        errors_count = 0

        with tqdm(total=(len(files)), position=0, leave=True):
            for ok, result in parallel_bulk(self.es, iterator(files=files, idx=index_name, generator=generator, source=source), chunk_size=chunk_size, request_timeout=60*3):
                if ok is not True:
                    logger.error('Failed to import data')
                    logger.error(str(result))
                    errors_count += 1

                if errors_count == errors_before_interrupt:
                    logging.fatal('Too many import errors, exiting with error code')
                    exit(1)

                successes += ok

    def search(self, query_, k=5):
        results = self.es.search(
            index = "*",
            query = {
                "match": {
                    "document.text": query_,
                    },
            },
            size=k)

        hits = results["hits"]["hits"]

        return hits

    # Elasticsearch Controls
    def __enter__(self):
        return self

    def __close__(self):
        self.es = None



