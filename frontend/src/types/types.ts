export type Source = {
  id: string;
  title: string;
  authors: string[];
  url: string;
  year?: string;
};

export type Message = {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
  image?: string;
  isError?: boolean;
  sources?: Source[];
};

export type ChatResponse = {
  response: string;
  image?: string;
  sources?: Source[];
};
