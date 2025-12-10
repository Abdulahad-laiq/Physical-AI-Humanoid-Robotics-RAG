// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A University-Level Textbook on Embodied Intelligence and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://Abdulahad-laiq.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/', // Changed to '/' for local development

  // GitHub pages deployment config
  organizationName: 'Abdulahad-laiq', // Usually your GitHub org/user name.
  projectName: 'Physical-AI-Humanoid-Robotics', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'warn',  // Changed to 'warn' for initial build - will fix links in Phase 3
  onBrokenMarkdownLinks: 'warn',

  // Internationalization (i18n)
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
          sidebarPath: require.resolve('./sidebars.js'),
          // Edit URL for GitHub
          editUrl: 'https://github.com/Abdulahad-laiq/Physical-AI-Humanoid-Robotics/tree/main/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false, // Disable blog for textbook
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],


  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card for sharing
      image: 'img/physical-ai-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        items: [
          {
            type: 'dropdown',
            label: 'Chapters',
            position: 'left',
            items: [
              {
                to: '/docs/ch01-introduction',
                label: 'Ch 1: Introduction to Physical AI',
              },
              {
                to: '/docs/ch02-robot-fundamentals',
                label: 'Ch 2: Robot Fundamentals',
              },
              {
                to: '/docs/ch03-kinematics',
                label: 'Ch 3: Humanoid Kinematics',
              },
              {
                to: '/docs/ch04-dynamics',
                label: 'Ch 4: Dynamics & Control',
              },
            ],
          },
          {
            to: '/docs/glossary',
            label: 'Glossary',
            position: 'left',
          },
          {
            to: '/docs/bibliography',
            label: 'Bibliography',
            position: 'left',
          },
          {
            href: 'https://github.com/Abdulahad-laiq/Physical-AI-Humanoid-Robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Glossary',
                to: '/docs/glossary',
              },
              {
                label: 'Bibliography',
                to: '/docs/bibliography',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Glossary',
                to: '/docs/glossary',
              },
              {
                label: 'Bibliography',
                to: '/docs/bibliography',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Abdulahad-laiq/Physical-AI-Humanoid-Robotics',
              },
              {
                label: 'License (CC BY-NC-SA 4.0)',
                href: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} PIAIC Quarter 4. Built with Docusaurus. Licensed under CC BY-NC-SA 4.0.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['python', 'bash', 'yaml', 'json'],
      },
      // Algolia search (optional - configure later if needed)
      // algolia: {
      //   appId: 'YOUR_APP_ID',
      //   apiKey: 'YOUR_SEARCH_API_KEY',
      //   indexName: 'physical-ai-textbook',
      // },
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
    }),
};

module.exports = config;
