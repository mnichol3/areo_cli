"""
aero_api.py

Class to interact with the FlightAware Aero API.
"""
import requests
import os
import sys
from pathlib import Path

import pandas as pd


class AeroAPI(object):

    def __init__(self, **kwargs):
        self._api_key = kwargs.get('api_key', os.environ['AEROAPI_KEY'])
        self._api_url = 'https://aeroapi.flightaware.com/aeroapi'
        self._session = requests.Session()
        self._session.headers.update({"x-apikey": self._api_key})
        self._payload = None
        self._cursor = None

    def get_arrivals(self, icao, **kwargs):
        url = self._get_airport_request_url('arrivals', icao, **kwargs)
        payload, cursor = self._make_request(url)

    def get_scheduled_arrivals(self, icao, **kwargs):
        url = self._get_airport_request_url('scheduled_arrivals', icao, **kwargs)
        payload, cursor = self._make_request(url)

    def get_departures(self, icao, **kwargs):
        url = self._get_airport_request_url('departures', icao, **kwargs)
        payload, cursor = self._make_request(url)

    def get_scheduled_departures(self, icao, **kwargs):
        url = self._get_airport_request_url('scheduled_departures', icao, **kwargs)
        payload, cursor = self._make_request(url)

    def get_flights_between(self, origin, dest, **kwargs):
        url = self._get_airport_request_url('flights_to', origin, dest=dest)
        payload, cursor = self._make_request(url)

    def _get_airport_request_url(self, req_type, icao, **kwargs):
        """
        Construct the URL for an airport-based request, e.g. KLAX arrivals.

        Args:
            req_type: str
                Request type, e.g. 'arrivals', 'scheduled_departures'.
            icao: str
                4-letter airport ICAO code, e.g. 'KLAX'.
            **kwargs: dict
                Keyword Args.

        Returns:
            str

        Raises:
            ValueError: If 'req_type' is 'flights_to' but destination airport
                        keyword parameter 'dest' is not passed.
        """
        req_str = f'{self._api_url}/airports/{icao}/flights/'

        if req_type == 'flights_to':
            if 'dest' not in kwargs:
                raise ValueError('"dest" parameter must be given for "flights_to" request.')
            else:
                req_str += f'to/{kwargs.get("dest")}'

        return req_str

    def _make_request(self, req_url, return_json=False, **kwargs):
        auth_hdr = {'x-apikey': self._api_key}
        req_params = {key: val for key, val in kwargs if val is not None}

        #response = requests.get(req_url, params=req_params, headers=auth_hdr)
        response = self._session.get(req_url, params=req_params)
        response.raise_for_status()  # Raise error if status is not between 200-400
        json_data = response.json()

        num_pages = json_data['num_pages']
        next_chunk = json_data['links']['next']
        cursor = next_chunk.split('&')[-1].split('=')[1]

        for key in ['links', 'num_pages']:
            json_data.pop(key, None)

        if return_json:
            payload = json_data
        else:
            payload = self._json_to_df(json_data)

        # Save current state
        self._payload = payload
        self._cursor = cursor

        return payload, cursor

    def _json_to_df(self, json_data):
        col_names = [
            'flight_num', 'origin', 'dest', 'origin_gate', 'origin_terminal',
            'dest_gate', 'dest_terminal', 'filed_ete', 'rte_dist', 'acft_type',
            'acft_reg', 'sched_out', 'est_out', 'act_out', 'sched_off', 'est_off',
            'act_off', 'sched_on', 'est_on', 'act_on', 'sched_in', 'est_in',
            'act_in', 'dep_delay', 'arr_delay',
        ]
        df_list = []
        for j_key, flt_list in json_data.items():
            for flt_dict in flt_list:
                this_dict = {}

                # Skip flight if we can't get the origin and/or destination.
                origin = flt_dict.get('origin').get('code')
                dest = flt_dict.get('destination').get('code')
                if origin is None or dest is None:
                    continue

                this_dict['flight_num'] = flt_dict.get('ident', 'UNKN')
                this_dict['origin'] = origin
                this_dict['dest'] = dest
                this_dict['acft_type'] = flt_dict.get('aircraft_type', 'UNKN')
                this_dict['acft_reg'] = flt_dict.get('registration', 'UNKN')

                this_dict['sched_out'] = flt_dict.get('scheduled_out', 'UNKN')
                this_dict['est_out'] = flt_dict.get('estimated_out', 'UNKN')
                this_dict['act_out'] = flt_dict.get('actual_out', 'UNKN')

                this_dict['sched_off'] = flt_dict.get('scheduled_off', 'UNKN')
                this_dict['est_off'] = flt_dict.get('estimated_off', 'UNKN')
                this_dict['act_off'] = flt_dict.get('actual_off', 'UNKN')

                this_dict['sched_on'] = flt_dict.get('scheduled_on', 'UNKN')
                this_dict['est_on'] = flt_dict.get('estimated_on', 'UNKN')
                this_dict['act_on'] = flt_dict.get('actual_on', 'UNKN')

                this_dict['sched_in'] = flt_dict.get('scheduled_in', 'UNKN')
                this_dict['est_in'] = flt_dict.get('estimated_in', 'UNKN')
                this_dict['act_in'] = flt_dict.get('actual_in', 'UNKN')

                this_dict['dep_delay'] = flt_dict.get('departure_delay', 'UNKN')
                this_dict['arr_delay'] = flt_dict.get('arrival_delay', 'UNKN')

                this_dict['origin_gate'] = flt_dict.get('gate_origin', 'TBD')
                this_dict['origin_terminal'] = flt_dict.get('terminal_origin', 'TBD')
                this_dict['dest_gate'] = flt_dict.get('gate_destination', 'TBD')
                this_dict['dest_terminal'] = flt_dict.get('terminal_destination', 'TBD')
                this_dict['rte_dist'] = flt_dict.get('route_distance', 'UNKN')
                this_dict['ete'] = flt_dict.get('filed_ete', 'UNKN')

                for key, val in this_dict.items():
                    if val == '' or val is None:
                        this_dict.update({key: 'UNKN'})

                df_list.append(this_dict)

        sched_df = pd.DataFrame(df_list, columns=col_names)

        # Convert datetime strings to datetime objects
        dt_fmt = '%Y-%m-%dT%H:%M:%S'
        for (col_name, col_val) in sched_df.iteritems():
            if col_name.split('_')[1] in ['out', 'off', 'on', 'in']:
                sched_df[col_name] = pd.to_datetime(col_val, format=dt_fmt,
                                                    errors='coerce')
        return sched_df

    @staticmethod
    def concat_df_from_obj(obj, df_var, new_df, set_attr=True):
        curr_df = getattr(obj, df_var)
        if curr_df is None:
            curr_df = new_df
        else:
            curr_df = pd.concat([curr_df, new_df], ignore_index=True)

        if set_attr:
            setattr(obj, df_var, curr_df)

        return curr_df

    @staticmethod
    def print_df(df, actual_times=False):
        """
        Print the DataFrame from an API call.

        Args:
            df: Pandas DataFrame

        Returns:
            None
        """
        # TODO: format datetimes
        # TODO: convert ETE from seconds to hours:mins
        # TODO: verbose option showing delays

        def _print_row(row, act_times=False):
            """Print a DataFrame row"""
            flt_num = row['flight_num'].ljust(7)
            orgn = row['origin']
            dest = row['dest']
            t_out = row['sched_out']
            t_in = row['sched_in']
            ete = row['ete']
            gate_o = row['origin_gate'].ljust(4)
            gate_d = row['dest_gate'].ljust(4)

            ln = f'{flt_num}  {orgn}{t_out}  {t_in}{dest}  {ete}  {gate_o}  {gate_d}'
            print(ln)

        for index, df_row in df.iterrows():
            _print_row(df_row)

        return

    @property
    def api_key(self):
        return self._api_key

    @property
    def api_url(self):
        return self._api_url
