import './AnalysisResults.css';
import { BarChart, Bar, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import CountUp from 'react-countup';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { motion } from 'framer-motion';

const AnalysisResults = ({ data, onReset }) => {
    const { analysis, detected_skills, project_analysis, capability_analysis, resume_grade } = data;

    if (!analysis) {
        return <div className="container">No analysis data available</div>;
    }

    // Check if we have advanced analysis
    const hasAdvancedAnalysis = project_analysis && capability_analysis && resume_grade;

    const getRiskColor = (risk) => {
        if (risk.includes('Low')) return 'success';
        if (risk.includes('Moderate')) return 'warning';
        return 'danger';
    };

    // PDF Export Handler
    const handleExportPDF = async () => {
        const element = document.getElementById('results-content');
        const canvas = await html2canvas(element, { scale: 2 });
        const imgData = canvas.toDataURL('image/png');

        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('KAPP_Career_Analysis.pdf');
    };

    // Prepare chart data
    const domainChartData = Object.entries(analysis.domain_strength_breakdown)
        .sort(([, a], [, b]) => b - a)
        .map(([domain, score]) => ({ name: domain, value: score }));

    const roleChartData = Object.entries(analysis.role_match_breakdown)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .map(([role, score]) => ({ name: role, value: score }));

    const colors = ['#00FFD1', '#00D4FF', '#8B5CF6', '#FFD700', '#FF006E'];

    return (
        <div className="results-page">
            <div className="container" id="results-content">
                {/* Header */}
                <header className="results-header fade-in">
                    <h1>YOUR CAREER ANALYSIS</h1>
                    <p className="subtitle">The analysis is complete. Your optimal career path has been identified.</p>
                    <div className="header-buttons">
                        <button className="btn btn-export" onClick={handleExportPDF}>📄 Export to PDF</button>
                        <button className="btn" onClick={onReset}>Analyze Another Resume</button>
                    </div>
                </header>

                {/* Main Stats */}
                <div className="stats-grid fade-in">
                    <div className="stat-card primary">
                        <div className="stat-value">
                            <CountUp end={analysis.general_strength_score} duration={2} suffix="%" />
                        </div>
                        <div className="stat-label">General Strength Score</div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${analysis.general_strength_score}%` }}
                            ></div>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-value">
                            <CountUp end={analysis.market_alignment_score} duration={2} suffix="%" />
                        </div>
                        <div className="stat-label">Market Alignment</div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${analysis.market_alignment_score}%` }}
                            ></div>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">🎯</div>
                        <div className="stat-label">Recommended Role</div>
                        <div className="stat-text">{analysis.recommended_role}</div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">🌍</div>
                        <div className="stat-label">Strongest Domain</div>
                        <div className="stat-text">{analysis.strongest_domain}</div>
                    </div>
                </div>

                {/* Resume Grade Section - AI-POWERED */}
                {hasAdvancedAnalysis && (
                    <div className="card fade-in primary-card" style={{ background: 'linear-gradient(135deg, rgba(139,92,246,0.2), rgba(0,255,209,0.2))', backdropFilter: 'blur(20px)', border: '2px solid #00FFD1' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                            <h2 style={{ margin: 0 }}>📊 RESUME QUALITY GRADE</h2>
                            {resume_grade.ai_powered && (
                                <div style={{
                                    padding: '6px 16px',
                                    borderRadius: '20px',
                                    background: 'linear-gradient(135deg, #00FFD1, #00D4FF)',
                                    fontSize: '12px',
                                    fontWeight: 'bold',
                                    color: '#000',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '6px'
                                }}>
                                    🤖 AI-POWERED
                                </div>
                            )}
                        </div>
                        <div className="divider"></div>
                        <div className="grid grid-2" style={{ marginTop: '20px' }}>
                            <div style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: '80px', fontWeight: 'bold', color: '#FFD700', textShadow: '0 0 30px rgba(255,215,0,0.6)' }}>
                                    {resume_grade.letter_grade}
                                </div>
                                <div style={{ fontSize: '18px', color: '#00FFD1', marginTop: '10px' }}>
                                    Score: <CountUp end={resume_grade.overall_score} duration={2} decimals={1} /> / 100
                                </div>
                                <div style={{ fontSize: '14px', color: '#8B5CF6', marginTop: '5px' }}>
                                    {resume_grade.grade_description}
                                </div>
                            </div>
                            <div>
                                <div style={{ marginBottom: '15px' }}>
                                    <div style={{ fontSize: '16px', color: '#00FFD1', fontWeight: 'bold', marginBottom: '5px' }}>
                                        🏆 Market Tier
                                    </div>
                                    <div style={{ fontSize: '14px', color: '#fff' }}>
                                        {resume_grade.market_tier}
                                    </div>
                                </div>
                                <div style={{ marginBottom: '15px' }}>
                                    <div style={{ fontSize: '16px', color: '#00FFD1', fontWeight: 'bold', marginBottom: '5px' }}>
                                        📈 Percentile Rank
                                    </div>
                                    <div style={{ fontSize: '14px', color: '#FFD700' }}>
                                        {resume_grade.percentile_rank}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Component Scores */}
                        <h3 style={{ marginTop: '30px', color: '#00FFD1' }}>Score Breakdown</h3>
                        <div className="grid grid-2" style={{ gap: '10px', marginTop: '15px' }}>
                            {Object.entries(resume_grade.component_scores).map(([component, score]) => (
                                <div key={component} style={{ background: 'rgba(0,0,0,0.3)', padding: '15px', borderRadius: '12px', border: '1px solid rgba(0,255,209,0.3)' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <span style={{ fontSize: '13px', textTransform: 'capitalize', color: '#00D4FF' }}>
                                            {component.replace(/_/g, ' ')}
                                        </span>
                                        <span style={{ fontSize: '16px', fontWeight: 'bold', color: score >= 75 ? '#00FFD1' : score >= 50 ? '#FFD700' : '#FF006E' }}>
                                            {score}
                                        </span>
                                    </div>
                                    <div className="progress-bar" style={{ marginTop: '8px', height: '6px' }}>
                                        <div className="progress-fill" style={{ width: `${score}%`, background: score >= 75 ? '#00FFD1' : score >= 50 ? '#FFD700' : '#FF006E' }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* AI Justification */}
                        {resume_grade.ai_powered && resume_grade.justification && (
                            <div style={{ marginTop: '25px', padding: '20px', background: 'rgba(0,255,209,0.1)', borderRadius: '12px', border: '1px solid rgba(0,255,209,0.3)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                                    <span style={{ fontSize: '18px' }}>🤖</span>
                                    <h3 style={{ margin: 0, color: '#00FFD1' }}>AI Analysis</h3>
                                </div>
                                <p style={{ fontSize: '14px', color: '#fff', lineHeight: '1.6', margin: 0 }}>
                                    {resume_grade.justification}
                                </p>
                            </div>
                        )}

                        {/* Improvement Areas */}
                        {resume_grade.improvement_areas && resume_grade.improvement_areas.length > 0 && (
                            <div style={{ marginTop: '25px', padding: '15px', background: 'rgba(255,215,0,0.1)', borderRadius: '12px', border: '1px solid rgba(255,215,0,0.3)' }}>
                                <h4 style={{ color: '#FFD700', marginBottom: '10px' }}>💡 Areas for Improvement</h4>
                                <ul style={{ paddingLeft: '20px', color: '#fff' }}>
                                    {resume_grade.improvement_areas.map((area, idx) => (
                                        <li key={idx} style={{ marginBottom: '5px', fontSize: '14px' }}>{area}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}



                {/* Capability Assessment Section - NEW */}
                {hasAdvancedAnalysis && capability_analysis.top_capabilities && (
                    <div className="card fade-in">
                        <h2>💪 SKILL CAPABILITY ASSESSMENT</h2>
                        <div className="divider"></div>
                        <p style={{ marginBottom: '20px', color: '#00D4FF' }}>
                            Evidence-based skill mastery levels (not just counts)
                        </p>

                        {/* Top Capabilities */}
                        <div style={{ display: 'grid', gap: '12px' }}>
                            {Object.entries(capability_analysis.top_capabilities).slice(0, 8).map(([skill, data]) => (
                                <div key={skill} style={{
                                    padding: '15px',
                                    background: 'rgba(0,0,0,0.3)',
                                    borderRadius: '12px',
                                    border: `2px solid ${data.capability_level === 'EXPERT' ? '#FFD700' :
                                        data.capability_level === 'ADVANCED' ? '#00FFD1' :
                                            data.capability_level === 'INTERMEDIATE' ? '#8B5CF6' : '#00D4FF'
                                        }`
                                }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                                        <div>
                                            <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#fff' }}>{skill}</span>
                                            <span style={{
                                                marginLeft: '12px',
                                                padding: '4px 12px',
                                                borderRadius: '20px',
                                                fontSize: '12px',
                                                fontWeight: 'bold',
                                                background: data.capability_level === 'EXPERT' ? 'rgba(255,215,0,0.2)' :
                                                    data.capability_level === 'ADVANCED' ? 'rgba(0,255,209,0.2)' :
                                                        data.capability_level === 'INTERMEDIATE' ? 'rgba(139,92,246,0.2)' : 'rgba(0,212,255,0.2)',
                                                color: data.capability_level === 'EXPERT' ? '#FFD700' :
                                                    data.capability_level === 'ADVANCED' ? '#00FFD1' :
                                                        data.capability_level === 'INTERMEDIATE' ? '#8B5CF6' : '#00D4FF'
                                            }}>
                                                {data.capability_level}
                                            </span>
                                        </div>
                                        <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#00FFD1' }}>
                                            {data.capability_score.toFixed(1)}/10
                                        </div>
                                    </div>

                                    {/* Evidence */}
                                    <div style={{ display: 'flex', gap: '15px', fontSize: '12px', color: '#8B5CF6', marginBottom: '8px' }}>
                                        <span>📁 {data.evidence.project_count} projects</span>
                                        <span>🔢 {data.evidence.mentions} mentions</span>
                                        <span>⭐ Max complexity: {data.evidence.max_complexity.toFixed(1)}</span>
                                        <span>📊 {data.evidence.role_context}</span>
                                    </div>
                                </div>
                            ))}
                        </div>


                    </div>
                )}

                {/* Skills Section */}
                <div className="card fade-in">
                    <h2>🔺 TOP DETECTED SKILLS</h2>
                    <div className="divider"></div>
                    <div className="skills-container">
                        {analysis.top_3_skills.map((skill, index) => (
                            <div key={index} className="skill-badge-large">
                                <span className="skill-rank">#{index + 1}</span>
                                <span className="skill-name">{skill}</span>
                                {analysis.skill_depth_breakdown[skill] && (
                                    <span className={`skill-depth depth-${analysis.skill_depth_breakdown[skill].toLowerCase()}`}>
                                        {analysis.skill_depth_breakdown[skill]}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>

                    <h3 className="mt-3">All Detected Skills</h3>
                    <div className="skills-grid">
                        {analysis.ranked_skills.map((skill, index) => (
                            <span key={index} className="badge">
                                {skill}
                                {analysis.skill_depth_breakdown[skill] && (
                                    <span className="skill-depth-mini"> • {analysis.skill_depth_breakdown[skill]}</span>
                                )}
                            </span>
                        ))}
                    </div>
                </div>



                {/* Missing Skills */}
                {analysis.missing_skills_for_best_role && analysis.missing_skills_for_best_role.length > 0 && (
                    <div className="card fade-in warning-card">
                        <h3>🎯 SKILLS TO MASTER FOR {analysis.recommended_role}</h3>
                        <div className="divider"></div>
                        <p className="mb-2">To strengthen your profile for the {analysis.recommended_role} role, consider developing these skills:</p>
                        <div className="skills-grid">
                            {analysis.missing_skills_for_best_role.map((skill, index) => (
                                <span key={index} className="badge badge-warning">{skill}</span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Insights */}
                <div className="grid grid-2">
                    <div className="card fade-in">
                        <h3>💡 CAREER ALIGNMENT</h3>
                        <div className="divider"></div>
                        <p>{analysis.career_alignment_analysis}</p>
                    </div>

                    <div className="card fade-in">
                        <h3>🔄 SKILL SYNERGY</h3>
                        <div className="divider"></div>
                        <p>{analysis.skill_synergy_analysis}</p>
                    </div>
                </div>

                {/* Roadmap */}
                <div className="card fade-in roadmap-card">
                    <h2>🗺️ YOUR 4-WEEK CAREER ROADMAP</h2>
                    <div className="divider"></div>
                    <div className="roadmap-grid">
                        {Object.entries(analysis.roadmap).map(([week, task], index) => (
                            <div key={week} className="roadmap-item">
                                <div className="roadmap-week">
                                    <div className="week-number">{index + 1}</div>
                                    <div className="week-label">WEEK</div>
                                </div>
                                <div className="roadmap-content">
                                    <p>{task}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Domain & Role Breakdown */}
                <div className="grid grid-2">
                    <motion.div
                        className="card fade-in chart-card"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        <h3>🏆 DOMAIN STRENGTH BREAKDOWN</h3>
                        <div className="divider"></div>
                        <ResponsiveContainer width="100%" height={300}>
                            <RadarChart data={domainChartData}>
                                <PolarGrid stroke="#00FFD1" strokeOpacity={0.3} />
                                <PolarAngleAxis
                                    dataKey="name"
                                    stroke="#00FFD1"
                                    style={{ fontSize: '12px', fontFamily: 'Orbitron' }}
                                />
                                <PolarRadiusAxis stroke="#00FFD1" strokeOpacity={0.3} />
                                <Radar
                                    dataKey="value"
                                    stroke="#00FFD1"
                                    fill="#00FFD1"
                                    fillOpacity={0.6}
                                    animationDuration={1500}
                                />
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(0, 0, 0, 0.9)',
                                        border: '1px solid #00FFD1',
                                        borderRadius: '12px',
                                        color: '#00FFD1',
                                        fontFamily: 'Orbitron'
                                    }}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </motion.div>

                    <motion.div
                        className="card fade-in chart-card"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.4 }}
                    >
                        <h3>💼 ROLE MATCH BREAKDOWN</h3>
                        <div className="divider"></div>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={roleChartData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="#00FFD1" strokeOpacity={0.2} />
                                <XAxis type="number" stroke="#00FFD1" />
                                <YAxis
                                    type="category"
                                    dataKey="name"
                                    stroke="#00FFD1"
                                    width={120}
                                    style={{ fontSize: '11px', fontFamily: 'Orbitron' }}
                                />
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(0, 0, 0, 0.9)',
                                        border: '1px solid #00FFD1',
                                        borderRadius: '12px',
                                        color: '#00FFD1',
                                        fontFamily: 'Orbitron'
                                    }}
                                />
                                <Bar dataKey="value" animationDuration={1500} radius={[0, 8, 8, 0]}>
                                    {roleChartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </motion.div>
                </div>

                {/* Footer */}
                <footer className="results-footer fade-in">
                    <div className="quote">
                        "Success is where preparation meets opportunity."
                    </div>
                    <button className="btn btn-primary mt-3" onClick={onReset}>
                        Analyze Another Resume
                    </button>
                </footer>
            </div>
        </div>
    );
};

export default AnalysisResults;
