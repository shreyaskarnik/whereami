# -*- coding: utf-8 -*-
import reverse_geocoder as rg


def geocode(results):
    pretty_results = []
    for result in rg.search([tuple(res) for res in results]):
        geo = {
            "country": result['cc'],
            "city": result['name'],
            "region": result['admin1'],
            "lat": result['lat'],
            "lon": result['lon']
        }
        pretty_results.append(geo)
    return pretty_results
