const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
	context: __dirname,
	entry: {
		app: "./assets/scripts/index.js",
		uploadimage: "./assets/scripts/uploadimage.js",
	},
	output: {
		filename: "[name].bundle.js",
		path: path.resolve(__dirname, "core", "static"),
	},
	module: {
		rules: [
			{
				test: /\.css$/i,
				use: ["style-loader", "css-loader"],
			},
		],
	},
	optimization: {
		minimize: true,
		minimizer: [new TerserPlugin({})],
	},
};
