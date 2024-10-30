// components/QuizList.js
import Link from 'next/link';

const QuizList = ({ quizzes }) => (
  <div>
    {quizzes.map((quiz) => (
      <div key={quiz.id}>
        <h2>{quiz.title}</h2>
        <Link href={`/submit-quiz?quizId=${quiz.id}`}>Take Quiz</Link>
      </div>
    ))}
  </div>
);

export default QuizList;
