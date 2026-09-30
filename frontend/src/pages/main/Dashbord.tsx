import React from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import About from "../components/About";
import HowItWorks from "../components/HowitWork";

const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-white text-black">
      <Navbar />

      <main>
        <Hero />
        <Features />
      </main>
      <About/>
      <HowItWorks/>
    </div>
  );
};

export default Dashboard;