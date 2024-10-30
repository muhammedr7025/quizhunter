// pages/index.js
import Header from '../components/Header';

export default function Home() {
  return (
    <div className="container">
      <Header />
      <h1>Welcome to the Quiz App</h1>
      <p>Register or log in to get started.</p>
    </div>
  );
}
