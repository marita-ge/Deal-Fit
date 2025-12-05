export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface PitchDeck {
  id: string;
  name: string;
  uploadedAt: Date;
  textContent?: string;
}

export interface InvestorRecommendation {
  firm: string;
  relevanceScore: number;
  focusAreas: string[];
  checkSize: string;
  stage: string;
  contacts?: Contact[];
  whyMatch: string;
}

export interface Contact {
  name: string;
  email: string;
  role?: string;
  background?: string;
}

export interface ChatState {
  messages: ChatMessage[];
  currentPitchDeck: PitchDeck | null;
  isLoading: boolean;
  error: string | null;
}

