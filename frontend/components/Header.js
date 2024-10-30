// components/Header.js
import Link from 'next/link';
import styles from '../styles/Header.module.css';
import { useRouter } from 'next/router';
import { logoutUser } from '../api';

const Header = () => {
  const router = useRouter();

  const handleLogout = async () => {
    await logoutUser();
    router.push('/login');
  };

  return (
    <header className={styles.header}>
      <h1 className={styles.logo}>Quiz App</h1>
      <nav className={styles.navLinks}>  {/* Use navLinks here */}
        <Link href="/" className={styles.navLink}>Home</Link>
        <Link href="/create-quiz" className={styles.navLink}>Create Quiz</Link>
        <Link href="/statistics" className={styles.navLink}>Statistics</Link>
        <button onClick={handleLogout} className={styles.navLink}>Logout</button>
      </nav>
    </header>
  );
};

export default Header;
