from google.cloud import ndb
from flask import jsonify


class AdminView:
    """
        i can use adminView to control how to access the database easily
    """

    client = ndb.Client()

    def update_property_types(self, property_selections):
        print(property_selections)
        selected_properties = []
        for key, value in enumerate(property_selections):
            if property_selections[value]:
                selected_properties.append(value)
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()
            default_api.set_property_types(property_types=selected_properties)
            default_api.put()
        return jsonify({'status': 'success', 'message': "property types successfully updated"}), 200

    def fetch_all_admin_defaults(self):

        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()
            return {'status': 'success', 'payload': default_api.to_dict(),
                    'message': 'successfully fetched default api values'}

    def fetch_property_types(self):
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()

            return {'status': 'success', 'payload': default_api.get_property_types(),
                    'message': 'successfully fetched property types'}


class DefaultAPIQueries(ndb.Model):
    property_types = ndb.StringProperty(default="flat,detached_house,terraced_house,semi_detached_house")
    construction_dates = ndb.StringProperty(default="pre_1914,1914_2000,2000_onwards")
    finish_quality = ndb.StringProperty(default="very_high,high,average,below_average,unmodernised")
    outdoor_space = ndb.StringProperty(default="none,balcony_terrace,garden,garden_very_large")
    countries_list = ndb.StringProperty(default="england,scotland,wales,northern_ireland")
    uk_regions = ndb.StringProperty(default="north_east,north_west,east_midlands,west_midlands,east_of_england," +
                                            "greater_london,south_east,south_west,wales,scotland,northern_ireland")

    def get_property_types(self) -> list:
        return self.property_types.split(",")

    def set_property_types(self, property_types):
        if not isinstance(property_types, list):
            raise TypeError('Invalid property type argument')

        self.property_types = ",".join(property_types)

    def get_construction_dates(self):
        return self.construction_dates.split(",")

    def set_construction_dates(self, construction_dates):
        if not isinstance(construction_dates, list):
            raise TypeError("Invalid construction_dates argument")
        self.construction_dates = ",".join(construction_dates)

    def get_finish_quality(self):
        return self.finish_quality.split(",")

    def set_finish_quality(self, finish_quality):
        if not isinstance(finish_quality, list):
            raise TypeError("Invalid finish_quality argument")
        self.finish_quality = ",".join(finish_quality)

    def get_outdoor_space(self):
        return self.outdoor_space.split(",")

    def set_outdoor_space(self, outdoor_space):
        if not isinstance(outdoor_space, list):
            raise TypeError("Invalid outdoor_space argument")
        self.outdoor_space = ",".join(outdoor_space)

    def get_countries_list(self):
        return self.countries_list.split(",")

    def set_countries_list(self, countries_list):
        if not isinstance(countries_list, list):
            raise TypeError("Invalid countries_list argument")

        self.countries_list = ",".join(countries_list)

    def get_uk_regions(self):
        return self.uk_regions.split(",")

    def set_uk_regions(self, uk_regions):
        if not isinstance(uk_regions, list):
            raise TypeError("Invalid uk_regions argument")
        self.uk_regions = ",".join(uk_regions)

