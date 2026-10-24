import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import "./History.css";

function History() {
  const navigate = useNavigate();

  const [resumeId, setResumeId] = useState("");
  const [history, setHistory] = useState(null);
  const [interviewHistory, setInterviewHistory] = useState(null);

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [expandedInterview, setExpandedInterview] = useState(null);

  const fetchHistory = async () => {
    if (!resumeId) {
      setMessage("Please enter a resume ID.");
      setHistory(null);
      setInterviewHistory(null);
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setHistory(null);
      setInterviewHistory(null);
      setExpandedInterview(null);

      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      // =====================================================
      // RESUME ANALYSIS HISTORY
      // =====================================================

     const analysisResponse = await API.get(
      `/resume/${resumeId}/history`,
      {
        headers,
      }
    );

      console.log(
        "Analysis History Response:",
        analysisResponse.data
      );

      setHistory(analysisResponse.data);

      // =====================================================
      // INTERVIEW HISTORY
      // =====================================================

      try {
        const interviewResponse = await API.get(
          `/resume/${resumeId}/interview-history`,
          {
            headers,
          }
        );

        console.log(
          "Interview History Response:",
          interviewResponse.data
        );

        setInterviewHistory(interviewResponse.data);

      } catch (interviewError) {

        console.error(
          "Interview History Error:",
          interviewError
        );

        // Do not hide the analysis history if
        // interview history has an issue.
        setInterviewHistory({
          resume_id: Number(resumeId),
          total_interviews: 0,
          history: [],
        });
      }

    } catch (error) {

      console.error(
        "History Error:",
        error
      );

      setMessage(
        error.response?.data?.detail ||
        "Unable to fetch history."
      );

    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // TOGGLE INTERVIEW DETAILS
  // ==========================================================

  const toggleInterview = (id) => {
    if (expandedInterview === id) {
      setExpandedInterview(null);
    } else {
      setExpandedInterview(id);
    }
  };

  return (
    <div className="history-page">

      {/* =====================================================
          TOP BAR
      ===================================================== */}

      <header className="history-topbar">

        <div className="history-brand">

          <div className="history-logo">
            AI
          </div>

          <div>
            <h2>Resume Analyzer</h2>

            <span>
              AI-powered career assistant
            </span>
          </div>

        </div>

        <button
          type="button"
          className="history-dashboard-button"
          onClick={() => navigate("/dashboard")}
        >
          ← Dashboard
        </button>

      </header>


      {/* =====================================================
          PAGE HEADER
      ===================================================== */}

      <section className="history-heading">

        <span className="history-eyebrow">
          ANALYSIS & INTERVIEW TRACKER
        </span>

        <h1>
          History
        </h1>

        <p>
          Review your previous resume analyses and
          interview performance in one place.
        </p>

      </section>


      {/* =====================================================
          SEARCH CARD
      ===================================================== */}

      <section className="history-search-card">

        <div className="history-search-icon">
          🔎
        </div>

        <div className="history-search-content">

          <h2>
            Find Your Resume
          </h2>

          <p>
            Enter the Resume ID you received after uploading
            your resume.
          </p>

          <div className="history-search-row">

            <input
              type="number"
              min="1"
              placeholder="Enter Resume ID"
              value={resumeId}
              onChange={(e) => {
                setResumeId(e.target.value);
                setMessage("");
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  fetchHistory();
                }
              }}
            />

            <button
              type="button"
              onClick={fetchHistory}
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="history-spinner"></span>
                  Loading...
                </>
              ) : (
                <>
                  View History →
                </>
              )}

            </button>

          </div>

        </div>

      </section>


      {/* =====================================================
          LOADING
      ===================================================== */}

      {loading && (
        <div className="history-loading">

          <div className="history-large-spinner"></div>

          <div>

            <strong>
              Loading history...
            </strong>

            <p>
              Retrieving your resume analyses and interview history.
            </p>

          </div>

        </div>
      )}


      {/* =====================================================
          MESSAGE
      ===================================================== */}

      {message && (
        <div className="history-message">

          <span>!</span>

          {message}

        </div>
      )}


      {/* =====================================================
          HISTORY RESULTS
      ===================================================== */}

      {history && (
        <section className="history-results">

          {/* =================================================
              RESUME SUMMARY
          ================================================= */}

          <div className="history-summary">

            <div>

              <span className="history-eyebrow">
                RESUME
              </span>

              <h2>
                {history.filename}
              </h2>

              <p className="history-resume-id">
                Resume ID: {history.resume_id}
              </p>

            </div>

            <div className="total-analysis">

              <span>
                Total Analyses
              </span>

              <strong>
                {history.total_analyses}
              </strong>

            </div>

          </div>


          {/* =================================================
              NO ANALYSIS HISTORY
          ================================================= */}

          {history.history &&
          history.history.length === 0 ? (

            <div className="empty-history">

              <div className="empty-history-icon">
                📊
              </div>

              <h3>
                No analyses yet
              </h3>

              <p>
                This resume does not have any analysis
                results yet.
              </p>

              <button
                type="button"
                onClick={() => navigate("/analyze")}
              >
                Start Analysis →
              </button>

            </div>

          ) : (

            <div className="history-list">

              {history.history.map((item) => (

                <article
                  key={item.analysis_id}
                  className="history-analysis-card"
                >

                  {/* CARD HEADER */}

                  <div className="analysis-card-header">

                    <div className="analysis-number">

                      <span>
                        ANALYSIS
                      </span>

                      <strong>
                        #{item.analysis_id}
                      </strong>

                    </div>

                    <div className="analysis-date">
                      🕒{" "}
                      {new Date(
                        item.created_at
                      ).toLocaleString()}
                    </div>

                  </div>


                  {/* SCORES */}

                  <div className="history-score-grid">

                    {/* FINAL MATCH */}

                    <div className="history-score-card final-history-score">

                      <div className="history-score-top">

                        <span>
                          Final Match
                        </span>

                        <div className="history-score-icon">
                          ★
                        </div>

                      </div>

                      <strong>
                        {item.final_match_percentage}%
                      </strong>

                      <div className="history-progress">

                        <div
                          className="history-progress-bar final-history-progress"
                          style={{
                            width:
                              `${item.final_match_percentage}%`
                          }}
                        ></div>

                      </div>

                    </div>


                    {/* SKILL MATCH */}

                    <div className="history-score-card">

                      <div className="history-score-top">

                        <span>
                          Skill Match
                        </span>

                        <div className="history-score-icon">
                          ◈
                        </div>

                      </div>

                      <strong>
                        {item.skill_match_percentage}%
                      </strong>

                      <div className="history-progress">

                        <div
                          className="history-progress-bar skill-history-progress"
                          style={{
                            width:
                              `${item.skill_match_percentage}%`
                          }}
                        ></div>

                      </div>

                    </div>


                    {/* SEMANTIC MATCH */}

                    <div className="history-score-card">

                      <div className="history-score-top">

                        <span>
                          Semantic Match
                        </span>

                        <div className="history-score-icon">
                          ◉
                        </div>

                      </div>

                      <strong>
                        {item.semantic_match_percentage}%
                      </strong>

                      <div className="history-progress">

                        <div
                          className="history-progress-bar semantic-history-progress"
                          style={{
                            width:
                              `${item.semantic_match_percentage}%`
                          }}
                        ></div>

                      </div>

                    </div>

                  </div>


                  {/* =================================================
                      SKILLS
                  ================================================= */}

                  <div className="history-skills-container">

                    {/* MATCHED */}

                    <div className="history-skill-section">

                      <div className="history-skill-heading">

                        <div className="matched-history-icon">
                          ✓
                        </div>

                        <div>

                          <h3>
                            Matched Skills
                          </h3>

                          <span>
                            Skills found in your resume
                          </span>

                        </div>

                      </div>

                      <div className="history-skills">

                        {item.matched_skills &&
                        item.matched_skills.length > 0 ? (

                          item.matched_skills.map(
                            (skill, skillIndex) => (

                              <span
                                key={skillIndex}
                                className="history-badge history-matched"
                              >
                                ✓ {skill}
                              </span>

                            )
                          )

                        ) : (

                          <span className="history-empty-skills">
                            No matched skills.
                          </span>

                        )}

                      </div>

                    </div>


                    {/* MISSING */}

                    <div className="history-skill-section">

                      <div className="history-skill-heading">

                        <div className="missing-history-icon">
                          !
                        </div>

                        <div>

                          <h3>
                            Missing Skills
                          </h3>

                          <span>
                            Skills you may want to develop
                          </span>

                        </div>

                      </div>

                      <div className="history-skills">

                        {item.missing_skills &&
                        item.missing_skills.length > 0 ? (

                          item.missing_skills.map(
                            (skill, skillIndex) => (

                              <span
                                key={skillIndex}
                                className="history-badge history-missing"
                              >
                                ⚠ {skill}
                              </span>

                            )
                          )

                        ) : (

                          <span className="history-empty-skills">
                            No missing skills.
                          </span>

                        )}

                      </div>

                    </div>

                  </div>

                </article>

              ))}

            </div>

          )}


          {/* =====================================================
              INTERVIEW HISTORY
          ===================================================== */}

          {interviewHistory && (

            <section className="interview-history-section">

              {/* INTERVIEW HEADER */}

              <div className="interview-history-header">

                <div>

                  <span className="history-eyebrow">
                    INTERVIEW TRACKER
                  </span>

                  <h2>
                    🎤 Interview History
                  </h2>

                  <p>
                    Review your interview questions,
                    answers, scores, and feedback.
                  </p>

                </div>

                <div className="total-interviews">

                  <span>
                    Total Interviews
                  </span>

                  <strong>
                    {interviewHistory.total_interviews || 0}
                  </strong>

                </div>

              </div>


              {/* NO INTERVIEW HISTORY */}

              {!interviewHistory.history ||
              interviewHistory.history.length === 0 ? (

                <div className="empty-interview-history">

                  <div className="empty-interview-icon">
                    🎤
                  </div>

                  <h3>
                    No interview history yet
                  </h3>

                  <p>
                    Complete an interview to see your
                    questions, answers, scores, and feedback here.
                  </p>

                  <button
                    type="button"
                    onClick={() => navigate("/interview")}
                  >
                    Start Interview →
                  </button>

                </div>

              ) : (

                <div className="interview-history-list">

                  {interviewHistory.history.map(
                    (item, index) => {

                      const isExpanded =
                        expandedInterview === item.id;

                      return (

                        <article
                          key={item.id}
                          className="interview-history-card"
                        >

                          {/* =====================================
                              INTERVIEW CARD HEADER
                          ===================================== */}

                          <div
                            className="interview-card-header"
                            onClick={() =>
                              toggleInterview(item.id)
                            }
                          >

                            <div className="interview-number">

                              <span>
                                INTERVIEW
                              </span>

                              <strong>
                                #{item.id}
                              </strong>

                            </div>

                            <div className="interview-question-preview">

                              <h3>
                                {item.question}
                              </h3>

                              <div className="interview-meta">

                                <span>
                                  Skill: {item.skill || "General"}
                                </span>

                                <span>
                                  Type: {item.question_type || "General"}
                                </span>

                                <span>
                                  Difficulty: {item.difficulty || "Medium"}
                                </span>

                              </div>

                            </div>

                            <div className="interview-score">

                              <strong>
                                {item.score}%
                              </strong>

                              <span>
                                {isExpanded
                                  ? "▲ Hide"
                                  : "▼ Details"}
                              </span>

                            </div>

                          </div>


                          {/* =====================================
                              INTERVIEW DETAILS
                          ===================================== */}

                          {isExpanded && (

                            <div className="interview-details">

                              {/* ANSWER */}

                              <div className="interview-detail-block">

                                <h4>
                                  📝 Your Answer
                                </h4>

                                <p className="interview-answer">
                                  {item.answer ||
                                    "No answer recorded."}
                                </p>

                              </div>


                              {/* SCORE GRID */}

                              <div className="interview-score-grid">

                                <div>
                                  <span>Overall</span>
                                  <strong>
                                    {item.score}%
                                  </strong>
                                </div>

                                <div>
                                  <span>Relevance</span>
                                  <strong>
                                    {item.relevance_score}%
                                  </strong>
                                </div>

                                <div>
                                  <span>Technical</span>
                                  <strong>
                                    {item.technical_score}%
                                  </strong>
                                </div>

                                <div>
                                  <span>Project</span>
                                  <strong>
                                    {item.project_score}%
                                  </strong>
                                </div>

                                <div>
                                  <span>Communication</span>
                                  <strong>
                                    {item.communication_score}%
                                  </strong>
                                </div>

                                <div>
                                  <span>Time</span>
                                  <strong>
                                    {item.time_score}%
                                  </strong>
                                </div>

                              </div>


                              {/* TIME */}

                              <div className="interview-time-info">

                                <span>
                                  ⏱ Time Taken:
                                  {" "}
                                  {item.time_taken} sec
                                </span>

                                <span>
                                  Time Limit:
                                  {" "}
                                  {item.time_limit} sec
                                </span>

                              </div>


                              {/* FEEDBACK */}

                              {item.feedback && (

                                <div className="interview-detail-block">

                                  <h4>
                                    💬 Feedback
                                  </h4>

                                  <p>
                                    {item.feedback}
                                  </p>

                                </div>

                              )}


                              {/* STRENGTHS */}

                              {item.strengths &&
                              item.strengths.length > 0 && (

                                <div className="interview-feedback-grid">

                                  <div className="interview-strengths">

                                    <h4>
                                      ✅ Strengths
                                    </h4>

                                    <ul>

                                      {item.strengths.map(
                                        (strength, strengthIndex) => (

                                          <li
                                            key={strengthIndex}
                                          >
                                            {strength}
                                          </li>

                                        )
                                      )}

                                    </ul>

                                  </div>


                                  {/* IMPROVEMENTS */}

                                  {item.improvements &&
                                  item.improvements.length > 0 && (

                                    <div className="interview-improvements">

                                      <h4>
                                        📈 Improvements
                                      </h4>

                                      <ul>

                                        {item.improvements.map(
                                          (
                                            improvement,
                                            improvementIndex
                                          ) => (

                                            <li
                                              key={improvementIndex}
                                            >
                                              {improvement}
                                            </li>

                                          )
                                        )}

                                      </ul>

                                    </div>

                                  )}

                                </div>

                              )}


                              {/* TOPICS */}

                              {item.matched_topics &&
                              item.matched_topics.length > 0 && (

                                <div className="interview-topics">

                                  <h4>
                                    🎯 Matched Topics
                                  </h4>

                                  <div>

                                    {item.matched_topics.map(
                                      (topic, topicIndex) => (

                                        <span
                                          key={topicIndex}
                                        >
                                          {topic}
                                        </span>

                                      )
                                    )}

                                  </div>

                                </div>

                              )}


                              {/* DATE */}

                              <div className="interview-created-date">

                                🕒{" "}
                                {new Date(
                                  item.created_at
                                ).toLocaleString()}

                              </div>

                            </div>

                          )}

                        </article>

                      );


                    }
                  )}

                </div>

              )}

            </section>

          )}

        </section>
      )}


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="history-footer">
        AI Resume Analyzer • Track your progress. Improve your career.
      </footer>

    </div>
  );
}

export default History;