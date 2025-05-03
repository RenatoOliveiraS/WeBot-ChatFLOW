module.exports = {
    testEnvironment: "jsdom",
    setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
    moduleFileExtensions: ["js","jsx","ts","tsx"],
    transform: {
      "^.+\\.(js|jsx|ts|tsx)$": "babel-jest"
    }
  };
  