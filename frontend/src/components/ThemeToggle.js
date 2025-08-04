import React, { useState, useEffect } from "react";
import "./ThemeToggle.css";

const ThemeToggle = ({ onThemeChange }) => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem("torko-theme");
    if (savedTheme) {
      setIsDark(savedTheme === "dark");
      onThemeChange(savedTheme === "dark");
    }
  }, [onThemeChange]);

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    localStorage.setItem("torko-theme", newTheme ? "dark" : "light");
    onThemeChange(newTheme);
  };

  return (
    <button
      className={`theme-toggle ${isDark ? "dark" : "light"}`}
      onClick={toggleTheme}
      title="Toggle theme"
    >
      <div className="toggle-track">
        <div className="toggle-thumb">{isDark ? "🌙" : "☀️"}</div>
      </div>
    </button>
  );
};

export default ThemeToggle;
