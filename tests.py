#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler import crawler

links = {
    '2015_16_teams_general_traditional': 'http://stats.nba.com/teams/traditional/#!?sort=W_PCT&dir=-1&Season=2015-16&SeasonType=Regular%20Season&PerMode=Totals',
    '2015_16_teams_clutch_traditional': 'http://stats.nba.com/teams/clutch-traditional/#!?sort=W_PCT&dir=-1&Season=2015-16&SeasonType=Regular%20Season&PerMode=Totals',
    '2016_17_teams_shooting': 'http://stats.nba.com/teams/shooting/#!?Season=2016-17&SeasonType=Regular%20Season&PerMode=Totals&sort=Less%20Than%205%20ft.%20FGM&dir=1',
    '2016_17_teams_hustle': 'http://stats.nba.com/teams/hustle/#!?Season=2016-17&SeasonType=Regular%20Season&PerMode=Totals',
    '2012_13_teams_opp_shooting_overall_totals': 'http://stats.nba.com/teams/opponent-shooting/#!?Season=2012-13&SeasonType=Regular%20Season&PerMode=Totals',
    '2012-13_teams_opp_shooting_overall_pg': 'http://stats.nba.com/teams/opponent-shooting/#!?Season=2012-13&SeasonType=Regular%20Season'
}

print(crawler(links))
