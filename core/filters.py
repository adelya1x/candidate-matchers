def by_location(city: str):
    return lambda c: c.location.lower() == city.lower()


def by_exp_range(lo: int, hi: int):
    return lambda c: lo <= c.exp_years <= hi


def by_skill(skill: str):
    return lambda c: skill.lower() in map(str.lower, c.skills)
