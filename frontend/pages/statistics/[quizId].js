// pages/statistics/[quizId].js
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getQuizStatistics } from '../../api';
import QuestionStatistics from '../../components/QuestionStatistics';

export default function QuizStatistics() {
  const router = useRouter();
  const { quizId } = router.query;
  const [statistics, setStatistics] = useState([]);

  useEffect(() => {
    if (quizId) {
      getQuizStatistics(quizId).then((response) => {
        setStatistics(response.data);
      });
    }
  }, [quizId]);

  return (
    <div>
      <h1>Quiz Statistics</h1>
      <QuestionStatistics statistics={statistics} />
    </div>
  );
}
