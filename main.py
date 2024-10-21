# Call simulatorData.py to initialize failure scenario
# Will return altitude and airspeed vector
# Pass in final arrays for analysis

from simulatorData import connectToSim
from autogen import ConversableAgent
import Util.prompts
import os

#altitudes, speeds = connectToSim(agentIP="10.0.0.203")
altitudes = [1976, 1980, 1980, 1979, 1979, 1976, 1975, 1977, 1978, 1977, 1975, 1974, 1975, 1976, 1976, 1972, 1968, 1963, 1958, 1954, 1950, 1947, 1941, 1934, 1924, 1912, 1897, 1877, 1853, 1830, 1809, 1790, 1773, 1754, 1739, 1728, 1719, 1711, 1702, 1693, 1684, 1674, 1661, 1645, 1624, 1604, 1586, 1570, 1557, 1544, 1533, 1521, 1508, 1495, 1483, 1467, 1455, 1441, 1428, 1416, 1403, 1392, 1381, 1368, 1355, 1335, 1323, 1310, 1297, 1284, 1271, 1253, 1240, 1225, 1211, 1197, 1183, 1168, 1154, 1139, 1124, 1106, 1091, 1076, 1062, 1047, 1032, 1018, 1001, 985, 969, 954, 941, 929, 915, 901, 885, 868, 850, 832, 818, 806, 796, 786, 775, 764, 755, 744, 733, 720, 707, 695, 682, 668, 653, 634, 615, 597, 574, 555, 533, 510, 489, 465, 449, 434, 419, 402, 387, 376, 363, 352, 342, 332, 322, 309, 295, 280, 265, 250, 238, 223, 207, 194, 180, 168, 153, 133, 110, 85, 63, 43, 31, 20, 12, 7]
speeds = [113, 113, 110, 108, 106, 103, 101, 98, 96, 94, 92, 89, 87, 85, 82, 79, 77, 75, 73, 72, 70, 69, 67, 65, 64, 62, 62, 62, 64, 67, 70, 71, 71, 72, 72, 71, 70, 70, 68, 67, 66, 65, 65, 64, 64, 65, 66, 66, 67, 67, 67, 67, 66, 65, 65, 64, 64, 64, 64, 64, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 64, 64, 64, 64, 64, 65, 65, 65, 65, 65, 64, 65, 65, 65, 65, 65, 65, 66, 66, 66, 67, 67, 66, 66, 66, 67, 68, 69, 69, 69, 68, 67, 66, 65, 64, 64, 63, 63, 62, 62, 62, 62, 62, 62, 63, 63, 64, 65, 67, 68, 69, 70, 71, 71, 71, 71, 71, 70, 70, 69, 68, 66, 65, 65, 64, 64, 64, 63, 64, 63, 63, 63, 62, 61, 60, 61, 61, 58, 58, 59, 59, 59, 58, 56]

def main():
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    glide_analysis_agent = ConversableAgent("glide_analysis_agent", 
                                        system_message=Util.prompts.glide_analysis_query(), 
                                        llm_config=llm_config)
    glide_analysis_agent.register_for_llm(name="glide_analysis_agent", description="Analyzes how the pilot maintains best glide speed.")(glide_analysis_agent)
    glide_analysis_agent.register_for_execution(name="glide_analysis_agent")(glide_analysis_agent)

if __name__ == "__main__":
    main()

