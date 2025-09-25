// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'loop-scroll': 'loop-scroll 20s linear infinite',
      },
      keyframes: {
        "loop-scroll": {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [],
};
