const path = require('path');

module.exports = function (context, options) {
  return {
    name: 'floating-chat-plugin',

    getClientModules() {
      return [path.resolve(__dirname, './FloatingChatInjector')];
    },

    injectHtmlTags() {
      return {
        postBodyTags: [
          `<div id="floating-chat-root"></div>`
        ],
      };
    },
  };
};