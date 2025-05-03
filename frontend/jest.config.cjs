// frontend/jest.config.cjs
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.cjs'],
  moduleFileExtensions: ['js','jsx','ts','tsx','cjs'],
  transform: {}
}
