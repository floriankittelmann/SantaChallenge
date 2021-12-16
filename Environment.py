import math
import pandas as pd
from TSPRoute import TSPRoute


class Environment:

    def __init__(self, data_path: str):
        self.all_gifts = pd.read_csv(data_path)

    def get_biggest_gift_not_assigned_yet(self, gifts_assigned_to_routes: pd.DataFrame) -> pd.Series:
        not_assigned = self.__get_gifts_not_assigned_yet(gifts_assigned_to_routes)
        max_id = not_assigned['Weight'].idxmax()
        return self.all_gifts.loc[max_id]

    def __get_gifts_not_assigned_yet(self, gifts_assigned_to_routes: pd.DataFrame, cur_tsp_route: TSPRoute = None) -> pd.DataFrame:
        gifts_not_assigned = self.all_gifts
        if gifts_assigned_to_routes.shape[0] != 0:
            gifts_not_assigned = self.all_gifts.loc[~self.all_gifts["GiftId"].isin(gifts_assigned_to_routes["GiftId"])]
            if cur_tsp_route is not None:
                gift_ids_in_cur_route = cur_tsp_route.get_all_gifts_assigned()["GiftId"]
                gifts_not_assigned = gifts_not_assigned.loc[~gifts_not_assigned["GiftId"].isin(gift_ids_in_cur_route)]
        return gifts_not_assigned

    def nof_gifts_not_assigned_yet(self, gifts_assigned_to_routes: pd.DataFrame) -> int:
        not_assigned_yet = self.__get_gifts_not_assigned_yet(gifts_assigned_to_routes)
        return not_assigned_yet.shape[0]

    def get_gifts_still_fit_in_sleigh_and_not_assigned_yet(self, space_in_slave: float, gifts_assigned_to_routes: pd.DataFrame, cur_tsp_route: TSPRoute) -> pd.DataFrame:
        not_assigned = self.__get_gifts_not_assigned_yet(gifts_assigned_to_routes, cur_tsp_route)
        not_assigned = not_assigned.where(not_assigned['Weight'] <= space_in_slave)
        return not_assigned.dropna()

    def find_gifts_in_area(self, gift: pd.Series, gifts_assigned_to_routes: pd.DataFrame, cur_tsp_route: TSPRoute) -> pd.DataFrame:
        gifts_not_assigned_yet = self.__get_gifts_not_assigned_yet(gifts_assigned_to_routes, cur_tsp_route)

        coordinates_min = gifts_not_assigned_yet.min()
        coordinates_max = gifts_not_assigned_yet.max()

        # the initial threshold is set to the farest distance of all gifts not assigned yet. this is the bigger distance to either the min or the 
        # max value of all gifts.
        threshold_longitude: float = max(abs(coordinates_max["Longitude"] - gift["Longitude"]), abs(coordinates_min["Longitude"] + gift["Longitude"]))
        threshold_latitude: float = max(abs(coordinates_max["Latitude"] - gift["Latitude"]), abs(coordinates_min["Latitude"] + gift["Latitude"]))

        gifts_amount_target = 500
        gifts_amount_max = gifts_amount_target * 2

        # the threshold is decreased in each iteration to find only the closest gifts to the current gift. the loop aborts if the search has been 
        # narrowed to at most gifts_amount_max gifts. in each iteration the threshold an thus the search area is reduced more based on the amount
        # of gifts that are still left to an expected amount of gifts_amount_target. this means, if far too many gifts are found, the threshold is 
        # reduced much more (calculation is based on an equal distribution, which is obviously not correct).

        while len(gifts_not_assigned_yet.index) >= gifts_amount_max:
            threshold_longitude = threshold_longitude * math.sqrt(gifts_amount_target / len(gifts_not_assigned_yet.index))
            threshold_latitude = threshold_latitude * math.sqrt(gifts_amount_target / len(gifts_not_assigned_yet.index))

            gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Longitude"] >= (gift["Longitude"] - threshold_longitude))
            gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Longitude"] <= (gift["Longitude"] + threshold_longitude))
            gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Latitude"] >= (gift["Latitude"] - threshold_latitude))
            gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Latitude"] <= (gift["Latitude"] + threshold_latitude))
            gifts_not_assigned_yet = gifts_not_assigned_yet.dropna()
        return gifts_not_assigned_yet
