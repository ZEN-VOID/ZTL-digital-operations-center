import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Database type definitions
export type Database = {
  public: {
    Tables: {
      agents: {
        Row: {
          id: string;
          name: string;
          description: string;
          group: string;
          model: string | null;
          tools: string[];
          expertise: string[];
          created_at: string;
          updated_at: string;
        };
        Insert: Omit<Database['public']['Tables']['agents']['Row'], 'created_at' | 'updated_at'>;
        Update: Partial<Database['public']['Tables']['agents']['Insert']>;
      };
      conversations: {
        Row: {
          id: string;
          agent_id: string;
          title: string;
          created_at: string;
          updated_at: string;
        };
        Insert: Omit<Database['public']['Tables']['conversations']['Row'], 'id' | 'created_at' | 'updated_at'>;
        Update: Partial<Database['public']['Tables']['conversations']['Insert']>;
      };
      messages: {
        Row: {
          id: string;
          conversation_id: string;
          role: 'user' | 'assistant';
          content: string;
          created_at: string;
        };
        Insert: Omit<Database['public']['Tables']['messages']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['messages']['Insert']>;
      };
      files: {
        Row: {
          id: string;
          name: string;
          path: string;
          size: number;
          type: string;
          folder: string;
          created_at: string;
        };
        Insert: Omit<Database['public']['Tables']['files']['Row'], 'id' | 'created_at'>;
        Update: Partial<Database['public']['Tables']['files']['Insert']>;
      };
    };
  };
};

// Create typed Supabase client (only if credentials are provided)
export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient<Database>(supabaseUrl, supabaseAnonKey)
  : null;

// Check if Supabase is configured
export const isSupabaseConfigured = () => Boolean(supabase);

// Storage bucket name
export const STORAGE_BUCKET = 'resources';
