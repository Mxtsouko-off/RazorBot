import re
import json


class DumperFile:
    @staticmethod
    def process_file(file_content):
        json_data = json.loads(file_content)

        replacements = [
                                {"searchText": "EventFlag", "replacementText": "NotEventFlag"},
                                {"searchText": "activeQuestDefinitions", "replacementText": "NotactiveQuestDefinitions"},
                                {"searchText": "requirements", "replacementText": "Notrequirements"},
                                {"searchText": "/Script/Engine.DataTable'/Game/Balance/DataTables/GameDifficultyGrowthBounds.GameDifficultyGrowthBounds'", "replacementText": "powerlevel"},
                                {"searchText": '"theaterType"\\s*:\\s*"Tutorial"', "replacementText": '"theaterType": "Standard"'},
                                {"searchText": '"bHideLikeTestTheater":\\s*true', "replacementText": '"bHideLikeTestTheater": false'},
                                {"searchText": '"missionGenerator"\\s*:\\s*"None"', "replacementText": '"missionGenerator": "/SaveTheWorld/World/MissionGens/MissionGen_T1_HT_EvacuateTheSurvivors.MissionGen_T1_HT_EvacuateTheSurvivors_C"'},
                                {"searchText": '"Theater_Phoenix_Zone02"', "replacementText": '"Theater_Start_Zone2"'},
                                {"searchText": '"Theater_Phoenix_Zone03"', "replacementText": '"Theater_Start_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone03"', "replacementText": '"Theater_Start_Group_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Zone05"', "replacementText": '"Theater_Start_Zone5"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone05"', "replacementText": '"Theater_Start_Group_Zone5"'},
                                {"searchText": '"Theater_Phoenix_Zone07"', "replacementText": '"Theater_Normal_Zone2"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone07"', "replacementText": '"Theater_Normal_Group_Zone2"'},
                                {"searchText": '"Theater_Phoenix_Zone09"', "replacementText": '"Theater_Normal_Zone4"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone09"', "replacementText": '"Theater_Normal_Group_Zone4"'},
                                {"searchText": '"Theater_Phoenix_Zone11"', "replacementText": '"Theater_Hard_Zone1"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone11"', "replacementText": '"Theater_Hard_Group_Zone1"'},
                                {"searchText": '"Theater_Phoenix_Zone13"', "replacementText": '"Theater_Hard_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone13"', "replacementText": '"Theater_Hard_Group_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Zone15"', "replacementText": '"Theater_Hard_Zone5"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone15"', "replacementText": '"Theater_Hard_Group_Zone5"'},
                                {"searchText": '"Theater_Phoenix_Zone17"', "replacementText": '"Theater_Nightmare_Zone2"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone17"', "replacementText": '"Theater_Nightmare_Group_Zone2"'},
                                {"searchText": '"Theater_Phoenix_Zone19"', "replacementText": '"Theater_Nightmare_Zone4"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone19"', "replacementText": '"Theater_Nightmare_Group_Zone4"'},
                                {"searchText": '"Theater_Phoenix_Zone21"', "replacementText": '"Theater_Endgame_Zone1"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone21"', "replacementText": '"Theater_Endgame_Group_Zone1"'},
                                {"searchText": '"Theater_Phoenix_Zone23"', "replacementText": '"Theater_Endgame_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone23"', "replacementText": '"Theater_Endgame_Group_Zone3"'},
                                {"searchText": '"Theater_Phoenix_Zone25"', "replacementText": '"Theater_Endgame_Zone5"'},
                                {"searchText": '"Theater_Phoenix_Group_Zone25"', "replacementText": '"Theater_Endgame_Group_Zone5"'},
                                {"searchText": '"theaterSlot"\\s*:\\s*2', "replacementText": '"theaterSlot": 0'},
                                {"searchText": "HV3_01", "replacementText": "Start_Zone4"},
                                {"searchText": "HV3_02", "replacementText": "Start_Zone5"},
                                {"searchText": "HV3_03", "replacementText": "Normal_Zone2"},
                                {"searchText": "HV3_04", "replacementText": "Normal_Zone4"},
                                {"searchText": "HV3_05", "replacementText": "Hard_Zone1"},
                                {"searchText": "HV3_06", "replacementText": "Hard_Zone3"},
                                {"searchText": "HV3_07", "replacementText": "Hard_Zone5"},
                                {"searchText": "HV3_08", "replacementText": "Nightmare_Zone2"},
                                {"searchText": "HV3_09", "replacementText": "Nightmare_Zone4"},
                                {"searchText": "HV3_10", "replacementText": "Endgame_Zone1"},
                                {"searchText": "HV3_11", "replacementText": "Endgame_Zone3"},
                                {"searchText": "HV3_12", "replacementText": "Endgame_Zone5"},
                                {"searchText": "_Starlight_Start_Zone2", "replacementText": "_Start_Zone3"},
                                {"searchText": "_StarlightTimed_Start_Zone2", "replacementText": "_Start_Zone3"},
                                {"searchText": "Theater_Starlight_", "replacementText": "Theater_"},
                                {"searchText": "_StarlightTimed_", "replacementText": "_"},
                                {"searchText": "Theater_Endless_", "replacementText": "Theater_"},
                                {"searchText": "Theater_Mayday_Start_Zone5", "replacementText": "Theater_Start_Zone5"},
                                {"searchText": "Theater_Mayday_Normal_Zone3", "replacementText": "Theater_Normal_Zone3"},
                                {"searchText": "Theater_Mayday_Normal_Zone5", "replacementText": "Theater_Normal_Zone5"},
                                {"searchText": "Theater_Mayday_Hard_Zone3", "replacementText": "Theater_Hard_Zone3"},
                                {"searchText": "Theater_Mayday_Hard_Zone5", "replacementText": "Theater_Hard_Zone5"},
                                {"searchText": "Theater_Mayday_Nightmare_Zone3", "replacementText": "Theater_Nightmare_Zone3"},
                                {"searchText": "Theater_Mayday_Nightmare_Zone5", "replacementText": "Theater_Nightmare_Zone5"},
                                {"searchText": "Theater_Mayday_Endgame_Zone5", "replacementText": "Theater_Endgame_Zone5"},
                            ]

        json_string = json.dumps(json_data)
        for replacement in replacements:
            search_text = replacement['searchText']
            replacement_text = replacement['replacementText']
            json_string = re.sub(search_text, replacement_text, json_string, flags=re.IGNORECASE)

        return json.loads(json_string)