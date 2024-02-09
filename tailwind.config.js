module.exports = {
    content: ["./templates/**/*.html"],
    darkMode: 'class',
    theme: {
      extend: {
        backgroundImage: {
          "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
          "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
          'bg-menu': "url('rekap/static/images/bg-menu.png')",
          'bg-user': "url('rekap/static/images/notification-bg.png')",
        },
        width: {
          128: "32rem",
        },
        height: {
          100: "27em",
        },
        colors: {
          primary: {
            50: "#FFF2E5",
            100: "#FFE6CC",
            200: "#FFCC99",
            300: "#FFB366",
            400: "#FF9933",
            500: "#FF8101",
            600: "#CC6600",
            700: "#994D00",
            800: "#663300",
            900: "#331A00",
            950: "#190D00",
            DEFAULT: '#FF8101',
            light: '#FFE6CC',
            'dark-light': 'rgba(255,129,1,.15)',
          },
          secondary: {
            DEFAULT: '#805dca',
            light: '#ebe4f7',
            'dark-light': 'rgb(128 93 202 / 15%)',
          },
          success: {
              DEFAULT: '#00ab55',
              light: '#ddf5f0',
              'dark-light': 'rgba(0,171,85,.15)',
          },
          danger: {
              50: "#fef2f2",
              100: "#fee2e2",
              200: "#fecaca",
              300: "#fca5a5",
              400: "#f87171",
              500: "#ef4444",
              600: "#dc2626",
              700: "#b91c1c",
              800: "#991b1b",
              900: "#7f1d1d",
              950: "#450a0a",
              DEFAULT: '#e7515a',
              light: '#fff5f5',
              'dark-light': 'rgba(231,81,90,.15)',
          },
          warning: {
              DEFAULT: '#e2a03f',
              light: '#fff9ed',
              'dark-light': 'rgba(226,160,63,.15)',
          },
          info: {
              DEFAULT: '#2196f3',
              light: '#e7f7ff',
              'dark-light': 'rgba(33,150,243,.15)',
          },
          dark: {
              DEFAULT: '#3b3f5c',
              light: '#eaeaec',
              'dark-light': 'rgba(59,63,92,.15)',
          },
          black: {
              DEFAULT: '#0e1726',
              light: '#e3e4eb',
              'dark-light': 'rgba(14,23,38,.15)',
          },
          white: {
              DEFAULT: '#ffffff',
              light: '#e0e6ed',
              dark: '#888ea8',
          },
        },
        fontFamily: {
          nunito: ['Nunito', 'sans-serif'],
        },
        spacing: {
            4.5: '18px',
        },
        boxShadow: {
            '3xl': '0 2px 2px rgb(224 230 237 / 46%), 1px 6px 7px rgb(224 230 237 / 46%)',
        },
        typography: ({ theme }) => ({
          DEFAULT: {
              css: {
                  '--tw-prose-invert-headings': theme('colors.white.dark'),
                  '--tw-prose-invert-links': theme('colors.white.dark'),
                  h1: { fontSize: '40px', marginBottom: '0.5rem', marginTop: 0 },
                  h2: { fontSize: '32px', marginBottom: '0.5rem', marginTop: 0 },
                  h3: { fontSize: '28px', marginBottom: '0.5rem', marginTop: 0 },
                  h4: { fontSize: '24px', marginBottom: '0.5rem', marginTop: 0 },
                  h5: { fontSize: '20px', marginBottom: '0.5rem', marginTop: 0 },
                  h6: { fontSize: '16px', marginBottom: '0.5rem', marginTop: 0 },
                  p: { marginBottom: '0.5rem' },
                  li: { margin: 0 },
                  img: { margin: 0 },
              },
          },
      }),
      },
      minWidth: {
        90: "90%",
      },
      container: {
        center: true,
      },
    },
    plugins: [
      // ...
      require("@tailwindcss/forms"),
      require('@tailwindcss/typography'),
    ],
  };
  