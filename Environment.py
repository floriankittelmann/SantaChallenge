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

    def find_gifts_in_area(self, gift: pd.Series, gifts_assigned_to_routes: pd.DataFrame, cur_tsp_route: TSPRoute, threshold: float) -> pd.DataFrame:
        gifts_not_assigned_yet = self.__get_gifts_not_assigned_yet(gifts_assigned_to_routes, cur_tsp_route)
        gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Longitude"] >= (gift["Longitude"] - threshold))
        gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Longitude"] <= (gift["Longitude"] + threshold))
        gifts_not_assigned_yet = gifts_not_assigned_yet.where(gifts_not_assigned_yet["Latitude"] >= (gift["Latitude"] - threshold))
        gifts_not_assigned_yet.where(gifts_not_assigned_yet["Latitude"] <= (gift["Latitude"] + threshold))
        gifts_not_assigned_yet = gifts_not_assigned_yet.dropna()
        return gifts_not_assigned_yet
