// @ts-check
// @type {import('@docusaurus/types').Config}

const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'A comprehensive guide generated and evolved with AI assistance.',
  favicon: 'img/favicon.ico',

  url: 'https://Mahnoor-Ghaffar.github.io',
  baseUrl: '/',
  organizationName: 'Mahnoor-Ghaffar', // Usually your GitHub org/user name.
  projectName: 'ai-native-book', // Usually your repo name.


  onBrokenLinks: 'throw',
  onBrokenAnchors: 'warn',
  onDuplicateRoutes: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
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
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
        defaultMode: 'light',
        disableSwitch: false,
      },
      navbar: {
        title: 'AI/Spec-Driven Book',
        logo: {
          alt: 'Robot Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
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
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
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
};

module.exports = config;
