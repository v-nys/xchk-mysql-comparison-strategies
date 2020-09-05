# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xchk_mysql_comparison_strategies']

package_data = \
{'': ['*'],
 'xchk_mysql_comparison_strategies': ['static/xchk_mysql_comparison_strategies/images/*', 'templates/xchk_mysql_comparison_strategies/*']}

install_requires = \
[]

setup_kwargs = {
    'name': 'xchk_mysql_comparison_strategies',
    'version': '0.0.1',
    'description': 'Checks and strategies for comparing MySQL databases',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincentnys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
