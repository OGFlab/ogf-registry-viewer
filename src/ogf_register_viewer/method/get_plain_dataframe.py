import urllib.parse
from typing import Dict, List

import requests

# import loguru
# import rich


def get_plain_dataframe(query_option: dict) -> List[Dict]:
    # dataframe also can be generated by pandas csv reader or keqing

    mode_load_method = "network"

    query_option_key = query_option["key"]
    query_option_type = query_option["type"]
    query_option_poly = query_option["poly"]

    with open("../assets/poly/" + query_option_poly, "r") as f:
        OVERPASS_QL_POLY = f.read()

    OVERPASS_QL_ENDPOINT = (
        "https://overpass.opengeofiction.net/api//interpreter?data="
    )
    # TODO
    # CSV gen can be replaced with Yuheng
    OVERPASS_QL_CONTENT = """
[out:csv(
    ::type,
    ::id,{{键}};
    true; "|"
)];

nwr{{类型}}{{边界}};

out meta asc;
"""

    OVERPASS_QL = (
        OVERPASS_QL_CONTENT.replace(
            "{{键}}", ",".join(['"' + i + '"' for i in query_option_key])
        )
        .replace("{{类型}}", query_option_type)
        .replace("{{边界}}", OVERPASS_QL_POLY.replace("\n", ""))
    )

    OVERPASS_QL_URL = OVERPASS_QL_ENDPOINT + urllib.parse.quote(OVERPASS_QL)

    try:
        query_result = requests.get(
            url=OVERPASS_QL_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Referer": "https://registry.moe.gov.hx/index.html",
            },
        ).content.decode("utf-8")
    except Exception as e:
        print(e)
        print(OVERPASS_QL)
        print(OVERPASS_QL_URL)
        exit()

    # print(OVERPASS_QL)
    # print(OVERPASS_QL_URL)
    # print(query_result)

    header = query_result.split("\n")[0].split("|")
    df_raw = query_result.replace(str("|".join(header) + "\n"), "")

    df: List[Dict] = [
        dict(zip(header, item.split("|")))
        for item in list(filter(bool, df_raw.split("\n")))
    ]

    return df
