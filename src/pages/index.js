import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HeroBanner from '@site/src/components/HeroBanner';

function HomepageFeatures() {
  const features = [
    {
      title: '🎯 Evidence-Based Learning',
      description: (
        <>
          Every technical claim backed by authoritative citations from foundational
          textbooks and seminal research papers. Learn with confidence from verified sources.
        </>
      ),
    },
    {
      title: '🤖 Hands-On Simulations',
      description: (
        <>
          Practice with free, open-source simulators (PyBullet, Webots, MuJoCo).
          All exercises include step-by-step guidance and expected outputs.
        </>
      ),
    },
    {
      title: '🚀 Future-Ready Skills',
      description: (
        <>
          Master Physical AI systems that combine digital intelligence with physical
          embodiment. Prepare for the AI-augmented workforce with ethical, collaborative robotics.
        </>
      ),
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div key={idx} className={clsx('col col--4')}>
              <div className={styles.featureCard}>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function LearningPath() {
  const parts = [
    {
      title: 'Part I: Fundamentals',
      chapters: ['Introduction to Physical AI', 'Robot Fundamentals'],
      icon: '📚',
    },
    {
      title: 'Part II: Core Robotics',
      chapters: ['Humanoid Kinematics', 'Dynamics & Control'],
      icon: '⚙️',
    },
  ];

  return (
    <section className={styles.learningPath}>
      <div className="container">
        <h2 className={styles.sectionTitle}>📖 Learning Path</h2>
        <p className={styles.sectionSubtitle}>
          A structured curriculum from fundamentals to advanced robotics
        </p>
        <div className={styles.pathGrid}>
          {parts.map((part, idx) => (
            <div key={idx} className={styles.pathCard}>
              <div className={styles.pathIcon}>{part.icon}</div>
              <h3>{part.title}</h3>
              <ul className={styles.chapterList}>
                {part.chapters.map((chapter, chIdx) => (
                  <li key={chIdx}>{chapter}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CallToAction() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <h2>Ready to Build the Future?</h2>
        <p>Start your journey into Physical AI and Humanoid Robotics today</p>
        <div className={styles.ctaButtons}>
          <Link
            className={styles.ctaPrimary}
            to="/docs/ch01-introduction">
            Begin Chapter 1
          </Link>
          <Link
            className={styles.ctaSecondary}
            to="/docs/glossary">
            Browse Glossary
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive university-level textbook on embodied intelligence and humanoid robotics">
      <HeroBanner />
      <main>
        <HomepageFeatures />
        <LearningPath />
        <CallToAction />
      </main>
    </Layout>
  );
}
