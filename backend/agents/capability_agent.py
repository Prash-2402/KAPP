"""
Advanced Capability Assessment Agent
Multi-dimensional skill depth analysis based on evidence, not just frequency.
"""

from typing import Dict, List


class CapabilityScorer:
    """
    Evidence-based capability assessment.
    Analyzes actual usage in projects, complexity, and role to determine true skill mastery.
    """
    
    # Capability levels with score ranges
    CAPABILITY_LEVELS = {
        'NOVICE': (1, 3),        # Mentioned, minimal usage
        'BEGINNER': (3, 5),      # Used in 1-2 simple projects
        'INTERMEDIATE': (5, 7),  # Multiple projects, moderate complexity
        'ADVANCED': (7, 9),      # Complex projects, primary technology
        'EXPERT': (9, 10)        # High-impact projects, mastery evident
    }
    
    def __init__(self, project_analysis: Dict, skill_frequency: Dict):
        """
        Args:
            project_analysis: Output from ProjectAnalyzer
            skill_frequency: Skill mention counts from initial extraction
        """
        self.project_analysis = project_analysis
        self.skill_frequency = skill_frequency
        self.tech_to_projects = project_analysis.get('tech_to_projects', {})
        self.tech_max_complexity = project_analysis.get('tech_max_complexity', {})
        
    def assess_all_capabilities(self) -> Dict:
        """Calculate capability scores for all detected skills."""
        capability_scores = {}
        
        for skill in self.skill_frequency.keys():
            capability_scores[skill] = self._assess_single_skill(skill)
        
        # Identify top skills by capability
        top_capabilities = sorted(
            capability_scores.items(),
            key=lambda x: x[1]['capability_score'],
            reverse=True
        )[:10]
        
        return {
            'detailed_capabilities': capability_scores,
            'top_capabilities': dict(top_capabilities),
            'expert_skills': [s for s, data in capability_scores.items() 
                            if data['capability_level'] == 'EXPERT'],
            'advanced_skills': [s for s, data in capability_scores.items() 
                              if data['capability_level'] in ['ADVANCED', 'EXPERT']],
            'developing_skills': [s for s, data in capability_scores.items() 
                                if data['capability_level'] in ['BEGINNER', 'INTERMEDIATE']],
            'overall_capability_strength': self._calculate_overall_strength(capability_scores)
        }
    
    def _assess_single_skill(self, skill: str) -> Dict:
        """Deep assessment of a single skill."""
        # CRITICAL FIX: Frequency is NOT expertise!
        # Complexity and role context matter WAY more than mention count
        
        # Factor 1: Mention frequency (5% weight - REDUCED from 20%)
        # Just confirms skill is relevant, doesn't indicate mastery
        mention_score = min(self.skill_frequency.get(skill, 0) * 2, 10)
        
        # Factor 2: Project count (20% weight)
        project_count = len(self.tech_to_projects.get(skill, []))
        project_score = min(project_count * 2.5, 10)
        
        # Factor 3: Max project complexity (50% weight - INCREASED from 35%)
        # THIS IS THE REAL INDICATOR OF EXPERTISE
        max_complexity = self.tech_max_complexity.get(skill, 0)
        complexity_score = max_complexity
        
        # If no complexity data but skill is detected, assume moderate complexity
        if complexity_score == 0 and skill in self.skill_frequency:
            complexity_score = 5  # Default assumption - better than 0
        
        # Factor 4: Project role analysis (25% weight - INCREASED from 20%)
        # How skill was used matters more than how often mentioned
        role_score = self._calculate_role_score(skill)
        
        # REVISED WEIGHTS: Complexity + Role = 75% (was 55%)
        capability_score = (
            mention_score * 0.05 +      # Just 5%
            project_score * 0.20 +      # 20%
            complexity_score * 0.50 +   # 50% - MOST IMPORTANT
            role_score * 0.25           # 25%
        )
        
        # Determine capability level
        capability_level = self._score_to_level(capability_score)
        
        # Evidence gathering
        evidence = {
            'mentions': self.skill_frequency.get(skill, 0),
            'project_count': project_count,
            'projects': self.tech_to_projects.get(skill, [])[:3],  # Top 3
            'max_complexity': max_complexity,
            'role_context': self._get_role_context(skill)
        }
        
        return {
            'capability_score': round(capability_score, 1),
            'capability_level': capability_level,
            'mention_score': round(mention_score, 1),
            'project_score': round(project_score, 1),
            'complexity_score': round(complexity_score, 1),
            'role_score': round(role_score, 1),
            'evidence': evidence,
            'confidence': self._calculate_confidence(evidence)
        }
    
    def _calculate_role_score(self, skill: str) -> float:
        """Analyze how the skill was used (primary tech, supporting, mentioned)."""
        # Check if skill appears in high-quality projects
        detailed_projects = self.project_analysis.get('detailed_projects', [])
        
        primary_tech_count = 0
        supporting_tech_count = 0
        
        for project in detailed_projects:
            if skill in project.get('technologies', []):
                # If it's in title or early in description → primary
                title = project.get('title', '').lower()
                desc = project.get('description', '').lower()
                
                if skill.lower() in title or desc.find(skill.lower()) < 100:
                    primary_tech_count += 1
                else:
                    supporting_tech_count += 1
        
        # Score: Primary tech = higher score
        score = (primary_tech_count * 3) + (supporting_tech_count * 1)
        return min(score, 10)
    
    def _get_role_context(self, skill: str) -> str:
        """Determine if skill was used as primary tech, supporting, or mentioned."""
        detailed_projects = self.project_analysis.get('detailed_projects', [])
        
        for project in detailed_projects:
            if skill in project.get('technologies', []):
                title = project.get('title', '').lower()
                if skill.lower() in title:
                    return 'Primary Technology'
        
        if len(self.tech_to_projects.get(skill, [])) > 2:
            return 'Core Technology'
        elif len(self.tech_to_projects.get(skill, [])) > 0:
            return 'Supporting Technology'
        else:
            return 'Mentioned'
    
    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to capability level."""
        if score >= 9:
            return 'EXPERT'
        elif score >= 7:
            return 'ADVANCED'
        elif score >= 5:
            return 'INTERMEDIATE'
        elif score >= 3:
            return 'BEGINNER'
        else:
            return 'NOVICE'
    
    def _calculate_confidence(self, evidence: Dict) -> str:
        """Calculate confidence in the assessment."""
        project_count = evidence['project_count']
        mentions = evidence['mentions']
        
        if project_count >= 3 and mentions >= 5:
            return 'HIGH'
        elif project_count >= 2 or mentions >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_overall_strength(self, capabilities: Dict) -> float:
        """Calculate overall capability strength score."""
        if not capabilities:
            return 0
        
        # Weight expert/advanced skills more heavily
        total_weighted_score = 0
        total_weight = 0
        
        for skill, data in capabilities.items():
            level = data['capability_level']
            score = data['capability_score']
            
            if level == 'EXPERT':
                weight = 1.5
            elif level == 'ADVANCED':
                weight = 1.2
            else:
                weight = 1.0
            
            total_weighted_score += score * weight
            total_weight += weight
        
        overall = (total_weighted_score / total_weight) if total_weight > 0 else 0
        return round(overall, 1)


def assess_capabilities(project_analysis: Dict, skill_frequency: Dict) -> Dict:
    """Main function for capability assessment."""
    scorer = CapabilityScorer(project_analysis, skill_frequency)
    return scorer.assess_all_capabilities()
