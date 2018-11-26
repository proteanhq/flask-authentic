"""
Default settings. Override these with settings in the module pointed to
by the PROTEAN_CONFIG environment variable.
"""
 ####################
# CORE             #
####################

DEBUG = False

# A secret key for this particular Protean installation. Used in secret-key
# hashing algorithms.
SECRET_KEY = 'abcdefghijklmn'

# Flag indicates that we are testing
TESTING = True

# Define the repositories
REPOSITORIES = {
    'default': {
        'PROVIDER': 'protean.impl.repository.dict_repo'
    }
}

# Set account schema and provider
ACCOUNT_SCHEMA = 'tests.support.sample_app.schemas.AccountSchema'
ACCOUNT_SERIALIZER = 'tests.support.sample_app.serializers.AccountSerializer'
