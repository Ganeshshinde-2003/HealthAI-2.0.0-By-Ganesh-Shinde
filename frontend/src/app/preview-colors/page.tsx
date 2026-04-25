'use client';

import { colorPalettes } from '@/styles/colors';

export default function ColorPreviewPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-4">
          Nova Health Color Palettes
        </h1>
        <p className="text-center text-gray-600 mb-12">
          Preview all available color schemes
        </p>

        <div className="space-y-8">
          {Object.entries(colorPalettes).map(([key, palette]) => (
            <div
              key={key}
              className="bg-white rounded-2xl shadow-lg overflow-hidden"
            >
              {/* Header */}
              <div
                className="p-6 text-white"
                style={{ background: palette.gradient }}
              >
                <h2 className="text-2xl font-bold mb-2">{palette.name}</h2>
                <p className="text-white/90 text-sm">Palette ID: {key}</p>
              </div>

              {/* Color Swatches */}
              <div className="p-6 space-y-6">
                {/* Primary Colors */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    Primary Colors
                  </h3>
                  <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
                    {Object.entries(palette.primary).map(([shade, color]) => {
                      if (shade === 'DEFAULT' || shade === 'dark') return null;
                      return (
                        <div key={shade} className="text-center">
                          <div
                            className="w-full h-16 rounded-lg shadow-sm"
                            style={{ backgroundColor: color }}
                          ></div>
                          <p className="text-xs text-gray-600 mt-1">{shade}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Accent & Status Colors */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    Accent & Status Colors
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div>
                      <div
                        className="w-full h-20 rounded-lg shadow-sm"
                        style={{ backgroundColor: palette.accent.DEFAULT }}
                      ></div>
                      <p className="text-sm font-medium text-gray-700 mt-2">
                        Accent
                      </p>
                      <p className="text-xs text-gray-500">
                        {palette.accent.DEFAULT}
                      </p>
                    </div>
                    <div>
                      <div
                        className="w-full h-20 rounded-lg shadow-sm"
                        style={{ backgroundColor: palette.success.DEFAULT }}
                      ></div>
                      <p className="text-sm font-medium text-gray-700 mt-2">
                        Success
                      </p>
                      <p className="text-xs text-gray-500">
                        {palette.success.DEFAULT}
                      </p>
                    </div>
                    <div>
                      <div
                        className="w-full h-20 rounded-lg shadow-sm"
                        style={{ backgroundColor: palette.warning.DEFAULT }}
                      ></div>
                      <p className="text-sm font-medium text-gray-700 mt-2">
                        Warning
                      </p>
                      <p className="text-xs text-gray-500">
                        {palette.warning.DEFAULT}
                      </p>
                    </div>
                    <div>
                      <div
                        className="w-full h-20 rounded-lg shadow-sm"
                        style={{ backgroundColor: palette.danger.DEFAULT }}
                      ></div>
                      <p className="text-sm font-medium text-gray-700 mt-2">
                        Danger
                      </p>
                      <p className="text-xs text-gray-500">
                        {palette.danger.DEFAULT}
                      </p>
                    </div>
                    <div>
                      <div
                        className="w-full h-20 rounded-lg shadow-sm"
                        style={{ backgroundColor: palette.info.DEFAULT }}
                      ></div>
                      <p className="text-sm font-medium text-gray-700 mt-2">
                        Info
                      </p>
                      <p className="text-xs text-gray-500">
                        {palette.info.DEFAULT}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Example Components */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    Component Examples
                  </h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    {/* Button */}
                    <div className="space-y-2">
                      <button
                        className="w-full px-6 py-3 text-white font-semibold rounded-lg shadow-md"
                        style={{ background: palette.gradient }}
                      >
                        Primary Button
                      </button>
                      <button
                        className="w-full px-6 py-3 text-white font-semibold rounded-lg"
                        style={{ backgroundColor: palette.success.DEFAULT }}
                      >
                        Success Button
                      </button>
                    </div>

                    {/* Card */}
                    <div
                      className="p-4 rounded-lg border-2"
                      style={{ borderColor: palette.primary.DEFAULT }}
                    >
                      <h4
                        className="font-semibold mb-2"
                        style={{ color: palette.primary.DEFAULT }}
                      >
                        Card Title
                      </h4>
                      <p className="text-sm text-gray-600">
                        Example card with primary border and heading color
                      </p>
                    </div>

                    {/* Badge */}
                    <div className="flex flex-wrap gap-2">
                      <span
                        className="px-3 py-1 text-sm font-medium rounded-full text-white"
                        style={{ backgroundColor: palette.success.DEFAULT }}
                      >
                        Success
                      </span>
                      <span
                        className="px-3 py-1 text-sm font-medium rounded-full text-white"
                        style={{ backgroundColor: palette.warning.DEFAULT }}
                      >
                        Warning
                      </span>
                      <span
                        className="px-3 py-1 text-sm font-medium rounded-full text-white"
                        style={{ backgroundColor: palette.danger.DEFAULT }}
                      >
                        Danger
                      </span>
                    </div>
                  </div>
                </div>

                {/* Instructions */}
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-700">
                    <strong>To use this palette:</strong> Open{' '}
                    <code className="bg-gray-200 px-2 py-1 rounded">
                      src/styles/colors.ts
                    </code>{' '}
                    and change{' '}
                    <code className="bg-gray-200 px-2 py-1 rounded">
                      activeColorPalette
                    </code>{' '}
                    to{' '}
                    <code className="bg-gray-200 px-2 py-1 rounded">
                      '{key}'
                    </code>
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
