'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface DebateFormProps {
  onSubmit: (topic: string) => void;
  isLoading?: boolean;
}

const DebateForm: React.FC<DebateFormProps> = ({ onSubmit, isLoading = false }) => {
  const [topic, setTopic] = React.useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim() && !isLoading) {
      onSubmit(topic.trim());
      setTopic('');
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit}
      className="max-w-2xl mx-auto p-6"
    >
      <div className="flex flex-col space-y-4">
        <label htmlFor="topic" className="text-lg font-semibold text-gray-700">
          Enter a topic to debate:
        </label>
        <input
          id="topic"
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g., Should artificial intelligence be regulated?"
          className="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!topic.trim() || isLoading}
          className={`
            p-3 rounded-lg font-semibold text-white transition-colors
            ${isLoading 
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600'
            }
          `}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
              Starting Debate...
            </div>
          ) : (
            'Start Debate'
          )}
        </button>
      </div>
    </motion.form>
  );
};

export default DebateForm;
