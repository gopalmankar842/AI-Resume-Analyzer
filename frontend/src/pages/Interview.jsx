import { useEffect, useRef, useState } from "react";
import axios from "axios";
import "./Interview.css";

function Interview() {
  const [resumeId, setResumeId] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);

  const [timeLeft, setTimeLeft] = useState(0);
  const [timeTaken, setTimeTaken] = useState(0);

  const [interviewStarted, setInterviewStarted] = useState(false);
  const [interviewFinished, setInterviewFinished] = useState(false);

  const [completedScores, setCompletedScores] = useState([]);

  /*
   * Prevents the timer from running before
   * the current question has been initialized.
   */
  const timerStartedRef = useRef(false);

  /*
   * Prevent multiple automatic skips.
   */
  const timeoutHandledRef = useRef(false);

  const question = questions[currentQuestion];

  // ============================================================
  // ANSWER VALIDATION
  // ============================================================

  const getAnswerValidationError = () => {
    const cleanedAnswer = answer.trim();

    if (!cleanedAnswer) {
      return "Please write your answer.";
    }

    const words = cleanedAnswer.split(/\s+/);

    if (words.length < 5) {
      return "Your answer is too short.";
    }

    const letters = cleanedAnswer.replace(
      /[^a-zA-Z]/g,
      ""
    );

    if (letters.length < 10) {
      return "Please provide a meaningful answer.";
    }

    return null;
  };

  const isAnswerValid = () => {
    return getAnswerValidationError() === null;
  };

  // ============================================================
  // START INTERVIEW
  // ============================================================

  const startInterview = async () => {
    if (!resumeId.trim()) {
      setMessage("Please enter a resume ID.");
      return;
    }

    if (!jobDescription.trim()) {
      setMessage("Please enter a job description.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      setQuestions([]);
      setCurrentQuestion(0);

      setAnswer("");
      setEvaluation(null);

      setInterviewFinished(false);
      setCompletedScores([]);

      setTimeLeft(0);
      setTimeTaken(0);

      timerStartedRef.current = false;
      timeoutHandledRef.current = false;

      const response = await axios.post(
        `http://127.0.0.1:8000/resume/${resumeId}/interview-questions`,
        null,
        {
          params: {
            job_description: jobDescription,
          },
        }
      );

      console.log(
        "Interview Questions:",
        response.data
      );

      const generatedQuestions =
        response.data.questions || [];

      if (!generatedQuestions.length) {
        setMessage(
          "No interview questions were generated."
        );
        return;
      }

      setQuestions(generatedQuestions);
      setCurrentQuestion(0);

      setInterviewStarted(true);
      setInterviewFinished(false);

      setMessage(
        "Interview started successfully!"
      );

    } catch (error) {
      console.error(
        "Interview Generation Error:",
        error
      );

      setMessage(
        error.response?.data?.detail ||
        "Unable to generate interview questions."
      );

    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // INITIALIZE CURRENT QUESTION TIMER
  // ============================================================

  useEffect(() => {
    if (
      !interviewStarted ||
      !question ||
      interviewFinished
    ) {
      return;
    }

    timerStartedRef.current = false;
    timeoutHandledRef.current = false;

    setAnswer("");
    setEvaluation(null);
    setMessage("");

    const limit =
      Number(question.time_limit) || 90;

    setTimeLeft(limit);
    setTimeTaken(0);

    const timerStart = setTimeout(() => {
      timerStartedRef.current = true;
    }, 0);

    return () => {
      clearTimeout(timerStart);
    };

  }, [
    currentQuestion,
    interviewStarted,
    interviewFinished
  ]);

  // ============================================================
  // MOVE TO NEXT QUESTION
  // ============================================================

  const moveToNextQuestion = () => {
    timerStartedRef.current = false;
    timeoutHandledRef.current = false;

    if (
      currentQuestion <
      questions.length - 1
    ) {
      setCurrentQuestion(
        (previous) =>
          previous + 1
      );

      setAnswer("");
      setEvaluation(null);

      setMessage("");

      setTimeLeft(0);
      setTimeTaken(0);

    } else {
      setInterviewFinished(true);
      setInterviewStarted(false);

      setEvaluation(null);

      setMessage(
        "🎉 Interview completed successfully!"
      );
    }
  };

  // ============================================================
  // SKIP QUESTION
  // ============================================================

  const skipQuestion = () => {
    if (timeoutHandledRef.current) {
      return;
    }

    timeoutHandledRef.current = true;

    timerStartedRef.current = false;

    console.log(
      `Question ${
        currentQuestion + 1
      } skipped.`
    );

    setCompletedScores(
      (previous) => [
        ...previous,
        {
          score: 0,
          overall_score: 0,
          skipped: true,
        },
      ]
    );

    setMessage(
      "⏰ Time's up! Question skipped."
    );

    setTimeout(() => {
      moveToNextQuestion();
    }, 800);
  };

  // ============================================================
  // TIMER
  // ============================================================

  useEffect(() => {
    if (
      !interviewStarted ||
      !question ||
      evaluation ||
      interviewFinished ||
      evaluating
    ) {
      return;
    }

    if (!timerStartedRef.current) {
      return;
    }

    if (timeLeft <= 0) {
      if (timeoutHandledRef.current) {
        return;
      }

      if (!answer.trim()) {
        skipQuestion();
        return;
      }

      submitAnswer(true);
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(
        (previous) => {
          if (previous <= 1) {
            return 0;
          }

          return previous - 1;
        }
      );

      setTimeTaken(
        (previous) =>
          previous + 1
      );
    }, 1000);

    return () => {
      clearInterval(timer);
    };

  }, [
    timeLeft,
    interviewStarted,
    question,
    evaluation,
    interviewFinished,
    answer,
    evaluating,
    currentQuestion
  ]);

  // ============================================================
  // FORMAT TIME
  // ============================================================

  const formatTime = (seconds) => {
    const safeSeconds =
      Math.max(
        0,
        Number(seconds) || 0
      );

    const minutes =
      Math.floor(
        safeSeconds / 60
      );

    const remainingSeconds =
      safeSeconds % 60;

    return `${String(minutes).padStart(
      2,
      "0"
    )}:${String(
      remainingSeconds
    ).padStart(
      2,
      "0"
    )}`;
  };

  // ============================================================
  // TIMER COLOR
  // ============================================================

  const getTimerClass = () => {
    if (timeLeft <= 10) {
      return "timer-danger";
    }

    if (timeLeft <= 30) {
      return "timer-warning";
    }

    return "timer-normal";
  };

  // ============================================================
  // SUBMIT ANSWER
  // ============================================================

  const submitAnswer = async (
    autoSubmitted = false
  ) => {
    if (!question) {
      return;
    }

    const cleanedAnswer =
      answer.trim();

    // ==========================================================
    // EMPTY ANSWER
    // ==========================================================

    if (!cleanedAnswer) {
      if (autoSubmitted) {
        skipQuestion();
      } else {
        setMessage(
          "✍️ Please write your answer before submitting."
        );
      }

      return;
    }

    // ==========================================================
    // WORD COUNT
    // ==========================================================

    const words =
      cleanedAnswer.split(/\s+/);

    if (words.length < 5) {
      if (autoSubmitted) {
        skipQuestion();
      } else {
        setMessage(
          "⚠️ Your answer is too short. Please explain your answer properly using at least 5 words."
        );
      }

      return;
    }

    // ==========================================================
    // RANDOM CHARACTER CHECK
    // ==========================================================

    const letters =
      cleanedAnswer.replace(
        /[^a-zA-Z]/g,
        ""
      );

    if (letters.length < 10) {
      if (autoSubmitted) {
        skipQuestion();
      } else {
        setMessage(
          "⚠️ Please provide a meaningful answer."
        );
      }

      return;
    }

    try {
      /*
       * Stop timer while evaluating.
       */
      timerStartedRef.current = false;

      setEvaluating(true);
      setMessage("");

      const timeLimit =
        Number(
          question.time_limit
        ) || 90;

      let calculatedTime =
        timeLimit -
        timeLeft;

      if (autoSubmitted) {
        calculatedTime = timeLimit;
      }

      const finalTimeTaken =
        Math.max(
          0,
          Math.min(
            calculatedTime,
            timeLimit
          )
        );

      // ========================================================
      // QUESTION METADATA
      // ========================================================

      const questionSkill =
        question.skill ||
        "General";

      const questionType =
        question.type ||
        "Technical";

      const questionDifficulty =
        question.difficulty ||
        "Medium";

      console.log(
        "Submitting Answer:",
        {
          resumeId,
          question:
            question.question,
          answer:
            cleanedAnswer,
          job_description:
            jobDescription,
          time_taken:
            finalTimeTaken,
          time_limit:
            timeLimit,

          // STEP 68.5.1
          skill:
            questionSkill,

          question_type:
            questionType,

          difficulty:
            questionDifficulty,
        }
      );

      // ========================================================
      // API
      // ========================================================

      const response =
        await axios.post(
          `http://127.0.0.1:8000/resume/${resumeId}/evaluate-answer`,
          {
            question:
              question.question,

            answer:
              cleanedAnswer,

            job_description:
              jobDescription,

            time_taken:
              finalTimeTaken,

            time_limit:
              timeLimit,

            // ==================================================
            // STEP 68.5.1
            // SEND QUESTION METADATA
            // ==================================================

            skill:
              questionSkill,

            question_type:
              questionType,

            difficulty:
              questionDifficulty,
          }
        );

      console.log(
        "Answer Evaluation:",
        response.data
      );

      const result =
        response.data.evaluation ||
        response.data;

      setEvaluation(result);

      setCompletedScores(
        (previous) => [
          ...previous,
          result,
        ]
      );

      if (autoSubmitted) {
        setMessage(
          "⏰ Time's up! Your answer was submitted and evaluated."
        );
      } else {
        setMessage(
          "✅ Answer evaluated successfully!"
        );
      }

    } catch (error) {
      console.error(
        "Answer Evaluation Error:",
        error
      );

      console.error(
        "Backend Response:",
        error.response?.data
      );

      timerStartedRef.current = false;

      setMessage(
        error.response?.data?.detail ||
        "Unable to evaluate your answer."
      );

    } finally {
      setEvaluating(false);
    }
  };

  // ============================================================
  // RESTART INTERVIEW
  // ============================================================

  const restartInterview = () => {
    timerStartedRef.current = false;
    timeoutHandledRef.current = false;

    setQuestions([]);

    setCurrentQuestion(0);

    setAnswer("");

    setEvaluation(null);

    setMessage("");

    setTimeLeft(0);

    setTimeTaken(0);

    setInterviewStarted(false);

    setInterviewFinished(false);

    setCompletedScores([]);
  };

  // ============================================================
// FINAL SCORE
// ============================================================

const calculateFinalScore = () => {

  /*
   * Only answered questions should
   * contribute to the final score.
   *
   * Skipped questions are displayed
   * separately and do not reduce the
   * interview score.
   */

  const answeredScores =
    completedScores
      .filter(
        (item) =>
          !item?.skipped
      )
      .map(
        (item) =>
          Number(
            item?.score ??
            item?.overall_score ??
            0
          )
      )
      .filter(
        (score) =>
          Number.isFinite(score)
      );

  /*
   * No answered questions.
   */

  if (
    answeredScores.length === 0
  ) {
    return 0;
  }

  /*
   * Calculate average score
   * using answered questions only.
   */

  const total =
    answeredScores.reduce(
      (sum, score) =>
        sum + score,
      0
    );

  return Math.round(
    total /
    answeredScores.length
  );
};

  // ============================================================
  // WORD COUNT
  // ============================================================

  const getWordCount = () => {
    if (!answer.trim()) {
      return 0;
    }

    return answer
      .trim()
      .split(/\s+/)
      .length;
  };

  // ============================================================
  // SCORE VALUE HELPER
  // ============================================================

  const getScore = (value) => {
    const score =
      Number(value ?? 0);

    return Math.min(
      100,
      Math.max(
        0,
        score
      )
    );
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="interview-container">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="interview-header">

        <div className="interview-icon">
          🎤
        </div>

        <div>

          <h1>
            Interview Preparation
          </h1>

          <p>
            Practice interview questions and get
            instant AI-powered feedback.
          </p>

        </div>

      </div>

      {/* ======================================================
          START INTERVIEW
      ====================================================== */}

      {!interviewStarted &&
        !interviewFinished && (

        <div className="interview-form">

          <div className="form-title">

            <h2>
              🚀 Start Your Interview
            </h2>

            <p>
              Enter your resume ID and target
              job description to begin.
            </p>

          </div>

          <div className="interview-field">

            <label>
              Resume ID
            </label>

            <input
              type="number"
              placeholder="Enter Resume ID"
              value={resumeId}
              onChange={(e) => {
                setResumeId(
                  e.target.value
                );

                setMessage("");
              }}
            />

          </div>

          <div className="interview-field">

            <label>
              Job Description
            </label>

            <textarea
              rows="10"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(
                  e.target.value
                );

                setMessage("");
              }}
            />

          </div>

          <button
            className="interview-button"
            onClick={startInterview}
            disabled={
              loading ||
              !resumeId.trim() ||
              !jobDescription.trim()
            }
          >

            {loading ? (

              <>
                <span className="button-spinner"></span>
                Generating Interview...
              </>

            ) : (

              <>
                🎯 Start Interview
              </>

            )}

          </button>

          {loading && (

            <div className="loading-container">

              <div className="spinner"></div>

              <p className="loading-text">
                Preparing your interview questions...
              </p>

            </div>

          )}

        </div>

      )}

      {/* ======================================================
          MESSAGE
      ====================================================== */}

      {message && (

        <div
          className={`interview-message ${
            message.includes(
              "successfully"
            )
              ? "success"
              : "warning"
          }`}
        >

          {message}

        </div>

      )}

      {/* ======================================================
          FINISHED
      ====================================================== */}

      {interviewFinished && (

        <div className="interview-finished">

          <div className="finished-icon">
            🏆
          </div>

          <h2>
            Interview Completed!
          </h2>

          <p>
            Great job! You completed all
            interview questions.
          </p>

          <div className="final-score-card">

            <span>
              Final Interview Score
            </span>

            <strong>
              {calculateFinalScore()}%
            </strong>

          </div>

          <div className="final-stats">

            <div>

              <strong>
                {questions.length}
              </strong>

              <span>
                Total Questions
              </span>

            </div>

            <div>

              <strong>
                {
                  completedScores.filter(
                    (item) =>
                      !item?.skipped
                  ).length
                }
              </strong>

              <span>
                Answered
              </span>

            </div>

            <div>

              <strong>
                {
                  completedScores.filter(
                    (item) =>
                      item?.skipped
                  ).length
                }
              </strong>

              <span>
                Skipped
              </span>

            </div>

          </div>

          <button
            className="interview-button"
            onClick={
              restartInterview
            }
          >
            🔄 Practice Again
          </button>

        </div>

      )}

      {/* ======================================================
          ACTIVE INTERVIEW
      ====================================================== */}

      {interviewStarted &&
        !interviewFinished &&
        question && (

        <div className="active-interview">

          {/* ==================================================
              PROGRESS
          ================================================== */}

          <div className="interview-progress">

            <div>

              Question{" "}

              <strong>
                {currentQuestion + 1}
              </strong>

              {" "}of{" "}

              <strong>
                {questions.length}
              </strong>

            </div>

            <div>

              {Math.round(
                (
                  (
                    currentQuestion + 1
                  ) /
                  questions.length
                ) * 100
              )}

              % Complete

            </div>

          </div>

          <div className="progress-track">

            <div
              className="progress-fill"
              style={{
                width: `${
                  (
                    (
                      currentQuestion + 1
                    ) /
                    questions.length
                  ) * 100
                }%`
              }}
            ></div>

          </div>

          {/* ==================================================
              QUESTION CARD
          ================================================== */}

          <div className="question-card">

            <div className="question-top">

              <div className="question-badges">

                <span className="skill-badge">
                  {question.skill}
                </span>

                <span className="type-badge">
                  {question.type}
                </span>

                <span
                  className={`difficulty-badge ${
                    question.difficulty
                      ?.toLowerCase()
                  }`}
                >
                  {question.difficulty}
                </span>

              </div>

              {/* TIMER */}

              <div
                className={`question-timer ${
                  getTimerClass()
                }`}
              >

                <span>
                  ⏱️
                </span>

                <strong>
                  {formatTime(
                    timeLeft
                  )}
                </strong>

              </div>

            </div>

            <div className="question-number">

              QUESTION{" "}
              {currentQuestion + 1}

            </div>

            <h2 className="question-text">

              {question.question}

            </h2>

            <div className="time-info">

              <span>
                ⏳ Time limit:
              </span>

              <strong>
                {
                  question.time_limit ||
                  90
                }{" "}
                seconds
              </strong>

            </div>

            <div className="question-divider"></div>

            {/* =================================================
                ANSWER
            ================================================= */}

            {!evaluation && (

              <div className="answer-section">

                <label>
                  ✍️ Your Answer
                </label>

                <textarea
                  className="answer-textarea"
                  rows="9"
                  placeholder="Type your answer here. Explain your answer clearly with examples where possible..."
                  value={answer}
                  onChange={(e) => {

                    setAnswer(
                      e.target.value
                    );

                    setMessage("");

                  }}
                  disabled={
                    evaluating
                  }
                />

                <div className="answer-footer">

                  <span>

                    {getWordCount()}{" "}

                    {
                      getWordCount() === 1
                        ? "word"
                        : "words"
                    }

                  </span>

                  <span>

                    Time used:{" "}

                    {formatTime(
                      timeTaken
                    )}

                  </span>

                </div>

                <button
                  className="submit-answer-button"
                  onClick={() =>
                    submitAnswer(false)
                  }
                  disabled={
                    evaluating ||
                    !isAnswerValid()
                  }
                >

                  {evaluating ? (

                    <>
                      <span className="button-spinner"></span>
                      Evaluating...
                    </>

                  ) : (

                    <>
                      🚀 Submit Answer
                    </>

                  )}

                </button>

                {!answer.trim() && (

                  <p className="answer-hint">

                    ✍️ Write your answer to enable
                    submission.

                  </p>

                )}

                {answer.trim() &&
                  getWordCount() < 5 && (

                  <p className="answer-hint warning-hint">

                    ⚠️ Please provide at least
                    5 words.

                  </p>

                )}

              </div>

            )}

            {/* =================================================
                IMPROVED EVALUATION
            ================================================= */}

            {evaluation && (

              <div className="evaluation-section">

                <div className="evaluation-title">

                  <div className="evaluation-icon">
                    🤖
                  </div>

                  <div>

                    <h2>
                      AI Answer Evaluation
                    </h2>

                    <p>
                      Here's how your answer performed.
                    </p>

                  </div>

                </div>

                {/* =================================================
                    SCORE GRID
                ================================================= */}

                <div className="evaluation-grid">

                  {/* Overall Score */}

                  <div className="evaluation-card overall">

                    <span>
                      🎯 Overall Score
                    </span>

                    <strong>
                      {
                        evaluation.score ??
                        evaluation.overall_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.score ??
                              evaluation.overall_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                  {/* Relevance */}

                  <div className="evaluation-card">

                    <span>
                      🎯 Relevance
                    </span>

                    <strong>
                      {
                        evaluation.relevance_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.relevance_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                  {/* Technical */}

                  <div className="evaluation-card">

                    <span>
                      💻 Technical
                    </span>

                    <strong>
                      {
                        evaluation.technical_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.technical_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                  {/* Project */}

                  <div className="evaluation-card">

                    <span>
                      🚀 Project
                    </span>

                    <strong>
                      {
                        evaluation.project_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.project_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                  {/* Communication */}

                  <div className="evaluation-card">

                    <span>
                      🗣️ Communication
                    </span>

                    <strong>
                      {
                        evaluation.communication_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.communication_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                  {/* Time */}

                  <div className="evaluation-card">

                    <span>
                      ⏱️ Time Management
                    </span>

                    <strong>
                      {
                        evaluation.time_score ??
                        0
                      }%
                    </strong>

                    <div className="evaluation-progress">

                      <div
                        className="evaluation-progress-fill"
                        style={{
                          width: `${
                            getScore(
                              evaluation.time_score
                            )
                          }%`
                        }}
                      ></div>

                    </div>

                  </div>

                </div>

                {/* =================================================
                    FEEDBACK
                ================================================= */}

                {evaluation.feedback && (

                  <div className="feedback-card">

                    <h3>
                      💡 Feedback
                    </h3>

                    <p>
                      {evaluation.feedback}
                    </p>

                  </div>

                )}

                {/* =================================================
                    STRENGTHS
                ================================================= */}

                {evaluation.strengths?.length > 0 && (

                  <div className="evaluation-list strengths">

                    <h3>
                      ✅ Strengths
                    </h3>

                    {evaluation.strengths.map(
                      (
                        item,
                        index
                      ) => (

                        <div
                          key={index}
                          className="evaluation-list-item"
                        >

                          ✓ {item}

                        </div>

                      )
                    )}

                  </div>

                )}

                {/* =================================================
                    IMPROVEMENTS
                ================================================= */}

                {evaluation.improvements?.length > 0 && (

                  <div className="evaluation-list improvements">

                    <h3>
                      ⚠️ Areas to Improve
                    </h3>

                    {evaluation.improvements.map(
                      (
                        item,
                        index
                      ) => (

                        <div
                          key={index}
                          className="evaluation-list-item"
                        >

                          → {item}

                        </div>

                      )
                    )}

                  </div>

                )}

                {/* =================================================
                    MATCHED TOPICS
                ================================================= */}

                {evaluation.matched_topics?.length > 0 && (

                  <div className="topics-section">

                    <h3>
                      🧠 Topics Detected
                    </h3>

                    <div className="topics-list">

                      {evaluation.matched_topics.map(
                        (
                          topic,
                          index
                        ) => (

                          <span
                            key={index}
                          >
                            {topic}
                          </span>

                        )
                      )}

                    </div>

                  </div>

                )}

                {/* =================================================
                    PROJECT TOPICS
                ================================================= */}

                {evaluation.project_topics?.length > 0 && (

                  <div className="topics-section">

                    <h3>
                      🚀 Project Topics
                    </h3>

                    <div className="topics-list">

                      {evaluation.project_topics.map(
                        (
                          topic,
                          index
                        ) => (

                          <span
                            key={index}
                          >
                            {topic}
                          </span>

                        )
                      )}

                    </div>

                  </div>

                )}

                {/* =================================================
                    ANSWER DETAILS
                ================================================= */}

                <div className="answer-evaluation-details">

                  <div>

                    <span>
                      📝 Words
                    </span>

                    <strong>
                      {
                        evaluation.word_count ??
                        getWordCount()
                      }
                    </strong>

                  </div>

                  <div>

                    <span>
                      ⏱️ Time Used
                    </span>

                    <strong>
                      {
                        formatTime(
                          evaluation.time_taken ??
                          timeTaken
                        )
                      }
                    </strong>

                  </div>

                  <div>

                    <span>
                      ⏳ Time Limit
                    </span>

                    <strong>
                      {
                        formatTime(
                          evaluation.time_limit ??
                          question.time_limit ??
                          90
                        )
                      }
                    </strong>

                  </div>

                </div>

                {/* =================================================
                    NEXT QUESTION
                ================================================= */}

                <button
                  className="next-question-button"
                  onClick={
                    moveToNextQuestion
                  }
                >

                  {currentQuestion <
                  questions.length - 1
                    ? "Next Question →"
                    : "Finish Interview 🏆"}

                </button>

              </div>

            )}

          </div>

        </div>

      )}

    </div>
  );
}

export default Interview;