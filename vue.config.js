const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  publicPath: "/",
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.40.188:8001/',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
      '/service': {
        target: 'http://192.168.40.188:3004/',
        changeOrigin: true,
        logLevel: 'debug'
        // pathRewrite: {
        //   '^/service/VehiclePass': '',
        // },
      },
    },
  },
})

