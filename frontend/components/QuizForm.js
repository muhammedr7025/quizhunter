// components/QuizForm.js
import { useState } from 'react';
import styles from '../styles/QuizForm.module.css';
import { createQuiz } from '../api';

const QuizForm = () => {
  const [title, setTitle] = useState('');
  const [passMark, setPassMark] = useState(0);
  const [questionCount, setQuestionCount] = useState(0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createQuiz({ title, pass_mark: passMark, question_count: questionCount });
    setTitle('');
    setPassMark(0);
    setQuestionCount(0);
  };

  return (
    <div className={styles.form}>
      <h2>Create a New Quiz</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Quiz Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="number"
          placeholder="Pass Mark"
          value={passMark}
          onChange={(e) => setPassMark(e.target.value)}
        />
        <input
          type="number"
          placeholder="Question Count"
          value={questionCount}
          onChange={(e) => setQuestionCount(e.target.value)}
        />
        <button type="submit" className={styles.submitButton}>Create Quiz</button>
      </form>
    </div>
  );
};

export default QuizForm;
