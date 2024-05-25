const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        'VUE_PROD_HYDRATION_MISMATCH_DETAILS': JSON.stringify(false)
      })
    ]
  },
  transpileDependencies: true
})