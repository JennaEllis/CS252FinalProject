import os


def init_env():
    # flask secret key
    os.environ['SECRET_KEY'] = 'b2e4d39074fb44dc4a3dd80cb054b34e9b38352bc29f6fd4adba96552281b2f5'

    # database urls
    os.environ['DATABASE_DEV_URL'] = 'postgresql://localhost:5432/lab6'
    os.environ['DATABASE_TEST_URL'] = 'postgresql://localhost:5432/lab6_test'

    # security hashes
    os.environ['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    os.environ['SECURITY_PASSWORD_SALT'] = 'b48a8f1418bd81b0a760820b5f25a637d1fcd2a06e5d9a18f51d16d' \
        + '6bfa3584877f4f7c7294bb60b18a80622d12f6155b3969e29c0e6f8694deef0936da1e239'

    # other additions...
