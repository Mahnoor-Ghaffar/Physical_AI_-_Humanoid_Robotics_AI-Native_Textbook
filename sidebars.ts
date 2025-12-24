import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Chapter 1: Getting Started',
      link: {
        type: 'generated-index',
        title: 'Chapter 1: Getting Started',
        slug: '/category/chapter-1-getting-started',
        description: 'An introduction to the book.',
      },
      items: ['chapter1/index'],
    },
    {
      type: 'category',
      label: 'Chapter 2: Core Concepts',
      link: {
        type: 'generated-index',
        title: 'Chapter 2: Core Concepts',
        slug: '/category/chapter-2-core-concepts',
        description: 'Explore the core concepts.',
      },
      items: ['chapter2/index'],
    },
    {
      type: 'category',
      label: 'Chapter 3: Advanced Topics',
      link: {
        type: 'generated-index',
        title: 'Chapter 3: Advanced Topics',
        slug: '/category/chapter-3-advanced-topics',
        description: 'Delve into advanced topics.',
      },
      items: ['chapter3/index'],
    },
    {
      type: 'category',
      label: 'Chapter 4: The AI-Native Mindset',
      link: {
        type: 'generated-index',
        title: 'Chapter 4: The AI-Native Mindset',
        slug: '/category/chapter-4-the-ai-native-mindset',
        description: 'Understand the AI-native mindset.',
      },
      items: ['chapter4/index'],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin',
      link: {
        type: 'generated-index',
        title: 'Module 2: Digital Twin',
        slug: '/category/module-2-digital-twin',
        description: 'Learn about digital twins, focusing on physics, rendering, and sensors.',
      },
      items: [
        'module2-digital-twin/ch1-physics',
        'module2-digital-twin/ch2-rendering',
        'module2-digital-twin/ch3-sensors',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      link: {
        type: 'generated-index',
        title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
        slug: '/category/module-3-ai-robot-brain',
        description: 'Explore NVIDIA Isaac ecosystem for advanced robotics simulation, perception, and navigation.',
      },
      items: [
        'module3-nvidia-isaac/ch1-sim',
        'module3-nvidia-isaac/ch2-perception',
        'module3-nvidia-isaac/ch3-nav2',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      link: {
        type: 'generated-index',
        title: 'Module 4: Vision-Language-Action (VLA)',
        slug: '/category/module-4-vla',
        description: 'Explore Vision-Language-Action integration for autonomous humanoid robots using OpenAI Whisper, LLMs, and VLA models.',
      },
      items: [
        'module4-vla/ch1-voice',
        'module4-vla/ch2-planning',
        'module4-vla/ch3-integration',
      ],
    },
  ],
};

export default sidebars;
