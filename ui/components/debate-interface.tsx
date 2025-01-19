'use client';

import * as React from 'react';
import { motion } from 'framer-motion';

interface DebateMessage {
  content: string;
  speaker: string;
  timestamp: string;
}

interface DebateInterfaceProps {
  prosecutorArguments?: DebateMessage[];
  defendantArguments?: DebateMessage[];
  judgment?: string | null;
  isLoading?: boolean;
}

const DebateInterface: React.FC<DebateInterfaceProps> = ({
  prosecutorArguments = [],
  defendantArguments = [],
  judgment = null,
  isLoading = false,
}) => {
  const containerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [prosecutorArguments, defendantArguments, judgment]);

  if (isLoading) {
    return (
      <div className="w-full max-w-4xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-6" ref={containerRef}>
      <div className="space-y-4">
        {prosecutorArguments.map((arg, index) => (
          <motion.div
            key={`prosecutor-${index}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: index * 0.2 }}
            className="bg-red-100 p-4 rounded-lg shadow"
          >
            <h3 className="font-bold text-red-900">Prosecutor</h3>
            <p className="text-red-800">{arg.content}</p>
            <span className="text-xs text-red-600">{arg.timestamp}</span>
          </motion.div>
        ))}

        {defendantArguments.map((arg, index) => (
          <motion.div
            key={`defendant-${index}`}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: index * 0.2 }}
            className="bg-blue-100 p-4 rounded-lg shadow"
          >
            <h3 className="font-bold text-blue-900">Defendant</h3>
            <p className="text-blue-800">{arg.content}</p>
            <span className="text-xs text-blue-600">{arg.timestamp}</span>
          </motion.div>
        ))}
      </div>

      {judgment && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-purple-100 p-6 rounded-lg shadow-lg mt-8"
        >
          <h3 className="font-bold text-purple-900 text-xl mb-2">Final Judgment</h3>
          <p className="text-purple-800">{judgment}</p>
        </motion.div>
      )}
    </div>
  );
};

export default DebateInterface;
