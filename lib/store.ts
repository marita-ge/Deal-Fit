import { create } from 'zustand';
import { ChatMessage, PitchDeck } from '@/types';

interface ChatStore {
  messages: ChatMessage[];
  currentPitchDeck: PitchDeck | null;
  isLoading: boolean;
  error: string | null;
  
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setPitchDeck: (deck: PitchDeck | null) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  currentPitchDeck: null,
  isLoading: false,
  error: null,
  
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  
  setLoading: (loading) =>
    set({ isLoading: loading }),
  
  setError: (error) =>
    set({ error }),
  
  setPitchDeck: (deck) =>
    set({ currentPitchDeck: deck }),
  
  clearChat: () =>
    set({
      messages: [],
      currentPitchDeck: null,
      error: null,
    }),
}));

