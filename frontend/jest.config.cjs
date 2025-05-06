// frontend/jest.config.cjs
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',

  // 1) Carrega globalmente TextEncoder/TextDecoder antes de tudo
  setupFiles: [
    '<rootDir>/src/polyfills.ts'
  ],

  // 2) Após o Jest inicializar o ambiente de testes, carrega jest-dom
  setupFilesAfterEnv: [
    '<rootDir>/src/setupTests.ts'
  ],

  moduleNameMapper: {
    '\\.(css|less|scss|svg)$': 'identity-obj-proxy'
  }
}
