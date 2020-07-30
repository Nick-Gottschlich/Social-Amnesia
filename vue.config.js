module.exports = {
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        extraFiles: [
          {
            from: "assets",
            to: "resources",
            filter: ["**/*"]
          }
        ]
      }
    }
  }
};
