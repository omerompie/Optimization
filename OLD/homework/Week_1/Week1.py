from scipy.optimize import minimize

# GENERAL VARIABLES
COSTS = [71.8, 107.3, 224.6]
CREW_SIZE_PER_FLIGHT = [6, 8, 21]
PASSENGERS_PER_AIRCRAFT = [110, 165, 280]

FlIGHTS_PER_DAY = [4, 4, 2]
FLIGHTS_PER_CREW = [2, 2, 1]

AVAILABLE_CREW_MEMBERS = 200
AVAILABLE_MONEY = 1300

def crew_per_day_calculator(CREW_SIZE, FlIGHTS, CREW_NEEDED_PER_DAY):
    people_required_per_day = []

    for i in range(len(CREW_SIZE)):
        people_required_per_day.append(FlIGHTS[i] / CREW_NEEDED_PER_DAY[i] * CREW_SIZE[i])
    return people_required_per_day

people_required_per_day = crew_per_day_calculator(CREW_SIZE_PER_FLIGHT, FlIGHTS_PER_DAY, FLIGHTS_PER_CREW)


def objective_function(x):

    x0 = x[0]
    x1 = x[1]
    x2 = x[2]

    return -(PASSENGERS_PER_AIRCRAFT[0] * FlIGHTS_PER_DAY[0] * x0 +
             PASSENGERS_PER_AIRCRAFT[1] * FlIGHTS_PER_DAY[1] * x1 +
             PASSENGERS_PER_AIRCRAFT[2] * FlIGHTS_PER_DAY[2] * x2)

bounds = [(2, None), (2, None), (2, None)]
initial_guess = [2, 2, 2]

constraints = [
    {"type": "ineq",
     'fun': lambda x: AVAILABLE_MONEY - (COSTS[0] * x[0] + COSTS[1] * x[1] + COSTS[2] * x[2])
     },
    {"type": "ineq",
     'fun': lambda x: AVAILABLE_CREW_MEMBERS - (people_required_per_day[0] * x[0] +
                                                people_required_per_day[1] * x[1] +
                                                people_required_per_day[2] * x[2])
     }
]

opt = minimize(objective_function, x0=initial_guess, method="SLSQP", bounds=bounds, constraints=constraints)
print(opt)

































""" Step 1
Decision Variables = amount of aircraft
x1 = amount of Bombardier
x2 = amount of Airbus
x3 = amount of Boeing
"""
#-----------------------------------------------------------------------------------------------------------------------
""" Step 2
define the constraints = amount of times an aircraft can be flown 
h1 = 4 times a day, with subsequent crew members per 2 flights 
h2 = 4 times a day, with subsequent crew members per 2 flights
h3 = 2 times a day, with 1 crew member per flight

people required 
h1 = ( flights / crews ) * Crew size
#example = 4 / 2 * 6 = 12 for the bombardier
so h1 = ( a / b ) * c
etc for the other aircraft...

so essentially,

12h1 + 16h2 + 42h3 ≤ 200

"""
#-----------------------------------------------------------------------------------------------------------------------
""" Step 3
Objective Function = F(x) = a1x1 + a2x2 + a3x3

ai = passengers_per_flight * flights_per_day
"""
#-----------------------------------------------------------------------------------------------------------------------
""" Step 4 
Limiting Factors
x1 * 71.8 + x2 * 107.3 + x3 * 224.6 <= 1300
x1 >= 2, x2 >= 2, x3 >= 2
available_crew_members = 200
"""

