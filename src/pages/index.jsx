import React from 'react';
import Layout from '@theme/Layout';
import { motion } from 'framer-motion';
import Link from '@docusaurus/Link';
import Logo from '../components/Homepage/Logo';
import HeroSection from '../components/HeroSection';
import StatusSection from '../components/StatusSection';
import BackgroundOverlays from '../components/BackgroundOverlays';
import HumanoidNavigation from '@site/static/img/homepage/cards/humanoid-robot-navigation.png';
import RoboticManipulation from '@site/static/img/homepage/cards/robotic-arm-manipulation.png';
import AIPerception from '@site/static/img/homepage/cards/AI-computer-vision-perception.png';


const Section = ({ children, title, className }) => (
  <section className={`section ${className}`}>
    <div className="section-wrapper">
      <BackgroundOverlays className={className.replace('section-', '')} />
      <div className="container">
        {title && <h2 className="section-title">{title}</h2>}
        {children}
      </div>
    </div>
  </section>
);

const HomePage = () => {
  return (
    <Layout>
      <HeroSection />
      <StatusSection />
      <FeaturesSection />
      <CoreTopicsSection />
      <AdvancedTopicsSection />
      <RealWorldApplicationsSection />
      <TestimonialsSection />
    </Layout>
  );
};

// Define missing components that are used in HomePage



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
          {topic: 'SLAM and Navigation', link: '/module3-nvidia-isaac/ch3-nav2'},
          {topic: 'Computer Vision', link: '/module3-nvidia-isaac/ch2-perception'},
          {topic: 'Sensor Fusion', link: '/module2-digital-twin/ch3-sensors'},
          {topic: 'Control Systems', link: '/chapter3'},
          {topic: 'Humanoid Control', link: '/module4-vla/ch1-voice'},
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

const AdvancedTopicsSection = () => {
  return (
    <Section title="Advanced Topics" className="advanced-topics-section">
      <div className="cards-grid">
        {[
          {
            title: 'Reinforcement Learning',
            description: 'Train robots using advanced RL algorithms for complex tasks.',
            icon: '🧠',
            link: '/module4-vla/ch1-voice'
          },
          {
            title: 'AI Planning & Reasoning',
            description: 'Implement intelligent decision-making for autonomous systems.',
            icon: '🧩',
            link: '/module4-vla/ch2-planning'
          },
          {
            title: 'Multi-Robot Systems',
            description: 'Coordinate multiple robots for collaborative tasks.',
            icon: '🤖',
            link: '/chapter3'
          },
          {
            title: 'Human-Robot Interaction',
            description: 'Design intuitive interfaces for human-robot collaboration.',
            icon: '🤝',
            link: '/module4-vla/ch1-voice'
          },
        ].map((topic, i) => (
          <Link to={topic.link} key={topic.title} className="card-link">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="card"
            >
              <div className="card-icon" style={{ fontSize: '3rem', textAlign: 'center', padding: '1.5rem', color: 'var(--primary-accent)' }}>
                {topic.icon}
              </div>
              <div className="card-content">
                <h3>{topic.title}</h3>
                <p>{topic.description}</p>
              </div>
            </motion.div>
          </Link>
        ))}
      </div>
    </Section>
  );
};


const RealWorldApplicationsSection = () => {
  return (
    <Section title="Real-World Applications" className="applications-section">
      <div className="cards-grid">
        {[
          {
            title: 'Humanoid Navigation',
            description: 'Teach a humanoid robot to navigate complex environments.',
            image: HumanoidNavigation,
            link: '/module3-nvidia-isaac/ch3-nav2'
          },
          {
            title: 'Robotic Manipulation',
            description: 'Develop precise and intelligent robotic manipulation systems.',
            image: RoboticManipulation,
            link: '/chapter4'
          },
          {
            title: 'AI Perception',
            description: 'Build advanced perception systems for autonomous agents.',
            image: AIPerception,
            link: '/module3-nvidia-isaac/ch2-perception'
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