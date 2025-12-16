import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ai-native-book/docs',
    component: ComponentCreator('/ai-native-book/docs', 'a84'),
    routes: [
      {
        path: '/ai-native-book/docs',
        component: ComponentCreator('/ai-native-book/docs', '804'),
        routes: [
          {
            path: '/ai-native-book/docs',
            component: ComponentCreator('/ai-native-book/docs', 'e33'),
            routes: [
              {
                path: '/ai-native-book/docs/category/chapter-1-getting-started',
                component: ComponentCreator('/ai-native-book/docs/category/chapter-1-getting-started', '1dc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/category/chapter-2-core-concepts',
                component: ComponentCreator('/ai-native-book/docs/category/chapter-2-core-concepts', '127'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/category/chapter-3-advanced-topics',
                component: ComponentCreator('/ai-native-book/docs/category/chapter-3-advanced-topics', 'dc0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/category/chapter-4-the-ai-native-mindset',
                component: ComponentCreator('/ai-native-book/docs/category/chapter-4-the-ai-native-mindset', 'b4e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/category/module-2-digital-twin',
                component: ComponentCreator('/ai-native-book/docs/category/module-2-digital-twin', '162'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/chapter1/',
                component: ComponentCreator('/ai-native-book/docs/chapter1/', 'e5b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/chapter2/',
                component: ComponentCreator('/ai-native-book/docs/chapter2/', '8cb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/chapter3/',
                component: ComponentCreator('/ai-native-book/docs/chapter3/', 'c1a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/chapter4/',
                component: ComponentCreator('/ai-native-book/docs/chapter4/', '075'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/intro',
                component: ComponentCreator('/ai-native-book/docs/intro', 'e31'),
                exact: true
              },
              {
                path: '/ai-native-book/docs/module2-digital-twin/ch1-physics',
                component: ComponentCreator('/ai-native-book/docs/module2-digital-twin/ch1-physics', '57a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2-digital-twin/ch2-rendering',
                component: ComponentCreator('/ai-native-book/docs/module2-digital-twin/ch2-rendering', 'd6b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ai-native-book/docs/module2-digital-twin/ch3-sensors',
                component: ComponentCreator('/ai-native-book/docs/module2-digital-twin/ch3-sensors', 'cd9'),
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
    path: '/ai-native-book/',
    component: ComponentCreator('/ai-native-book/', 'af3'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
