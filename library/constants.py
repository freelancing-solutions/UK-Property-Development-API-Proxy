import os


class Const:
    property_type = ['flat', 'detached_house', 'terrace_house', 'semi_detached_house']
    construction_dates = ['pre_1914', '1914_2000', '2000_onwards']
    finish_quality = ['very_high', 'high', 'average', 'below_average', 'unmodernised']
    outdoor_space = ['none', 'balcony_terrace', 'garden', 'garden_very_large']
    accepted_property_types = ['flat', 'terraced_house', 'semi_detached_house']
    countries_list = ['england', 'scotland', 'wales', 'northern_ireland']
    uk_regions = ['north_east', 'north_west', 'east_midlands', 'west_midlands', 'east_of_england', 'greater_london',
                  'south_east', 'south_west', 'wales', 'scotland', 'northern_ireland']
    property_lists = [
        'repossessed-properties', 'unmodernised-properties', 'cash-buyers-only-properties', 'auction-properties',
        'quick-sale-properties', 'land-plots-for-sale', 'new-build-properties', 'hmo-licenced-properties',
        'reduced-properties', 'investment-portfolios', 'back-on-market', 'slow-to-sell-properties', 'short-lease-properties',
        'georgian-houses', 'holiday-let-properties', 'properties-in-growth-zones', 'high-yield-properties',
        'tenanted-properties-for-sale', 'properties-with-good-views', 'properties-with-no-chain', 'properties-with-planning-granted',
        'properties-near-a-university', 'properties-with-an-annexe', 'large-properties', 'properties-on-a-corner-plot',
        'bungalows-for-sale']