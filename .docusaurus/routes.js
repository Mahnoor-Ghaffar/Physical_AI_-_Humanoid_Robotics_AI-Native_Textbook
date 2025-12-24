import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '070'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '24c'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', 'd24'),
        routes: [
          {
            path: '/',
            component: ComponentCreator('/', 'bcb'),
            routes: [
              {
                path: '/category/chapter-1-getting-started',
                component: ComponentCreator('/category/chapter-1-getting-started', '665'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/chapter-2-core-concepts',
                component: ComponentCreator('/category/chapter-2-core-concepts', '533'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/chapter-3-advanced-topics',
                component: ComponentCreator('/category/chapter-3-advanced-topics', '5f2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/chapter-4-the-ai-native-mindset',
                component: ComponentCreator('/category/chapter-4-the-ai-native-mindset', '606'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/module-2-digital-twin',
                component: ComponentCreator('/category/module-2-digital-twin', '398'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/module-3-ai-robot-brain',
                component: ComponentCreator('/category/module-3-ai-robot-brain', '4d3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/category/module-4-vla',
                component: ComponentCreator('/category/module-4-vla', '103'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/chapter1/',
                component: ComponentCreator('/chapter1/', '382'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/chapter2/',
                component: ComponentCreator('/chapter2/', '74e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/chapter3/',
                component: ComponentCreator('/chapter3/', 'c06'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/chapter4/',
                component: ComponentCreator('/chapter4/', '94d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/intro',
                component: ComponentCreator('/intro', 'c96'),
                exact: true
              },
              {
                path: '/module2-digital-twin/ch1-physics',
                component: ComponentCreator('/module2-digital-twin/ch1-physics', '739'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module2-digital-twin/ch2-rendering',
                component: ComponentCreator('/module2-digital-twin/ch2-rendering', '4f8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module2-digital-twin/ch3-sensors',
                component: ComponentCreator('/module2-digital-twin/ch3-sensors', '402'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module3-nvidia-isaac/ch1-sim',
                component: ComponentCreator('/module3-nvidia-isaac/ch1-sim', '5ea'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module3-nvidia-isaac/ch2-perception',
                component: ComponentCreator('/module3-nvidia-isaac/ch2-perception', '4d3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module3-nvidia-isaac/ch3-nav2',
                component: ComponentCreator('/module3-nvidia-isaac/ch3-nav2', '7f5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module4-vla/ch1-voice',
                component: ComponentCreator('/module4-vla/ch1-voice', 'a7c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module4-vla/ch2-planning',
                component: ComponentCreator('/module4-vla/ch2-planning', 'cc7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/module4-vla/ch3-integration',
                component: ComponentCreator('/module4-vla/ch3-integration', 'e46'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
