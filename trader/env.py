# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999


import os

env_local = 'local'
env_gcp = 'gcp'


def env():
    if os.environ.get('IS_LOCAL') == 'true':
        return env_local
    return env_gcp


def is_local():
    return env() == env_local


def is_gcp():
    return env() == env_gcp
