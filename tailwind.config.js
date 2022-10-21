module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#67e8f9', // blue
        'primary-contrast': '#2dd4bf',
        'primary-dark': '#002029',
        'secondary-dark': '#18001A', // purple
        'tertiary-dark': '', // gold
        'warning': '#ff6e6e'
      },
      fontFamily: {
        'minecraft': ['Minecraft', 'san-serif'],
        'minecraft-ten': ['MinecraftTen', 'ui-serif'],
      }
    },
  },
  plugins: [],
}
