/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main textbook sidebar with 5 categories
  textbookSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    // Fundamentals - Chapters 1-2
    {
      type: 'category',
      label: 'I. Fundamentals',
      collapsed: false,
      items: [
        'ch01-introduction/ch01-introduction',
        'ch02-robot-fundamentals/ch02-robot-fundamentals',
      ],
    },
    // Core Robotics - Chapters 3-4
    {
      type: 'category',
      label: 'II. Core Robotics',
      collapsed: false,
      items: [
        'ch03-kinematics/ch03-kinematics',
        'ch04-dynamics/ch04-dynamics',
      ],
    },
    // {
    //   type: 'category',
    //   label: 'III. Advanced Topics',
    //   collapsed: false,
    //   items: [
    //     'ch04-dynamics/index',
    //     'ch05-perception/index',
    //     'ch06-planning/index',
    //     'ch07-manipulation/index',
    //   ],
    // },
    // {
    //   type: 'category',
    //   label: 'III. Advanced Topics',
    //   collapsed: false,
    //   items: [
    //     'ch08-locomotion/index',
    //     'ch09-learning/index',
    //     'ch10-collaboration/index',
    //   ],
    // },
    {
      type: 'category',
      label: 'Reference',
      collapsed: true,
      items: [
        'glossary',
        'bibliography',
      ],
    },
    // {
    //   type: 'category',
    //   label: 'Appendices',
    //   collapsed: true,
    //   items: [
    //     'appendices/setup-guide',
    //     'appendices/webots-setup',
    //     'appendices/pybullet-setup',
    //     'appendices/mujoco-setup',
    //     'appendices/math-review',
    //     'appendices/troubleshooting',
    //   ],
    // },
  ],
};

module.exports = sidebars;
