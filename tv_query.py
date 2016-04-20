#!/usr/bin/env python3

import tvdb_api as tvdb
import re
import argparse

class TVError(Exception):
    def __init__(self, args):
        self.args = args
    def display(self):
        print(''.join(self.args))

class Series:
    def __init__(self, tv, tv_name):
        self.tv = tv
        self.name = tv_name
        self.show = self.tv[tv_name]
        self.episodes = []

    def get_season(self, index):
        season  = {}
        s = self.show[index]
        slen = len(s.keys())

        season['name'] = self.tv
        season['total'] = slen
        season['season_number'] = index

        for i in range(1, slen+1):
            ep = self.get_episode_details(index, i)
            season[i] = ep
        return season

    def get_episode_details(self, snum, epnum):
        season = self.show[snum]
        episode = season[epnum]
        ep = {}

        ep['season_number'] = snum
        ep['episode_number'] = epnum
        ep['name'] = episode['episodename'] if episode['episodename'] is not None \
                                            else "still not named"
        ep['air_date'] = episode['firstaired']
        return ep

    def __getitem__(self, index):
        return self.show[index]

def display_full(s, ep=None):
    print('-' * 50)
    print(s['name'])
    print('-' * 50)
    if ep:
        for key in ep:
            print(key, " : ", ep[key])
    else:
        print("season ", s['season_number'])
        print('-' * 50)
        for i in range(1, s['total']+1):
            print("{:3s} {:35s} {:45s}".format(str(i), s[i]['name'], s[i]['air_date']))

def parse(tv):
    parser = argparse.ArgumentParser(description = "TV series shit")

    parser.add_argument("-n", "--name",
            help = "series name"
            )
    parser.add_argument("-s", "--season",
            help = """season in format : xxyy\n
                    xx : season number\n
                    yy : episode number(optional)
                    """
            )

    args = parser.parse_args()
    try:
        if not args.name or not args.season:
            raise TVError("retard! Try -h or --help")
        if len(args.season) > 4:
            raise TVError("LOL! season's format is sxxeyy")

        sn = int(args.season[:2])
        ep = int(args.season[2:4]) if args.season[2:4] else None

        tvwrap = Series(tv, args.name)
        s = tvwrap.get_season(sn)

        if ep is not None:
            display_full(s, s[ep])
        else:
            display_full(s, None)

    except TVError as terr:
        terr.display()

def main():
    tv = tvdb.Tvdb()
    parse(tv)

if __name__ == "__main__":
    main()

