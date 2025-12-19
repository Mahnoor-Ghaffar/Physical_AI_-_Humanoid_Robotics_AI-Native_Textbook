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
    component: ComponentCreator('/', '47d'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', 'eee'),
        routes: [
          {
            path: '/',
            component: ComponentCreator('/', '0d9'),
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
