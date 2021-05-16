# Testing CDRs Generator

The tool to generate testing Call Detail Records files and some adds for Elasticsearch

The repository includes the following files:

1. **cdr.py** - Class for CDR entity.
2. **cdrs_file_generator.py** - Generator of cdr files making use of FakeCallDetailRecord class from cdr.py. Beeing run as a standalone script generates a file and attempts to load it into the Elasticsearch index.
3. **batch_cdrs_loader.py** - Script to load set of files from the ./cdr directory (./cdr/\*.cdr file mask is used) into the Elasticsearch index.
4. **elastic_index_creation.txt** -  DELETE & PUT script to create index for CDRs in Elasticsearch (can be run from Kibana / Dev tools). 
5. **The rest of the python files** are related to generation of testing MSISDNs (phone numbers). They can be also found in repository https://github.com/nomadrain/simple_msisdn_python along with the description. 
