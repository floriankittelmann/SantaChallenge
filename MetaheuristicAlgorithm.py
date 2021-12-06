import pandas as pd
from TSPRoute import TSPRoute


class MetaheuristicAlgorithm:

    def __init__(self, data_path: str):
        self.all_gifts = pd.read_csv(data_path)
        self.gifts_assigned_to_route = pd.DataFrame()
        self.routes = []

    def get_biggest_gift_not_assigned_yet(self) -> pd.Series:
        not_assigned = self.gifts_assigned_to_route()
        max_id = not_assigned['Weight'].idxmax()
        return self.all_gifts.loc[max_id]

    def get_gifts_not_assigned_yet(self) -> pd.DataFrame:
        return self.all_gifts.loc[~self.all_gifts["GiftId"].isin(self.gifts_assigned_to_route["GiftId"])]

    def nof_gifts_not_assigned_yet(self) -> int:
        not_assigned_yet = self.get_gifts_not_assigned_yet()
        return not_assigned_yet.shape[0]

    def get_gifts_still_fit_in_sleigh_and_not_assigned_yet(self, space_in_slave: float) -> pd.DataFrame:
        not_assigned = self.get_gifts_not_assigned_yet()
        return not_assigned.where(not_assigned['Weight'] <= space_in_slave)

    def find_gifts_in_area(self, gift: pd.Series, gifts_to_find_locals: pd.DataFrame) -> pd.DataFrame:
        threeshold_north_south = 10.0
        threeshold_west_east = 10.0
        return gifts_to_find_locals.where(
            gifts_to_find_locals["Longitude"] >= (gift["Longitude"] - threeshold_west_east) and
            gifts_to_find_locals["Longitude"] <= (gift["Longitude"] + threeshold_west_east) and
            gifts_to_find_locals["Latitude"] >= (gift["Latitude"] - threeshold_north_south) and
            gifts_to_find_locals["Latitude"] <= (gift["Latitude"] + threeshold_north_south)
        )

    def beam_search(
            self,
            lookahead: int,
            width: int,
            nof_route: int,
            gifts_available: pd.DataFrame,
            initial_gift: pd.Series
    ) -> TSPRoute:
        tsp_route = TSPRoute(nof_route)
        # TODO: make sure that during beamsearch the choosen gifts doesnt get choosen twice -> maybe make a class
        return tsp_route

    def create_route(self, nof_route):
        biggest_gift = self.get_biggest_gift_not_assigned_yet()
        # TODO: append self.gifts_assigned_to_route with biggest gift
        # to implement

        # TODO: find gifts in area, with gifts not assigned yet
        # to implement
        local_gifts_and_available = pd.DataFrame()

        # TODO: make beam search for others with lookahead etc.
        tsp_route = self.beam_search(lookahead=1, width=1, nofRoute=nof_route, gifts_available=local_gifts_and_available, initial_gift=biggest_gift)

        # TODO: make local improvements of with 2-opt for example
        tsp_route.locally_optimize()
        return tsp_route

    def create_initial_tsp(self):
        index = 1
        while self.nof_gifts_not_assigned_yet() > 0:
            tsp = self.create_route(index)
            self.routes.append(tsp)
            index = index + 1


