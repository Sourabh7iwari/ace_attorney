'use client';

import { useState } from 'react';
import DebateForm from '../components/debate-form';
import DebateInterface from '../components/debate-interface';
import { CopilotTextarea } from "@copilotkit/react-textarea";
import { motion } from 'framer-motion';

interface DebateMessage {
  content: string;
  speaker: string;
  timestamp: string;
  confidence: number;
  references?: string[];
}

interface DebateResponse {
  topic: string;
  prosecutor_arguments: DebateMessage[];
  defendant_arguments: DebateMessage[];
  judgment: string | null;
  metadata: {
    round: number;
    current_speaker: string;
    start_time: string;
    status: string;
  };
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [prosecutorArguments, setProsecutorArguments] = useState<DebateMessage[]>([]);
  const [defendantArguments, setDefendantArguments] = useState<DebateMessage[]>([]);
  const [judgment, setJudgment] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleStartDebate = async (topic: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/debate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to start debate');
      }

      const data: DebateResponse = await response.json();
      
      // Update state with debate data
      setProsecutorArguments(data.prosecutor_arguments);
      setDefendantArguments(data.defendant_arguments);
      setJudgment(data.judgment);
    } catch (error) {
      console.error('Error starting debate:', error);
      setError(error instanceof Error ? error.message : 'Failed to start debate');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="container mx-auto px-4 py-8"
      >
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Ace Attorney AI
        </h1>
        
        {error && (
          <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <DebateForm onSubmit={handleStartDebate} isLoading={isLoading} />
        
        <DebateInterface
          prosecutorArguments={prosecutorArguments}
          defendantArguments={defendantArguments}
          judgment={judgment}
          isLoading={isLoading}
        />
      </motion.div>
    </main>
  );
}