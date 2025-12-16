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
    path: '/docs',
    component: ComponentCreator('/docs', '5c9'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'd03'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '432'),
            routes: [
              {
                path: '/docs/category/chapter-1-getting-started',
                component: ComponentCreator('/docs/category/chapter-1-getting-started', '635'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/chapter-2-core-concepts',
                component: ComponentCreator('/docs/category/chapter-2-core-concepts', '1cf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/chapter-3-advanced-topics',
                component: ComponentCreator('/docs/category/chapter-3-advanced-topics', '047'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/chapter-4-the-ai-native-mindset',
                component: ComponentCreator('/docs/category/chapter-4-the-ai-native-mindset', 'dce'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/module-2-digital-twin',
                component: ComponentCreator('/docs/category/module-2-digital-twin', '0e9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter1/',
                component: ComponentCreator('/docs/chapter1/', '3be'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter2/',
                component: ComponentCreator('/docs/chapter2/', '413'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter3/',
                component: ComponentCreator('/docs/chapter3/', 'c09'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter4/',
                component: ComponentCreator('/docs/chapter4/', 'aef'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'a4b'),
                exact: true
              },
              {
                path: '/docs/module2-digital-twin/ch1-physics',
                component: ComponentCreator('/docs/module2-digital-twin/ch1-physics', '7b9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2-digital-twin/ch2-rendering',
                component: ComponentCreator('/docs/module2-digital-twin/ch2-rendering', 'b7a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2-digital-twin/ch3-sensors',
                component: ComponentCreator('/docs/module2-digital-twin/ch3-sensors', '681'),
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
    path: '/',
    component: ComponentCreator('/', '070'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
