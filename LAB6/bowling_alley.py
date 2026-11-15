LANE_RATE = {"weekday": 400, "weekend": 600}


def lane_cost(day_type, games, players, shoe_rentals, is_league_member):
    if day_type not in LANE_RATE:
        raise ValueError("unknown day type")
    if games < 1 or players < 1 or players > 6:
        raise ValueError("invalid booking")
    if shoe_rentals > players:
        raise ValueError("too many shoe rentals")
    cost = LANE_RATE[day_type] * games
    if players > 4:
        cost += 100 * games
    cost += shoe_rentals * 50
    if is_league_member:
        cost -= cost // 5
    return cost


def frame_score(first_roll, second_roll, bonus_rolls):
    if first_roll < 0 or first_roll > 10 or second_roll < 0:
        raise ValueError("invalid roll")
    if first_roll == 10:
        return 10 + bonus_rolls[0] + bonus_rolls[1]
    if first_roll + second_roll > 10:
        raise ValueError("invalid frame")
    if first_roll + second_roll == 10:
        return 10 + bonus_rolls[0]
    return first_roll + second_roll


def lane_assignment(players, has_kids, lanes_free):
    if lanes_free == 0:
        return "wait"
    if has_kids:
        return "bumper lane"
    if players > 6 and lanes_free >= 2:
        return "two lanes"
    elif players > 6:
        return "wait"
    return "standard lane"
