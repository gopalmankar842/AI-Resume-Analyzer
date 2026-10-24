import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import "./Analyze.css";

function Analyze() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [message, setMessage] = useState("");
  const [resumeId, setResumeId] = useState(null);

  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const [result, setResult] = useState(null);
  const [atsResult, setAtsResult] = useState(null);
  const [checkingATS, setCheckingATS] = useState(false);

  // =========================
  // FILE SELECT
  // =========================

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setFile(null);
      setMessage("Please select a PDF file only.");
      return;
    }

    setFile(selectedFile);
    setMessage("");
    setResumeId(null);
    setResult(null);
    setAtsResult(null);
  };

  // =========================
  // UPLOAD RESUME
  // =========================

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF resume.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setUploading(true);
      setMessage("");

      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const response = await API.post(
        "/resume/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload Response:", response.data);

      setResumeId(response.data.resume_id);

      setMessage("Resume uploaded successfully!");

    } catch (error) {
      console.error("Upload Error:", error);

      setMessage(
        error.response?.data?.detail ||
        "Resume upload failed."
      );

    } finally {
      setUploading(false);
    }
  };

  // =========================
  // ANALYZE RESUME
  // =========================

  const handleAnalyze = async () => {
    if (!resumeId) {
      setMessage("Please upload your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      return;
    }

    try {
      setAnalyzing(true);
      setMessage("");
      setResult(null);

    const response = await API.post(
      `/resume/${resumeId}/final-match`,
        null,
        {
          params: {
            job_description: jobDescription,
          },
        }
      );

      console.log("Analysis Result:", response.data);

      setResult(response.data);

      setMessage("Resume analyzed successfully!");

    } catch (error) {
      console.error("Analysis Error:", error);

      setMessage(
        error.response?.data?.detail ||
        "Resume analysis failed."
      );

    } finally {
      setAnalyzing(false);
    }
  };
  
  const handleATSCheck = async () => {
    if (!resumeId) {
      setMessage("Please upload your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      return;
    }

    try {
      setCheckingATS(true);
      setMessage("");
      setAtsResult(null);

      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      const response = await API.post(
        `/resume/${resumeId}/ats-check`,
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

      console.log("ATS Check Result:", response.data);
      setAtsResult(response.data);
      setMessage("ATS check completed successfully!");
    } catch (error) {
      console.error("ATS Check Error:", error);

      setMessage(
        error.response?.data?.detail ||
          "ATS check failed. Please try again."
      );
    } finally {
      setCheckingATS(false);
    }
  };


  return (
    <div className="analyze-page">

      {/* =========================
          TOP NAVIGATION
      ========================= */}

      <header className="analyze-topbar">

        <div className="analyze-brand">

          <div className="analyze-logo">
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
          className="back-dashboard-button"
          onClick={() => navigate("/dashboard")}
        >
          ← Dashboard
        </button>

      </header>


      {/* =========================
          PAGE HEADER
      ========================= */}

      <section className="analyze-header">

        <div>

          <span className="analyze-eyebrow">
            AI RESUME ANALYSIS
          </span>

          <h1>
            Analyze Your Resume
          </h1>

          <p>
            Compare your resume with a target job
            description and discover how well you match.
          </p>

        </div>

      </section>


      {/* =========================
          ANALYSIS WORKSPACE
      ========================= */}

      <section className="analysis-workspace">


        {/* =========================
            UPLOAD CARD
        ========================= */}

        <div className="analysis-card">

          <div className="card-heading">

            <div className="step-number">
              01
            </div>

            <div>
              <h2>
                Upload Resume
              </h2>

              <p>
                Upload your latest PDF resume.
              </p>
            </div>

          </div>


          {/* FILE DROP AREA */}

          <label
            htmlFor="resume-file"
            className={`file-drop-zone ${
              file ? "file-selected" : ""
            }`}
          >

            <div className="upload-icon">
              {file ? "✓" : "↑"}
            </div>

            {file ? (
              <>
                <h3>
                  Resume Selected
                </h3>

                <p className="selected-file">
                  {file.name}
                </p>

                <span>
                  Click to choose another PDF
                </span>
              </>
            ) : (
              <>
                <h3>
                  Choose your resume
                </h3>

                <p>
                  Click here to select a PDF file
                </p>

                <span>
                  PDF files only
                </span>
              </>
            )}

            <input
              id="resume-file"
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              hidden
            />

          </label>


          {/* UPLOAD BUTTON */}

          <button
            type="button"
            className="primary-analyze-button"
            onClick={handleUpload}
            disabled={uploading || !file}
          >

            {uploading ? (
              <>
                <span className="analyze-spinner"></span>
                Uploading...
              </>
            ) : (
              <>
                Upload Resume →
              </>
            )}

          </button>


          {/* RESUME ID */}

          {resumeId && (
            <div className="resume-id-box">

              <span>
                Resume ID
              </span>

              <strong>
                #{resumeId}
              </strong>

              <span className="success-dot">
                ● Uploaded
              </span>

            </div>
          )}

        </div>


        {/* =========================
            JOB DESCRIPTION CARD
        ========================= */}

        <div className="analysis-card">

          <div className="card-heading">

            <div className="step-number">
              02
            </div>

            <div>
              <h2>
                Job Description
              </h2>

              <p>
                Paste the job description you're targeting.
              </p>
            </div>

          </div>


          <div className="job-description-wrapper">

            <textarea
              className="job-description-input"
              rows="13"
              placeholder="Paste the complete job description here...

Example:
We are looking for a Python Developer with experience in FastAPI, SQL, Machine Learning, Docker and AWS..."
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value);
                setMessage("");
              }}
            />

            <div className="character-count">
              {jobDescription.length} characters
            </div>

          </div>


          {/* ANALYZE BUTTON */}

          <button
            type="button"
            className="primary-analyze-button analyze-submit"
            onClick={handleAnalyze}
            disabled={
              analyzing ||
              !resumeId ||
              !jobDescription.trim()
            }
          >

            {analyzing ? (
              <>
                <span className="analyze-spinner"></span>
                Analyzing Resume...
              </>
            ) : (
              <>
                ✨ Analyze Resume
              </>
            )}

          </button>
          
          <button
            type="button"
            className="primary-analyze-button analyze-submit"
            onClick={handleATSCheck}
            disabled={
              checkingATS ||
              !resumeId ||
              !jobDescription.trim()
            }
          >
            {checkingATS ? (
              <>
                <span className="analyze-spinner"></span>
                Checking ATS Compatibility...
              </>
            ) : (
              <>📋 Check ATS Compatibility</>
            )}
          </button>


          {!resumeId && (
            <p className="helper-text">
              Upload your resume first to enable analysis.
            </p>
          )}

        </div>

      </section>


      {/* =========================
          LOADING
      ========================= */}

      {(uploading || analyzing || checkingATS) && (
        <div className="analysis-loading">

          <div className="large-spinner"></div>

          <div>
            <strong>
              {uploading
                ? "Uploading your resume..."
                : checkingATS
                  ? "Checking ATS compatibility..."
                  : "Analyzing your resume..."}
            </strong>

            <p>
              Please wait while AI processes your information.
            </p>
          </div>

        </div>
      )}


      {/* =========================
          MESSAGE
      ========================= */}

      {message && (
        <div
          className={`analysis-message ${
            message.toLowerCase().includes("success")
              ? "success"
              : "error"
          }`}
        >
          <span>
            {message.toLowerCase().includes("success")
              ? "✓"
              : "!"}
          </span>

          {message}
        </div>
      )}


      {/* =========================
          RESULTS
      ========================= */}

      {result && (
        <section className="results-section">

          <div className="results-header">

            <div>

              <span className="analyze-eyebrow">
                ANALYSIS COMPLETE
              </span>

              <h2>
                Your Resume Results
              </h2>

              <p>
                Here's how your resume matches the job description.
              </p>

            </div>

            <div className="result-status">
              ✓ Complete
            </div>

          </div>


          {/* SCORE CARDS */}

          <div className="result-grid">


            {/* FINAL MATCH */}

            <div className="result-score-card featured-score">

              <div className="score-card-title">
                <span>
                  Final Match
                </span>

                <div className="score-mini-icon">
                  ★
                </div>
              </div>

              <div className="big-score">
                {result.final_match_percentage}%
              </div>

              <div className="progress-container">

                <div
                  className="progress-bar final-progress"
                  style={{
                    width: `${result.final_match_percentage}%`
                  }}
                ></div>

              </div>

              <p>
                Overall compatibility
              </p>

            </div>


            {/* SKILL MATCH */}

            <div className="result-score-card">

              <div className="score-card-title">
                <span>
                  Skill Match
                </span>

                <div className="score-mini-icon">
                  ◈
                </div>
              </div>

              <div className="big-score">
                {result.skill_match_percentage}%
              </div>

              <div className="progress-container">

                <div
                  className="progress-bar skill-progress"
                  style={{
                    width: `${result.skill_match_percentage}%`
                  }}
                ></div>

              </div>

              <p>
                Required skills matched
              </p>

            </div>


            {/* SEMANTIC MATCH */}

            <div className="result-score-card">

              <div className="score-card-title">
                <span>
                  Semantic Match
                </span>

                <div className="score-mini-icon">
                  ◉
                </div>
              </div>

              <div className="big-score">
                {result.semantic_match_percentage}%
              </div>

              <div className="progress-container">

                <div
                  className="progress-bar semantic-progress"
                  style={{
                    width: `${result.semantic_match_percentage}%`
                  }}
                ></div>

              </div>

              <p>
                Content similarity
              </p>

            </div>

          </div>


          {/* SKILLS */}

          <div className="skills-container">


            {/* MATCHED */}

            <div className="skill-box matched-box">

              <div className="skill-box-header">

                <div className="skill-box-icon">
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


              <div className="skill-list">

                {result.matched_skills &&
                result.matched_skills.length > 0 ? (
                  result.matched_skills.map(
                    (skill, index) => (
                      <span
                        key={index}
                        className="skill-badge matched-badge"
                      >
                        ✓ {skill}
                      </span>
                    )
                  )
                ) : (
                  <span className="empty-skills">
                    No matched skills found.
                  </span>
                )}

              </div>

            </div>


            {/* MISSING */}

            <div className="skill-box missing-box">

              <div className="skill-box-header">

                <div className="skill-box-icon">
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


              <div className="skill-list">

                {result.missing_skills &&
                result.missing_skills.length > 0 ? (
                  result.missing_skills.map(
                    (skill, index) => (
                      <span
                        key={index}
                        className="skill-badge missing-badge"
                      >
                        ⚠ {skill}
                      </span>
                    )
                  )
                ) : (
                  <span className="empty-skills">
                    No missing skills found.
                  </span>
                )}

              </div>

            </div>

          </div>


          {/* NEXT ACTIONS */}

          <div className="result-actions">

            <button
              type="button"
              onClick={() => navigate("/recommendations")}
            >
              🎯 Career Recommendations
            </button>
            
            
            <button
              type="button"
              onClick={() => navigate("/interview")}
            >
              🎤 Interview Preparation
            </button>

            <button
              type="button"
              onClick={() => navigate("/history")}
            >
              ◷ View History
            </button>

          </div>

        </section>
      )}

      
        {atsResult && (
          <section className="results-section ats-results-section">
            <div className="results-header">
              <div>
                <span className="analyze-eyebrow">
                  ATS CHECK COMPLETE
                </span>
                <h2>ATS Compatibility Report</h2>
                <p>
                  An estimated assessment of your resume against
                  the selected job description.
                </p>
              </div>

              <div className="result-status">✓ Complete</div>
            </div>

            <div className="result-grid">
              <div className="result-score-card featured-score">
                <div className="score-card-title">
                  <span>Estimated ATS Score</span>
                  <div className="score-mini-icon">✓</div>
                </div>

                <div className="big-score">
                  {atsResult.ats_score}%
                </div>

                <div className="progress-container">
                  <div
                    className="progress-bar final-progress"
                    style={{
                      width: `${Math.min(
                        100,
                        Math.max(0, Number(atsResult.ats_score) || 0)
                      )}%`,
                    }}
                  />
                </div>

                <p>{atsResult.score_type}</p>
              </div>

              {Object.entries(
                atsResult.score_breakdown || {}
              ).map(([key, value]) => (
                <div className="result-score-card" key={key}>
                  <div className="score-card-title">
                    <span>
                      {key
                        .replaceAll("_", " ")
                        .replace(/\b\w/g, (char) =>
                          char.toUpperCase()
                        )}
                    </span>
                  </div>

                  <div className="big-score">{value}%</div>

                  <div className="progress-container">
                    <div
                      className="progress-bar skill-progress"
                      style={{
                        width: `${Math.min(
                          100,
                          Math.max(0, Number(value) || 0)
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <div className="skills-container">
              <div className="skill-box matched-box">
                <div className="skill-box-header">
                  <div className="skill-box-icon">✓</div>
                  <div>
                    <h3>ATS Matched Skills</h3>
                    <span>
                      {atsResult.matched_skills?.length || 0} skills found
                    </span>
                  </div>
                </div>

                <div className="skill-list">
                  {atsResult.matched_skills?.length ? (
                    atsResult.matched_skills.map((skill) => (
                      <span
                        key={skill}
                        className="skill-badge matched-badge"
                      >
                        ✓ {skill}
                      </span>
                    ))
                  ) : (
                    <span className="empty-skills">
                      No matched skills found.
                    </span>
                  )}
                </div>
              </div>

              <div className="skill-box missing-box">
                <div className="skill-box-header">
                  <div className="skill-box-icon">!</div>
                  <div>
                    <h3>ATS Missing Skills</h3>
                    <span>
                      {atsResult.missing_skills?.length || 0} skills not detected
                    </span>
                  </div>
                </div>

                <div className="skill-list">
                  {atsResult.missing_skills?.length ? (
                    atsResult.missing_skills.map((skill) => (
                      <span
                        key={skill}
                        className="skill-badge missing-badge"
                      >
                        ⚠ {skill}
                      </span>
                    ))
                  ) : (
                    <span className="empty-skills">
                      No missing skills detected.
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="analysis-card">
              <h3>Resume Section Checklist</h3>

              <p>
                Word count: <strong>{atsResult.word_count ?? 0}</strong>
              </p>

              {Object.entries(
                atsResult.sections_found || {}
              ).map(([section, found]) => (
                <p key={section}>
                  {found ? "✓" : "✗"}{" "}
                  {section
                    .replaceAll("_", " ")
                    .replace(/\b\w/g, (char) =>
                      char.toUpperCase()
                    )}{" "}
                  — {found ? "Detected" : "Not detected"}
                </p>
              ))}
            </div>

            {atsResult.warnings?.length > 0 && (
              <div className="analysis-card">
                <h3>Warnings</h3>
                <ul>
                  {atsResult.warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}

            {atsResult.suggestions?.length > 0 && (
              <div className="analysis-card">
                <h3>Suggestions to Improve Your ATS Score</h3>
                <ul>
                  {atsResult.suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}

            <p className="helper-text">
              {atsResult.disclaimer ||
                "This is an estimate, not a score from an employer's ATS."}
            </p>
          </section>
        )}



      {/* =========================
          FOOTER
      ========================= */}

      <footer className="analyze-footer">
        AI Resume Analyzer • Analyze smarter. Prepare better.
      </footer>

    </div>
  );
}

export default Analyze;