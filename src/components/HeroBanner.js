import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './HeroBanner.module.css';

export default function HeroBanner() {
  const {siteConfig} = useDocusaurusContext();

  const chapters = [
    { id: 1, title: 'Introduction to Physical AI', link: '/docs/ch01-introduction' },
    { id: 2, title: 'Robot Fundamentals', link: '/docs/ch02-robot-fundamentals' },
    { id: 3, title: 'Humanoid Kinematics', link: '/docs/ch03-kinematics' },
    { id: 4, title: 'Dynamics & Control', link: '/docs/ch04-dynamics' },
  ];

  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
          <p className={styles.heroTagline}>{siteConfig.tagline}</p>

          <div className={styles.heroButtons}>
            <Link
              className={styles.primaryButton}
              to="/docs/ch01-introduction">
              🚀 Start Reading
            </Link>
            <Link
              className={styles.secondaryButton}
              to="/docs/intro">
              📖 Overview
            </Link>
          </div>

          <div className={styles.chaptersSection}>
            <h3 className={styles.chaptersTitle}>📚 Quick Chapter Access</h3>
            <div className={styles.chapterGrid}>
              {chapters.map((chapter) => (
                <Link
                  key={chapter.id}
                  to={chapter.link}
                  className={styles.chapterCard}>
                  <span className={styles.chapterNumber}>Ch {chapter.id}</span>
                  <span className={styles.chapterTitle}>{chapter.title}</span>
                </Link>
              ))}
            </div>
          </div>

          <div className={styles.features}>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🎯</span>
              <span className={styles.featureText}>University-Level Content</span>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>🤖</span>
              <span className={styles.featureText}>Hands-on Simulations</span>
            </div>
            <div className={styles.feature}>
              <span className={styles.featureIcon}>📊</span>
              <span className={styles.featureText}>Evidence-Based Learning</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
