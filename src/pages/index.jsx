import React from 'react';
import Layout from '@theme/Layout';
import { motion } from 'framer-motion';
import Link from '@docusaurus/Link';
import Logo from '../components/Homepage/Logo';

const Section = ({ children, title, className }) => (
  <section className={`section ${className}`}>
    <div className="container">
      {title && <h2 className="section-title">{title}</h2>}
      {children}
    </div>
  </section>
);

const HomePage = () => {
  return (
    <Layout>
      <Header />
      <FeaturesSection />
      <CoreTopicsSection />
      <RealWorldApplicationsSection />
      <TestimonialsSection />
    </Layout>
  );
};

const Header = () => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="hero-section"
    >
      <div className="container">
        <Logo />
        <h1 className="hero-title">Physical AI & Advanced Robotics</h1>
        <p className="hero-tagline">An advanced textbook for the next generation of robotics engineers.</p>
        <div className="hero-buttons">
          <Link to="/chapter1" className="button button--primary">Start Learning</Link>
          <Link to="/intro" className="button button--secondary">Browse Glossary</Link>
        </div>
      </div>
    </motion.header>
  );
};

const FeaturesSection = () => {
  return (
    <Section title="What You'll Master" className="features-section">
      <div className="features-grid">
        {[
          { icon: '🤖', title: 'Robot', description: 'Build and control complex robotic systems.' },
          { icon: '💻', title: 'Code', description: 'Implement advanced algorithms in ROS 2.' },
          { icon: '⚙️', title: 'Gear', description: 'Master the mechanics of robotic hardware.' },
          { icon: '📖', title: 'Book', description: 'Learn from a comprehensive, up-to-date textbook.' },
        ].map((feature, i) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className="feature-card"
          >
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </Section>
  );
};

const CoreTopicsSection = () => {
  return (
    <Section title="Core Topics" className="core-topics-section">
      <div className="chips-grid">
        {[
          {topic: 'Forward & Inverse Kinematics', link: '/chapter4'},
          {topic: 'ROS 2 Architecture', link: '/chapter1'},
          {topic: 'SLAM and Navigation', link: '/'},
          {topic: 'Computer Vision', link: '/'},
          {topic: 'Sensor Fusion', link: '/module2-digital-twin/ch3-sensors'},
          {topic: 'Control Systems', link: '/'},
          {topic: 'Humanoid Control', link: '/'},
          {topic: 'Simulation & Digital Twins', link: '/category/module-2-digital-twin'},
        ].map((item, i) => (
          <Link to={item.link} key={item.topic}>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05, duration: 0.3 }}
              className="chip"
            >
              {item.topic}
            </motion.div>
          </Link>
        ))}
      </div>
    </Section>
  );
};

import HumanoidNavigation from '@site/src/img/homepage/humanoid-navigation.png';
import RoboticManipulation from '@site/src/img/homepage/robotic-manipulation.png';
import AIPerception from '@site/src/img/homepage/ai-perception.png';

const RealWorldApplicationsSection = () => {
  return (
    <Section title="Real-World Applications" className="applications-section">
      <div className="cards-grid">
        {[
          {
            title: 'Humanoid Navigation',
            description: 'Teach a humanoid robot to navigate complex environments.',
            image: HumanoidNavigation,
            link: '/'
          },
          {
            title: 'Robotic Manipulation',
            description: 'Develop precise and intelligent robotic manipulation systems.',
            image: RoboticManipulation,
            link: '/'
          },
          {
            title: 'AI Perception',
            description: 'Build advanced perception systems for autonomous agents.',
            image: AIPerception,
            link: '/chapter3'
          },
        ].map((app, i) => (
          <Link to={app.link} key={app.title} className="card-link">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="card"
            >
              <div className="card-image" style={{ backgroundImage: `url(${app.image})` }}></div>
              <div className="card-content">
                <h3>{app.title}</h3>
                <p>{app.description}</p>
              </div>
            </motion.div>
          </Link>
        ))}
      </div>
    </Section>
  );
};

const TestimonialsSection = () => {
  return (
    <Section title="What Our Readers Say" className="testimonials-section">
      <div className="testimonials-grid">
        {[
          {
            quote: 'This is the best robotics textbook I have ever read. Truly groundbreaking.',
            author: 'Dr. Evelyn Reed',
            role: 'Professor of AI, MIT',
            avatar: 'https://i.pravatar.cc/150?u=evelyn',
          },
          {
            quote: 'A must-have for any serious robotics student. The practical examples are invaluable.',
            author: 'Kenji Tanaka',
            role: 'Lead Robotics Engineer, Boston Dynamics',
            avatar: 'https://i.pravatar.cc/150?u=kenji',
          },
          {
            quote: 'Comprehensive, practical, and perfectly aligned with the future of the industry.',
            author: 'Fatima Al-Jamil',
            role: 'PhD Researcher, Stanford University',
            avatar: 'https://i.pravatar.cc/150?u=fatima',
          },
        ].map((testimonial, i) => (
          <motion.div
            key={testimonial.author}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className="testimonial-card"
          >
            <p className="quote">"{testimonial.quote}"</p>
            <div className="author">
              <img src={testimonial.avatar} alt={testimonial.author} />
              <div>
                <h4>{testimonial.author}</h4>
                <p>{testimonial.role}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </Section>
  );
};

export default HomePage;