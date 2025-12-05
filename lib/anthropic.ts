// Anthropic client configuration
// This is used if you want to call Claude directly from the frontend
// However, we recommend using the backend API instead for security

export const ANTHROPIC_CONFIG = {
  // API key should be in backend, not frontend
  // This is just for reference
  model: 'claude-sonnet-4-5-20250929',
  maxTokens: 2000,
};
