module.exports = function (grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		browserify: {
			dev: {
				files: {
					'app.js': ['src/**.js', 'src/**/*.jsx']
				},
				options: {
					transform: [
						['babelify', {presets: ['es2015', 'react']}]
					]
				},
			}
		},
    uglify: {
			'app.min.js': 'app.js'
    },
		watch: {
			src: {
				files: ['src/**/*.js', 'src/**/*.jsx'],
				tasks: ['browserify:dev'],
				options: {
					livereload: true
				}
			}
		}
	});

	grunt.loadNpmTasks('grunt-browserify');
  grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-watch');

	grunt.registerTask('start:dev', ['browserify', 'watch']);

	grunt.registerTask('default', ['browserify', 'uglify']);
};
