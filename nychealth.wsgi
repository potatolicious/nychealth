activate_this = '/var/www/nychealth/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/nychealth')

from nychealth import app as application
