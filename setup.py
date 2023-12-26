import os

from setuptools import setup

env_dict = {}


def get_requirements() -> list[str]:
    with open(os.path.join(os.getcwd(), 'requirements.txt'), 'r') as req_file:
        requirements_list = ''.join([_ for _ in req_file.readlines()]).split('\n')
        return requirements_list


def env_variables() -> None:
    with open(os.path.join(os.getcwd(), 'config.env'), 'r') as env_file:
        global env_dict
        env_list = ''.join([_ for _ in env_file.readlines()]).split('\n')
        print(env_list)
        env_dict = {i.split('=')[0]: i.split('=')[1] for i in env_list}


if __name__ == '__main__':
    env_variables()
    print(env_dict)
    print(get_requirements())
    setup(
        name=env_dict.get('MODULE_NAME'),
        version=env_dict.get('VERSION'),

        url=env_dict.get('GITHUB_URL'),
        description='time auxiliary module',

        py_modules=env_dict.get('PY_MODULES').split(',') if env_dict.get('PY_MODULES') else [],
        install_requires=get_requirements(),
    )
