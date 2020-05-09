const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports={

	mode:'production',
	entry: {
		index: [
			path.resolve(__dirname,'./src/js/index.js'),
			path.resolve(__dirname,'./src/js/main.js')
		]
		
	},
	output:{
		path: path.resolve(__dirname+'/dist/js'),
		filename: '[name].js'
	},
	module:{
		rules:[
			{
				test: /\.js$/,
				loader:'babel-loader',
				exclude: path.resolve(__dirname, 'node_modules')
			},
			{
				test: /\.css$/,
				use:[
					'style-loader',
					'css-loader'
				]
			},
			{
				test: /\.scss$/,
				use:[
					'style-loader',
					'css-loader',
					'sass-loader'
				]
			},
			{
				test: /\.tpl$/,
				use:[
					'ejs-loader'
				]
			}
		]
	},
	plugins : [
		new HtmlWebpackPlugin({
			filemane: 'index.html',
			template: path.resolve(__dirname,'./src/index.html'),
			chunks:[
				'index'
			],
			excludeChunks:['node_modules']
		})
	],
	devServer:{
		open: true,
		host: 'localhost',
		port: 8080
	}
}