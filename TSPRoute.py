import pandas as pd


class TSPRoute:

    def __init__(self, nof_route: int):
        self.nof_route = nof_route
        self.gifts = pd.DataFrame()
        self.max_cargo_weight = 1000.0
        # self.sleigh_base_weight = 10

    def get_gift_by_number(self, intNofInRoute: int) -> pd.Series:
        return self.gifts.loc[intNofInRoute]

    def get_all_gifts_assigned(self) -> pd.DataFrame:
        return self.gifts

    def get_route_number(self) -> int:
        return self.nof_route

    def add_gift_to_current_route(self, gift: pd.Series):
        self.gifts = self.gifts.append(gift)
        if self.get_current_cargo_weight() > self.max_cargo_weight:
            raise Exception("Cargo weight exceeded. the algorithm is wrong")

    def get_current_cargo_weight(self) -> float:
        return self.gifts["Weight"].sum()

    def get_free_weight_cargo(self) -> float:
        free_weight = self.max_cargo_weight - self.get_current_cargo_weight()
        if free_weight < 0:
            free_weight = 0
        return free_weight

    def is_sleight_full(self, additional_package: pd.Series = None) -> bool:
        weight = self.get_current_cargo_weight()
        if additional_package is not None:
            weight = weight + additional_package['Weight']
        return weight > self.max_cargo_weight

    def locally_optimize(self):
        # TODO: make 2 opt for example
        test = self.gifts
