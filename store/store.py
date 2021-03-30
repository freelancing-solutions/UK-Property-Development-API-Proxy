from google.cloud import ndb
from flask import jsonify
from library.utils import timestamp
from cachetools import cached, TTLCache
from library.config import Config


class AdminView:
    """
        i can use adminView to control how to access the database easily
    """
    cache_ttl = 43200
    client = ndb.Client(namespace="main", project=Config().PROJECT)
    mem_cache = TTLCache(maxsize=2048, ttl=cache_ttl)

    def __init__(self, config):
        self.cache_ttl = config.CACHE_TTL
        self.mem_cache = TTLCache(maxsize=config.CACHE_SIZE, ttl=config.CACHE_TTL)

    def get_cache(self, key: str) -> any:
        """
        :param key:
        :return:
        """
        try:
            return self.mem_cache.pop(key)
        except KeyError as e:
            pass

        with self.client.context():
            cache_values = StoreCache().query(StoreCache.cache_key == key).fetch()
            if len(cache_values) > 0:
                cache = cache_values[0]
                now = timestamp()
                if now - cache.last_accessed > self.cache_ttl:
                    return None
                return cache.response
            return None

    def set_cache(self, key: str, response: dict) -> bool:
        try:
            self.mem_cache[key] = response
        except Exception as e:
            pass

        with self.client.context():
            cache_values = StoreCache().query(StoreCache.cache_key == key).fetch()
            if len(cache_values) > 0:
                cache = cache_values[0]
            else:
                cache = StoreCache()
            cache.cache_key = key
            cache.response = response
            cache.last_accessed = timestamp()
            cache.put()
            return True

    def is_shutdown(self) -> bool:
        with self.client.context():
            api_settings_list = SettingsAPI.query().fetch()
            if len(api_settings_list) > 0:
                api_settings = api_settings_list[0]
            else:
                api_settings = SettingsAPI()

            return api_settings.user_shutdown

    def update_property_types(self, property_selections: list) -> tuple:
        selected_properties = []
        for _, value in enumerate(property_selections):
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

    def update_dates_selected(self, dates_selected: list) -> tuple:
        selected_properties = []
        for _, value in enumerate(dates_selected):
            if dates_selected[value]:
                selected_properties.append(value)
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()
            default_api.set_construction_dates(construction_dates=selected_properties)
            default_api.put()
        return jsonify({'status': 'success', 'message': "construction dates successfully updated"}), 200

    def update_finish_quality(self, finish_quality: list) -> tuple:
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()
            default_api.set_finish_quality(finish_quality=[finish_quality[value]
                                                           for _, value in enumerate(finish_quality)])
            default_api.put()
            return jsonify({'status': 'success', 'message': "finish quality successfully updated"}), 200

    def fetch_all_admin_defaults(self) -> dict:

        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()
            return {'status': 'success', 'payload': default_api.to_dict(),
                    'message': 'successfully fetched default api values'}

    def fetch_property_types(self) -> dict:
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()

            return jsonify({'status': 'success', 'payload': default_api.get_property_types(),
                            'message': 'successfully fetched property types'})

    def fetch_finishing_quality(self) -> dict:
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()

            return jsonify({'status': 'success', 'payload': default_api.get_finish_quality(),
                            'message': 'successfully fetched property types'})

    def get_construction_dates(self) -> dict:
        with self.client.context():
            defaults_list = DefaultAPIQueries.query().fetch()
            if len(defaults_list) > 0:
                default_api = defaults_list[0]
            else:
                default_api = DefaultAPIQueries()

            return jsonify({'status': 'success', 'payload': default_api.get_construction_dates(),
                            'message': 'successfully fetched construction dates'})

    def set_shutdown_status(self, status: bool) -> dict:
        with self.client.context():
            settings_list = SettingsAPI.query().fetch()
            if len(settings_list) > 0:
                default_settings = settings_list[0]
            else:
                default_settings = SettingsAPI()

            default_settings.set_shutdown_status(status=status)
            default_settings.put()
            if status:
                message = 'API is Shutting down ...'
            else:
                message = 'API is Restarting ....'
            return jsonify({'status': 'success', 'payload': default_settings.to_dict(),
                            'message': message})

    def get_settings(self) -> dict:
        with self.client.context():
            settings_list = SettingsAPI.query().fetch()
            if len(settings_list) > 0:
                default_settings = settings_list[0]
            else:
                default_settings = SettingsAPI()

            return jsonify({'status': 'success', 'payload': default_settings.to_dict(),
                            'message': 'Successfully fetched api settings'})

    def add_successful_request(self) -> bool:
        with self.client.context():
            settings_list = SettingsAPI.query().fetch()
            if len(settings_list) > 0:
                default_settings = settings_list[0]
            else:
                default_settings = SettingsAPI()

            default_settings.add_successful_request()
            default_settings.put()
            return True

    def add_failed_request(self) -> bool:
        with self.client.context():
            settings_list = SettingsAPI.query().fetch()
            if len(settings_list) > 0:
                default_settings = settings_list[0]
            else:
                default_settings = SettingsAPI()

            default_settings.add_error_request()
            default_settings.put()
            return True

    def add_cached_request(self) -> bool:
        with self.client.context():
            settings_list = SettingsAPI.query().fetch()
            if len(settings_list) > 0:
                default_settings = settings_list[0]
            else:
                default_settings = SettingsAPI()

            default_settings.add_cached_request()
            default_settings.put()
            return True


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

    def set_property_types(self, property_types: list) -> None:
        if not isinstance(property_types, list):
            raise TypeError('Invalid property type argument')

        self.property_types = ",".join(property_types)

    def get_construction_dates(self) -> list:
        return self.construction_dates.split(",")

    def set_construction_dates(self, construction_dates: list) -> None:
        if not isinstance(construction_dates, list):
            raise TypeError("Invalid construction_dates argument")
        self.construction_dates = ",".join(construction_dates)

    def get_finish_quality(self) -> list:
        return self.finish_quality.split(",")

    def set_finish_quality(self, finish_quality: list) -> None:
        if not isinstance(finish_quality, list):
            raise TypeError("Invalid finish_quality argument")
        self.finish_quality = ",".join(finish_quality)

    def get_outdoor_space(self) -> list:
        return self.outdoor_space.split(",")

    def set_outdoor_space(self, outdoor_space: list) -> None:
        if not isinstance(outdoor_space, list):
            raise TypeError("Invalid outdoor_space argument")
        self.outdoor_space = ",".join(outdoor_space)

    def get_countries_list(self) -> list:
        return self.countries_list.split(",")

    def set_countries_list(self, countries_list: list) -> None:
        if not isinstance(countries_list, list):
            raise TypeError("Invalid countries_list argument")

        self.countries_list = ",".join(countries_list)

    def get_uk_regions(self) -> list:
        return self.uk_regions.split(",")

    def set_uk_regions(self, uk_regions: list) -> None:
        if not isinstance(uk_regions, list):
            raise TypeError("Invalid uk_regions argument")
        self.uk_regions = ",".join(uk_regions)


class SettingsAPI(ndb.Model):
    user_shutdown = ndb.BooleanProperty(default=False)
    api_status = ndb.BooleanProperty(default=True)
    api_health = ndb.BooleanProperty(default=True)
    total_requests = ndb.IntegerProperty(default=257)
    cached_requests = ndb.IntegerProperty(default=12)
    failed_requests = ndb.IntegerProperty(default=0)

    def set_shutdown_status(self, status: bool) -> None:
        if not isinstance(status, bool):
            raise TypeError('Invalid argument for API Shutdown')
        self.user_shutdown = status
        if status is True:
            self.api_status = False
        else:
            self.api_status = True

    def add_successful_request(self) -> int:
        self.total_requests += 1
        return self.total_requests

    def add_error_request(self) -> int:
        self.failed_requests += 1
        return self.total_requests

    def add_cached_request(self) -> int:
        self.cached_requests += 1
        return self.cached_requests


class StoreCache(ndb.Model):
    cache_key = ndb.StringProperty()
    response = ndb.PickleProperty()
    last_accessed = ndb.IntegerProperty()


admin_view = AdminView(config=Config())
