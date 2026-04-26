'use client';

import { Sparkles } from 'lucide-react';

export function FullPageLoader({ message = 'Getting things ready…' }: { message?: string }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div className="relative mb-8">
        <div className="w-20 h-20 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-lg animate-pulse">
          <Sparkles className="w-9 h-9 text-white" />
        </div>
        <span className="absolute -bottom-1 -right-1 w-6 h-6 bg-white border-2 border-primary-200 rounded-full flex items-center justify-center">
          <span className="w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin block" />
        </span>
      </div>
      <h1 className="text-xl font-bold text-gray-900 mb-2">Nova Health</h1>
      <p className="text-gray-400 text-sm">{message}</p>
      <div className="flex gap-1.5 mt-6">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-2 h-2 bg-primary-300 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  );
}
