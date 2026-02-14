from roles import ROLES
from domain_map import DOMAIN_MAP
from skill_weights import SKILL_WEIGHTS


def rank_user_skills(user_skills):
    return sorted(
        user_skills,
        key=lambda x: SKILL_WEIGHTS.get(x, 5),
        reverse=True
    )


def calculate_general_strength(user_skills):
    total = sum(SKILL_WEIGHTS.get(skill, 5) for skill in user_skills)
    return min(int(total / 4), 95)


def calculate_skill_depth(frequency):
    depth = {}
    for skill, count in frequency.items():
        if count >= 3:
            depth[skill] = "Advanced"
        elif count == 2:
            depth[skill] = "Intermediate"
        else:
            depth[skill] = "Basic"
    return depth


def detect_best_role(user_skills):
    scores = {}
    for role, required in ROLES.items():
        scores[role] = len(set(user_skills) & set(required))
    best = max(scores, key=scores.get)
    return best, scores


def detect_strong_domain(user_skills):
    scores = {}
    for domain, skills in DOMAIN_MAP.items():
        scores[domain] = len(set(user_skills) & set(skills))
    strongest = max(scores, key=scores.get)
    return strongest, scores


def detect_missing_for_role(role, user_skills):
    required = ROLES.get(role, [])
    return [skill for skill in required if skill not in user_skills]


def calculate_resume_complexity(user_skills):
    count = len(user_skills)
    if count > 12:
        return "Highly Diversified Profile"
    elif count > 8:
        return "Balanced Technical Profile"
    elif count > 4:
        return "Focused Skill Profile"
    else:
        return "Emerging Skill Profile"


def calculate_market_alignment(user_skills):
    market_score = sum(SKILL_WEIGHTS.get(skill, 5) for skill in user_skills)
    return min(int(market_score / 3), 95)


def calculate_risk_index(missing_count):
    if missing_count == 0:
        return "Low Strategic Risk"
    elif missing_count <= 2:
        return "Moderate Competitive Risk"
    elif missing_count <= 4:
        return "High Competitive Risk"
    else:
        return "Critical Skill Gap Risk"


def placement_probability(general_strength):
    if general_strength > 80:
        return "Very High (80–90%)"
    elif general_strength > 60:
        return "Good (60–75%)"
    elif general_strength > 40:
        return "Moderate (40–60%)"
    else:
        return "Needs Improvement (<40%)"


def generate_roadmap(role, missing):
    return {
        "week1": f"Strengthen fundamentals of {', '.join(missing[:2])}" if missing else "Refine core strengths",
        "week2": f"Build an advanced {role} level project",
        "week3": "Practice system design & DSA",
        "week4": "Mock interviews + resume optimization"
    }


def career_alignment_analysis(strongest_domain, best_role):
    if strongest_domain not in best_role:
        return f"Your strongest domain is {strongest_domain}, consider aligning career strategy accordingly."
    return "Your career alignment is strategically consistent."


def run_orchestrator(user_skills, frequency):

    ranked = rank_user_skills(user_skills)
    general_strength = calculate_general_strength(user_skills)
    skill_depth = calculate_skill_depth(frequency)

    best_role, role_scores = detect_best_role(user_skills)
    strongest_domain, domain_scores = detect_strong_domain(user_skills)
    missing = detect_missing_for_role(best_role, user_skills)

    roadmap = generate_roadmap(best_role, missing)
    complexity = calculate_resume_complexity(user_skills)
    market_score = calculate_market_alignment(user_skills)
    risk_index = calculate_risk_index(len(missing))
    placement = placement_probability(general_strength)
    pivot = career_alignment_analysis(strongest_domain, best_role)

    return {
        "ranked_skills": ranked,
        "top_3_skills": ranked[:3],
        "skill_depth_breakdown": skill_depth,
        "resume_complexity": complexity,
        "strongest_domain": strongest_domain,
        "recommended_role": best_role,
        "missing_skills_for_best_role": missing,
        "risk_index": risk_index,
        "market_alignment_score": market_score,
        "general_strength_score": general_strength,
        "placement_probability_estimate": placement,
        "career_alignment_analysis": pivot,
        "role_match_breakdown": role_scores,
        "domain_strength_breakdown": domain_scores,
        "roadmap": roadmap
    }
