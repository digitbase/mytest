const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  publicPath: "/",
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
      '/service': {
        target: 'http://127.0.0.1:3004/',
        changeOrigin: true,
        logLevel: 'debug'
        // pathRewrite: {
        //   '^/service/VehiclePass': '',
        // },
      },
    },
  },
})

