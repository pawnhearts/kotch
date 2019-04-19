import pygeoip
import json
from .models import LocationSchema
from .settings import BASE_DIR

geoip_db = pygeoip.GeoIP(BASE_DIR / 'GeoLiteCity.dat')
with open('regioncodes.json') as f:
    region_names = json.load(f)


def get_location(remote_ip):
    schema = LocationSchema()
    location = geoip_db.record_by_addr(remote_ip)
    if location['country_code']:
        return {
            'country': location['country_code'],
            'region': location.get('region_code', ''),
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'country_name': location['country_name'],
            'region_name': region_names.get('{}-{}'.format(location['country_code'], location.get('region_code', ''))),
        }
