const path = require('path');
const webpack = require('webpack');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const extractCSS = new ExtractTextPlugin('stylesheets/[name]-one.css');
const extractSCSS = new ExtractTextPlugin('stylesheets/[name]-two.css');
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const AddAssetHtmlCdnWebpackPlugin = require('add-asset-html-cdn-webpack-plugin');

module.exports={

	mode: 'development',
	entry: {
		index: [
			path.resolve(__dirname,'./src/js/index.js'),
		]
		
	},
	output:{
		// path: path.resolve(__dirname + '/dist/'),
		// filename: 'bundle.js',
		//publicPath: "/dist/"
	},
	module:{
		rules:[
			{
				test: /\.js$/,
				loader:'babel-loader',
				exclude: path.resolve(__dirname, 'node_modules'),
			},
			{
			  test: /\.css$/,
			  use: extractCSS.extract({
			  	fallback: 'style-loader', 
			  	use: [ 'css-loader' ]
			  })
			},
			{
			  test: /\.scss$/i,
			  use: extractSCSS.extract({
			  		fallback: 'style-loader', 
			  		use: [ 'css-loader', 'sass-loader' ]
			  	})
			},
			{
				test: /\.tpl$/,
				use:[
					'ejs-loader'
				]
			},
			{
			    test: /\.(htm|html)$/i,
			     use:[ 'html-loader'],
				  
			},
			{
				test: /\.(jpg|png)$/,
				use:[
					{
						loader: 'file-loader',
						options:{
							name: '[name].[ext]',
							outputPath: 'img/',
							publicPath: 'img/'
						}
					}
				]
			},

		]
	},
	plugins : [

		new webpack.ProvidePlugin({
           $: 'jquery',
           jQuery: 'jquery'
        }),
		extractCSS,
	  	extractSCSS,
	  	// new CleanWebpackPlugin({
	  	//     cleanAfterEveryBuildPatterns: ['build']
	  	// }),
		new HtmlWebpackPlugin({
			filemane: 'index.html',
			template: './src/index.html',
		}),


	],
	devServer:{
		open: true,
		host: 'localhost',
		port: 8080
	}
}