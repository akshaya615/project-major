import { useEffect } from "react";

export default function VoiceAlert() {
  useEffect(() => {
    const speak = (text) => {
      const msg = new SpeechSynthesisUtterance(text);
      msg.lang = "en-US";
      window.speechSynthesis.speak(msg);
    };

    speak("Warning. Accident hotspot ahead. Please slow down.");
  }, []);

  return null;
}