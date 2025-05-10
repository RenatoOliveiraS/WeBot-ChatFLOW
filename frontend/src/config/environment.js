// frontend/src/config/environment.ts
const getEnvironment = () => {
    if (process.env.NODE_ENV === 'test') {
        return {
            apiUrl: process.env.VITE_API_URL || 'http://localhost:8000'
        };
    }
    return {
        apiUrl: import.meta.env.VITE_API_URL
    };
};
export const environment = getEnvironment();
