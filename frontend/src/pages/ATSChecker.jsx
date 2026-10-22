
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./ATSChecker.css";
function ATSChecker() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setFile(null);
      setResult(null);
      setMessage("Please select a PDF resume.");
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setMessage("");
  };

  const handleCheckATS = async () => {
    if (!file) {
      setMessage("Please select a PDF resume first.");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");
      setResult(null);

      // Upload the resume using the existing endpoint.
      const uploadResponse = await axios.post(
        "http://127.0.0.1:8000/resume/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const resumeId = uploadResponse.data.resume_id;

      // This standalone endpoint will be implemented
      // separately on the backend.
      const scoreResponse = await axios.post(
        `http://127.0.0.1:8000/resume/${resumeId}/ats-score`,
        null,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(scoreResponse.data);
      setMessage("ATS score calculated successfully!");
    } catch (error) {
      console.error("ATS Score Checker Error:", error);

      setMessage(
        error.response?.data?.detail ||
          "Could not calculate the ATS score. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

return (
  <div className="ats-checker-page">
    <div className="ats-checker-container">
      <header className="ats-checker-header">
        <div>
            <h1 className="ats-checker-heading">
            ATS Score Checker
            </h1>

            <p className="ats-checker-subtitle">
            Upload your resume to evaluate its ATS readiness.
            No job description is required.
            </p>
        </div>

        <button
            type="button"
            className="ats-back-button"
            onClick={() => navigate("/dashboard")}
        >
            ← Dashboard
        </button>
        </header>

      <section className="ats-panel">
        <h2 className="ats-panel-title">Upload Your Resume</h2>

        <p className="ats-muted">
            Upload your PDF to check its general ATS readiness.
        </p>

        <div className="ats-upload-zone">
            <label htmlFor="ats-resume">
            Select your PDF resume
            </label>

            <input
            id="ats-resume"
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            />

            {file && (
            <p className="ats-file-name">
                Selected: {file.name}
            </p>
            )}
        </div>

        <button
            type="button"
            className="ats-primary-button"
            onClick={handleCheckATS}
            disabled={!file || loading}
        >
            {loading ? "Checking ATS Score..." : "Check ATS Score"}
        </button>
        </section>

      {message && (
        <p
            className={`ats-message ${
            message === "ATS score calculated successfully!"
                ? "ats-message-success"
                : "ats-message-error"
            }`}
            role="status"
        >
            {message}
        </p>
        )}

     
  {result && (
    <>
      {/* ATS SCORE SUMMARY */}
      <section className="ats-panel">
        <div className="ats-score-panel">
          <div>
            <p className="ats-score-label">
              YOUR RESUME ATS READINESS
            </p>

            <h2 className="ats-score-number">
              {result.ats_score}
              <span> / 100</span>
            </h2>

            <p className="ats-score-description">
              Estimated ATS readiness based on your resume's
              extracted text and section completeness.
            </p>
          </div>

          <div
            className="ats-score-ring"
            style={{
              "--score": Math.max(
                0,
                Math.min(100, Number(result.ats_score) || 0)
              ),
            }}
            role="img"
            aria-label={`ATS score ${result.ats_score} out of 100`}
          >
            <div className="ats-score-ring-content">
              <div className="ats-score-ring-value">
                {result.ats_score}
              </div>
              <div className="ats-score-ring-caption">
                OUT OF 100
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SCORE BREAKDOWN */}
      {result.score_breakdown && (
        <section className="ats-panel">
          <h2 className="ats-panel-title">Score Breakdown</h2>

          <div className="ats-breakdown-list">
            {Object.entries(result.score_breakdown).map(
              ([name, score]) => {
                const value = Math.max(
                  0,
                  Math.min(100, Number(score) || 0)
                );

                return (
                  <div className="ats-breakdown-item" key={name}>
                    <div className="ats-breakdown-heading">
                      <span>
                        {name
                          .replaceAll("_", " ")
                          .replace(/\b\w/g, (letter) =>
                            letter.toUpperCase()
                          )}
                      </span>
                      <strong>{value}/100</strong>
                    </div>

                    <div className="ats-breakdown-track">
                      <div
                        className="ats-breakdown-fill"
                        style={{ width: `${value}%` }}
                      />
                    </div>
                  </div>
                );
              }
            )}
          </div>
        </section>
      )}

      {/* RESUME SECTION CHECKLIST */}
      {result.sections_found && (
        <section className="ats-panel">
          <h2 className="ats-panel-title">
            Resume Section Checklist
          </h2>

          <div className="ats-section-list">
            {Object.entries(result.sections_found).map(
              ([name, found]) => (
                <div
                  key={name}
                  className={`ats-section-item ${
                    found
                      ? "ats-section-found"
                      : "ats-section-missing"
                  }`}
                >
                  <span className="ats-section-icon">
                    {found ? "✓" : "!"}
                  </span>

                  <span className="ats-section-name">
                    {name
                      .replaceAll("_", " ")
                      .replace(/\b\w/g, (letter) =>
                        letter.toUpperCase()
                      )}
                  </span>

                  <span className="ats-muted">
                    {found ? "Detected" : "Not detected"}
                  </span>
                </div>
              )
            )}
          </div>
        </section>
      )}

      {/* WARNINGS */}
      {result.warnings?.length > 0 && (
        <section className="ats-panel">
          <h2 className="ats-panel-title">Warnings</h2>
          <ul className="ats-list">
            {result.warnings.map((warning, index) => (
              <li key={index}>{warning}</li>
            ))}
          </ul>
        </section>
      )}

      {/* IMPROVEMENT SUGGESTIONS */}
      {result.suggestions?.length > 0 && (
        <section className="ats-panel">
          <h2 className="ats-panel-title">
            Improvement Suggestions
          </h2>

          <p className="ats-muted">
            Review these suggestions to improve your resume's structure
            and readability.
          </p>

          <ul className="ats-list">
            {result.suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </section>
      )}

      {/* DISCLAIMER */}
      {result.disclaimer && (
        <div className="ats-disclaimer">
          <strong>Important:</strong> {result.disclaimer}
        </div>
      )}
       </>
  )}
    </div>
  </div>
  );
}

export default ATSChecker;
