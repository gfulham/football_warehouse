# ESPN Fantasy Roster web-Scraper 
# Pulls in rosters from ESPN leagues, and simulates season outcomes to find trades for your specific team.


from pdb import main
import sys
import requests
import argparse
import requests
import pandas as pd
import getpass
import json

def today():
    from datetime import date
    return date.today().isoformat()


def main(league):
    config_path="web_scraping/ESPN_league_configs.json"
    # Load league configuration from the specified JSON file
    # Open the JSON file and load the league configurations
    with open(config_path, "r") as f:
        League_configs = json.load(f)

    League_config = League_configs[league]
    LEAGUE_ID = League_config["LEAGUE_ID"]
    YEAR = League_config["YEAR"]
    espn_s2 = League_config["espn_s2"]
    swid = League_config["swid"]

    cookies = {
        "espn_s2": espn_s2,
        "SWID": swid
    }   


    # =========================
    # 3. ESPN API request
    # =========================

    url = (
        f"https://lm-api-reads.fantasy.espn.com/"
        f"apis/v3/games/ffl/seasons/{YEAR}/segments/0/"
        f"leagues/{LEAGUE_ID}"
    )

    params = [
        ("view", "mTeam"),
        ("view", "mRoster")
    ]

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers
    )

    print("Status code:", response.status_code)

    response.raise_for_status()

    data = response.json()


    # %%

    # =========================
    # 4. Inspect response
    # =========================

    print("League:", data.get("settings", {}).get("name"))
    print("Teams:", len(data.get("teams", [])))

    # =========================
    # 5. Extract rosters
    # =========================

    rows = []

    for team in data.get("teams", []):

        team_name = team.get("name")
        team_id = team.get("id")

        for entry in team.get("roster", {}).get("entries", []):

            player = entry.get(
                "playerPoolEntry", {}
            ).get("player", {})

            rows.append({
                "Team_ID": team_id,
                "Team": team_name,
                "Player_ID": player.get("id"),
                "Player": player.get("fullName"),
                "Position_ID": player.get(
                    "defaultPositionId"
                ),
                "Lineup_Slot_ID": entry.get(
                    "lineupSlotId"
                )
            })

    rosters_df = pd.DataFrame(rows)

    # =========================
    # 6. Display and export
    # =========================

    print(rosters_df)

    rosters_df.to_csv(
        f"espn_rosters_{league}_{today()}.csv",
        index=False
    )

    print(f"\nSaved espn_rosters_{league}_{today()}.csv")

    return rosters_df
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape ESPN Fantasy Football rosters")
    parser.add_argument(
        "--league",
        required=True,
        help="which league configuration to use. Current Keys: Dolan, Jason",
    )
    args = parser.parse_args()
    try:
        main(args.league)
        print("\nScript executed successfully.")
    except Exception as e:
        print(f"\nScript failed: {e}", file=sys.stderr)
        sys.exit(1)