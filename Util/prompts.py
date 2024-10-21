def glide_analysis_query():
    s = """You are a helpful agent tasked to analyze a simulator pilot's handling of an in-flight engine failure.
    Your task is to identify whether the pilot was able maintaining the best glide speed of 65 knots during the descent.
    A margin of plus or minus 5 knots is acceptable, since it is impossible to realistically hold an exact airspeed.
    Note that usually the initial cruising airspeed is much greater than 65 knots, so it is natural to see a deceleration of 2 knots per second.
    
    You will be given 2 python lists: altitude and airspeed, each recorded at a 1-second interval. 
    The engine failure occurred at time 0. 
    Please determine whether the pilot maintains appropriate airspeed.
    """
    return s