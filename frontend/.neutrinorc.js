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
      neutrino.config.entry('index')
                      .add('./src/index.jsx')
                      .add('./src/Sidebar.jsx')

      neutrino.config.optimization.splitChunks(false);
    },
  ],
};