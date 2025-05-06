// frontend/src/polyfills.ts

// importa do Node
import { TextEncoder, TextDecoder } from 'util';

// expõe globalmente para o Jest/JSDOM
;(global as any).TextEncoder = TextEncoder
;(global as any).TextDecoder = TextDecoder
