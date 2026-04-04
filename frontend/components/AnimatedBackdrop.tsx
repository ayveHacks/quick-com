"use client";

import { motion } from "framer-motion";

export function AnimatedBackdrop() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <motion.div
        className="absolute -left-16 top-20 h-72 w-72 rounded-full bg-amber-400/25 blur-3xl"
        animate={{ y: [0, -18, 0], x: [0, 20, 0] }}
        transition={{ repeat: Infinity, duration: 12, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute right-[-40px] top-40 h-80 w-80 rounded-full bg-teal-400/25 blur-3xl"
        animate={{ y: [0, 16, 0], x: [0, -22, 0] }}
        transition={{ repeat: Infinity, duration: 10, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-[-80px] left-1/3 h-72 w-72 rounded-full bg-coral/20 blur-3xl"
        animate={{ y: [0, -12, 0] }}
        transition={{ repeat: Infinity, duration: 9, ease: "easeInOut" }}
      />
    </div>
  );
}


