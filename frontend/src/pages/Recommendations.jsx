import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Recommendations.css";

function Recommendations() {
  const navigate = useNavigate();

  const [resumeId, setResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [recommendations, setRecommendations] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [interviewHistory, setInterviewHistory] = useState([]);
  const [interviewLoading, setInterviewLoading] = useState(false);
  const [skillProgress, setSkillProgress] = useState({});
  const [progressFilter, setProgressFilter] = useState("ALL");

  const totalRecommendedSkills =
  recommendations?.recommendations?.length || 0;

  const completedSkills =
    recommendations?.recommendations?.filter(
      (recommendation) =>
        skillProgress[recommendation.skill] === "COMPLETED"
    ).length || 0;

  const inProgressSkills =
    recommendations?.recommendations?.filter(
      (recommendation) =>
        skillProgress[recommendation.skill] === "IN PROGRESS"
    ).length || 0;

  const notStartedSkills =
    recommendations?.recommendations?.filter(
      (recommendation) =>
        !skillProgress[recommendation.skill] ||
        skillProgress[recommendation.skill] === "NOT STARTED"
    ).length || 0;

  const learningProgress =
    totalRecommendedSkills > 0
      ? Math.round(
          (completedSkills / totalRecommendedSkills) * 100
        )
      : 0;

  const completedSkillNames =
    recommendations?.recommendations
      ?.filter(
        (recommendation) =>
          skillProgress[recommendation.skill] === "COMPLETED"
      )
      .map(
        (recommendation) => recommendation.skill
      ) || [];
    
    // =========================
    // Career Readiness
    // =========================

    const requiredSkills =
      recommendations?.required_skills || [];

    const missingSkills =
      recommendations?.missing_skills || [];

    const skillCoverage =
      requiredSkills.length > 0
        ? Math.round(
            ((requiredSkills.length - missingSkills.length) /
              requiredSkills.length) *
              100
          )
        : 100;

    const interviewScores = interviewHistory
      .map((interview) => Number(interview.score || 0))
      .filter((score) => !Number.isNaN(score));

    const interviewPerformance =
      interviewScores.length > 0
        ? Math.round(
            interviewScores.reduce(
              (total, score) => total + score,
              0
            ) / interviewScores.length
          )
        : 0;
    
    const skillContribution = Math.round(skillCoverage * 0.5);

    const interviewContribution =
      interviewScores.length > 0
        ? Math.round(interviewPerformance * 0.5)
        : 0;

    const careerReadiness =
      interviewScores.length > 0
        ? Math.round(
            skillCoverage * 0.5 +
            interviewPerformance * 0.5
          )
        : skillCoverage;

    const readinessStatus =
      careerReadiness >= 80
        ? "EXCELLENT"
        : careerReadiness >= 60
        ? "GOOD"
        : careerReadiness >= 40
        ? "NEEDS IMPROVEMENT"
        : "LOW READINESS";

    const readinessAdvice =
      skillCoverage < interviewPerformance
        ? "Your interview performance is stronger than your skill coverage. Focus on learning the missing job skills."
        : interviewPerformance < skillCoverage
        ? "Your resume shows good skill coverage, but your interview performance needs more practice."
        : "Your skills and interview performance are balanced. Continue improving both areas.";
        

      const fetchInterviewHistory = async () => {
          if (!resumeId) return;

          try {
            setInterviewLoading(true);

            const token = localStorage.getItem("token");

            const response = await fetch(
              `http://127.0.0.1:8000/resume/${resumeId}/interview-history`,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (!response.ok) {
              throw new Error("Failed to fetch interview history");
            }

            const data = await response.json();

            setInterviewHistory(data.history || []);

          } catch (error) {
            console.error(
              "Interview history error:",
              error
            );

            setInterviewHistory([]);

          } finally {
            setInterviewLoading(false);
          }
        };


      const fetchSkillProgress = async () => {
          if (!resumeId) return;

          try {
            const response = await axios.get(
              `http://127.0.0.1:8000/resume/${resumeId}/skill-progress`
            );

            const progressMap = {};

            response.data.progress.forEach((item) => {
              progressMap[item.skill] = item.status;
            });

            setSkillProgress(progressMap);

          } catch (error) {
            console.error(
              "Error fetching skill progress:",
              error
            );
          }
        };

      
      const updateSkillProgress = async (skill, status) => {
        try {
          const response = await axios.put(
            `http://127.0.0.1:8000/resume/${resumeId}/skill-progress`,
            {
              skill: skill,
              status: status,
            }
          );

          setSkillProgress((previous) => ({
            ...previous,
            [skill]: response.data.status,
          }));

        } catch (error) {
          console.error("Error updating skill progress:", error);
        }
      };

      useEffect(() => {
        if (resumeId) {
          fetchInterviewHistory();
          fetchSkillProgress();
        }
      }, [resumeId]);

  // =========================
  // Get Recommendations
  // =========================

  const getRecommendations = async () => {
    if (!resumeId) {
      setMessage("Please enter a resume ID.");
      setRecommendations(null);
      return;
    }

    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      setRecommendations(null);
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setRecommendations(null);

      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const response = await axios.post(
        `http://127.0.0.1:8000/resume/${resumeId}/recommendations`,
        null,
        {
          params: {
            job_description: jobDescription,
          },

          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(
        "Recommendations:",
        response.data
      );

      setRecommendations(response.data);

      await fetchInterviewHistory();

      setMessage(
        "Recommendations generated successfully!"
      );

    } catch (error) {
      console.error(
        "Recommendation Error:",
        error
      );

      setMessage(
        error.response?.data?.detail ||
        "Unable to generate recommendations."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recommendations-page">

      {/* =========================
          TOP BAR
      ========================= */}

      <header className="recommendations-topbar">

        <div className="recommendations-brand">

          <div className="recommendations-logo">
            AI
          </div>

          <div>
            <h2>
              Resume Analyzer
            </h2>

            <span>
              AI-powered career assistant
            </span>
          </div>

        </div>


        <button
          type="button"
          className="recommendations-dashboard-button"
          onClick={() => navigate("/dashboard")}
        >
          ← Dashboard
        </button>

      </header>


      {/* =========================
          PAGE HEADER
      ========================= */}

      <section className="recommendations-heading">

        <span className="recommendations-eyebrow">
          AI CAREER ASSISTANT
        </span>

        <h1>
          Career Recommendations
        </h1>

        <p>
          Discover personalized skills, career improvements,
          and recommendations based on your resume and target job.
        </p>

      </section>


      {/* =========================
          MAIN WORKSPACE
      ========================= */}

      <section className="recommendations-workspace">


        {/* =========================
            RESUME CARD
        ========================= */}

        <div className="recommendation-card">

          <div className="recommendation-card-heading">

            <div className="recommendation-step">
              01
            </div>

            <div>

              <h2>
                Your Resume
              </h2>

              <p>
                Enter the Resume ID from your analysis.
              </p>

            </div>

          </div>


          <div className="resume-input-wrapper">

            <span>
              #
            </span>

            <input
              type="number"
              min="1"
              placeholder="Enter Resume ID"
              value={resumeId}
              onChange={(e) => {
                setResumeId(e.target.value);
                setMessage("");
              }}
            />

          </div>


          <div className="resume-tip">

            <span>
              💡
            </span>

            <p>
              You can find your Resume ID on the
              Analyze page after uploading your resume.
            </p>

          </div>

        </div>


        {/* =========================
            JOB DESCRIPTION CARD
        ========================= */}

        <div className="recommendation-card">

          <div className="recommendation-card-heading">

            <div className="recommendation-step">
              02
            </div>

            <div>

              <h2>
                Target Job
              </h2>

              <p>
                Tell the AI about the position you're targeting.
              </p>

            </div>

          </div>


          <div className="recommendation-textarea-wrapper">

            <textarea
              placeholder={
                "Paste the complete job description here...\n\n" +
                "Example:\n" +
                "We are looking for a Python Developer with " +
                "experience in FastAPI, SQL, Machine Learning, " +
                "Docker and AWS..."
              }
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value);
                setMessage("");
              }}
            />

            <span className="recommendation-character-count">
              {jobDescription.length} characters
            </span>

          </div>


          <button
            type="button"
            className="recommend-button"
            onClick={getRecommendations}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="recommend-spinner"></span>
                Generating...
              </>
            ) : (
              <>
                ✨ Get Recommendations →
              </>
            )}

          </button>

        </div>

      </section>


      {/* =========================
          LOADING
      ========================= */}

      {loading && (

        <div className="recommendation-loading">

          <div className="recommend-large-spinner"></div>

          <div>

            <strong>
              AI is analyzing your career profile...
            </strong>

            <p>
              Comparing your resume with the target job.
            </p>

          </div>

        </div>

      )}


      {/* =========================
          MESSAGE
      ========================= */}

      {message && (

        <div
          className={
            message.includes("successfully")
              ? "recommendation-message success"
              : "recommendation-message error"
          }
        >

          <span>
            {message.includes("successfully")
              ? "✓"
              : "!"}
          </span>

          {message}

        </div>

      )}


      {/* =========================
          RESULTS
      ========================= */}

      {recommendations && (

        <section className="recommendations-results">


          {/* RESULTS HEADER */}

          <div className="results-title">

            <div>

              <span className="recommendations-eyebrow">
                ✨ AI CAREER INSIGHTS
              </span>

              <h2>
                Your Career Roadmap
              </h2>

              <p>
                Personalized recommendations based on your
                resume and target job.
              </p>

            </div>

            <div className="ai-badge">
              ✓ Analysis Complete
            </div>

          </div>


          {/* RESUME SUMMARY */}

          <div className="recommendation-summary">

            <div className="summary-icon">
              🎯
            </div>

            <div className="summary-content">

              <span>
                RESUME ANALYZED
              </span>

              <h3>
                {recommendations.filename}
              </h3>

            </div>

            <div className="missing-count">

              <strong>
                {recommendations.missing_skills?.length || 0}
              </strong>

              <span>
                Skills to improve
              </span>

            </div>

            </div>   {/* CLOSE recommendation-summary */}

          {/* =========================================================
          CAREER READINESS
          ========================================================= */}

          <div className="career-readiness-section">

            <div className="career-readiness-header">

                <div>

                  <span className="recommendations-eyebrow">
                    CAREER READINESS
                  </span>

                  <h2>
                    Your Career Readiness Score
                  </h2>

                  <p>
                    Your readiness is based on skill coverage and interview performance.
                  </p>

                </div>

                <div className={`readiness-status status-${readinessStatus
                  .toLowerCase()
                  .replace(/\s+/g, "-")}`}>
                  {readinessStatus}
                </div>

              </div>


            <div className="career-readiness-card">

              <div className="readiness-score">

                <strong>
                  {careerReadiness}%
                </strong>

                <span>
                  CAREER READINESS
                </span>

              </div>


              <div className="readiness-progress-area">

                <div className="readiness-progress-label">

                  <span>
                    Required Skills
                  </span>

                  <strong>
                    {requiredSkills.length - missingSkills.length}
                    {" / "}
                    {requiredSkills.length}
                  </strong>

                </div>


                <div className="readiness-progress">

                  <div
                    className="readiness-progress-fill"
                    style={{
                      width: `${skillCoverage}%`
                    }}
                  ></div>

                </div>


                <p>
                  {readinessAdvice}
                </p>

                <div className="readiness-breakdown">

                  <div className="breakdown-item">
                    <span>Skill Coverage</span>
                    <strong>
                      {skillCoverage}% × 50% = {skillContribution}%
                    </strong>
                  </div>

                  <div className="breakdown-item">
                    <span>Interview Performance</span>
                    <strong>
                      {interviewPerformance}% × 50% = {interviewContribution}%
                    </strong>
                  </div>

                </div>

              </div>


              <div className="readiness-stat">

                <strong>
                  {missingSkills.length}
                </strong>

                <span>
                  Missing Skills
                </span>

              </div>

              <div className="readiness-stat">

                <strong>
                  {interviewPerformance}%
                </strong>

                <span>
                  INTERVIEW PERFORMANCE
                </span>

                </div>

            </div>

          </div>




            {/* =========================================================
                SKILL PROFILE
            ========================================================= */}

            <div className="skill-profile-section">           
              <div className="skill-profile-heading">

                <div>

                  <span className="recommendations-eyebrow">
                    SKILL PROFILE
                  </span>

                  <h2>
                    Your Current Skill Status
                  </h2>

                  <p>
                    Understand your strengths and the skills you should improve
                    for your target job.
                  </p>

                </div>

              </div>


              <div className="skill-profile-grid">

                {/* =====================================================
                    SKILLS YOU HAVE
                ===================================================== */}

                <div className="skill-profile-card strong-skills-card">

                  <div className="skill-profile-card-header">

                    <div className="skill-profile-icon strong-icon">
                      ✓
                    </div>

                    <div>

                      <h3>
                        Skills You Have
                      </h3>

                      <span>
                        Detected in your resume
                      </span>

                    </div>

                  </div>


                  <div className="skill-profile-list">

                    {recommendations.resume_skills
                      ?.filter(
                        (skill) =>
                          !recommendations.missing_skills
                            ?.some(
                              (missing) =>
                                missing.toLowerCase() ===
                                skill.toLowerCase()
                            )
                      )
                      .map((skill, index) => (

                        <span
                          key={index}
                          className="skill-profile-tag strong-tag"
                        >
                          ✓ {skill}
                        </span>

                      ))}

                    {(!recommendations.resume_skills ||
                      recommendations.resume_skills.filter(
                        (skill) =>
                          !recommendations.missing_skills
                            ?.some(
                              (missing) =>
                                missing.toLowerCase() ===
                                skill.toLowerCase()
                            )
                      ).length === 0) && (

                      <span className="skill-profile-empty">
                        No existing skills detected.
                      </span>

                    )}

                  </div>

                </div>


                {/* =====================================================
                    INTERVIEW WEAKNESSES
                ===================================================== */}

                <div className="skill-profile-card weak-skills-card">

                  <div className="skill-profile-card-header">

                    <div className="skill-profile-icon weak-icon">
                      !
                    </div>

                    <div>

                      <h3>
                        Needs Practice
                      </h3>

                      <span>
                        Based on interview performance
                      </span>

                    </div>

                  </div>


                  <div className="skill-profile-list">

                    {recommendations.recommendations
                      ?.filter(
                        (recommendation) =>
                          recommendation.category ===
                          "Interview Weakness"
                      )
                      .map((recommendation, index) => (

                        <span
                          key={index}
                          className="skill-profile-tag weak-tag"
                        >
                          ⚠ {recommendation.skill}
                        </span>

                      ))}

                    {(!recommendations.recommendations ||
                      recommendations.recommendations.filter(
                        (recommendation) =>
                          recommendation.category ===
                          "Interview Weakness"
                      ).length === 0) && (

                      <span className="skill-profile-empty">
                        No interview weaknesses detected.
                      </span>

                    )}

                  </div>

                </div>


                {/* =====================================================
                    MISSING JOB SKILLS
                ===================================================== */}

                <div className="skill-profile-card missing-profile-card">

                  <div className="skill-profile-card-header">

                    <div className="skill-profile-icon missing-icon">
                      ⚠
                    </div>

                    <div>

                      <h3>
                        Missing Job Skills
                      </h3>

                      <span>
                        Required but not found in your resume
                      </span>

                    </div>

                  </div>


                  <div className="skill-profile-list">

                    {recommendations.missing_skills
                      ?.map((skill, index) => (

                        <span
                          key={index}
                          className="skill-profile-tag missing-tag"
                        >
                          ⚠ {skill}
                        </span>

                      ))}

                    {(!recommendations.missing_skills ||
                      recommendations.missing_skills.length === 0) && (

                      <span className="skill-profile-empty">
                        No missing job skills. Great match!
                      </span>

                    )}

                  </div>

                </div>

              </div>

            </div>

            <div className="recommendations-action-header">

              <div>
                <h2>
                  🚀 Recommended Skills
                </h2>

                <p>
                  Focus on these skills to improve your job match.
                </p>
              </div>

              <div className="priority-summary">

                <div className="priority-summary-item high">
                  <strong>
                    {recommendations.recommendations?.filter(
                      (item) => item.priority === "HIGH"
                    ).length || 0}
                  </strong>

                  <span>
                    HIGH PRIORITY
                  </span>
                </div>

                <div className="priority-summary-item medium">
                  <strong>
                    {recommendations.recommendations?.filter(
                      (item) => item.priority === "MEDIUM"
                    ).length || 0}
                  </strong>

                  <span>
                    MEDIUM PRIORITY
                  </span>
                </div>

              <div className="priority-summary-item low">
                <strong>
                  {recommendations.recommendations?.filter(
                    (item) => item.priority === "LOW"
                  ).length || 0}
                </strong>

                <span>
                  LOW PRIORITY
                </span>
              </div>

            </div>

          </div>
        

        {/* =========================================================
                  LEARNING PROGRESS
              ========================================================= */}

              <div className="learning-progress-card">

                <div className="learning-progress-header">

                  <div>
                    <span className="recommendations-eyebrow">
                      LEARNING PROGRESS
                    </span>

                    <h2>
                      Your Skill Learning Progress
                    </h2>

                    <p>
                      Track how many recommended skills you have completed.
                    </p>
                  </div>

                  <div className="learning-progress-score">
                    <strong>
                      {learningProgress}%
                    </strong>

                    <span>
                      COMPLETED
                    </span>
                  </div>

                </div>


                <div className="learning-progress-bar">

                  <div
                    className="learning-progress-fill"
                    style={{
                      width: `${learningProgress}%`
                    }}
                  ></div>

                </div>


                <div className="learning-progress-footer">

                  <span>
                    {completedSkills} of {totalRecommendedSkills} skills completed
                  </span>

                  <span>
                    {totalRecommendedSkills - completedSkills} remaining
                  </span>

                </div>

                <div className="learning-progress-stats">

                  <div className="learning-stat-card">
                    <strong>{notStartedSkills}</strong>
                    <span>NOT STARTED</span>
                  </div>

                  <div className="learning-stat-card">
                    <strong>{inProgressSkills}</strong>
                    <span>IN PROGRESS</span>
                  </div>

                  <div className="learning-stat-card">
                    <strong>{completedSkills}</strong>
                    <span>COMPLETED</span>
                  </div>

                </div>

              </div>
              


          {/* =========================================================
              COMPLETED SKILLS
          ========================================================= */}

          <div className="completed-skills-card">

            <div className="completed-skills-header">

              <div>

                <span className="recommendations-eyebrow">
                  COMPLETED SKILLS
                </span>

                <h2>
                  Skills You Have Completed
                </h2>

                <p>
                  Keep building your skills and track your achievements.
                </p>

              </div>


              <div className="completed-skills-count">

                <strong>
                  {completedSkillNames.length}
                </strong>

                <span>
                  COMPLETED
                </span>

              </div>

            </div>


            {completedSkillNames.length > 0 ? (

              <div className="completed-skills-list">

                {completedSkillNames.map(
                  (skill, index) => (

                    <div
                      className="completed-skill-item"
                      key={index}
                    >

                      <span className="completed-skill-check">
                        ✓
                      </span>

                      <span className="completed-skill-name">
                        {skill}
                      </span>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="completed-skills-empty">

                <span>
                  📚
                </span>

                <p>
                  No skills completed yet. Start learning to build your progress!
                </p>

              </div>

            )}

          </div>



        {/* RECOMMENDATION CARDS */}

        {/* =========================================================
                SKILL PROGRESS FILTER
            ========================================================= */}

           <div className="skill-progress-filter">

              <button
                type="button"
                className={progressFilter === "ALL" ? "active" : ""}
                onClick={() => setProgressFilter("ALL")}
              >
                All
                <span className="filter-count">
                  {totalRecommendedSkills}
                </span>
              </button>

              <button
                type="button"
                className={progressFilter === "NOT STARTED" ? "active" : ""}
                onClick={() => setProgressFilter("NOT STARTED")}
              >
                Not Started
                <span className="filter-count">
                  {notStartedSkills}
                </span>
              </button>

              <button
                type="button"
                className={progressFilter === "IN PROGRESS" ? "active" : ""}
                onClick={() => setProgressFilter("IN PROGRESS")}
              >
                In Progress
                <span className="filter-count">
                  {inProgressSkills}
                </span>
              </button>

              <button
                type="button"
                className={progressFilter === "COMPLETED" ? "active" : ""}
                onClick={() => setProgressFilter("COMPLETED")}
              >
                Completed
                <span className="filter-count">
                  {completedSkills}
                </span>
              </button>

            </div>
          <div className="recommendation-cards">

            {recommendations.recommendations
              ?.filter((recommendation) => {
                if (progressFilter === "ALL") {
                  return true;
                }

                const currentStatus =
                  skillProgress[recommendation.skill] || "NOT STARTED";

                return currentStatus === progressFilter;
              })
              .map((recommendation, index) => (

                <div
                  className="career-recommendation-card"
                  key={index}
                >


                  {/* CARD HEADER */}

                  <div className="career-card-top">

                    <div className="career-skill-icon">

                      {recommendation.skill
                        ?.toLowerCase()
                        .includes("docker")
                        ? "🐳"
                        : recommendation.skill
                            ?.toLowerCase()
                            .includes("aws")
                          ? "☁️"
                          : "💡"}

                    </div>


                    <div className="career-skill-title">

                      <h3>
                        {recommendation.skill}
                      </h3>

                      <span className="skill-label">
                        {(recommendation.category || "SKILL GAP").toUpperCase()}
                      </span>

                    </div>


                    <div
                      className={`priority-badge ${
                        recommendation.priority === "MEDIUM"
                        ? "medium-priority"
                        : "high-priority"
                      }`}
                    >
                      {recommendation.priority || "HIGH"} PRIORITY
                    </div>

                  </div>


                  {/* WHY IT MATTERS */}

                  <div className="career-reason">

                    <span>
                      WHY IT MATTERS
                    </span>

                    <p>
                      {recommendation.reason}
                    </p>

                  </div>

                  {recommendation.category === "Interview Weakness" && (
                    <div className="interview-score-indicator">

                      <span>
                        INTERVIEW SCORE
                      </span>

                      <strong>
                        {(() => {
                          const interview = interviewHistory.find(
                            (item) =>
                              item.skill?.toLowerCase() ===
                              recommendation.skill?.toLowerCase()
                          );

                          return interview
                            ? `${Math.round(Number(interview.score || 0))}%`
                            : "N/A";
                        })()}
                      </strong>

                    </div>
                  )}


                  {/* ACTION PLAN */}

                  <div className="action-plan">

                    <div className="action-plan-header">

                      <span className="action-plan-icon">
                        ✓
                      </span>

                      <div>

                        <h4>
                          Your Action Plan
                        </h4>

                        <p>
                          Recommended steps to learn this skill
                        </p>

                      </div>

                    </div>


                    <div className="action-list">

                      {recommendation.actions?.map(
                        (action, actionIndex) => (

                          <div
                            className="action-item"
                            key={actionIndex}
                          >

                            <span>
                              {actionIndex + 1}
                            </span>

                            <p>
                              {action}
                            </p>

                          </div>

                        )
                      )}

                    </div>

                                    </div>


                  {/* =========================================================
                  SKILL LEARNING PROGRESS
              ========================================================= */}

              <div className="skill-progress-section">

                <div className="skill-progress-header">

                  <span>
                    LEARNING PROGRESS
                  </span>

                  <strong>
                    {skillProgress[recommendation.skill] || "NOT STARTED"}
                  </strong>

                </div>


                {/* Progress Bar */}

                <div className="skill-progress-bar">

                  <div
                    className={`skill-progress-fill ${
                      skillProgress[recommendation.skill] === "COMPLETED"
                        ? "completed"
                        : skillProgress[recommendation.skill] === "IN PROGRESS"
                        ? "in-progress"
                        : "not-started"
                    }`}
                    style={{
                      width:
                        skillProgress[recommendation.skill] === "COMPLETED"
                          ? "100%"
                          : skillProgress[recommendation.skill] === "IN PROGRESS"
                          ? "50%"
                          : "0%"
                    }}
                  ></div>

                </div>


                {/* Progress Percentage */}

                <div className="skill-progress-percentage">

                  <span>
                    {skillProgress[recommendation.skill] === "COMPLETED"
                      ? "100%"
                      : skillProgress[recommendation.skill] === "IN PROGRESS"
                      ? "50%"
                      : "0%"}
                  </span>

                </div>


                {/* Buttons */}

                <div className="skill-progress-buttons">

                  {/* NOT STARTED */}
                  {(!skillProgress[recommendation.skill] ||
                    skillProgress[recommendation.skill] === "NOT STARTED") && (

                    <button
                      className="skill-progress-btn start-learning-btn"
                      onClick={() =>
                        updateSkillProgress(
                          recommendation.skill,
                          "IN PROGRESS"
                        )
                      }
                    >
                      Start Learning
                    </button>

                  )}

                  {/* IN PROGRESS */}
                  {skillProgress[recommendation.skill] === "IN PROGRESS" && (

                    <button
                      className="skill-progress-btn complete-learning-btn"
                      onClick={() =>
                        updateSkillProgress(
                          recommendation.skill,
                          "COMPLETED"
                        )
                      }
                    >
                      ✓ Mark Completed
                    </button>

                  )}

                  {/* COMPLETED */}
                  {skillProgress[recommendation.skill] === "COMPLETED" && (

                    <button
                      className="skill-progress-btn start-again-btn"
                      onClick={() =>
                        updateSkillProgress(
                          recommendation.skill,
                          "NOT STARTED"
                        )
                      }
                    >
                      ↻ Start Again
                    </button>

                  )}

                </div>

              </div>


                </div>

              )
            )}
            
            {recommendations.recommendations?.filter((recommendation) => {
              if (progressFilter === "ALL") {
                return true;
              }

              const currentStatus =
                skillProgress[recommendation.skill] || "NOT STARTED";

              return currentStatus === progressFilter;
            }).length === 0 && (
              <div className="skill-filter-empty">
                <div className="skill-filter-empty-icon">
                  {progressFilter === "COMPLETED"
                    ? "🏆"
                    : progressFilter === "IN PROGRESS"
                    ? "🚀"
                    : "📚"}
                </div>

                <h3>
                  {progressFilter === "COMPLETED"
                    ? "No completed skills yet"
                    : progressFilter === "IN PROGRESS"
                    ? "No skills currently in progress"
                    : "No skills waiting to be started"}
                </h3>

                <p>
                  {progressFilter === "COMPLETED"
                    ? "Complete a skill to see it in your completed skills."
                    : progressFilter === "IN PROGRESS"
                    ? "Start learning a skill to track your progress here."
                    : "All recommended skills have already been started."}
                </p>

                <button
                  type="button"
                  onClick={() => setProgressFilter("ALL")}
                >
                  View All Skills
                </button>
              </div>
            )}


          </div>


          {/* MISSING SKILLS */}

          {recommendations.missing_skills?.length > 0 && (

            <div className="missing-skills-summary">

              <div className="missing-summary-header">

                <div className="missing-summary-icon">
                  ⚠
                </div>

                <div>

                  <h3>
                    Skills Currently Missing
                  </h3>

                  <p>
                    These skills were not detected in your resume.
                  </p>

                </div>

              </div>


              <div className="missing-skill-list">

                {recommendations.missing_skills.map(
                  (skill, index) => (

                    <span
                      key={index}
                      className="missing-skill-tag"
                    >
                      ⚠ {skill}
                    </span>

                  )
                )}

              </div>

            </div>

          )}


          {/* ACTION BUTTONS */}

          <div className="recommendation-actions">

            <button
              type="button"
              onClick={() => navigate("/analyze")}
            >
              ← Analyze Resume
            </button>

            <button
              type="button"
              onClick={() => navigate("/interview")}
            >
              🎤 Prepare for Interview →
            </button>

          </div>

        </section>

      )}


      {/* =========================
          FOOTER
      ========================= */}

      <footer className="recommendations-footer">
        AI Resume Analyzer • Build your career with AI
      </footer>

    </div>
  );
}

export default Recommendations;