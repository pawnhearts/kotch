const VueLoaderPlugin = require('vue-loader/lib/plugin');
var path = require("path");


module.exports = {
  entry: './src/main.js',
  module: {
    rules: [
      { test: /\.js$/, use: 'babel-loader' },
      { test: /\.vue$/, use: 'vue-loader' },
      //{ test: /\.css$/, use: ['vue-style-loader', 'css-loader']},
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
  ],
  output: {
    path: path.resolve(__dirname, "static/js"),
    publicPath: "/assets/",
    filename: "bundle.js"
  }
};
