import pandas as pd


class TSPRoute:

    def __init__(self, nof_route: int):
        self.nof_route = nof_route
        self.gifts = pd.DataFrame()

    def get_gift_by_number(self, intNofInRoute: int) -> pd.Series:
        return self.gifts.loc[intNofInRoute]

    def get_route_number(self) -> int:
        return self.nof_route

    def add_gift_to_current_route(self, gift: pd.Series):
        # throw exception in case it gets overloaded
        # add to dataframe
        return "test"

    def get_weight_of_sleigh(self) -> float:
        return self.gifts["Weight"].sum()

    def locally_optimize(self):
        # TODO: make 2 opt for example
        test = self.gifts
