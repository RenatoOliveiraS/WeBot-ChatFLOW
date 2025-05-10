// frontend/src/setupTests.ts
import '@testing-library/jest-dom';
import i18n from './i18n';
// Define a variável de ambiente para testes
process.env.VITE_API_URL = 'http://localhost:8000';
class MockTextEncoder {
    encode(input) {
        const arr = new Uint8Array(input.length);
        for (let i = 0; i < input.length; i++) {
            arr[i] = input.charCodeAt(i);
        }
        return arr;
    }
}
class MockTextDecoder {
    decode(input) {
        if (!input)
            return '';
        const arr = input instanceof Uint8Array ? input : new Uint8Array(input);
        return String.fromCharCode.apply(null, Array.from(arr));
    }
}
global.TextEncoder = MockTextEncoder;
global.TextDecoder = MockTextDecoder;
// Mock do localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn(),
    key: jest.fn(),
    length: 0,
    [Symbol.iterator]: function* () {
        yield* Object.entries(this);
    }
};
global.localStorage = localStorageMock;
// Mock do matchMedia
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    })),
});
// Configuração do i18n para testes
beforeEach(() => {
    i18n.changeLanguage('en');
});
