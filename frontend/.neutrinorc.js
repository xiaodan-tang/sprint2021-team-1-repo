const react = require('@neutrinojs/react');

module.exports = {
  options: {
    root: __dirname,
    output: '../static/build'
  },
  use: [
    react({
      html: {
        title: 'frontend'
      },
      style: {
        extract: {
          enabled: true,
          loader: {
            esModule: true,
          },
          plugin: {
            filename: '[name].css',
          },
        }
      },
    }),
    neutrino => {
      neutrino.config.output.filename('[name].js');
      neutrino.config.optimization.splitChunks(false);
    },
  ],
};
