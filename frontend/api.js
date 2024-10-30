// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Django backend URL
  withCredentials: true,
});

export const registerUser = (username, password) =>
  api.post('/register/', { username, password });

export const loginUser = (username, password) =>
  api.post('/login/', { username, password });

export const logoutUser = () => api.post('/logout/');

export const createQuiz = (quizData) => api.post('/quiz/create/', quizData);

export const submitQuiz = (quizId, submissionData) =>
  api.post(`/quiz/${quizId}/submit/`, submissionData);

export const getQuizStatistics = (quizId) =>
  api.get(`/quiz/${quizId}/statistics/`);
