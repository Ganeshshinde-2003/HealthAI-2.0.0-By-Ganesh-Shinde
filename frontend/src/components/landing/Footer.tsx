'use client';

import Link from 'next/link';
import { Heart } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Product */}
          <div>
            <h3 className="text-white font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/mem/analyze" className="hover:text-white transition-colors">
                  Health Analysis
                </Link>
              </li>
              <li>
                <Link href="/mem/monthly" className="hover:text-white transition-colors">
                  Monthly Reports
                </Link>
              </li>
              <li>
                <a href="#how-it-works" className="hover:text-white transition-colors">
                  How It Works
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Health Guides
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Biomarker Library
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  FAQ
                </a>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-white font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Brand */}
          <div>
            <h3 className="text-white font-semibold mb-4">Nova Health</h3>
            <p className="text-sm mb-4">
              Your personal health intelligence layer powered by AI and
              functional medicine.
            </p>
            <div className="flex items-center gap-2 text-sm">
              <Heart className="w-4 h-4 text-danger" />
              <span>Built for precision health</span>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">
              © 2026 Nova Health. All rights reserved.
            </p>
            <p className="text-xs text-gray-500 text-center max-w-2xl">
              Nova Health is for informational and educational purposes only.
              Not intended to diagnose, treat, cure, or prevent any disease.
              Always consult a qualified healthcare provider.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
