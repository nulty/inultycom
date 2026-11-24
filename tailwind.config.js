module.exports = {
  content: [
    './blog/templates/**/*.html',
    './main/templates/**/*.html',
    './main/content.py', // toolbox tile classes
  ],
  darkMode: 'media', // or 'class'
  theme: {
    extend: {
      colors: {
        accent: { DEFAULT: '#3ca4c8', light: '#5eb8d6' },
        ink: {
          DEFAULT: '#212830', // page
          darkest: '#13181d', // text on accent buttons
          deep: '#1a2027', // header, hero, footer
          card: '#29313b',
          line: '#36404c', // card borders
          rule: '#2c3540', // header and footer borders
        },
        fog: {
          100: '#e2e8f0', // default text
          200: '#d3dce6', // hero paragraph
          300: '#c5d0dc', // card text
          400: '#a3b1c2', // muted
        },
        mint: { DEFAULT: '#7cc49a', light: '#bfe6cf' },
        clay: '#d97757',
      },
      maxWidth: { page: '1088px' },
    },
    fontFamily: {
      hero: ['Poppins', 'sans-serif'],
      content: ['Prompt', 'system-ui', 'sans-serif'],
      mono: ['ui-monospace', 'monospace'],
    },
  },
  plugins: [],
}
