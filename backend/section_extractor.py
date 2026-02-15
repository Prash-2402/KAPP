import re
from typing import Dict, List, Tuple


class SectionExtractor:
    """
    Advanced resume section extraction with intelligent pattern matching.
    Handles messy, unstructured resumes with multiple formats.
    """
    
    # Section header patterns (case-insensitive, flexible)
    SECTION_PATTERNS = {
        'objective': r'(?:objective|summary|profile|about\s*me|professional\s*summary|career\s*objective)',
        'projects': r'(?:projects?|portfolio|work\s*samples?|personal\s*projects?)',
        'experience': r'(?:experience|work\s*history|employment|professional\s*experience|work\s*experience)',
        'education': r'(?:education|academic|qualifications?|degrees?)',
        'skills': r'(?:skills?|technical\s*skills?|technologies|competencies)',
        'certifications': r'(?:certifications?|certificates?|licenses?)',
        'achievements': r'(?:achievements?|awards?|accomplishments?|honors?)'
    }
    
    def __init__(self, text: str):
        self.text = text.lower()
        self.original_text = text  # Keep case for extraction
        self.lines = [line.strip() for line in text.split('\n') if line.strip()]
        
    def extract_all_sections(self) -> Dict:
        """Extract all sections from resume."""
        sections = {}
        
        # Find section boundaries
        section_indices = self._find_section_boundaries()
        
        # Extract each section
        for section_name, (start, end) in section_indices.items():
            sections[section_name] = self._extract_section_content(start, end)
        
        # Parse projects
        projects_data = self._parse_projects(sections.get('projects', ''))
        
        # CRITICAL FIX: If no projects, extract from experience bullets
        # Essential for SAP ABAP/Enterprise professionals
        if not projects_data or len(projects_data) == 0:
            projects_data = self._extract_projects_from_experience(sections.get('experience', ''))
        
        # Parse structured data from sections
        return {
            'objective': self._parse_objective(sections.get('objective', '')),
            'projects': projects_data,
            'experience': self._parse_experience(sections.get('experience', '')),
            'education': self._parse_education(sections.get('education', '')),
            'skills': self._parse_skills(sections.get('skills', '')),
            'certifications': sections.get('certifications', ''),
            'achievements': sections.get('achievements', ''),
            'raw_sections': sections
        }
    
    def _find_section_boundaries(self) -> Dict[str, Tuple[int, int]]:
        """Find start and end line indices for each section."""
        boundaries = {}
        section_starts = []
        
        # Find all section headers
        for i, line in enumerate(self.lines):
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line.lower()):
                    section_starts.append((i, section_name))
                    break
        
        # Calculate boundaries
        for i, (start, name) in enumerate(section_starts):
            if i < len(section_starts) - 1:
                end = section_starts[i + 1][0]
            else:
                end = len(self.lines)
            boundaries[name] = (start + 1, end)  # +1 to skip header
        
        return boundaries
    
    def _extract_section_content(self, start: int, end: int) -> str:
        """Extract text content between line indices."""
        return '\n'.join(self.lines[start:end])
    
    def _parse_objective(self, text: str) -> Dict:
        """Extract career intent and preferences from objective/summary."""
        if not text:
            return {'text': '', 'career_keywords': [], 'passion_signals': []}
        
        # Career keywords
        career_keywords = []
        career_patterns = [
            r'seeking\s+(\w+(?:\s+\w+){0,3})\s+(?:role|position)',
            r'interested\s+in\s+(\w+(?:\s+\w+){0,3})',
            r'passionate\s+about\s+(\w+(?:\s+\w+){0,3})',
            r'aspiring\s+(\w+(?:\s+\w+){0,3})',
            r'looking\s+for\s+(\w+(?:\s+\w+){0,3})\s+(?:role|position|opportunity)'
        ]
        
        for pattern in career_patterns:
            matches = re.findall(pattern, text.lower())
            career_keywords.extend(matches)
        
        # Passion signals
        passion_words = ['passionate', 'enthusiastic', 'love', 'excited', 'driven', 'dedicated']
        passion_signals = [word for word in passion_words if word in text.lower()]
        
        return {
            'text': text,
            'career_keywords': list(set(career_keywords)),
            'passion_signals': passion_signals
        }
    
    def _parse_projects(self, text: str) -> List[Dict]:
        """
        Parse projects with advanced pattern matching.
        Handles various formats: bullet points, paragraphs, mixed.
        """
        if not text:
            return []
        
        projects = []
        current_project = None
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect project title (typically bold, capitalized, or has certain patterns)
            # Heuristics: Title if (a) all caps, (b) title case, (c) followed by description
            is_title = (
                len(line) < 80 and  # Not too long
                (line.isupper() or line.istitle() or 
                 re.match(r'^[\w\s\-]+(?:\([\w\s,]+\))?$', line))  # Simple format
            )
            
            if is_title and current_project:
                # Save previous project
                projects.append(current_project)
                current_project = {'title': line, 'description': '', 'technologies': []}
            elif is_title:
                # Start new project
                current_project = {'title': line, 'description': '', 'technologies': []}
            elif current_project:
                # Add to description
                current_project['description'] += line + ' '
        
        # Save last project
        if current_project:
            projects.append(current_project)
        
        # If no projects detected, treat entire text as single project
        if not projects and text:
            projects = [{'title': 'Project', 'description': text, 'technologies': []}]
        
        # Extract technologies from descriptions
        for project in projects:
            project['technologies'] = self._extract_technologies_from_text(project['description'])
            project['description'] = project['description'].strip()
        
        return projects
    
    def _parse_experience(self, text: str) -> List[Dict]:
        """Parse work experience entries."""
        if not text:
            return []
        
        experiences = []
        lines = text.split('\n')
        current_exp = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect company/role header (heuristic: short line, title case)
            if len(line) < 100 and (line.istitle() or '|' in line or '–' in line):
                if current_exp:
                    experiences.append(current_exp)
                current_exp = {'header': line, 'description': ''}
            elif current_exp:
                current_exp['description'] += line + ' '
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _parse_education(self, text: str) -> List[Dict]:
        """Parse education entries."""
        if not text:
            return []
        
        # Look for degree patterns
        degree_pattern = r'(b\.?s\.?|m\.?s\.?|b\.?tech|m\.?tech|bachelor|master|phd|b\.?e\.?|m\.?e\.?)'
        institutions = []
        
        lines = text.split('\n')
        for line in lines:
            if re.search(degree_pattern, line.lower()):
                institutions.append(line.strip())
        
        return institutions if institutions else [text.strip()]
    
    def _parse_skills(self, text: str) -> List[str]:
        """Extract skills from skills section."""
        # Split by common delimiters
        skills = re.split(r'[,;|•\n]', text)
        return [s.strip() for s in skills if s.strip() and len(s.strip()) > 1]
    
    def _extract_projects_from_experience(self, text: str) -> List[Dict]:
        """
        CRITICAL FALLBACK: Extract pseudo-projects from experience bullet points.
        Essential for SAP ABAP, enterprise professionals who list deliverables as bullets.
        """
        if not text:
            return []
        
        projects = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and short headers
            if not line or len(line) < 30:
                continue
            
            # Bullet point indicators
            if line.startswith(('•', '-', '*', '●', '◦')):
                line = line[1:].strip()
            
            # Each substantial bullet = a "project" or deliverable
            # Extract title (first 60 chars or until period)
            title_match = re.match(r'^([^.!?]{10,80})', line)
            title = title_match.group(1).strip() if title_match else line[:60]
            
            projects.append({
                'title': title,
                'description': line,
                'technologies': self._extract_technologies_from_text(line)
            })
        
        # Limit to max 10 most substantial projects
        projects.sort(key=lambda x: len(x['description']), reverse=True)
        return projects[:10]
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technology names from free text using common patterns."""
        # Common tech patterns (programming languages, frameworks, tools)
        tech_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'express', 'django', 'flask', 'fastapi', 'spring', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'mongodb', 'postgresql', 'mysql',
            'redis', 'kafka', 'git', 'jenkins', 'terraform', 'ansible'
        ]
        
        found = []
        text_lower = text.lower()
        for tech in tech_keywords:
            if tech in text_lower:
                found.append(tech.title())
        
        return list(set(found))


def extract_resume_sections(text: str) -> Dict:
    """Main function to extract all sections from resume text."""
    extractor = SectionExtractor(text)
    return extractor.extract_all_sections()
