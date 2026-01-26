// @ts-check
/** @type {import('@docusaurus/types').Config} */

const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'A comprehensive guide generated and evolved with AI assistance.',
  favicon: 'img/logo.png',

  url: 'https://ai-native-book.vercel.app', // Updated for Vercel deployment
  baseUrl: '/',
  organizationName: 'Mahnoor-Ghaffar', // Usually your GitHub org/user name.
  projectName: 'ai-native-book', // Usually your repo name.


  onBrokenLinks: 'warn',
  onBrokenAnchors: 'warn',
  onDuplicateRoutes: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'Urdu',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
        path: 'src/book-content',
        routeBasePath: '/',   // 🔥 important
        sidebarPath: './sidebars.ts',
        },

        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],



  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/logo.png',
      colorMode: {
        respectPrefersColorScheme: false, // Keep dark theme as default
        defaultMode: 'dark', // Set dark as default theme
        disableSwitch: true, // Disable theme switching
      },
      navbar: {
        title: 'AI/Spec-Driven Book',
        logo: {
          alt: 'Robot Logo',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/Mahnoor-Ghaffar/ai-native-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Book',
                to: '/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Mahnoor-Ghaffar/ai-native-book',
              },
            ],
          },
          {
            title: 'Book Author',
            items: [
              {
                label: 'Mahnoor Ghaffar',
                href: '#',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI Native Book. Built with Docusaurus. Author: Mahnoor Ghaffar`,
      },
      prism: {
        theme: {
          plain: {
            color: '#f8f8f2',
            backgroundColor: '#272822',
          },
          styles: [
            {
              types: ['changed'],
              style: {
                color: 'rgb(162, 191, 252)',
                fontStyle: 'italic',
              },
            },
            {
              types: ['deleted'],
              style: {
                color: '#f92672',
                fontStyle: 'italic',
              },
            },
            {
              types: ['inserted'],
              style: {
                color: 'rgb(173, 219, 103)',
                fontStyle: 'italic',
              },
            },
            {
              types: ['comment'],
              style: {
                color: '#8292a2',
                fontStyle: 'italic',
              },
            },
            {
              types: ['string', 'url'],
              style: {
                color: '#a6e22e',
              },
            },
            {
              types: ['variable'],
              style: {
                color: '#f8f8f2',
              },
            },
            {
              types: ['number'],
              style: {
                color: '#ae81ff',
              },
            },
            {
              types: ['builtin', 'char', 'constant', 'function', 'class-name'],
              style: {
                color: '#e6db74',
              },
            },
            {
              types: ['punctuation'],
              style: {
                color: '#f8f8f2',
              },
            },
            {
              types: ['selector', 'doctype'],
              style: {
                color: '#a6e22e',
                fontStyle: 'italic',
              },
            },
            {
              types: ['tag', 'operator', 'keyword'],
              style: {
                color: '#66d9ef',
              },
            },
            {
              types: ['boolean'],
              style: {
                color: '#ae81ff',
              },
            },
            {
              types: ['namespace'],
              style: {
                color: 'rgb(178, 204, 214)',
                opacity: 0.7,
              },
            },
            {
              types: ['tag', 'property'],
              style: {
                color: '#f92672',
              },
            },
            {
              types: ['attr-name'],
              style: {
                color: '#a6e22e !important',
              },
            },
            {
              types: ['doctype'],
              style: {
                color: '#8292a2',
              },
            },
            {
              types: ['rule'],
              style: {
                color: '#e6db74',
              },
            },
          ],
        },
        darkTheme: {
          plain: {
            color: '#F8F8F2',
            backgroundColor: '#282A36',
          },
          styles: [
            {
              types: ['prolog', 'constant', 'builtin'],
              style: {
                color: 'rgb(189, 147, 249)',
              },
            },
            {
              types: ['inserted', 'function'],
              style: {
                color: 'rgb(80, 250, 123)',
              },
            },
            {
              types: ['deleted'],
              style: {
                color: 'rgb(255, 85, 85)',
              },
            },
            {
              types: ['changed'],
              style: {
                color: 'rgb(255, 184, 108)',
              },
            },
            {
              types: ['punctuation', 'symbol'],
              style: {
                color: 'rgb(248, 248, 242)',
              },
            },
            {
              types: ['string', 'char', 'tag', 'selector'],
              style: {
                color: 'rgb(255, 121, 198)',
              },
            },
            {
              types: ['keyword', 'variable'],
              style: {
                color: 'rgb(189, 147, 249)',
                fontStyle: 'italic',
              },
            },
            {
              types: ['comment'],
              style: {
                color: 'rgb(98, 114, 164)',
              },
            },
            {
              types: ['attr-name'],
              style: {
                color: 'rgb(241, 250, 140)',
              },
            },
          ],
        },
        additionalLanguages: [],
        magicComments: [
          {
            className: 'theme-code-block-highlighted-line',
            line: 'highlight-next-line',
            block: {
              start: 'highlight-start',
              end: 'highlight-end',
            },
          },
        ],
      },
      docs: {
        versionPersistence: 'localStorage',
        sidebar: {
          hideable: false,
          autoCollapseCategories: false,
        },
      },

      metadata: [],
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
    }),

    plugins: [
      './src/plugins/floating-chat-plugin'
    ],

    themes: [],
    scripts: [],
    headTags: [],
    stylesheets: [],
    clientModules: [],

  };

module.exports = config;
