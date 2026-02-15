import { useState } from 'react';
import './LandingPage.css';

const LandingPage = ({ onAnalysisComplete, loading, setLoading }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setSelectedFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleSubmit = async () => {
        if (!selectedFile) return;

        setLoading(true);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/analyze/`, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            onAnalysisComplete(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to analyze resume. Make sure the backend is running.');
            setLoading(false);
        }
    };

    return (
        <div className="landing-page">
            <div className="container">
                <header className="hero fade-in">
                    <div className="logo-section">
                        <div className="dune-text">K A P P</div>
                        <div className="subtitle">CAREER INTELLIGENCE ENGINE</div>
                    </div>

                    <h1 className="main-title">
                        UNLOCK YOUR FUTURE
                    </h1>

                    <p className="hero-subtitle">
                        Upload your resume and discover your optimal career trajectory.
                        <br />
                        <span className="glow">AI-powered insights for your professional journey.</span>
                    </p>
                </header>

                <div className="upload-section fade-in">
                    <div
                        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        onClick={() => document.getElementById('fileInput').click()}
                    >
                        <input
                            id="fileInput"
                            type="file"
                            accept=".pdf,.doc,.docx"
                            onChange={handleChange}
                            style={{ display: 'none' }}
                        />

                        {!selectedFile ? (
                            <>
                                <div className="upload-icon">📄</div>
                                <h3>UPLOAD YOUR RESUME</h3>
                                <p>or click to select file</p>
                                <p className="file-types">Accepted: PDF, DOC, DOCX</p>
                            </>
                        ) : (
                            <>
                                <div className="upload-icon">✓</div>
                                <h3>{selectedFile.name}</h3>
                                <p className="file-selected">File ready for analysis</p>
                            </>
                        )}
                    </div>

                    {selectedFile && !loading && (
                        <button className="btn btn-primary analyze-btn" onClick={handleSubmit}>
                            BEGIN ANALYSIS
                        </button>
                    )}

                    {loading && (
                        <div className="loading-container">
                            <div className="loading"></div>
                            <p className="loading-text">Analyzing your career path through the sands of time...</p>
                        </div>
                    )}
                </div>

                <div className="features-grid fade-in">
                    <div className="feature-card">
                        <div className="feature-icon">🎯</div>
                        <h3>ROLE DETECTION</h3>
                        <p>AI-powered analysis identifies your optimal career path</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">📊</div>
                        <h3>SKILL MAPPING</h3>
                        <p>Comprehensive breakdown of your technical strengths</p>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🗺️</div>
                        <h3>CAREER ROADMAP</h3>
                        <p>Strategic guidance for your professional journey</p>
                    </div>
                </div>

                <footer className="landing-footer">
                    <p className="quote">
                        "The future belongs to those who prepare for it."
                    </p>
                    <p className="quote-author">- Your Career Intelligence Partner</p>
                </footer>
            </div>
        </div>
    );
};

export default LandingPage;
