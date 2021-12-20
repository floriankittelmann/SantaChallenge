import random
import pandas as pd

import BeamSearch


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
        gifts = self.gifts
        
        # set the maximum of iterations that are made without the solution to be improved, before quitting. tours usually have
        # something between 50 and 100. setting it to the amount of gifts yields in a good performance / improvment ratio
        non_improving_iterations = 0
        max_non_improving_iterations = len(gifts.index)

        gifts = gifts.reset_index()

        # the best cost value and the best permutation of the index are stored and updated in the loop
        best_index = gifts.index.values.copy()
        best_measure = BeamSearch.get_measure(gifts)

        print("before optimization: " + str(best_measure))

        # at least three gifts must be left. the biggest one left to start the tour and two to swap
        while non_improving_iterations < max_non_improving_iterations and len(best_index) >= 3:
             # choose two random gifts to swap, start with index 1, as the first (biggest) gift should not be swapped
            random_gift_index1 = random.randint(1, len(best_index) - 1)
            random_gift_index2 = random.randint(1, len(best_index) - 1)

            temp_index = best_index.copy()

            temp = temp_index[random_gift_index1]
            temp_index[random_gift_index1] = temp_index[random_gift_index2]
            temp_index[random_gift_index2] = temp

            # reindex the DataFrame with the new index and calculate the resulting cost
            gifts = gifts.reindex(temp_index)
            temp_measure = BeamSearch.get_measure(gifts)

            if temp_measure < best_measure:
                best_measure = temp_measure
                best_index = temp_index.copy()
            else:
                non_improving_iterations = non_improving_iterations + 1

        # apply the best index permutation found so far and apply it to the final result
        self.gifts = gifts.reindex(best_index)
        print("after optimization:  " + str(best_measure))
