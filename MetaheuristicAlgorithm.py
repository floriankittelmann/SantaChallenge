import pandas as pd
import time
import math

from BeamSearch import BeamSearch
from TSPRoute import TSPRoute
from Environment import Environment


class MetaheuristicAlgorithm:

    def __init__(self, data_path: str, output_path: str):
        self.env = Environment(data_path)
        self.output_path = output_path
        self.routes = []

    def __get_all_gifts_assigned(self) -> pd.DataFrame:
        all_gifts_assigned = pd.DataFrame()
        for route in self.routes:
            all_gifts_assigned = all_gifts_assigned.append(route.get_all_gifts_assigned())
        return all_gifts_assigned

    def __create_route(self, nof_route):
        time_start_beam = time.time()

        biggest_gift = self.env.get_biggest_gift_not_assigned_yet(self.__get_all_gifts_assigned())
        cur_tsp_route = TSPRoute(nof_route)
        cur_tsp_route.add_gift_to_current_route(biggest_gift)
        available_gifts = self.env.find_gifts_in_area(biggest_gift, self.__get_all_gifts_assigned(), cur_tsp_route)
        beam_search = BeamSearch(width=3)
        print("start beam search, with gifts: " + str(len(available_gifts.index)))
        tsp_route = beam_search.make_beam_search(cur_tsp_route, available_gifts)

        tsp_route.locally_optimize()
        time_end_beam = time.time()
        time_in_s = time_end_beam - time_start_beam
        print("time used for beam_search: ", '{:5.3f}s'.format(time_in_s))
        return tsp_route, time_in_s

    def create_initial_tsp(self):
        index = 0
        nof_gifts_total = self.env.nof_gifts_not_assigned_yet(self.__get_all_gifts_assigned())
        time_in_s = None
        last_nof_not_assigned = None
        while True:
            nof_not_assigned = self.env.nof_gifts_not_assigned_yet(self.__get_all_gifts_assigned())
            if time_in_s is not None and last_nof_not_assigned is not None:
                nof_assigned_in_this_round = last_nof_not_assigned - nof_not_assigned
                time_to_finish_s = nof_not_assigned / nof_assigned_in_this_round * time_in_s
                time_to_finish_min = time_to_finish_s / 60.0
                time_to_finish_s = time_to_finish_s % 60
                time_to_finish_min = math.floor(time_to_finish_min)

                time_to_finish_h = time_to_finish_min / 60.0
                time_to_finish_min = time_to_finish_min % 60
                time_to_finish_h = math.floor(time_to_finish_h)
                print("approx time use to finish: ", time_to_finish_h, 'h ', time_to_finish_min, 'min ', time_to_finish_s, 's')

            if nof_not_assigned <= 0:
                break
            print("--------- create a new route -------------")
            print("nof not assigned: ", nof_not_assigned)
            print("tripId ", index)
            tsp, time_in_s = self.__create_route(index)
            self.routes.append(tsp)
            #print("free weight: ", tsp.get_free_weight_cargo())
            last_nof_not_assigned = nof_not_assigned
            index = index + 1
        self.__write_to_csv()

    def __write_to_csv(self):
        df = pd.DataFrame()
        for route in self.routes:
            route_number = route.get_route_number()

            df_route = route.get_all_gifts_assigned()
            df_route.set_index("GiftId")
            df_route['TripId'] = route_number
            df_array = [df, df_route]
            df = pd.concat(df_array)
        df.to_csv(path_or_buf=self.output_path)
