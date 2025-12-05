import Hero from '@/components/landing/Hero'
import Features from '@/components/landing/Features'
import About from '@/components/landing/About'
import HowItWorks from '@/components/landing/HowItWorks'
import Testimonials from '@/components/landing/Testimonials'
import CTA from '@/components/landing/CTA'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <About />
      <HowItWorks />
      <Testimonials />
      <CTA />
    </main>
  )
}
