"""
Advanced Project Analysis Agent
Evaluates projects across 12+ dimensions for accurate capability assessment.
"""

import re
from typing import Dict, List
from skills import SKILLS_LIST


class ProjectAnalyzer:
    """
    Sophisticated multi-dimensional project analysis.
    Goes beyond simple keyword counting to understand actual capability.
    """
    
    # Complexity indicators with weights
    COMPLEXITY_INDICATORS = {
        # Architecture & Scale
        'microservices': 10, 'distributed': 10, 'scalable': 9, 'load balancing': 9,
        'high availability': 9, 'fault tolerant': 9, 'real-time': 8,
        'event-driven': 8, 'message queue': 8, 'caching': 7,
        
        # Scale indicators
        '1000+ users': 10, '10000+ users': 10, 'thousands': 9, 'production': 9,
        'enterprise': 9, 'million': 10, 'concurrent': 8, 'high traffic': 9,
        
        # Advanced patterns
        'ml model': 9, 'machine learning': 9, 'deep learning': 10, 'neural network': 10,
        'ci/cd': 8, 'devops': 7, 'containerized': 8, 'orchestration': 9,
        'authentication': 6, 'authorization': 6, 'api gateway': 8,
        
        # Database sophistication
        'nosql': 7, 'sharding': 9, 'replication': 8, 'indexing': 7,
        'transactions': 7, 'acid': 8, 'database design': 7,
        
        # Testing & Quality
        'unit test': 6, 'integration test': 7, 'e2e': 7, 'test coverage': 7,
        'automated': 6, 'monitoring': 7, 'logging': 6,
        
        # Security
        'oauth': 7, 'jwt': 7, 'encryption': 8, 'security': 6, 'ssl': 6,
        
        # Performance
        'optimized': 7, 'performance': 6, 'caching': 7, 'cdn': 7,
        'lazy loading': 6, 'async': 6, 'multithreading': 8
    }
    
    # Impact indicators
    IMPACT_INDICATORS = {
        'reduced cost': 10, 'increased revenue': 10, 'saved time': 8,
        'improved': 7, 'optimized': 7, 'enhanced': 6,
        'deployed': 8, 'live': 8, 'production': 9,
        'open source': 7, 'github': 5, 'published': 8,
        'award': 9, 'recognition': 8, 'featured': 8
    }
    
    # Leadership indicators
    LEADERSHIP_INDICATORS = {
        'led': 10, 'managed': 9, 'architected': 10, 'designed': 8,
        'coordinated': 8, 'mentored': 9, 'team': 6, 'collaborated': 5
    }
    
    # Solo project indicators (lower value, but still valid experience)
    SOLO_INDICATORS = {
        'personal project': 3, 'side project': 3, 'built': 4, 'created': 4,
        'developed': 4, 'implemented': 5
    }
    
    def __init__(self, projects: List[Dict], all_text: str):
        """
        Args:
            projects: List of project dicts from section_extractor
            all_text: Full resume text for context
        """
        self.projects = projects
        self.all_text = all_text.lower()
        
    def analyze_all_projects(self) -> Dict:
        """Comprehensive analysis of all projects."""
        if not self.projects:
            return self._empty_analysis()
        
        analyzed_projects = []
        for project in self.projects:
            analyzed_projects.append(self._analyze_single_project(project))
        
        # Aggregate insights
        return self._aggregate_analysis(analyzed_projects)
    
    def _analyze_single_project(self, project: Dict) -> Dict:
        """Deep analysis of a single project."""
        title = project.get('title', '')
        desc = project.get('description', '')
        combined = f"{title} {desc}".lower()
        
        # 1. Complexity scoring (1-10)
        complexity = self._calculate_complexity(combined)
        
        # 2. Impact detection
        impact_score = self._calculate_impact(combined)
        
        # 3. Role identification
        role_type, role_score = self._identify_role(combined)
        
        # 4. Technology extraction and depth
        technologies = self._extract_technologies(combined)
        
        # 5. Recency indicators
        is_recent = self._detect_recency(combined)
        
        # 6. Scope detection
        scope = self._detect_scope(combined)
        
        return {
            'title': title,
            'description': desc[:200],  # Truncate for storage
            'complexity_score': complexity,
            'impact_score': impact_score,
            'role_type': role_type,
            'role_score': role_score,
            'technologies': technologies,
            'is_recent': is_recent,
            'scope': scope,
            'overall_quality': self._calculate_quality(complexity, impact_score, role_score)
        }
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate project complexity on 1-10 scale."""
        score = 0
        matched_indicators = []
        
        for indicator, weight in self.COMPLEXITY_INDICATORS.items():
            if indicator in text:
                score += weight
                matched_indicators.append(indicator)
        
        # Normalize to 1-10 scale
        # Max realistic score ~50-60 for very complex project
        normalized = min(10, (score / 5) + 1)
        
        # Bonus for multiple tech stacks
        tech_count = len(self._extract_technologies(text))
        if tech_count > 5:
            normalized = min(10, normalized + 1)
        if tech_count > 10:
            normalized = min(10, normalized + 1)
        
        return round(normalized, 1)
    
    def _calculate_impact(self, text: str) -> float:
        """Calculate project impact on 1-10 scale."""
        score = 0
        
        for indicator, weight in self.IMPACT_INDICATORS.items():
            if indicator in text:
                score += weight
        
        # Check for numbers (users, revenue, metrics)
        number_patterns = [
            r'(\d+k|\d+,\d+)\s*users',
            r'(\d+)%\s*(?:improvement|increase|reduction)',
            r'\$(\d+k|\d+m)',
            r'(\d+)\s*companies'
        ]
        
        for pattern in number_patterns:
            if re.search(pattern, text):
                score += 8
        
        # Normalize to 1-10
        normalized = min(10, (score / 4) + 1)
        return round(normalized, 1)
    
    def _identify_role(self, text: str) -> tuple:
        """Identify user's role: Leader, Contributor, Solo."""
        leadership_score = sum(
            weight for indicator, weight in self.LEADERSHIP_INDICATORS.items()
            if indicator in text
        )
        
        solo_score = sum(
            weight for indicator, weight in self.SOLO_INDICATORS.items()
            if indicator in text
        )
        
        team_keywords = ['team', 'collaborated', 'group']
        has_team = any(kw in text for kw in team_keywords)
        
        if leadership_score > 15:
            return 'Tech Lead', leadership_score
        elif leadership_score > 8:
            return 'Senior Contributor', leadership_score  
        elif has_team:
            return 'Team Contributor', 5
        elif solo_score > 8:
            return 'Solo Developer', solo_score
        else:
            return 'Developer', 4
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract all technologies mentioned in project."""
        found = []
        for skill in SKILLS_LIST:
            if skill.lower() in text:
                found.append(skill)
        return found
    
    def _detect_recency(self, text: str) -> bool:
        """Detect if project is recent (2022-2026)."""
        recent_years = ['2022', '2023', '2024', '2025', '2026', 'current', 'present', 'ongoing']
        return any(year in text for year in recent_years)
    
    def _detect_scope(self, text: str) -> str:
        """Detect project scope: Enterprise, Production, POC, Learning."""
        if any(kw in text for kw in ['enterprise', 'production', 'deployed', '1000+ users']):
            return 'Production/Enterprise'
        elif any(kw in text for kw in ['prototype', 'poc', 'proof of concept', 'mvp']):
            return 'Prototype/MVP'
        elif any(kw in text for kw in ['learning', 'tutorial', 'practice', 'course']):
            return 'Learning Project'
        else:
            return 'Standard Development'
    
    def _calculate_quality(self, complexity: float, impact: float, role_score: float) -> float:
        """Calculate overall project quality score."""
        # Weighted average
        quality = (complexity * 0.4) + (impact * 0.4) + (min(role_score / 10, 1) * 10 * 0.2)
        return round(quality, 1)
    
    def _aggregate_analysis(self, analyzed_projects: List[Dict]) -> Dict:
        """Aggregate insights from all projects."""
        total_projects = len(analyzed_projects)
        
        # Calculate averages
        avg_complexity = sum(p['complexity_score'] for p in analyzed_projects) / total_projects
        avg_impact = sum(p['impact_score'] for p in analyzed_projects) / total_projects
        avg_quality = sum(p['overall_quality'] for p in analyzed_projects) / total_projects
        
        # High-value projects (quality > 7)
        high_quality_projects = [p for p in analyzed_projects if p['overall_quality'] >= 7]
        
        # Technology frequency across all projects
        tech_frequency = {}
        tech_to_projects = {}
        tech_max_complexity = {}
        
        for project in analyzed_projects:
            for tech in project['technologies']:
                tech_frequency[tech] = tech_frequency.get(tech, 0) + 1
                
                if tech not in tech_to_projects:
                    tech_to_projects[tech] = []
                tech_to_projects[tech].append(project['title'])
                
                current_max = tech_max_complexity.get(tech, 0)
                tech_max_complexity[tech] = max(current_max, project['complexity_score'])
        
        # Determine strongest project domain
        domain_scores = self._calculate_domain_scores(analyzed_projects)
        strongest_domain = max(domain_scores, key=domain_scores.get) if domain_scores else 'General'
        
        # Leadership experience
        leadership_projects = [p for p in analyzed_projects if p['role_type'] in ['Tech Lead', 'Senior Contributor']]
        
        return {
            'total_projects': total_projects,
            'avg_complexity': round(avg_complexity, 1),
            'avg_impact': round(avg_impact, 1),
            'avg_quality': round(avg_quality, 1),
            'high_quality_count': len(high_quality_projects),
            'strongest_project_domain': strongest_domain,
            'domain_scores': domain_scores,
            'tech_frequency': tech_frequency,
            'tech_to_projects': tech_to_projects,
            'tech_max_complexity': tech_max_complexity,
            'leadership_experience': len(leadership_projects) > 0,
            'leadership_project_count': len(leadership_projects),
            'recent_projects': sum(1 for p in analyzed_projects if p['is_recent']),
            'detailed_projects': analyzed_projects[:5],  # Top 5 for display
            'project_quality_distribution': self._get_quality_distribution(analyzed_projects)
        }
    
    def _calculate_domain_scores(self, projects: List[Dict]) -> Dict[str, float]:
        """Calculate domain strength based on projects."""
        from domain_map import DOMAIN_MAP
        
        domain_scores = {}
        
        for domain, skills in DOMAIN_MAP.items():
            score = 0
            for project in projects:
                project_domain_skills = set(project['technologies']) & set(skills)
                if project_domain_skills:
                    # Weight by project quality and number of matching skills
                    score += project['overall_quality'] * len(project_domain_skills)
            domain_scores[domain] = round(score, 1)
        
        return domain_scores
    
    def _get_quality_distribution(self, projects: List[Dict]) -> Dict:
        """Get distribution of project quality."""
        excellent = sum(1 for p in projects if p['overall_quality'] >= 8)
        good = sum(1 for p in projects if 6 <= p['overall_quality'] < 8)
        average = sum(1 for p in projects if 4 <= p['overall_quality'] < 6)
        below_avg = sum(1 for p in projects if p['overall_quality'] < 4)
        
        return {
            'excellent': excellent,  # 8-10
            'good': good,  # 6-8
            'average': average,  # 4-6
            'below_average': below_avg  # <4
        }
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure."""
        return {
            'total_projects': 0,
            'avg_complexity': 0,
            'avg_impact': 0,
            'avg_quality': 0,
            'high_quality_count': 0,
            'strongest_project_domain': 'Unknown',
            'domain_scores': {},
            'tech_frequency': {},
            'tech_to_projects': {},
            'tech_max_complexity': {},
            'leadership_experience': False,
            'leadership_project_count': 0,
            'recent_projects': 0,
            'detailed_projects': [],
            'project_quality_distribution': {'excellent': 0, 'good': 0, 'average': 0, 'below_average': 0}
        }


def analyze_projects(projects: List[Dict], full_resume_text: str) -> Dict:
    """Main function to analyze all projects."""
    analyzer = ProjectAnalyzer(projects, full_resume_text)
    return analyzer.analyze_all_projects()
