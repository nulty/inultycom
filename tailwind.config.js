module.exports = {
  content: [
    './blog/templates/**/*.html',
    './main/templates/**/*.html',
  ],
  watch: ['./main/static/css/**/*.scss'],
  darkMode: 'media', // or 'class'
  theme: {
    extend: {
      colors: {
        primary: '#3ca4c8',
        secondary: '#eaebf0',
        tertiary: '#212830',
      },
      backgroundImage: (theme) => ({
        'hero-pattern': 'url(/static/src/images/hero.jpg)',
      }),
    },
    fontFamily: {
      hero: ['Poppins'],
      content: ['Prompt'],
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
