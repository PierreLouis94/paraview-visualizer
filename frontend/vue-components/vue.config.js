module.exports = {
  outputDir: 'dist',  // Ensure the output folder is 'dist'
  configureWebpack: {
    output: {
      libraryExport: 'default',
    },
  },
  transpileDependencies: [],
};
