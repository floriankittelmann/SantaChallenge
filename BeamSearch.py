import pandas as pd
from TSPRoute import TSPRoute
import math


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


def get_measure(cur_route: TSPRoute, gifts_to_add: pd.DataFrame) -> float:
    start_end_latitude = 90.0
    start_end_longitude = 0.0
    last_latitude = start_end_latitude
    last_longitude = start_end_longitude
    df_route = cur_route.get_all_gifts_assigned()
    df_routes_together = [df_route, gifts_to_add]
    df = pd.concat(df_routes_together)
    measure = 0.0
    gifts_already_iterated = pd.DataFrame()
    weight_sleigh = 10
    for index, gift in df.iterrows():
        lat = gift['Latitude']
        lon = gift['Longitude']
        weight_gifts = 0
        if gifts_already_iterated.shape[0] != 0:
            gifts_in_sleigh = df.loc[~df["GiftId"].isin(gifts_already_iterated['GiftId'])]
            weight_gifts = gifts_in_sleigh['Weight'].sum()
        measure = measure + get_dist(last_latitude, last_longitude, lat, lon) * (
                weight_gifts + weight_sleigh)
        last_latitude = lat
        last_longitude = lon
        gifts_already_iterated.append(gift)
    return measure + get_dist(
        last_latitude,
        last_longitude,
        start_end_latitude,
        start_end_longitude
    ) * weight_sleigh


class BeamSearch:

    def __init__(self, width: int):
        # self.lookahead = lookahead
        self.width = width

    def make_beam_search(self, cur_route: TSPRoute, init_available_gifts: pd.DataFrame):
        while not cur_route.is_sleight_full():
            init_available_gifts = init_available_gifts.where(
                init_available_gifts['Weight'] <= cur_route.get_free_weight_cargo())
            init_available_gifts = init_available_gifts.dropna()
            if init_available_gifts.shape[0] == 0:
                break

            available_gifts = init_available_gifts
            best_sample = self.__get_random_sample(available_gifts)
            available_gifts = available_gifts.where(available_gifts['GiftId'] != best_sample['GiftId'])
            available_gifts = available_gifts.dropna()
            best_measure = get_measure(cur_route, pd.DataFrame(best_sample))
            iteration = self.width - 1
            if available_gifts.shape[0] < iteration:
                iteration = available_gifts.shape[0]
            for i_width in range(iteration):
                random_sample = self.__get_random_sample(available_gifts)
                measure = get_measure(cur_route, pd.DataFrame(random_sample))
                available_gifts = available_gifts.where(available_gifts['GiftId'] != random_sample['GiftId'])
                available_gifts = available_gifts.dropna()
                if measure < best_measure:
                    best_measure = measure
                    best_sample = random_sample
            cur_route.add_gift_to_current_route(best_sample)
            init_available_gifts = init_available_gifts.where(init_available_gifts['GiftId'] != best_sample['GiftId'])
            init_available_gifts = init_available_gifts.dropna()

        return cur_route

    def __get_random_sample(self, dataframe: pd.DataFrame) -> pd.Series:
        sample = dataframe.sample(ignore_index = True)
        return sample.loc[0]

