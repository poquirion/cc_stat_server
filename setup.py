from setuptools import setup

requirements = {
        "Flask": "1.0.2",
        "fabric": "2.1.3",
        "gunicorn": "19.8.1"
    }

setup(name='cc_stat_server',
      version='0.1',
      description='get info about CC',
      # url='http://github.com/',
      author='Pierre-Olivier Quirion',
      author_email='pierre-olivier.quirion@calculquebec.ca',
      license='MIT',
      packages=['cc_stat_server'],
      install_requires=["{}>={}".format(k, v) for k, v in requirements.items()],
      zip_safe=False)
