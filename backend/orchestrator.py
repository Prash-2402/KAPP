from roles import ROLES
from domain_map import DOMAIN_MAP
from skill_weights import SKILL_WEIGHTS


# ---------------------------------
# Rank skills by importance weight
# ---------------------------------
def rank_user_skills(user_skills):
    return sorted(
        user_skills,
        key=lambda x: SKILL_WEIGHTS.get(x, 5),
        reverse=True
    )


# ---------------------------------
# Depth-aware general strength score
# ---------------------------------
def calculate_general_strength(user_skills, frequency):
    if not user_skills:
        return 0

    total = 0

    for skill in user_skills:
        base_weight = SKILL_WEIGHTS.get(skill, 5)
        depth_multiplier = 1 + (frequency.get(skill, 1) * 0.2)
        total += base_weight * depth_multiplier

    average = total / len(user_skills)

    return min(int(average * 2.5), 85)


# ---------------------------------
# Skill depth classification
# ---------------------------------
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


# ---------------------------------
# Role detection
# ---------------------------------
def detect_best_role(user_skills):
    role_scores = {}

    for role, required in ROLES.items():
        role_scores[role] = len(set(user_skills) & set(required))

    best_role = max(role_scores, key=role_scores.get)
    return best_role, role_scores


# ---------------------------------
# Domain detection
# ---------------------------------
def detect_strong_domain(user_skills):
    domain_scores = {}

    for domain, skills in DOMAIN_MAP.items():
        domain_scores[domain] = len(set(user_skills) & set(skills))

    strongest_domain = max(domain_scores, key=domain_scores.get)
    return strongest_domain, domain_scores


# ---------------------------------
# Missing skills for role
# ---------------------------------
def detect_missing_for_role(role, user_skills):
    required = ROLES.get(role, [])
    return [skill for skill in required if skill not in user_skills]


# ---------------------------------
# Resume complexity
# ---------------------------------
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


# ---------------------------------
# Market alignment
# ---------------------------------
def calculate_market_alignment(user_skills):
    score = sum(SKILL_WEIGHTS.get(skill, 5) for skill in user_skills)
    return min(int(score / 2.2), 95)


# ---------------------------------
# Risk index
# ---------------------------------
def calculate_risk_index(missing_count):
    if missing_count == 0:
        return "Low Strategic Risk"
    elif missing_count <= 2:
        return "Moderate Competitive Risk"
    elif missing_count <= 4:
        return "High Competitive Risk"
    else:
        return "Critical Skill Gap Risk"


# ---------------------------------
# Placement probability
# ---------------------------------
def placement_probability(general_strength):
    if general_strength > 75:
        return "Very High (75–90%)"
    elif general_strength > 60:
        return "Good (60–75%)"
    elif general_strength > 50:
        return "Moderate (50–60%)"
    else:
        return "Needs Skill Strengthening (<50%)"


# ---------------------------------
# Career roadmap
# ---------------------------------
def generate_roadmap(role, missing):

    return {
        "week1": f"Strengthen fundamentals of {', '.join(missing[:2])}" if missing else "Refine core strengths",
        "week2": f"Build an advanced {role} level project",
        "week3": "Practice system design, scalability & DSA",
        "week4": "Mock interviews + resume refinement"
    }


# ---------------------------------
# Career alignment logic
# ---------------------------------
def career_alignment_analysis(strongest_domain, recommended_role):
    if strongest_domain not in recommended_role:
        return f"Your dominant expertise lies in {strongest_domain}. Strategic realignment may maximize growth."
    return "Your career alignment is strategically consistent."


# ---------------------------------
# Extraction confidence
# ---------------------------------
def extraction_confidence(user_skills):
    if len(user_skills) > 10:
        return "High Confidence Extraction"
    elif len(user_skills) > 6:
        return "Moderate Confidence Extraction"
    else:
        return "Low Confidence Extraction"


# ---------------------------------
# Domain-consistent synergy
# ---------------------------------
def detect_skill_synergy(domain_scores):

    if domain_scores.get("Frontend", 0) >= 3:
        return "Strong frontend engineering capability with UI stack consistency."

    if domain_scores.get("Data & AI", 0) >= 3:
        return "Strong AI/ML analytical foundation detected."

    if domain_scores.get("Backend", 0) >= 3:
        return "Strong backend architectural foundation detected."

    if domain_scores.get("DevOps & Cloud", 0) >= 2:
        return "Foundational cloud & deployment capability detected."

    return "Cross-domain exposure detected without strong specialization cluster."


# =================================
# MASTER ENGINE
# =================================
def run_orchestrator(user_skills, frequency):

    ranked_skills = rank_user_skills(user_skills)

    general_strength = calculate_general_strength(user_skills, frequency)
    skill_depth = calculate_skill_depth(frequency)

    recommended_role, role_scores = detect_best_role(user_skills)
    strongest_domain, domain_scores = detect_strong_domain(user_skills)

    missing_skills = detect_missing_for_role(recommended_role, user_skills)

    roadmap = generate_roadmap(recommended_role, missing_skills)
    complexity = calculate_resume_complexity(user_skills)
    market_alignment = calculate_market_alignment(user_skills)
    risk_index = calculate_risk_index(len(missing_skills))
    placement = placement_probability(general_strength)
    alignment_comment = career_alignment_analysis(strongest_domain, recommended_role)
    confidence = extraction_confidence(user_skills)
    synergy = detect_skill_synergy(domain_scores)

    competitive_summary = (
        f"You are positioned within the {placement} tier for {strongest_domain} domain roles."
    )

    return {
        "ranked_skills": ranked_skills,
        "top_3_skills": ranked_skills[:3],
        "skill_depth_breakdown": skill_depth,
        "resume_complexity": complexity,
        "strongest_domain": strongest_domain,
        "recommended_role": recommended_role,
        "missing_skills_for_best_role": missing_skills,
        "risk_index": risk_index,
        "market_alignment_score": market_alignment,
        "general_strength_score": general_strength,
        "placement_probability_estimate": placement,
        "career_alignment_analysis": alignment_comment,
        "competitive_summary": competitive_summary,
        "skill_synergy_analysis": synergy,
        "extraction_confidence": confidence,
        "role_match_breakdown": role_scores,
        "domain_strength_breakdown": domain_scores,
        "roadmap": roadmap
    }
