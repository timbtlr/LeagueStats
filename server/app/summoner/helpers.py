import pandas as pd
import numpy as np
import json

def fill_data_frame(matches, time_attr):
    """
    Given a list of MatchPerformance items, fill in a number of lists representing...
        the time of the match (based on the time attribute provided)
        KDA from the match
        Whether the match was a win
        Kills from the match
        Assists from the match
        Death from the match

    Time attribute must be "%H", "%w", or "%-m" as these return an integer number for 
    hour of day, day of week, or month of year using strftime. See

    https://www.programiz.com/python-programming/datetime/strftime

    for more details.
    """

    if time_attr not in ["%H", "%w", "%-m"]:
        raise ValueError("time_attr must be '%H', '%w', or '%-m'")
    times = []
    kdas = []
    wins = []
    kills = []
    assists = []
    deaths = []

    for match in matches.iterator():
        times.append(int(match.timestamp.strftime(time_attr)))
        if match.deaths > 0:
            kdas.append(float(match.kills + match.assists) / match.deaths)
        else:
            kdas.append(float(match.kills + match.assists))
        wins.append(int(match.win))
        kills.append(int(match.kills))
        assists.append(int(match.deaths))
        deaths.append(int(match.assists))

    return {
        "Time": times,
        "KDA": kdas,
        "Win": wins,
        "Kills": kills,
        "Deaths": deaths,
        "Assists": assists
    }



def normalize_kda_data(data_frame, index_range):
    frame = pd.DataFrame(data_frame)

    kda_groupings = frame.groupby(['Time']).aggregate(np.mean)
    kda_groupings = kda_groupings.reindex(index_range, fill_value=0)
    cols_to_norm = ['KDA', 'Win', 'Kills', 'Deaths', 'Assists']
    kda_groupings[cols_to_norm] = kda_groupings[cols_to_norm].apply(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )
    json_result = kda_groupings.to_json()
    return json.loads(json_result)
