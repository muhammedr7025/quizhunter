// components/QuestionStatistics.js
import styles from '../styles/QuestionStatistics.module.css';

const QuestionStatistics = ({ statistics }) => (
  <div className={styles.statisticsContainer}>
    {statistics.map((question) => (
      <div key={question.question_id} className={styles.question}>
        <h3>{question.question_text}</h3>
        {question.options.map((option) => (
          <div key={option.option_id} className={styles.option}>
            <span>{option.option_text}</span>
            <span>{option.click_count} clicks</span>
          </div>
        ))}
      </div>
    ))}
  </div>
);

export default QuestionStatistics;
