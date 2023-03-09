import babel from '@rollup/plugin-babel'
import postcss from 'rollup-plugin-postcss'
import nodeResolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import replace from '@rollup/plugin-replace'

export default {
  input: './main/static/src/main.js',
  output: {
    name: 'bundle',
    file: './main/static/dist/bundle.js',
    format: 'iife',
  },
  plugins: [
    nodeResolve({ browser: true }),
    commonjs(),
    replace({
      preventAssignment: true,
      values: {
        'process.env.npm_package_version': JSON.stringify('development'),
      },
    }),
    postcss({
      extract: true,
      minify: true,
      config: {
        path: 'postcss.config.js',
      },
      use: {
        sass: { javascriptEnabled: true },
      },
    }),
    babel({ babelHelpers: 'bundled' }),
  ],
  watch: {
    include: [
      'rollup.config.js',
      'postcss.config.js',
      'main/static/src/**/*.js',
      'main/static/**',
      'main/templates/**',
    ],
  },
}
