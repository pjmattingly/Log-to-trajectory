def log_to_trajectories(play):
    '''
    we take a play, and return a set of coordinates, forming a trajectory
    
    play, a data frame of learner actions for a single play of a storm chase
    '''
    
    #all measurement actions and their opens mapped to coordinates
    d_measurements_to_coordinate = {
        'HudPrecipitationType': (1, 3),
        'HudCloudType': (1, 2),
        'HudWindDirection': (1, 1),
        'HudAirMovement': (1, -1),
        'HudPrecipitationAmount':  (1, -2),
        'HudWindSpeed': (1, -3),
    }

    d_measurement_opens_to_coordintes = {
        'HudPrecipitationType_Open':  (0, 3),
        'HudCloudType_Open':  (0, 2), 
        'HudWindDirection_Open':  (0, 1),
        'HudAirMovement_Open': (0, -1),
        'HudPrecipitationAmount_Open': (0, -2),
        'HudWindSpeed_Open': (0, -3),
    }

    #all actions present in the logs that are associated with measurement
    s_actions = set(
        ['HudPrecipitationType_Open',
        'HudCloudType_Open', 
        'HudWindDirection_Open',
        'HudAirMovement_Open',
        'HudPrecipitationAmount_Open',
        'HudWindSpeed_Open',

        'HudPrecipitationType',
        'HudCloudType',
        'HudWindDirection',
        'HudAirMovement',
        'HudPrecipitationAmount',
        'HudWindSpeed',

        'HudPrecipitationType_Open_Retry',
        'HudCloudType_Open_Retry',
        'HudWindDirection_Open_Retry',
        'HudAirMovement_Open_Retry',
        'HudPrecipitationAmount_Open_Retry',
        'HudWindSpeed_Open_Retry',

        'HudPrecipitationType_Retry',
        'HudCloudType_Retry',
        'HudWindDirection_Retry',
        'HudAirMovement_Retry',
        'HudPrecipitationAmount_Retry',
        'HudWindSpeed_Retry',

        'HudHypothesis',

        'HudPickStorm'
        ]
    )

    #maps the first retry of a measurement to a coordinate
    d_retries_to_coordinates1 = {
        'HudPrecipitationType_Open_Retry': (2, 4),
        'HudCloudType_Open_Retry': (2, 1),
        'HudWindDirection_Open_Retry': (2, -2),
        'HudAirMovement_Open_Retry': (4, 4),
        'HudPrecipitationAmount_Open_Retry': (4, 1),
        'HudWindSpeed_Open_Retry': (4, -2),

        'HudPrecipitationType_Retry': (3, 4),
        'HudCloudType_Retry': (3, 1),
        'HudWindDirection_Retry': (3, -2),
        'HudAirMovement_Retry': (5, 4),
        'HudPrecipitationAmount_Retry': (5, 1),
        'HudWindSpeed_Retry': (5, -2),
    }

    #maps the second retry of a measurement to a coordinate
    d_retries_to_coordinates2 = {
        'HudPrecipitationType_Open_Retry': (2, 3),
        'HudCloudType_Open_Retry': (2, 0),
        'HudWindDirection_Open_Retry': (2, -3),
        'HudAirMovement_Open_Retry': (4, 3),
        'HudPrecipitationAmount_Open_Retry': (4, 0),
        'HudWindSpeed_Open_Retry': (4, -3),

        'HudPrecipitationType_Retry': (3, 3),
        'HudCloudType_Retry': (3, 0),
        'HudWindDirection_Retry': (3, -3),
        'HudAirMovement_Retry': (5, 3),
        'HudPrecipitationAmount_Retry': (5, 0),
        'HudWindSpeed_Retry': (5, -3),
    }
    
    #maps the third retry of a measurement to a coordinate
    d_retries_to_coordinates3 = {
        'HudPrecipitationType_Open_Retry': (2, 2),
        'HudCloudType_Open_Retry': (2, -1),
        'HudWindDirection_Open_Retry': (2, -4),
        'HudAirMovement_Open_Retry': (4, 2),
        'HudPrecipitationAmount_Open_Retry': (4, -1),
        'HudWindSpeed_Open_Retry': (4, -4),

        'HudPrecipitationType_Retry': (3, 2),
        'HudCloudType_Retry': (3, -1),
        'HudWindDirection_Retry': (3, -4),
        'HudAirMovement_Retry': (5, 2),
        'HudPrecipitationAmount_Retry': (5, -1),
        'HudWindSpeed_Retry': (5, -4),
    }

    l_retries_to_coordinates = [d_retries_to_coordinates1, d_retries_to_coordinates2, d_retries_to_coordinates3]

    d_hypothesis_to_coordinate1 = {
        'HudHypothesis': (6, 3),
    }
    
    d_hypothesis_to_coordinate2 = {
        'HudHypothesis': (6, 2),
    }
    
    d_hypothesis_to_coordinate3 = {
        'HudHypothesis': (6, 1),
    }
    
    d_hypothesis_to_coordinate4 = {
        'HudHypothesis': (6, -1),
    }
    
    d_hypothesis_to_coordinate5 = {
        'HudHypothesis': (6, -2),
    }
    
    d_hypothesis_to_coordinate6 = {
        'HudHypothesis': (6, -3),
    }

    l_hypothesis_to_coordinates = [d_hypothesis_to_coordinate1, d_hypothesis_to_coordinate2, d_hypothesis_to_coordinate3, 
        d_hypothesis_to_coordinate4, d_hypothesis_to_coordinate5, d_hypothesis_to_coordinate6]

    #maps the conclusion to a coordinate
    d_conclusion_to_coordinate1 = {
        'HudPickStorm': (7, 3),
    }
    
    d_conclusion_to_coordinate2 = {
        'HudPickStorm': (7, 2),
    }
    
    d_conclusion_to_coordinate3 = {
        'HudPickStorm': (7, 1),
    }
    
    d_conclusion_to_coordinate4 = {
        'HudPickStorm': (7, -1),
    }
    
    d_conclusion_to_coordinate5 = {
        'HudPickStorm': (7, -2),
    }
    
    d_conclusion_to_coordinate6 = {
        'HudPickStorm': (7, -3),
    }

    l_conclusion_to_coordinates = [d_conclusion_to_coordinate1, d_conclusion_to_coordinate2, d_conclusion_to_coordinate3, 
        d_conclusion_to_coordinate4, d_conclusion_to_coordinate5, d_conclusion_to_coordinate6]
    
    _l_trajectory = list()
    
    #ensure the play is ordered in time
    play = play.sort_values(by=['Timestamp'])

    #keep track of the number of some actions seen, to account for their order
    d_retries_to_num_seen = {
        'HudPrecipitationType_Retry' : 0,
        'HudCloudType_Retry' : 0,
        'HudWindDirection_Retry': 0,
        'HudAirMovement_Retry': 0,
        'HudPrecipitationAmount_Retry': 0,
        'HudWindSpeed_Retry': 0
    }

    d_hypothesis_to_num_seen = {
        'HudHypothesis' : 0
    }

    d_conclusion_to_num_seen = {
        'HudPickStorm' : 0
    }

    for _row in play.to_dict(orient="row"):
        _action = _row['action']

        #DEBUG
        #print(_action)
        #print(_action == 'HudHypothesis')

        if not _action in s_actions:
            #skip the actions not associated with measurement
            continue
    
        #check for measuremenets or opens
        if _action in d_measurements_to_coordinate:
            _l_trajectory.append( d_measurements_to_coordinate[_action] )
            continue

        if _action in d_measurement_opens_to_coordintes:
            _l_trajectory.append( d_measurement_opens_to_coordintes[_action] )
            continue

        #otherwise the action is a retry, hypothesis, or conclusion
        
        #checking for retries first, by finding which measurement they are trying to retry

        #refactoring as a function for additional control flow
        def _():
            for _measure in d_measurements_to_coordinate:
                #once we know which retry, check how many of that retry have been seen before
                #as the coordinates for the first, second, or third retry are different
                if _measure in _action:
                    _num_retry_seen = d_retries_to_num_seen[_measure + '_Retry']

                    #then find the proper dict corresponding to the order of the retry
                    _d_retry_to_coordinates = l_retries_to_coordinates[_num_retry_seen]

                    #then, given the proper dict, find the mapping between this retry and its coordinate
                    _l_trajectory.append( _d_retry_to_coordinates[_action] )

                    #finally, if we saw a retry then increment our counter
                    #if it was just an open, then don't do anything
                    if not 'Open' in _action:
                        d_retries_to_num_seen[_measure + '_Retry'] += 1

                    return True
            else:
                return False

        if _():
            continue

        #then hypothesis
        if _action == 'HudHypothesis':
            _l_trajectory.append( l_hypothesis_to_coordinates[ d_hypothesis_to_num_seen[_action] ]['HudHypothesis'] )
            d_hypothesis_to_num_seen[_action] += 1
            continue

        #finally, conclusions
        if _action == 'HudPickStorm':
            _l_trajectory.append( l_conclusion_to_coordinates[ d_conclusion_to_num_seen[_action] ]['HudPickStorm'] )
            d_conclusion_to_num_seen[_action] += 1
            continue

    return _l_trajectory