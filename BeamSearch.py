import pandas as pd
from TSPRoute import TSPRoute
import math
import time


def get_dist(
        point_one_latitude: float,
        point_one_longitude: float,
        point_two_latitude: float,
        point_two_longitude: float
) -> float:
    radius_earth_m = 6371000.0
    value_asin = math.sqrt(pow(math.sin((point_two_latitude - point_one_latitude) / 2), 2) +
                           math.cos(point_one_latitude) * math.cos(point_two_latitude) * pow(
        math.sin((point_two_longitude - point_one_longitude) / 2), 2))
    return 2 * radius_earth_m * math.asin(value_asin)


def gifts_not_already_taken(
        cur_route: TSPRoute,
        gifts_predicted: pd.DataFrame,
        available_gifts: pd.DataFrame
) -> pd.DataFrame:
    gifts_not_already_taken_2 = available_gifts.loc[~available_gifts["GiftId"].isin(gifts_predicted["GiftId"])]
    return gifts_not_already_taken_2.loc[
        ~gifts_not_already_taken_2["GiftId"].isin(cur_route.get_all_gifts_assigned()["GiftId"])
    ]


def dist_to_last(serie: pd.Series, all_data: pd.DataFrame):
    index = serie.name
    cur_lat = serie['Latitude']
    cur_lon = serie['Longitude']
    if index == 0:
        lat_last = 90.0
        lon_last = 0.0
    else:
        lat_last = all_data.loc[index - 1]['Latitude']
        lon_last = all_data.loc[index - 1]['Longitude']
    return get_dist(lat_last, lon_last, cur_lat, cur_lon)


def get_measure(cur_route: TSPRoute, gifts_to_add: pd.DataFrame) -> float:
    df_route = cur_route.get_all_gifts_assigned()
    df_routes_together = [df_route, gifts_to_add]
    df = pd.concat(df_routes_together)
    weight_sleigh = 10.0

    df = df.append({'GiftId': None, 'Latitude': 90.0, 'Longitude': 0.0, 'Weight': weight_sleigh}, ignore_index=True)
    df['weight_tot'] = df.loc[::-1, 'Weight'].cumsum()[::-1]
    df['dist_to_last'] = df.apply(lambda a: dist_to_last(a, df), axis=1)
    df['dist_mult_weight'] = df.apply(lambda a: a['weight_tot'] * a['dist_to_last'], axis=1)
    return df['dist_mult_weight'].sum()


class BeamSearch:

    def __init__(self, width: int):
        # self.lookahead = lookahead
        self.width = width

    def make_beam_search(self, cur_route: TSPRoute, init_available_gifts: pd.DataFrame):
        while cur_route.is_sleight_full() == False and init_available_gifts.shape[0] > 0:
            available_gifts = init_available_gifts
            best_sample = self.__get_random_sample(available_gifts)
            available_gifts.where(available_gifts['GiftId'] != best_sample['GiftId'], inplace=True)
            available_gifts.dropna(inplace=True)
            best_measure = get_measure(cur_route, pd.DataFrame(best_sample))
            iteration = self.width - 1
            if available_gifts.shape[0] < iteration:
                iteration = available_gifts.shape[0]
            for i_width in range(iteration):
                random_sample = self.__get_random_sample(available_gifts)
                measure = get_measure(cur_route, pd.DataFrame(random_sample))
                available_gifts.where(available_gifts['GiftId'] != random_sample['GiftId'], inplace=True)
                available_gifts.dropna(inplace=True)
                if measure < best_measure:
                    best_measure = measure
                    best_sample = random_sample
            cur_route.add_gift_to_current_route(best_sample)
            init_available_gifts.where(init_available_gifts['GiftId'] != best_sample['GiftId'], inplace=True)
            init_available_gifts.dropna(inplace=True)
            init_available_gifts.where(
                init_available_gifts['Weight'] <= cur_route.get_free_weight_cargo(),
                inplace=True
            )
            init_available_gifts.dropna(inplace=True)
        return cur_route

    def __get_random_sample(self, dataframe: pd.DataFrame) -> pd.Series:
        sample = dataframe.sample(ignore_index=True)
        return sample.loc[0]
