import requests
from requests.exceptions import HTTPError, ConnectTimeout, ConnectionError, Timeout
from library.config import Config
from library.constants import Const
from flask import jsonify
config = Config()
const = Const()
import logging

logging.basicConfig(filename='apicalls.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class EndPoints:
    """
        Investigate Using Coroutines to improve the speed of endpoints requester function
    """
    _api_base_url = config.API_ENDPOINT
    _key = config.API_KEY
    _postcode = ""

    @staticmethod
    def stats_logger(url, params, message, state):
        """
            logs actual api requests,
            :param message:
            :param url:
            :param params:
            :return:
        """
        logging.info(msg='''
        message: {} 
        url : {} 
        params : {}'''.format(message, url, params))

    @staticmethod
    def no_errors(params) -> any:
        """
            "key": self._key,
            "postcode": postcode or self._postcode,
            "internal_area": internal_area,
            "property_type": property_type,
            "construction_date": construction_date,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "finish_quality": finish_quality,
            "outdoor_space": outdoor_space,
            "off_street_parking": off_street_parking

        :param params:
        :return:
        """
        print(params)
        if not 'key' in params:
            return jsonify({'status': 'failure', 'message': 'invalid API Key or no Key '}), 401

        if 'property_type' in params:
            if not params['property_type'] in const.property_type:
                return jsonify({'status': 'failure', 'message': 'Invalid Property Type'}), 500

        if 'construction_date' in params:
            if not params['construction_date'] in const.construction_dates:
                return jsonify({'status': 'failure', 'message': 'Invalid Construction Date'}), 500

        if 'bedrooms' in params:
            if 16 < int(params['bedrooms']) > 0:
                return jsonify({'status': 'failure', 'message': 'Invalid Number of Bedrooms'}), 500

        if 'bathrooms' in params:
            if 3 < int(params['bathrooms']) > 0:
                return jsonify({'status': 'failure', 'message': 'Invalid Number of Bathrooms'}), 500

        if 'finish_quality' in params:
            if not params['finish_quality'] in const.finish_quality:
                return jsonify({'status': 'failure', 'message': 'Invalid Finish Quality'}), 500

        if 'outdoor_space' in params:
            if not params['outdoor_space'] in const.outdoor_space:
                return jsonify({'status': 'failure', 'message': 'Invalid Out Door Space'}), 500

        if 'region' in params:
            if not params['region'] in const.uk_regions:
                return jsonify({'status': 'failure', 'message': 'Invalid UK Region'}), 500

        if 'country' in params:
            if not params['country'] in const.countries_list:
                return jsonify({'status': 'failure', 'message': 'Invalid Country'}), 500

        return True

    def requester(self, url, params) -> any:
        """
            :param url: str
            :param params: dict {parameters}
            :return: json object
        """
        try:
            is_no_error = self.no_errors(params=params)

            if isinstance(is_no_error, bool):
                self.stats_logger(url=url, params=params, message='Successful', state=True)
                return requests.get(url, params=params).json(), 200
            else:
                self.stats_logger(url=url, params=params, message='Bad Argument', state=False)
            return is_no_error

        except HTTPError as e:
            self.stats_logger(url=url, params=params, message=e, state=False)
            return jsonify({'status': 'failure', 'message': 'an error occurred : {}'.format(e)}), 500
        except ConnectTimeout as e:
            self.stats_logger(url=url, params=params, message=e, state=False)
            return jsonify({'status': 'failure', 'message': 'connection taking too long : {}'.format(e)}), 500
        except ConnectionError as e:
            self.stats_logger(url=url, params=params, message=e, state=False)
            return jsonify({'status': 'failure', 'message': 'connection error : {}'.format(e)}), 500
        except Timeout as e:
            self.stats_logger(url=url, params=params, message=e, state=False)
            return jsonify({'status': 'failure', 'message': 'request has timeout : {}'.format(e)}), 500

    def valuation_sale(self, postcode, internal_area, property_type, construction_date, bedrooms,
                       bathrooms, finish_quality, outdoor_space, off_street_parking):
        """
        https://api.propertydata.co.uk/valuation-sale?key={API_KEY}&postcode=OX41YB&internal_area=828&property_type=flat&construction_date=pre_1914&bedrooms=3&bathrooms=1&finish_quality=below_average&outdoor_space=garden&off_street_parking=0

        {
          "status": "success",
          "postcode": "OX4 1YB",
          "postcode_type": "full",
          "params": {
            "property_type": "Flat",
            "construction_date": "Pre-1914",
            "internal_area": "828",
            "bedrooms": "3",
            "bathrooms": "1",
            "finish_quality": "Below average",
            "outdoor_space": "Garden",
            "off_street_parking": "0 spaces"
          },
          "result": {
            "estimate": 390000,
            "margin": 20000
          },
          "process_time": "0.40"
        }
        """

        params = {
            "key": self._key,
            "postcode": postcode or self._postcode,
            "internal_area": internal_area,
            "property_type": property_type,
            "construction_date": construction_date,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "finish_quality": finish_quality,
            "outdoor_space": outdoor_space,
            "off_street_parking": off_street_parking
        }
        _endpoint = 'valuation-sale'
        return self.requester(self._api_base_url + _endpoint, params)

    def prices(self, postcode, bedrooms=2):
        """
            example :     https://api.propertydata.co.uk/prices?key={API_KEY}&postcode=W149JH&bedrooms=2
            :return:
                    {
                      "status": "success",
                      "postcode": "W14 9JH",
                      "postcode_type": "full",
                      "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                      "bedrooms": 2,
                      "data": {
                        "points_analysed": 20,
                        "radius": "0.14",
                        "average": 602345,
                        "70pc_range": [
                          550000,
                          685000
                        ],
                        "80pc_range": [
                          535000,
                          725000
                        ],
                        "90pc_range": [
                          500000,
                          750000
                        ],
                        "100pc_range": [
                          495000,
                          799000
                        ],
                        "raw_data": []
                      },
                      "process_time": "1.03"
                    }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'bedrooms': bedrooms
        }
        _endpoint = 'prices'
        return self.requester(self._api_base_url + _endpoint, params)

    def prices_per_sqf(self, postcode):
        """
        example: https://api.propertydata.co.uk/prices-per-sqf?key={API_KEY}&postcode=W149JH
        :return:
                {
                  "status": "success",
                  "postcode": "W14 9JH",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                  "data": {
                    "points_analysed": 20,
                    "radius": "0.11",
                    "average": 862,
                    "70pc_range": [
                      744,
                      1020
                    ],
                    "80pc_range": [
                      740,
                      1043
                    ],
                    "90pc_range": [
                      739,
                      1134
                    ],
                    "100pc_range": [
                      711,
                      1288
                    ],
                    "raw_data": []
                  },
                  "process_time": "0.67"
        }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'prices-per-sqf'
        return self.requester(self._api_base_url + _endpoint, params)

    def sold_prices(self, postcode, property_type, max_age):
        """
        extra options for property types can be found on Notes.md
        example: https://api.propertydata.co.uk/sold-prices?key={API_KEY}&postcode=W149JH&type=flat&max_age=12
        :return:
                {
                  "status": "success",
                  "postcode": "W14 9JH",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                  "type": "flat",
                  "data": {
                    "points_analysed": 20,
                    "radius": "0.08",
                    "date_earliest": "2018-03-29",
                    "date_latest": "2018-12-20",
                    "average": 564300,
                    "70pc_range": [
                      475000,
                      700000
                    ],
                    "80pc_range": [
                      440000,
                      790000
                    ],
                    "90pc_range": [
                      435000,
                      910000
                    ],
                    "100pc_range": [
                      430500,
                      915000
                    ],
                    "raw_data": []
                  },
                  "process_time": "4.53"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'type': property_type,
            'max_age': max_age
        }
        _endpoint = 'sold-prices'
        return self.requester(self._api_base_url + _endpoint, params)

    def sold_prices_per_sqf(self, postcode):
        """
        example: https://api.propertydata.co.uk/sold-prices-per-sqf?key={API_KEY}&postcode=W149JH
        :return:
                {
                  "status": "success",
                  "postcode": "W14 9JH",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                  "data": {
                    "points_analysed": 20,
                    "radius": "0.17",
                    "date_earliest": "2017-12-08",
                    "date_latest": "2018-08-30",
                    "average": 860,
                    "70pc_range": [
                      717,
                      1034
                    ],
                    "80pc_range": [
                      633,
                      1068
                    ],
                    "90pc_range": [
                      470,
                      1114
                    ],
                    "100pc_range": [
                      309,
                      1165
                    ],
                    "raw_data": []
                  },
                  "process_time": "3.23"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = "sold-prices-per-sqf"
        return self.requester(self._api_base_url + _endpoint, params)

    def growth(self, postcode):
        """
        example: https://api.propertydata.co.uk/growth?key={API_KEY}&postcode=W14
        :return:
                {
                  "status": "success",
                  "postcode": "W14",
                  "postcode_type": "district",
                  "url": "https://propertydata.co.uk/draw?input=W14",
                  "data": [
                    [
                      "Aug 2013",
                      862199,
                      null
                    ],
                    [
                      "Aug 2014",
                      1039052,
                      "20.5%"
                    ],
                    [
                      "Aug 2015",
                      1069005,
                      "2.9%"
                    ],
                    [
                      "Aug 2016",
                      1077210,
                      "0.8%"
                    ],
                    [
                      "Aug 2017",
                      1123564,
                      "4.3%"
                    ],
                    [
                      "Aug 2018",
                      1109593,
                      "-1.2%"
                    ]
                  ],
                  "process_time": "0.57"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'growth'
        return self.requester(self._api_base_url + _endpoint, params)

    def postcode_key_stats(self, region):
        """
        example: https://api.propertydata.co.uk/postcode-key-stats?key={API_KEY}&region=south_east
        :return:
                {
                  "status": "success",
                  "region_used": "south_east",
                  "result_count": 336,
                  "data": [
                    {
                      "outcode": "BN1",
                      "avg_price": 395663.6,
                      "avg_price_psf": 447.5,
                      "avg_rent": 315.1,
                      "avg_yield": "4.1%",
                      "growth_1y": "3.6%",
                      "growth_3y": "6.1%",
                      "growth_5y": "17.8%",
                      "sales_per_month": 24,
                      "turnover": "1%"
                    },
                    {
                      "outcode": "BN10",
                      "avg_price": 338005.5,
                      "avg_price_psf": 312,
                      "avg_rent": null,
                      "avg_yield": null,
                      "growth_1y": "1.1%",
                      "growth_3y": "3.4%",
                      "growth_5y": "15.4%",
                      "sales_per_month": 8,
                      "turnover": "4%"
                    },
                    {
                      "outcode": "BN11",
                      "avg_price": 279408,
                      "avg_price_psf": 297,
                      "avg_rent": 187.2,
                      "avg_yield": "3.5%",
                      "growth_1y": "-0.6%",
                      "growth_3y": "2.6%",
                      "growth_5y": "14.4%",
                      "sales_per_month": 17,
                      "turnover": "2%"
                    }
                  ],
                  "process_time": "0.22"
                }
        """
        params = {
            'key': self._key,
            'region': region
        }
        _endpoint = 'postcode-key-stats'
        return self.requester(self._api_base_url + _endpoint, params)

    def sourced_properties(self, property_list, postcode, radius=20, results=60):
        """
        example: https://api.propertydata.co.uk/sourced-properties?key={API_KEY}&list=repossessed-properties&postcode=NW6+7YD&radius=20&results=60
        :return:
                {
                  "status": "success",
                  "list": {
                    "id": "repossessed-properties",
                    "name": "Repossessed properties"
                  },
                  "postcode": "NW6 7YD",
                  "radius": 20,
                  "result_count": 60,
                  "api_calls_cost": 6,
                  "properties": [
                    {
                      "id": "Z53924419",
                      "address": "Saltram Crescent, Maida Vale, London",
                      "postcode": "W9 3JX",
                      "type": "Flat",
                      "bedrooms": 1,
                      "price": 400000,
                      "sqf": 660,
                      "lat": "51.53137200",
                      "lng": "-0.20106800",
                      "distance_to": "0.82",
                      "highest_offer": null,
                      "url": "https://api.propertydata.co.uk/property/z/53924419"
                    },
                    {
                      "id": "Z53400803",
                      "address": "Melrose Avenue, London",
                      "postcode": "NW2 4JY",
                      "type": "Flat",
                      "bedrooms": 3,
                      "price": 425000,
                      "sqf": 0,
                      "lat": "51.55375300",
                      "lng": "-0.22870300",
                      "distance_to": "1.16",
                      "highest_offer": "475000",
                      "url": "https://api.propertydata.co.uk/property/z/53400803"
                    },
                    {
                      "id": "Z54367347",
                      "address": "Maida Vale, London",
                      "postcode": "W9 1RG",
                      "type": "Flat",
                      "bedrooms": 1,
                      "price": 315000,
                      "sqf": 0,
                      "lat": "51.53066600",
                      "lng": "-0.18358900",
                      "distance_to": "1.36",
                      "highest_offer": "325000",
                      "url": "https://api.propertydata.co.uk/property/z/54367347"
                    }
                  ],
                  "process_time": "0.32"
                }
        """
        params = {
            'key': self._key,
            'list': property_list,
            'postcode': postcode,
            'radius': radius,
            'results': results
        }

        _endpoint = 'sourced-properties'
        return self.requester(self._api_base_url + _endpoint, params)

    def property_info(self, property_id):
        """
        :example : https://api.propertydata.co.uk/property-info?key={API_KEY}&property_id=Z53400803

        :return:
            {
              "status": "success",
              "property": {
                "id": "Z53400803",
                "address": "Melrose Avenue, London",
                "postcode": "NW2 4JY",
                "type": "Flat",
                "bedrooms": 3,
                "price": 425000,
                "sqf": 0,
                "lat": "51.55375300",
                "lng": "-0.22870300"
              },
              "process_time": "0.03"
            }

            if property removed from market

            {
              "status": "error",
              "code": "1703",
              "message": "Property (ID: Z53403803) not found. This property may be been removed from the market.",
              "process_time": "0.04"
            }
        """
        params = {
            'key': self._key,
            'property_id': property_id
        }
        _endpoint = 'property-info'
        return self.requester(self._api_base_url + _endpoint, params)

    def development_gdv(self, postcode, flat_2, flat_1, finish_quality):
        """
        :example: https://api.propertydata.co.uk/development-gdv?key={API_KEY}&postcode=NW6+7YD&flat_2=4&flat_1=1&finish_quality=medium

        :return:
            {
              "status": "success",
              "postcode": "NW6 7YD",
              "postcode_type": "full",
              "params": {
                "flat_0": 0,
                "flat_1": "1",
                "flat_2": "4",
                "flat_3": 0,
                "flat_4": 0,
                "terraced_house_2": 0,
                "terraced_house_3": 0,
                "terraced_house_4": 0,
                "terraced_house_5": 0,
                "semi-detached_house_2": 0,
                "semi-detached_house_3": 0,
                "semi-detached_house_4": 0,
                "semi-detached_house_5": 0,
                "detached_house_2": 0,
                "detached_house_3": 0,
                "detached_house_4": 0,
                "detached_house_5": 0,
                "finish_quality": "medium"
              },
              "result": {
                "sale": {
                  "estimate": 3300000,
                  "margin": 165000
                },
                "rent": {
                  "estimate": 2125,
                  "unit": "gbp_per_week"
                }
              },
              "process_time": "1.76"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'flat_2': flat_2,
            'flat_1': flat_1,
            finish_quality: finish_quality
        }
        _endpoint = 'development-gdv'
        return self.requester(self._api_base_url + _endpoint, params)

    def valuation_rent(self, postcode, internal_area, property_type, construction_date, bedrooms, bathrooms,
                       finish_quality, outdoor_space, off_street_parking):
        """
            :example: https://api.propertydata.co.uk/valuation-rent?key={API_KEY}&postcode=OX41YB&internal_area=828&property_type=flat&construction_date=pre_1914&bedrooms=3&bathrooms=1&finish_quality=below_average&outdoor_space=garden&off_street_parking=0
            :return:
            {
              "status": "success",
              "postcode": "OX4 1YB",
              "postcode_type": "full",
              "params": {
                "property_type": "Flat",
                "construction_date": "Pre-1914",
                "internal_area": "828",
                "bedrooms": "3",
                "bathrooms": "1",
                "finish_quality": "Below average",
                "outdoor_space": "Garden",
                "off_street_parking": "0 spaces"
              },
              "result": {
                "estimate": 332,
                "unit": "gbp_per_week"
              },
              "process_time": "0.41"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'internal_area': internal_area,
            'property_type': property_type,
            'construction_date': construction_date,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'finish_quality': finish_quality,
            'outdoor_space': outdoor_space,
            'off_street_parking': off_street_parking
        }
        _endpoint = 'valuation-rent'
        return self.requester(self._api_base_url + _endpoint, params)

    def rents(self, postcode, bedrooms):
        """
        :example: https://api.propertydata.co.uk/rents?key={API_KEY}&postcode=W149JH&bedrooms=2
        :return:
                {
                  "status": "success",
                  "postcode": "W14 9JH",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                  "bedrooms": 2,
                  "data": {
                    "long_let": {
                      "points_analysed": 20,
                      "radius": "0.19",
                      "unit": "gbp_per_week",
                      "average": 438,
                      "70pc_range": [
                        385,
                        500
                      ],
                      "80pc_range": [
                        385,
                        705
                      ],
                      "90pc_range": [
                        381,
                        735
                      ],
                      "100pc_range": [
                        380,
                        804
                      ],
                      "raw_data": []
                    }
                  },
                  "process_time": "3.66"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'bedrooms': bedrooms
        }
        _endpoint = 'rents'
        return self.requester(self._api_base_url + _endpoint, params)

    def rents_hmo(self, postcode):
        """
        :example: https://api.propertydata.co.uk/rents-hmo?key={API_KEY}&postcode=W149JH
        :return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "url": "https://propertydata.co.uk/draw?input=W14+9JH",
              "data": {
                "double-ensuite": {
                  "points_analysed": 20,
                  "radius": "0.21",
                  "unit": "gbp_per_week",
                  "average": 239,
                  "70pc_range": [
                    207,
                    277
                  ],
                  "80pc_range": [
                    207,
                    312
                  ],
                  "90pc_range": [
                    207,
                    312
                  ],
                  "100pc_range": [
                    173,
                    312
                  ]
                },
                "double-shared-bath": {
                  "points_analysed": 20,
                  "radius": "0.06",
                  "unit": "gbp_per_week",
                  "average": 180,
                  "70pc_range": [
                    150,
                    219
                  ],
                  "80pc_range": [
                    138,
                    220
                  ],
                  "90pc_range": [
                    120,
                    225
                  ],
                  "100pc_range": [
                    120,
                    231
                  ]
                },
                "single-ensuite": {
                  "points_analysed": 20,
                  "radius": "1.23",
                  "unit": "gbp_per_week",
                  "average": 206,
                  "70pc_range": [
                    150,
                    250
                  ],
                  "80pc_range": [
                    150,
                    260
                  ],
                  "90pc_range": [
                    140,
                    265
                  ],
                  "100pc_range": [
                    122,
                    270
                  ]
                },
                "single-shared-bath": {
                  "points_analysed": 20,
                  "radius": "0.23",
                  "unit": "gbp_per_week",
                  "average": 158,
                  "70pc_range": [
                    130,
                    208
                  ],
                  "80pc_range": [
                    127,
                    210
                  ],
                  "90pc_range": [
                    127,
                    213
                  ],
                  "100pc_range": [
                    102,
                    254
                  ]
                }
              },
              "process_time": "0.47"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'rents-hmo'
        return self.requester(self._api_base_url + _endpoint, params)

    def yields(self, postcode, bedrooms):
        """
        :example: https://api.propertydata.co.uk/yields?key={API_KEY}&postcode=W149JH&bedrooms=2
        :return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "url": "https://propertydata.co.uk/draw?input=W14+9JH",
              "bedrooms": 2,
              "data": {
                "long_let": {
                  "points_analysed": 40,
                  "radius": "0.19",
                  "gross_yield": "3.7%"
                }
              },
              "process_time": "5.93"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'bedrooms': bedrooms
        }
        _endpoint = 'yields'
        return self.requester(self._api_base_url + _endpoint, params)

    def demand(self, postcode):
        """
        :example: https://api.propertydata.co.uk/demand?key={API_KEY}&postcode=W14
        :return:
            {
              "status": "success",
              "postcode": "W14",
              "postcode_type": "district",
              "total_for_sale": 718,
              "average_sales_per_month": 27,
              "turnover_per_month": "4%",
              "months_of_inventory": "25.0",
              "days_on_market": 761,
              "demand_rating": "Buyers market",
              "process_time": "9.78"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
        }
        _endpoint = 'demand'
        return self.requester(self._api_base_url + _endpoint, params)

    def demand_rent(self, postcode):
        """
        example: https://api.propertydata.co.uk/demand-rent?key={API_KEY}&postcode=W14
        :return:
            {
              "status": "success",
              "postcode": "W14",
              "postcode_type": "district",
              "total_for_rent": 656,
              "transactions_per_month": 138,
              "turnover_per_month": "21%",
              "months_of_inventory": "4.8",
              "days_on_market": 142,
              "rental_demand_rating": "Tenants market",
              "process_time": "4.32"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'demand-rent'
        return self.requester(self._api_base_url + _endpoint, params)

    def lha_rate(self, postcode, bedrooms):
        """
            example: https://api.propertydata.co.uk/lha-rate?key={API_KEY}&postcode=W14+9JH&bedrooms=2
        :return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "data": {
                "brma": "Inner West London BRMA",
                "rate": "339.45",
                "rate_unit": "gbp_per_week",
                "month": "July",
                "year": "2020"
              },
              "process_time": "3.29"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'bedrooms': bedrooms
        }
        _endpoint = 'lha-rate'
        return self.requester(self._api_base_url + _endpoint, params)

    def agents(self, postcode):
        """
         example: https://api.propertydata.co.uk/agents?key={API_KEY}&postcode=W14
        :return:
                {
                  "status": "success",
                  "postcode": "W14",
                  "postcode_type": "district",
                  "data": {
                    "Zoopla": {
                      "sale": [
                        {
                          "rank": 1,
                          "agent": "JLL",
                          "branches": [
                            "Kensington",
                            "New Homes"
                          ],
                          "units_offered": 30,
                          "total_value": 67960000,
                          "average_value": 1799688
                        },
                        {
                          "rank": 2,
                          "agent": "Machards",
                          "branches": [
                            "Machards"
                          ],
                          "units_offered": 13,
                          "total_value": 47350000,
                          "average_value": 2621429
                        },
                        {
                          "rank": 3,
                          "agent": "Knight Frank",
                          "branches": [
                            "Kensington",
                            "Fulham"
                          ],
                          "units_offered": 14,
                          "total_value": 44635000,
                          "average_value": 1516875
                        },
                        {
                          "rank": 4,
                          "agent": "Marsh & Parsons",
                          "branches": [
                            "Brook Green",
                            "Kensington",
                            "Holland Park",
                            "Fulham"
                          ],
                          "units_offered": 41,
                          "total_value": 43919950,
                          "average_value": 820712
                        },
                        {
                          "rank": 5,
                          "agent": "Dexters",
                          "branches": [
                            "Shepherds Bush",
                            "West Kensington",
                            "Westbourne Grove",
                            "Notting Hill"
                          ],
                          "units_offered": 56,
                          "total_value": 42004799,
                          "average_value": 660354
                        },
                        {
                          "rank": 6,
                          "agent": "Winston Crowns",
                          "branches": [
                            "Winston Crowns"
                          ],
                          "units_offered": 17,
                          "total_value": 39144950,
                          "average_value": 1784444
                        }
                      ],
                      "rent": [
                        {
                          "rank": 1,
                          "agent": "Machards",
                          "branches": [
                            "Machards"
                          ],
                          "units_offered": 15,
                          "total_value": 25540,
                          "average_value": 949,
                          "unit": "gbp_per_week"
                        },
                        {
                          "rank": 2,
                          "agent": "Latymers",
                          "branches": [
                            "Latymers"
                          ],
                          "units_offered": 6,
                          "total_value": 16695,
                          "average_value": 934,
                          "unit": "gbp_per_week"
                        },
                        {
                          "rank": 3,
                          "agent": "Dexters",
                          "branches": [
                            "Shepherds Bush",
                            "West Kensington",
                            "Westbourne Grove",
                            "Notting Hill"
                          ],
                          "units_offered": 33,
                          "total_value": 16580,
                          "average_value": 419,
                          "unit": "gbp_per_week"
                        },
                        {
                          "rank": 4,
                          "agent": "John D Wood & Co.",
                          "branches": [
                            "Fulham Broadway Sales",
                            "Kensington Sales",
                            "Chiswick Lettings",
                            "Notting Hill Lettings"
                          ],
                          "units_offered": 5,
                          "total_value": 15954,
                          "average_value": 1009,
                          "unit": "gbp_per_week"
                        },
                        {
                          "rank": 5,
                          "agent": "JLL",
                          "branches": [
                            "Kensington",
                            "New Homes"
                          ],
                          "units_offered": 16,
                          "total_value": 14624,
                          "average_value": 887,
                          "unit": "gbp_per_week"
                        },
                        {
                          "rank": 6,
                          "agent": "Marsh & Parsons",
                          "branches": [
                            "Brook Green",
                            "Kensington",
                            "Holland Park",
                            "Fulham"
                          ],
                          "units_offered": 18,
                          "total_value": 13757,
                          "average_value": 643,
                          "unit": "gbp_per_week"
                        }
                      ]
                    },
                    "OnTheMarket": {
                      "sale": [],
                      "rent": []
                    }
                  },
                  "process_time": "2.65"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'agents'
        return self.requester(self._api_base_url + _endpoint, params)

    def crime(self, postcode):
        """
            example: https://api.propertydata.co.uk/crime?key={API_KEY}&postcode=W14+9JH
        return:
            {
              "status": "success",
              "radius": "0.10",
              "population": 3529,
              "crimes_last_12m": 261,
              "crimes_per_thousand": 74,
              "crime_rating": "Low crime",
              "types": {
                "Anti-social behaviour": 67,
                "Burglary": 41,
                "Violence and sexual offences": 34,
                "Vehicle crime": 33,
                "Other theft": 25,
                "Bicycle theft": 14,
                "Criminal damage and arson": 13,
                "Public order": 12,
                "Shoplifting": 8,
                "Drugs": 7,
                "Robbery": 5,
                "Theft from the person": 2
              },
              "observations": [
                "Incidence of Bicycle theft is above national average",
                "Incidence of Shoplifting is below national average",
                "Incidence of Theft from the person is below national average"
              ],
              "process_time": "0.06"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'crime'
        return self.requester(self._api_base_url + _endpoint, params)

    def demographics(self, postcode):
        """
            example: https://api.propertydata.co.uk/demographics?key={API_KEY}&postcode=W149JH
        return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "radius": 0,
              "url": "https://propertydata.co.uk/draw?input=W14+9JH",
              "data": {
                "deprivation": 22,
                "health": 62,
                "social_grade": {
                  "ab": "39.8",
                  "c1": "34.6",
                  "c2": "9.1",
                  "de": "16.4"
                },
                "age": {
                  "0-4": "4.75",
                  "5-9": "3.27",
                  "10-14": "3.06",
                  "15-19": "3.91",
                  "20-24": "11.91",
                  "25-29": "17.89",
                  "30-34": "15.26",
                  "35-39": "9.37",
                  "40-44": "7.14",
                  "45-49": "5.59",
                  "50-54": "4.06",
                  "55-59": "3.65",
                  "60-64": "3.28",
                  "65-69": "2.27",
                  "70-74": "1.95",
                  "75-79": "1.42",
                  "80-84": "0.78",
                  "85-89": "0.43"
                },
                "politics": {
                  "results": {
                    "Labour": "64%",
                    "Conservative": "28%",
                    "Liberal Democrats": "5%",
                    "Green Party": "2%"
                  },
                  "constituences": [
                    "Hammersmith"
                  ]
                },
                "proportion_with_degree": 58,
                "vehicles_per_household": "0.4",
                "commute_method": {
                  "at_home": "5.1",
                  "underground_light_rail": "51.7",
                  "train": "4.0",
                  "bus": "8.6",
                  "taxi": "0.2",
                  "motorcycle": "1.5",
                  "car_driver": "8.9",
                  "car_passenger": "0.5",
                  "bicycle": "6.0",
                  "foot": "12.7",
                  "other": "0.7"
                }
              },
              "process_time": "0.04"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'demographics'
        return self.requester(self._api_base_url + _endpoint, params)

    def schools(self, postcode):
        """
            example: https://api.propertydata.co.uk/schools?key={API_KEY}&postcode=W21TR
        return:
            {
              "status": "success",
              "postcode": "W2 1TR",
              "postcode_type": "full",
              "url": "https://propertydata.co.uk/draw?input=W2+1TR",
              "data": {
                "state": {
                  "average_score": "1.55",
                  "rating": "Good schools",
                  "nearest": [
                    {
                      "name": "St James & St John Church of England Primary School",
                      "local_authority": "Westminster",
                      "postcode": "W2 3QD",
                      "type": "Voluntary Aided School",
                      "phase": "Primary",
                      "sixth_form": "Does not have a sixth form",
                      "rating": "Good",
                      "num_pupils": 176,
                      "deprivation": 4,
                      "inspection_start": "2012-03-22",
                      "inspection_end": "2012-03-23",
                      "inspection_pub": "2012-04-23",
                      "url": "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/101132",
                      "distance": "0.22"
                    },
                    {
                      "name": "Hampden Gurney CofE Primary School",
                      "local_authority": "Westminster",
                      "postcode": "W1H 5HA",
                      "type": "Voluntary Aided School",
                      "phase": "Primary",
                      "sixth_form": "Does not have a sixth form",
                      "rating": "Outstanding",
                      "num_pupils": 234,
                      "deprivation": 4,
                      "inspection_start": "2009-05-08",
                      "inspection_end": "2009-05-08",
                      "inspection_pub": "2009-06-04",
                      "url": "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/101123",
                      "distance": "0.49"
                    },
                    {
                      "name": "Hallfield Primary School",
                      "local_authority": "Westminster",
                      "postcode": "W2 6JJ",
                      "type": "Community School",
                      "phase": "Primary",
                      "sixth_form": "Does not have a sixth form",
                      "rating": "Good",
                      "num_pupils": 455,
                      "deprivation": 4,
                      "inspection_start": "2013-10-23",
                      "inspection_end": "2013-10-24",
                      "inspection_pub": "2013-11-18",
                      "url": "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/101116",
                      "distance": "0.50"
                    },
                    {
                      "name": "Ark King Solomon Academy",
                      "local_authority": "Westminster",
                      "postcode": "NW1 6RU",
                      "type": "Academy Sponsor Led",
                      "phase": "Secondary",
                      "sixth_form": "Has a sixth form",
                      "rating": "Outstanding",
                      "num_pupils": 912,
                      "deprivation": 5,
                      "inspection_start": "2013-05-14",
                      "inspection_end": "2013-05-15",
                      "inspection_pub": "2013-06-05",
                      "url": "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/135242",
                      "distance": "0.50"
                    },
                    {
                      "name": "Christ Church Bentinck CofE Primary School",
                      "local_authority": "Westminster",
                      "postcode": "NW1 5NS",
                      "type": "Voluntary Aided School",
                      "phase": "Primary",
                      "sixth_form": "Does not have a sixth form",
                      "rating": "Outstanding",
                      "num_pupils": 202,
                      "deprivation": 5,
                      "inspection_start": "2019-02-26",
                      "inspection_end": "2019-02-27",
                      "inspection_pub": "2019-04-23",
                      "url": "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/provider/ELS/101147",
                      "distance": "0.59"
                    }
                  ]
                },
                "independent": {
                  "nearest": [
                    {
                      "url": "http://isi.net/school/abercorn-school-6180?results=true",
                      "name": "Abercorn School",
                      "lat": "51.52126000",
                      "lng": "-0.16404270",
                      "postcode": "NW1 6JF",
                      "type": "Day",
                      "ages": "2 - 13",
                      "gender": "Co-ed",
                      "telephone": "020 7723 8700",
                      "website": "http://www.abercornschool.com"
                    },
                    {
                      "url": "http://isi.net/school/abingdon-house-school-7492?results=true",
                      "name": "Abingdon House School",
                      "lat": "51.52394000",
                      "lng": "-0.16634270",
                      "postcode": "NW1 6LG",
                      "type": "Day",
                      "ages": "5 - 13",
                      "gender": "Co-ed",
                      "telephone": "0845 2300426",
                      "website": "http://www.abingdonhouseschool.co.uk"
                    },
                    {
                      "url": "http://isi.net/school/arnold-house-school-6202?results=true",
                      "name": "Arnold House School",
                      "lat": "51.53417000",
                      "lng": "-0.17703360",
                      "postcode": "NW8 0LH",
                      "type": "Day",
                      "ages": "5 - 13",
                      "gender": "Boys",
                      "telephone": "020 72664840",
                      "website": "http://www.arnoldhouse.co.uk"
                    },
                    {
                      "url": "http://isi.net/school/eaton-square-school--kensington-8228?results=true",
                      "name": "Eaton Square School, Kensington",
                      "lat": "51.49758000",
                      "lng": "-0.18078440",
                      "postcode": "SW7 5NL",
                      "type": "Day",
                      "ages": "2 - 11",
                      "gender": "Co-ed",
                      "telephone": "020 7225 3131",
                      "website": "http://www.hydeparkschool.co.uk"
                    },
                    {
                      "url": "http://isi.net/school/francis-holland-school--regents-park-6465?results=true",
                      "name": "Francis Holland School, Regents Park",
                      "lat": "51.52467000",
                      "lng": "-0.16031630",
                      "postcode": "NW1 6XR",
                      "type": "Day",
                      "ages": "11 - 19",
                      "gender": "Girls",
                      "telephone": "020 77230176",
                      "website": "http://www.fhs-nw1.org.uk"
                    }
                  ]
                }
              },
              "process_time": "0.75"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'schools'
        return self.requester(self._api_base_url + _endpoint, params)

    def restaurants(self, postcode):
        """
            example: https://api.propertydata.co.uk/restaurants?key={API_KEY}&postcode=OX73EX
        return:
            {
              "status": "success",
              "postcode": "OX7 3EX",
              "postcode_type": "full",
              "url": "https://propertydata.co.uk/draw?input=OX7+3EX",
              "data": {
                "average_hygiene": "4.88",
                "proportion_bad": 0,
                "rating": "Very good restaurant hygiene",
                "nearby": [
                  {
                    "name": "Five Ways Tandoori",
                    "address": "Fiveways, Sturt Road, Charlbury",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": 5,
                    "rating_date": "2017-09-13",
                    "lat": "51.86695500",
                    "lng": "-1.47839700",
                    "distance": "0.70"
                  },
                  {
                    "name": "Fiveways Stores",
                    "address": "Five Ways Stores, Sturt Road, Charlbury",
                    "type": "Retailers - supermarkets/hypermarkets",
                    "hygiene": 5,
                    "rating_date": "2016-02-16",
                    "lat": "51.86884700",
                    "lng": "-1.47730000",
                    "distance": "0.70"
                  },
                  {
                    "name": "Charlbury Bowls Club",
                    "address": "74 Ticknell Piece Road, Charlbury, Chipping Norton",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": null,
                    "rating_date": "2017-11-08",
                    "lat": "51.87409400",
                    "lng": "-1.47458100",
                    "distance": "0.82"
                  },
                  {
                    "name": "Charlbury County Primary School",
                    "address": "Charlbury Primary School, Crawborough, Charlbury",
                    "type": "School/college/university",
                    "hygiene": 5,
                    "rating_date": "2017-04-25",
                    "lat": "51.87330200",
                    "lng": "-1.47843900",
                    "distance": "0.90"
                  },
                  {
                    "name": "The Bull Inn",
                    "address": "Sheep Street, Charlbury, Chipping Norton",
                    "type": "Pub/bar/nightclub",
                    "hygiene": 5,
                    "rating_date": "2018-02-14",
                    "lat": "51.87232700",
                    "lng": "-1.48144300",
                    "distance": "0.96"
                  },
                  {
                    "name": "The Curiosities Company Ltd",
                    "address": "39 Sheep Street, Charlbury, Chipping Norton",
                    "type": "Manufacturers/packers",
                    "hygiene": 5,
                    "rating_date": "2018-09-25",
                    "lat": "51.87232700",
                    "lng": "-1.48144300",
                    "distance": "0.96"
                  },
                  {
                    "name": "Ye Olde Three Horseshoes",
                    "address": "Sheep Street, Charlbury, Chipping Norton",
                    "type": "Pub/bar/nightclub",
                    "hygiene": 5,
                    "rating_date": "2017-12-05",
                    "lat": "51.87232700",
                    "lng": "-1.48144300",
                    "distance": "0.96"
                  },
                  {
                    "name": "Little Monkeys Charlbury",
                    "address": "Chapmans, Church Street, Charlbury",
                    "type": "Hospitals/Childcare/Caring Premises",
                    "hygiene": 5,
                    "rating_date": "2018-02-14",
                    "lat": "51.87226000",
                    "lng": "-1.48275100",
                    "distance": "1.01"
                  },
                  {
                    "name": "Bell Inn",
                    "address": "Bell Hotel, Church Street, Charlbury",
                    "type": "Hotel/bed & breakfast/guest house",
                    "hygiene": 4,
                    "rating_date": "2017-02-06",
                    "lat": "51.87226100",
                    "lng": "-1.48275100",
                    "distance": "1.01"
                  },
                  {
                    "name": "Charlbury Day Centre",
                    "address": "Memorial Hall, Browns Lane, Charlbury",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": 5,
                    "rating_date": "2017-08-16",
                    "lat": "51.87335400",
                    "lng": "-1.48194000",
                    "distance": "1.02"
                  },
                  {
                    "name": "Charlbury Baby & Toddler Group",
                    "address": "Memorial Hall, Browns Lane, Charlbury",
                    "type": "Hospitals/Childcare/Caring Premises",
                    "hygiene": null,
                    "rating_date": "2018-10-03",
                    "lat": "51.87335400",
                    "lng": "-1.48194000",
                    "distance": "1.02"
                  },
                  {
                    "name": "Charlbury Pre School",
                    "address": "Charlbury Playgroup, Park Street, Charlbury",
                    "type": "Hospitals/Childcare/Caring Premises",
                    "hygiene": 5,
                    "rating_date": "2016-11-21",
                    "lat": "51.87131300",
                    "lng": "-1.48385100",
                    "distance": "1.02"
                  },
                  {
                    "name": "Rose & Crown",
                    "address": "Market Street, Charlbury, Chipping Norton",
                    "type": "Pub/bar/nightclub",
                    "hygiene": 5,
                    "rating_date": "2016-11-22",
                    "lat": "51.87291700",
                    "lng": "-1.48288800",
                    "distance": "1.04"
                  },
                  {
                    "name": "Charlbury Deli And Cafe Ltd",
                    "address": "The Old Bank House, Market Street, Charlbury",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": 4,
                    "rating_date": "2017-08-25",
                    "lat": "51.87291718",
                    "lng": "-1.48288906",
                    "distance": "1.04"
                  },
                  {
                    "name": "Co-op Pharmacy",
                    "address": "The Pharmacy, Market Street, Charlbury",
                    "type": "Retailers - other",
                    "hygiene": null,
                    "rating_date": "2018-08-14",
                    "lat": "51.87291800",
                    "lng": "-1.48288900",
                    "distance": "1.04"
                  },
                  {
                    "name": "Co-op",
                    "address": "Spendlove Centre, Enstone Road, Charlbury",
                    "type": "Retailers - supermarkets/hypermarkets",
                    "hygiene": 5,
                    "rating_date": "2017-05-08",
                    "lat": "51.87425400",
                    "lng": "-1.48217600",
                    "distance": "1.06"
                  },
                  {
                    "name": "Charlbury Community Centre Cafe",
                    "address": "Charlbury Community Centre, Enstone Road, Charlbury",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": 5,
                    "rating_date": "2018-09-25",
                    "lat": "51.87425613",
                    "lng": "-1.48217595",
                    "distance": "1.06"
                  },
                  {
                    "name": "Font Cafe",
                    "address": "St Marys Church, Church Street, Charlbury",
                    "type": "Restaurant/Cafe/Canteen",
                    "hygiene": 5,
                    "rating_date": "2017-11-08",
                    "lat": "51.87273000",
                    "lng": "-1.48527300",
                    "distance": "1.12"
                  },
                  {
                    "name": "Cotswold View Caravan & Camping Park- The Old Shed",
                    "address": "Banbury Hill Farm, Enstone Road, Charlbury",
                    "type": "Retailers - other",
                    "hygiene": 5,
                    "rating_date": "2018-01-17",
                    "lat": "51.88604000",
                    "lng": "-1.47176900",
                    "distance": "1.51"
                  },
                  {
                    "name": "Bridewell Organic Gardens",
                    "address": "Wilcote Manor, Wilcote, Chipping Norton",
                    "type": "Manufacturers/packers",
                    "hygiene": null,
                    "rating_date": "2017-08-24",
                    "lat": "51.83637400",
                    "lng": "-1.46201600",
                    "distance": "1.97"
                  }
                ]
              },
              "process_time": "3.30"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'restaurants'
        return self.requester(self._api_base_url + _endpoint, params)

    def politics(self, postcode):
        """
            example: https://api.propertydata.co.uk/politics?key={API_KEY}&postcode=W14+9JH

        :return:
                {
                  "status": "success",
                  "postcode": "W14 9JH",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/draw?input=W14+9JH",
                  "data": {
                    "constituency": "Hammersmith",
                    "constituency_code": "E14000726",
                    "last_result": {
                      "event_name": "General Election 2019",
                      "vote_counts": {
                        "Labour": 30074,
                        "Conservative": 12227,
                        "Liberal Democrat": 6947,
                        "Green": 1744,
                        "Brexit Party": 974
                      }
                    }
                  },
                  "process_time": "1.04"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'politics'
        return self.requester(self._api_base_url + _endpoint, params)

    def planning(self, postcode, decision_rating, category, max_age_decision, results):
        """
            example: https://api.propertydata.co.uk/planning?key={API_KEY}&postcode=NW6+7YD&decision_rating=positive&category=EXTENSION&max_age_decision=120&results=20
        return:
            {
              "status": "success",
              "postcode": "NW6 7YD",
              "postcode_type": "full",
              "url": "https://propertydata.co.uk/plot-map?input=NW6+7YD",
              "result_count": 20,
              "api_calls_cost": 2,
              "data": {
                "planning_applications": [
                  {
                    "url": "https://pa.brent.gov.uk/online-applications/applicationDetails.do?keyVal=DCAPR_149804&activeTab=summary",
                    "address": "27 Winchester Avenue, Kilburn, London, NW6 7TT",
                    "agent": {
                      "name": "Mr Eric Haendler",
                      "company": "EH Architects Ltd",
                      "address": "69 Harlesden Gardens, London, NW10 4HB"
                    },
                    "authority": "Brent Council",
                    "ward": "Queens Park",
                    "case_officer": "Kim Pang",
                    "reference": "20/1291",
                    "category": "EXTENSION",
                    "proposal": "Certificate of lawfulness for proposed erection of single storey outbuilding to rear of dwellinghouse.",
                    "type": "Certificate of Lawfulness - Proposed",
                    "est_construction_cost": "£0 - 100k",
                    "status": "Decided",
                    "decision": {
                      "text": "Certificate of Lawfulness - Granted",
                      "rating": "positive"
                    },
                    "appeal": {
                      "status": null,
                      "decision": "Not Available"
                    },
                    "dates": {
                      "received_at": "2020-04-29",
                      "validated_at": "2020-04-29",
                      "decided_at": "2020-06-23"
                    },
                    "lat": "51.54118450",
                    "lng": "-0.20853790",
                    "distance": "0.07"
                  },
                  {
                    "url": "https://pa.brent.gov.uk/online-applications/applicationDetails.do?keyVal=DCAPR_147687&activeTab=summary",
                    "address": "17 The Avenue, London, NW6 7NR",
                    "agent": {
                      "name": "Ms Georgina Turvey",
                      "company": "Peek Architecture Ltd",
                      "address": "12-13 Poland Street, Noland House, Second Floor, London, W1F 8QB"
                    },
                    "authority": "Brent Council",
                    "ward": "Brondesbury Park",
                    "case_officer": "Lena Summers",
                    "reference": "19/3918",
                    "category": "EXTENSION",
                    "proposal": "Erection of a single storey side and rear extension, first floor side extension, replacement of rear first floor window with juliet balcony, and conversion of garage into a habitable room with replacement of garage door with window to dwellinghouse",
                    "type": "Householder",
                    "est_construction_cost": "£0 - 100k",
                    "status": "Decided",
                    "decision": {
                      "text": "Permission Granted",
                      "rating": "positive"
                    },
                    "appeal": {
                      "status": null,
                      "decision": "Not Available"
                    },
                    "dates": {
                      "received_at": "2019-11-05",
                      "validated_at": "2019-11-21",
                      "decided_at": "2020-01-16"
                    },
                    "lat": "51.54137250",
                    "lng": "-0.21127550",
                    "distance": "0.08"
                  }
                ]
              },
              "process_time": "1.78"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'decision_rating': decision_rating,
            'category': category,
            'max_age_decision': max_age_decision,
            'results': results
        }
        _endpoint = 'planning'
        return self.requester(self._api_base_url + _endpoint, params)

    def freehold_titles(self, postcode):
        """
        example: https://api.propertydata.co.uk/freehold-titles?key={API_KEY}&postcode=NW6+7YD
        return:
                {
                  "status": "success",
                  "postcode": "NW6 7YD",
                  "postcode_type": "full",
                  "url": "https://propertydata.co.uk/plot-map?input=NW6+7YD",
                  "data": [
                    {
                      "title_number": "MX368346",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35684657,
                          "lat": "51.54197406",
                          "lng": "-0.20952620",
                          "distance": "0.00",
                          "num_points": 10,
                          "leaseholds": 6
                        }
                      ]
                    },
                    {
                      "title_number": "MX362534",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35680208,
                          "lat": "51.54178347",
                          "lng": "-0.20966039",
                          "distance": "0.01",
                          "num_points": 11,
                          "leaseholds": 6
                        }
                      ]
                    },
                    {
                      "title_number": "MX363949",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35683280,
                          "lat": "51.54188056",
                          "lng": "-0.20961567",
                          "distance": "0.01",
                          "num_points": 11,
                          "leaseholds": 5
                        }
                      ]
                    },
                    {
                      "title_number": "MX363328",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35686352,
                          "lat": "51.54203440",
                          "lng": "-0.20936230",
                          "distance": "0.01",
                          "num_points": 11,
                          "leaseholds": 0
                        }
                      ]
                    },
                    {
                      "title_number": "NGL691299",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35687544,
                          "lat": "51.54213453",
                          "lng": "-0.20925572",
                          "distance": "0.02",
                          "num_points": 11,
                          "leaseholds": 4
                        }
                      ]
                    },
                    {
                      "title_number": "MX362821",
                      "class": "Absolute freehold title",
                      "num_polygons": 1,
                      "polygons": [
                        {
                          "id": 35678864,
                          "lat": "51.54173375",
                          "lng": "-0.20981798",
                          "distance": "0.02",
                          "num_points": 9,
                          "leaseholds": 0
                        }
                      ]
                    }
                  ],
                  "process_time": "1.35"
                }
        """
        _endpoint = 'freehold-titles'
        params = {
            'key': self._key,
            'postcode': postcode
        }
        return self.requester(self._api_base_url + _endpoint, params)

    def title_info(self, title):
        """
        example: https://api.propertydata.co.uk/title-info?key={API_KEY}&title=LN149464
        return:
            {
              "status": "success",
              "title_number": "LN149464",
              "data": {
                "address": "36\nCharleville Road\nFulham",
                "class": "Absolute freehold title",
                "estate_interest": "Estate in land",
                "ownership": {
                  "type": "Corporate",
                  "details": {
                    "owner": "36 CHARLEVILLE ROAD LIMITED",
                    "company_reg": "1999402",
                    "owner_type": "Limited Company or Public Limited Company",
                    "owner_address": "36 Charleville Road, London W14 9JH",
                    "date_added": "27-11-1986",
                    "country": "UK"
                  }
                },
                "polygons": 1,
                "approx_centre": {
                  "lat": "51.48889170",
                  "lng": "-0.20779772"
                },
                "plot_size": "0.03",
                "leaseholds": [
                  "NGL483215",
                  "NGL457050",
                  "BGL147669",
                  "BGL147671",
                  "NGL420884"
                ]
              },
              "process_time": "0.56"
            }
        """
        _endpoint = 'title-info'
        params = {
            'key': self._key,
            'title': title
        }
        return self.requester(self._api_base_url + _endpoint, params)

    def stamp_duty(self, value, country, additional):
        """
            example: https://api.propertydata.co.uk/stamp-duty?key={API_KEY}&value=250000&country=scotland&additional=1
        return:
            {
              "status": "success",
              "country_used": "scotland",
              "sdlt_payable": 9600,
              "additional_rate_used": true,
              "first_time_buyer": false,
              "process_time": "0.03"
            }
        """
        _endpoint = 'stamp-duty'
        params = {
            'key': self._key,
            'value': value,
            'country': country,
            'additional': additional
        }
        return self.requester(self._api_base_url + _endpoint, params)

    def area_type(self, postcode):
        """
            example: https://api.propertydata.co.uk/area-type?key={API_KEY}&postcode=OX44+9LW
        return:
                {
                  "status": "success",
                  "postcode": "OX44 9LW",
                  "postcode_type": "full",
                  "area_type": "Rural hamlet and isolated dwellings",
                  "process_time": "0.03"
                }
        """
        _endpoint = 'area-type'

        params = {
            'key': self._key,
            'postcode': postcode
        }
        return self.requester(self._api_base_url + _endpoint, params)

    def green_belt(self, postcode):
        """
            description: For a full UK postcode, returns whether the property is within the green belt (and if applicable the green belt name).

            example: https://api.propertydata.co.uk/green-belt?key={API_KEY}&postcode=OX44+9LW

        return:
            {
              "status": "success",
              "postcode": "OX44 9LW",
              "postcode_type": "full",
              "green_belt": true,
              "green_belt_name": "Oxford Greenbelt",
              "process_time": "2.75"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'green-belt'
        return self.requester(self._api_base_url + _endpoint, params)

    def national_park(self, postcode):
        """
            description: For a full UK postcode, returns whether the property is within a national park (and if applicable the national park name).
            example: https://api.propertydata.co.uk/national-park?key={API_KEY}&postcode=EX35+6EQ

        return:
                {
                  "status": "success",
                  "postcode": "EX35 6EQ",
                  "postcode_type": "full",
                  "national_park": true,
                  "national_park_name": "Exmoor National Park",
                  "process_time": "1.02"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'national-park'
        return self.requester(self._api_base_url + _endpoint, params)

    def aonb(self, postcode):
        """
            description: For a full UK postcode, returns whether the property is within an Area of Outstanding National Beauty (AONB) (and if applicable the AONB name).
            example: https://api.propertydata.co.uk/aonb?key={API_KEY}&postcode=OX7+3EX
        return:
                {
                  "status": "success",
                  "postcode": "OX7 3EX",
                  "postcode_type": "full",
                  "aonb": true,
                  "aonb_name": "Cotswolds AONB",
                  "process_time": "1.87"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'aonb'
        return self.requester(self._api_base_url + _endpoint, params)

    def flood_risk(self, postcode):
        """
            description: For a full postcode in England, returns the risk of flooding from rivers and sea. Possible flood risk values are
            example: https://api.propertydata.co.uk/flood-risk?key={API_KEY}&postcode=OX7+3EX

        return:
                {
                  "status": "success",
                  "postcode": "OX10 7JP",
                  "postcode_type": "full",
                  "flood_risk": "Low",
                  "process_time": "0.03"
                }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'flood-risk'
        return self.requester(self._api_base_url + _endpoint, params)

    def internet_speed(self, postcode):
        """
            description: For a full postcode UK postcode, returns analytics on the internet speeds available.
            example: https://api.propertydata.co.uk/internet-speed?key={API_KEY}&postcode=DY3+2QG

        :return:
            {
              "status": "success",
              "postcode": "DY3 2QG",
              "postcode_type": "full",
              "internet": {
                "SFBB_availability": "0.0",
                "UFBB_availability": "100.0",
                "FTPP_availability": "0.0",
                "premises_unable_10mpbs": "0.0",
                "premises_unable_30mbps": "0.0",
                "premises_below_uso": "0.0"
              },
              "process_time": "0.03"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'internet-speed'
        return self.requester(self._api_base_url + _endpoint, params)

    def build_cost(self, postcode, property_type, internal_area, finish_quality):
        """
            description : For a full UK postcode, building type, internal area (in square feet) and finish quality returns the estimated building cost (both total and per square foot
            example: https://api.propertydata.co.uk/build-cost?key={API_KEY}&postcode=CF158RU&type=house&internal_area=2500&finish_quality=medium

        return:
            {
              "status": "success",
              "postcode": "CF15 8RU",
              "postcode_type": "full",
              "type": "house",
              "internal_area": "2500",
              "finish_quality": "medium",
              "data": {
                "total_cost": 320000,
                "cost_per_sqf": 128
              },
              "process_time": "0.03"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'property_type': property_type,
            'internal_area': internal_area,
            'finish_quality': finish_quality
        }
        _endpoint = 'internet-speed'
        return self.requester(self._api_base_url + _endpoint, params)

    def ptal(self, postcode):
        """
            description: For a full UK postcode within Greater London, returns the PTAL score. Possible values for the 'ptal' field from worst to best are: 01a1b23456a6b
            example: https://api.propertydata.co.uk/ptal?key={API_KEY}&postcode=W14+9JH

        return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "ptal": "4",
              "process_time": "0.05"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'ptal'
        return self.requester(self._api_base_url + _endpoint, params)

    def council_tax(self, postcode):
        """
            description: For a full UK postcode, returns analytics on average council tax by property band in the council area, plus a rating on how well this council is performing on keeping tax low. Additionally returns known individual property council tax bands for the area.
            example: https://api.propertydata.co.uk/council-tax?key={API_KEY}&postcode=W14+9JH

        return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "council": "Hammersmith & Fulham",
              "council_rating": "Low tax",
              "year": "2020/21",
              "annual_change": "+3.99%",
              "council_tax": {
                "band_a": "528.28",
                "band_b": "616.33",
                "band_c": "704.37",
                "band_d": "792.42",
                "band_e": "968.51",
                "band_f": "1,144.61",
                "band_g": "1,320.70",
                "band_h": "1,584.84"
              },
              "note": "These figures include adult social care and the Greater London Authority precept (if applicable) but exclude any parish precepts.",
              "properties": [
                {
                  "address": "MAIS 1ST 2ND & 3RD FLRS AT 3, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "E"
                },
                {
                  "address": "MAIS BST & GND FLR AT 46, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "F"
                },
                {
                  "address": "FLAT 3 AT 48, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "C"
                },
                {
                  "address": "FLAT 2A AT 48, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "A"
                },
                {
                  "address": "FLAT 2 AT 48, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "C"
                },
                {
                  "address": "FLAT 1 AT 48, CHARLEVILLE ROAD, LONDON, W14 9JH",
                  "band": "C"
                }
              ],
              "process_time": "0.44"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'council-tax'
        return self.requester(self._api_base_url + _endpoint, params)

    def floor_areas(self, postcode):
        """
            description:
            example: https://api.propertydata.co.uk/floor-areas?key={API_KEY}&postcode=W14+9JH
        return:
            {
              "status": "success",
              "postcode": "W14 9JH",
              "postcode_type": "full",
              "known_floor_areas": [
                {
                  "inspection_date": "2016-08-31",
                  "address": "Third Floor Flat, 32 Charleville Road",
                  "square_feet": 603
                },
                {
                  "inspection_date": "2016-04-13",
                  "address": "Flat B8, 32 Charleville Road",
                  "square_feet": 258
                },
                {
                  "inspection_date": "2016-03-22",
                  "address": "First Floor Flat, 46 Charleville Road",
                  "square_feet": 603
                },
                {
                  "inspection_date": "2016-02-02",
                  "address": "18b Charleville Road",
                  "square_feet": 258
                },
                {
                  "inspection_date": "2015-12-15",
                  "address": "Flat 1, 48 Charleville Road",
                  "square_feet": 215
                }
              ],
              "process_time": "0.03"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode
        }
        _endpoint = 'floor-areas'
        return self.requester(self._api_base_url + _endpoint, params)

    def listed_buildings(self, postcode, grade, listed_after):
        """
            description: For a given full English postcode, returns up to 10 of the closest listed buildings which match the supplied filters.
            example: https://api.propertydata.co.uk/listed-buildings?key={API_KEY}&postcode=NW6+7YD&grade=II*&listed_after=1975

        return:
        {
              "status": "success",
              "postcode": "NW6 7YD",
              "postcode_type": "full",
              "data": {
                "listed_buildings": {
                  "0": {
                    "name": "MECCA BINGO",
                    "grade": "II*",
                    "list_date": "1980/10/10",
                    "lat": "51.54135000",
                    "lng": "-0.19828000",
                    "url": "https://historicengland.org.uk/listing/the-list/list-entry/1078889",
                    "distance": "0.49"
                  },
                  "1": {
                    "name": "TRELLICK TOWER CHELTENHAM ESTATE",
                    "grade": "II*",
                    "list_date": "1998/12/22",
                    "lat": "51.52366000",
                    "lng": "-0.20539000",
                    "url": "https://historicengland.org.uk/listing/the-list/list-entry/1246688",
                    "distance": "1.28"
                  },
                  "2": {
                    "name": "KENSAL HOUSE",
                    "grade": "II*",
                    "list_date": "1981/03/19",
                    "lat": "51.52499000",
                    "lng": "-0.21524000",
                    "url": "https://historicengland.org.uk/listing/the-list/list-entry/1225244",
                    "distance": "1.20"
                  }
                }
              },
              "process_time": "0.54"
            }
        """
        params = {
            'key': self._key,
            'postcode': postcode,
            'grade': grade,
            'listed_after': listed_after
        }
        _endpoint = 'listed-buildings'
        return self.requester(self._api_base_url + _endpoint, params)
